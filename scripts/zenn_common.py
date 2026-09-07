"""草案の frontmatter と Zenn frontmatter を扱う共通処理。

外部ライブラリに依存しない（PyYAML なしで動く）ことを条件にしている。
草案の frontmatter は「文字列 or 文字列リスト」だけで構成されているため、
最小のパーサで十分。想定外の構造が来たら黙って落とさず例外にする。
"""
import json
import os
import re
import unicodedata

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(REPO_ROOT, "config", "zenn.json")

ZENN_KEY_ORDER = ["title", "emoji", "type", "topics", "published", "published_at", "publication_name"]
SLUG_RE = re.compile(r"^[a-z0-9_-]{12,50}$")


def load_config(path=CONFIG_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def split_frontmatter(text):
    """(frontmatter文字列, 本文) を返す。frontmatter が無ければ ('', text)。"""
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 3)
    if end == -1:
        raise ValueError("frontmatter の終端 '---' が見つかりません")
    return text[4:end + 1], text[end + 5:]


def parse_frontmatter(fm_text):
    """key: value と `key:` + `- item` 形式だけを解釈する最小パーサ。"""
    data = {}
    current_list_key = None
    for raw in fm_text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.lstrip().startswith("- "):
            if current_list_key is None:
                raise ValueError("リスト項目の親キーが不明です: %r" % raw)
            data[current_list_key].append(_unquote(raw.lstrip()[2:].strip()))
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if not m:
            raise ValueError("解釈できない frontmatter 行です: %r" % raw)
        key, value = m.group(1), m.group(2).strip()
        if value == "":
            data[key] = []
            current_list_key = key
        else:
            data[key] = _unquote(value)
            current_list_key = None
    return data


def _unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def dump_zenn_frontmatter(data):
    lines = ["---"]
    for key in ZENN_KEY_ORDER:
        if key not in data:
            continue
        value = data[key]
        if isinstance(value, list):
            lines.append("%s: [%s]" % (key, ", ".join('"%s"' % v for v in value)))
        elif isinstance(value, bool):
            lines.append("%s: %s" % (key, "true" if value else "false"))
        else:
            lines.append('%s: "%s"' % (key, str(value).replace('"', '\\"')))
    lines.append("---")
    return "\n".join(lines) + "\n"


def count_emoji(value):
    """先頭のサロゲート/結合文字を1文字として数え、絵文字の個数を返す。"""
    chars = [c for c in value if not unicodedata.combining(c) and c not in "️‍"]
    return len(chars)


def visible_length(body):
    """本文の文字数（コードブロック・HTMLコメントを除いた概算）。"""
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"\s", "", body)
    return len(body)
