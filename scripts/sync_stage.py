#!/usr/bin/env python3
"""草案（articles/drafts/）の stage を、記事の実際の状態に合わせて更新する。

レビュー中の記事は PR ブランチ上にしか存在しないため、main の articles/ 直下を
見ても全体像が分からない。そこで草案側の stage に状態を写し、main から
「どの草案がいまどの段階か」を追えるようにする。

  python3 scripts/sync_stage.py           # 更新する
  python3 scripts/sync_stage.py --check   # 差分があれば exit 1

判定（AGENTS.md §4 の stage 定義に対応）:
  published : main の articles/<slug>.md が published: true
  review    : オープンな PR（ブランチ article/<slug>）が存在する
  draft     : どちらでもない（書き直し中・未変換を含む）
"""
import glob
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zenn_common import REPO_ROOT, load_config, parse_frontmatter, split_frontmatter


def published_slugs():
    slugs = set()
    for path in glob.glob(os.path.join(REPO_ROOT, "articles", "*.md")):
        fm_text, _ = split_frontmatter(open(path, encoding="utf-8").read())
        if not fm_text:
            continue
        if str(parse_frontmatter(fm_text).get("published", "")).lower() == "true":
            slugs.add(os.path.splitext(os.path.basename(path))[0])
    return slugs


def review_slugs():
    """オープンな PR のブランチ article/<slug> を列挙する。"""
    try:
        out = subprocess.run(["git", "ls-remote", "--heads", "origin", "refs/heads/article/*"],
                             cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return set()
    return {line.split("refs/heads/article/")[1].strip() for line in out.splitlines() if "refs/heads/article/" in line}


def main():
    config = load_config()
    published, review = published_slugs(), review_slugs()
    changed = []
    for path in sorted(glob.glob(os.path.join(REPO_ROOT, "articles", "drafts", "*.md"))):
        src = open(path, encoding="utf-8").read()
        fm_text, _ = split_frontmatter(src)
        if not fm_text:
            continue
        fm = parse_frontmatter(fm_text)
        slug = fm.get("slug", "")
        want = "published" if slug in published else ("review" if slug in review else "draft")
        now = fm.get("stage", "")
        if now == want:
            continue
        changed.append((os.path.basename(path), now, want))
        if "--check" not in sys.argv:
            new = re.sub(r'^stage: "[^"]*"', 'stage: "%s"' % want, src, count=1, flags=re.M)
            if slug in published and 'published_url: ""' in new:
                new = new.replace('published_url: ""',
                                  'published_url: "https://zenn.dev/%s/articles/%s"'
                                  % (config["publication_name"], slug), 1)
            open(path, "w", encoding="utf-8").write(new)

    if not changed:
        print("stage は最新です（公開 %d / レビュー中 %d）" % (len(published), len(review)))
        return 0
    for name, now, want in changed:
        print("  %-52s %s → %s" % (name, now or "(なし)", want))
    if "--check" in sys.argv:
        print("\nstage が実態と合っていません。`python3 scripts/sync_stage.py` を実行してください")
        return 1
    print("\n%d 件更新しました" % len(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
