#!/usr/bin/env python3
"""articles/published/INDEX.md を articles/ 直下の記事から再生成する。

公開PRごとに INDEX.md を書き換えると、公開PRを並行させたときに必ず衝突する
（全記事が同じ表に1行ずつ追記するため）。そこで索引は公開PRから外し、
merge 後に main 上でこのスクリプトを回して更新する。

  python3 scripts/update_index.py           # 更新する
  python3 scripts/update_index.py --check   # 差分があれば exit 1（CI用）

公開日の決め方:
  1. 既に INDEX.md に載っている記事は、そこに書かれた日付を保つ
  2. 新規は frontmatter の published_at、無ければ published: true を入れた
     コミットの日付、それも取れなければ本日
"""
import glob
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zenn_common import REPO_ROOT, load_config, parse_frontmatter, split_frontmatter

INDEX = os.path.join(REPO_ROOT, "articles", "published", "INDEX.md")
HEADER = """# 公開済み記事の索引

Zenn へ公開した記事の一覧。**記事ファイル本体は `articles/` 直下から移動しない**（移動・削除しても Zenn 側の記事は消えず、運用が壊れるため）。

**この表は手で編集しない。** 公開PRを並行させると衝突するため、merge 後に main で次を実行して再生成する。

```bash
python3 scripts/update_index.py
```

| 公開日 | タイトル | 記事ファイル | 公開URL |
|---|---|---|---|
"""


def existing_dates():
    if not os.path.exists(INDEX):
        return {}
    dates = {}
    for line in open(INDEX, encoding="utf-8"):
        m = re.match(r"\| (\d{4}-\d{2}-\d{2}) \|.*?\(\.\./([^)]+)\.md\)", line)
        if m:
            dates[m.group(2)] = m.group(1)
    return dates


def published_date(path, fm, known):
    slug = os.path.splitext(os.path.basename(path))[0]
    if slug in known:
        return known[slug]
    if fm.get("published_at"):
        return fm["published_at"][:10]
    try:
        out = subprocess.run(
            ["git", "log", "-S", "published: true", "--diff-filter=AM",
             "--format=%ad", "--date=short", "-1", "--", path],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout.strip()
        if out:
            return out
    except subprocess.CalledProcessError:
        pass
    return subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()


def build():
    config = load_config()
    known = existing_dates()
    rows = []
    for path in sorted(glob.glob(os.path.join(REPO_ROOT, "articles", "*.md"))):
        fm_text, _ = split_frontmatter(open(path, encoding="utf-8").read())
        if not fm_text:
            continue
        fm = parse_frontmatter(fm_text)
        if str(fm.get("published", "")).lower() != "true":
            continue
        slug = os.path.splitext(os.path.basename(path))[0]
        rows.append((published_date(path, fm, known), fm.get("title", slug), slug))
    rows.sort()
    if not rows:
        body = "| - | （まだありません） | - | - |\n"
    else:
        body = "".join(
            "| %s | %s | [articles/%s.md](../%s.md) | https://zenn.dev/%s/articles/%s |\n"
            % (d, t, s, s, config["publication_name"], s) for d, t, s in rows)
    return HEADER + body, len(rows)


def main():
    content, n = build()
    current = open(INDEX, encoding="utf-8").read() if os.path.exists(INDEX) else ""
    if "--check" in sys.argv:
        if current != content:
            print("INDEX.md が最新ではありません。`python3 scripts/update_index.py` を実行してください")
            return 1
        print("INDEX.md は最新です（公開済み %d 件）" % n)
        return 0
    if current == content:
        print("変更なし（公開済み %d 件）" % n)
        return 0
    open(INDEX, "w", encoding="utf-8").write(content)
    print("INDEX.md を更新しました（公開済み %d 件）" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
