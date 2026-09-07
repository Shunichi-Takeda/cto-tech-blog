#!/usr/bin/env python3
"""articles/ 直下の Zenn 記事を検証する。CI（.github/workflows/zenn-validate.yml）からも実行される。

  python3 scripts/validate_zenn.py            # articles/*.md を全件検証
  python3 scripts/validate_zenn.py articles/foo.md

検証対象は2つある。

  articles/*.md        Zenn が読む記事の正本
  articles/drafts/*.md 草案。本リポジトリは public なので、Zenn に出ない記述も公開される

検証項目（Zenn 側で弾かれる／公開後に事故になるもの）:
  - ファイル名（= slug）が a-z0-9 - _ の 12〜50 文字
  - title / emoji（1文字） / type（tech|idea） / topics（1〜5件） / published（真偽値）
  - publication_name が config/zenn.json の値と一致（未指定だと個人アカウントで公開されてしまう）
  - published: true の記事に「置換漏れのプレースホルダ」が残っていないか
  - 機密情報ガードの機械チェック（社内URL・想定外ドメイン）
  - 本文の分量（2,000〜5,000 文字目安）は警告のみ
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zenn_common import (REPO_ROOT, SLUG_RE, count_emoji, load_config,
                         parse_frontmatter, split_frontmatter, visible_length)

# 社外に出てはいけない内部URL・認証情報
FORBIDDEN_PATTERNS = [
    (r"[a-z0-9-]+\.backlog\.(jp|com)", "BacklogのURL"),
    (r"[a-z0-9-]+\.slack\.com", "SlackのURL"),
    # ドキュメント用のプレースホルダ（123456789012 等）は除外する
    (r"\b(?!123456789012\b|0{12}\b|1{12}\b)\d{12}\b", "AWSアカウントIDらしい12桁の数値"),
    (r"(?i)(aws_secret|api[_-]?key\s*=\s*['\"][A-Za-z0-9/+=]{16,})", "認証情報らしい値"),
]
PLACEHOLDER_PATTERNS = [r"TODO", r"FIXME", r"XXX", r"タイトル案", r"未確定", r"〇〇"]

# 草案にだけ現れ、Zenn 記事には変換時に落ちるもの。
# draft_to_zenn.py が除去するため Zenn には出ないが、本リポジトリは public なので
# GitHub 上では公開される。落とし忘れを CI で止める。
DRAFT_ONLY_LEAKS = [
    (r"(?m)^source_context:", "着想元の業務文脈（source_context）。記事の題材ではなく社内の取り組みが読み取れる"),
    (r"書き直しメモ|レビュー用メモ|公開留保", "内部レビューメモ"),
    (r"voice\.md|disclosure\.md|公理A\d|OriginalityMarker|CarrierShift|disc:[A-Z]", "非公開オントロジーの参照・内部用語"),
]

# GitHub の rich diff では正しく描画されない Zenn 独自記法。
# 使っている記事はレビュー時にローカルプレビュー（npm run preview）が必要になる。
ZENN_ONLY_SYNTAX = [
    (r"^:::", "メッセージ/アコーディオン（:::message, :::details）"),
    (r"^@\[", "埋め込み（@[tweet], @[youtube] など）"),
    (r"^\$\$", "数式ブロック（KaTeX）"),
    (r"```mermaid", "mermaid 図"),
]


def check(path, config):
    errors, warnings = [], []
    rel = os.path.relpath(path, REPO_ROOT)
    slug = os.path.splitext(os.path.basename(path))[0]
    if not SLUG_RE.match(slug):
        errors.append("ファイル名（slug）が Zenn の制約を満たしません: %r（a-z0-9 と - _ の12〜50文字）" % slug)

    text = open(path, encoding="utf-8").read()
    try:
        fm_text, body = split_frontmatter(text)
    except ValueError as e:
        return ["frontmatter を解釈できません: %s" % e], warnings
    if not fm_text:
        return ["frontmatter がありません"], warnings
    try:
        fm = parse_frontmatter(fm_text)
    except ValueError as e:
        return ["frontmatter を解釈できません: %s" % e], warnings

    if not fm.get("title"):
        errors.append("title が空です")
    elif len(fm["title"]) > 70:
        warnings.append("title が %d 文字あります（一覧で切れるため60文字前後を推奨）" % len(fm["title"]))

    emoji = fm.get("emoji", "")
    if not emoji:
        errors.append("emoji がありません（Zenn のアイキャッチに必須）")
    elif count_emoji(emoji) != 1:
        errors.append("emoji は絵文字1文字にしてください: %r" % emoji)

    if fm.get("type") not in ("tech", "idea"):
        errors.append('type は "tech" か "idea" にしてください: %r' % fm.get("type"))

    topics = fm.get("topics")
    if isinstance(topics, str):
        topics = [t.strip().strip('"') for t in topics.strip("[]").split(",") if t.strip()]
    if not topics:
        errors.append("topics が空です")
    elif len(topics) > 5:
        errors.append("topics は5件までです（現在 %d 件: %s）" % (len(topics), ", ".join(topics)))

    published = str(fm.get("published", "")).lower()
    if published not in ("true", "false"):
        errors.append("published は true / false で指定してください: %r" % fm.get("published"))

    expected_pub = config["publication_name"]
    if fm.get("publication_name") != expected_pub:
        errors.append("publication_name が %r ではありません: %r（未指定だと Publication ではなく個人アカウントで公開されます）"
                      % (expected_pub, fm.get("publication_name")))

    for pattern, label in FORBIDDEN_PATTERNS:
        m = re.search(pattern, text)
        if m:
            errors.append("公開してはいけない情報が含まれている可能性があります（%s）: %r" % (label, m.group(0)))

    if published == "true":
        # コード例の伏せ字（cost=0.00..XXXX など）は未確定の記述ではないため、
        # コードブロックを除いた散文だけを見る。
        prose = re.sub(r"```.*?```", "", body, flags=re.S)
        prose = re.sub(r"`[^`]*`", "", prose)
        for pattern in PLACEHOLDER_PATTERNS:
            m = re.search(pattern, prose)
            if m:
                errors.append("published: true ですが未確定の記述が残っています: %r" % m.group(0))

    # 公開留保メモ（disclosure 判定でホールドされた記事）が本文に残っていないか。
    # Zenn では引用として読者に表示されるため、記事本文に置いてはならない。
    hold = re.search(r"公開留保|レビュー用メモ|解禁[:：]", body)
    if hold:
        if published == "true":
            errors.append("公開留保メモが本文に残ったまま published: true になっています: %r" % hold.group(0))
        else:
            warnings.append("公開留保メモが本文にあります（%r）。Zenn では引用として表示されるため、"
                            "留保の記録は草案側／PRに置き、記事本文からは外してください" % hold.group(0))

    # Zenn は本文の HTML を解釈しないため、HTML コメントは読者にそのまま表示される
    m = re.search(r"<!--", body)
    if m:
        errors.append("本文に HTML コメントがあります。Zenn は HTML を解釈しないため、"
                      "コメントが読者にそのまま表示されます")

    zenn_only = [label for pattern, label in ZENN_ONLY_SYNTAX
                 if re.search(pattern, body, flags=re.M)]
    if zenn_only:
        warnings.append("Zenn独自記法を使用（%s）。GitHub の rich diff では描画されないため、"
                        "レビュー用に `npm run preview` のスクリーンショットを PR に添付してください"
                        % " / ".join(zenn_only))

    length = visible_length(body)
    if length < 1500:
        warnings.append("本文が約 %d 文字です（目安は 2,000〜5,000 文字）" % length)
    elif length > 6000:
        warnings.append("本文が約 %d 文字です（長いので分割を検討）" % length)

    return ["%s: %s" % (rel, e) for e in errors], ["%s: %s" % (rel, w) for w in warnings]


def check_draft(path):
    """草案を検査する。Zenn の frontmatter 制約は掛からないが、公開されることは同じ。"""
    errors = []
    rel = os.path.relpath(path, REPO_ROOT)
    text = open(path, encoding="utf-8").read()
    for pattern, label in DRAFT_ONLY_LEAKS + FORBIDDEN_PATTERNS:
        m = re.search(pattern, text)
        if m:
            errors.append("%s: 公開したくない記述が残っています（%s）: %r"
                          % (rel, label, m.group(0)[:40]))
    return errors, []


def main():
    config = load_config()
    explicit = sys.argv[1:]
    if explicit:
        targets, drafts = [], []
        for path in explicit:
            (drafts if os.sep + "drafts" + os.sep in path else targets).append(path)
    else:
        targets = sorted(glob.glob(os.path.join(REPO_ROOT, "articles", "*.md")))
        drafts = sorted(glob.glob(os.path.join(REPO_ROOT, "articles", "drafts", "*.md")))
    if not targets and not drafts:
        print("検証対象がありません")
        return 0
    all_errors, all_warnings = [], []
    for path in targets:
        errors, warnings = check(path, config)
        all_errors += errors
        all_warnings += warnings
    for path in drafts:
        errors, warnings = check_draft(path)
        all_errors += errors
        all_warnings += warnings
    for w in all_warnings:
        print("WARN  %s" % w)
    for e in all_errors:
        print("ERROR %s" % e)
    print("\n記事 %d 件 / 草案 %d 件を検証: エラー %d 件 / 警告 %d 件"
          % (len(targets), len(drafts), len(all_errors), len(all_warnings)))
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
