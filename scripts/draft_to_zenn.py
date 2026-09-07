#!/usr/bin/env python3
"""草案（articles/drafts/YYYY-MM-DD_slug.md）を Zenn 形式に変換して articles/ 直下へ出す。

  python3 scripts/draft_to_zenn.py articles/drafts/2026-08-06_ecs-....md
  python3 scripts/draft_to_zenn.py <draft> --emoji 🚢 --topics aws,ecs,cicd --dry-run

変換内容:
  - frontmatter を Zenn の項目（title / emoji / type / topics / published / publication_name）へ写す
  - 草案側のメタ情報（stage・source_context 等）は持ち込まない（Zennは本文のHTMLコメントをそのまま表示してしまう）
  - 本文先頭の H1 は Zenn がタイトルを別に描画するため削除
  - 著者フッタ（UTM付きリンク）を末尾に付与
  - published は必ず false で出力する（公開は published: true への変更を人がレビューしてから）
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zenn_common import (REPO_ROOT, SLUG_RE, count_emoji, dump_zenn_frontmatter,
                         load_config, parse_frontmatter, split_frontmatter)

MAX_TOPICS = 5


def build_topics(draft, config, override):
    if override:
        topics = [t.strip() for t in override.split(",") if t.strip()]
    else:
        mapping = config["tag_to_topic"]
        topics = []
        unmapped = []
        for tag in draft.get("tags", []):
            topic = mapping.get(tag)
            if topic is None:
                unmapped.append(tag)
                continue
            if topic not in topics:
                topics.append(topic)
        if unmapped:
            print("  ! topics に写せなかったタグ: %s（config/zenn.json の tag_to_topic に追加、"
                  "または --topics で明示指定してください）" % ", ".join(unmapped), file=sys.stderr)
    if len(topics) > MAX_TOPICS:
        print("  ! topics が %d 件あるため先頭 %d 件に切り詰めました: 落としたのは %s"
              % (len(topics), MAX_TOPICS, ", ".join(topics[MAX_TOPICS:])), file=sys.stderr)
        topics = topics[:MAX_TOPICS]
    return topics


def build_footer(config, slug):
    """フッタの各リンクに UTM を付けて template に流し込む。

    template では links のキー名 + "_url"（例: {product_url}）で参照する。
    """
    footer = config["footer"]
    params = "&".join("%s=%s" % (k, v.replace("{slug}", slug)) for k, v in footer["utm_params"].items())
    values = {
        "author_name": config["author"]["name"],
        "author_github": config["author"]["github"],
    }
    for name, link in footer["links"].items():
        base = link["base_url"]
        values["%s_url" % name] = base + ("&" if "?" in base else "?") + params
    return footer["template"].format(**values)


def strip_draft_footer(body):
    """草案テンプレート末尾の著者ブロックを落とす（Zenn側は config のフッタを正とする）。"""
    m = re.search(r"\n-{3,}\s*\n+(?:>[^\n]*\n?)*$", body)
    if m and "著者" in m.group(0):
        return body[:m.start()] + "\n"
    return body


def strip_hold_memo(body):
    """公開留保メモ（> ⚠️ **公開留保...** の引用ブロック）を Zenn 記事本文から外す。

    Zenn は引用をそのまま表示するため、レビュー用メモが読者に見えてしまう。
    留保の記録は草案側（articles/drafts/）と PR に残す。
    """
    lines = body.splitlines(keepends=True)
    out, i, removed = [], 0, False
    while i < len(lines):
        if lines[i].lstrip().startswith(">") and re.search(r"公開留保|レビュー用メモ", lines[i]):
            while i < len(lines) and (lines[i].lstrip().startswith(">") or not lines[i].strip()):
                i += 1
            removed = True
            continue
        out.append(lines[i])
        i += 1
    if removed:
        print("  ! 公開留保メモを本文から除去しました（草案側とPRに記録を残すこと）")
    return "".join(out)


def strip_leading_h1(body):
    lines = body.lstrip("\n").splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return "".join(lines[:i] + lines[i + 1:]).lstrip("\n")
        if line.strip():
            break
    return body.lstrip("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft", help="articles/drafts/ 配下の草案ファイル")
    ap.add_argument("--emoji", help="アイキャッチ絵文字（未指定なら category から決定）")
    ap.add_argument("--topics", help="topics をカンマ区切りで明示指定（最大5件）")
    ap.add_argument("--type", dest="type_", choices=["tech", "idea"], help="記事種別を明示指定")
    ap.add_argument("--slug", help="出力ファイル名のスラッグを明示指定")
    ap.add_argument("--dry-run", action="store_true", help="ファイルを書かず標準出力に出す")
    ap.add_argument("--force", action="store_true", help="既存の articles/<slug>.md を上書きする")
    args = ap.parse_args()

    config = load_config()
    if not os.path.isfile(args.draft):
        sys.exit("草案ファイルが見つかりません: %s" % args.draft)
    text = open(args.draft, encoding="utf-8").read()
    fm_text, body = split_frontmatter(text)
    if not fm_text:
        sys.exit("frontmatter がありません: %s" % args.draft)
    draft = parse_frontmatter(fm_text)

    slug = args.slug or draft.get("slug") or ""
    if not SLUG_RE.match(slug):
        sys.exit("slug が Zenn の制約（a-z0-9 と - _ の 12〜50 文字）を満たしません: %r" % slug)

    category = draft.get("category", "engineering")
    emoji = args.emoji or config["category_to_emoji"].get(category, "📝")
    if count_emoji(emoji) != 1:
        sys.exit("emoji は絵文字1文字にしてください: %r" % emoji)

    zenn = {
        "title": draft.get("title", ""),
        "emoji": emoji,
        "type": args.type_ or config["category_to_type"].get(category, "tech"),
        "topics": build_topics(draft, config, args.topics),
        "published": False,
        "publication_name": config["publication_name"],
    }
    if not zenn["title"]:
        sys.exit("title が空です")
    if not zenn["topics"]:
        sys.exit("topics が0件です。--topics で指定してください")

    # Zenn の本文は HTML を解釈しないため、HTML コメントを置くと読者にそのまま表示される。
    # よって草案側のメタ情報（category / source_context 等）は Zenn 記事に持ち込まない。
    # 草案との対応は slug で辿れる（articles/drafts/<date>_<slug>.md）。
    body_out = strip_draft_footer(strip_leading_h1(strip_hold_memo(body))).rstrip()
    out = dump_zenn_frontmatter(zenn) + "\n" + body_out + "\n\n" + build_footer(config, slug)
    out = re.sub(r"\n{3,}", "\n\n", out)

    if args.dry_run:
        sys.stdout.write(out)
        return

    dest = os.path.join(REPO_ROOT, "articles", slug + ".md")
    if os.path.exists(dest) and not args.force:
        sys.exit("既に存在します（上書きするなら --force）: %s" % dest)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(out)
    print("生成: %s" % os.path.relpath(dest, REPO_ROOT))
    print("次に: python3 scripts/validate_zenn.py で検証 → npx zenn preview で表示確認")
    print("  published: false のまま PR を作る（Zenn が下書きデプロイし、マーケ広報がレビューする）")


if __name__ == "__main__":
    main()
