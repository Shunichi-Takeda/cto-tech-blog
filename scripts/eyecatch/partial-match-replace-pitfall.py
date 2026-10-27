"""1文字の登録が無関係な単語を書き換える — イメージ図

記事本文と同じ架空の例（「P」を「パイナップル」の略称として登録）で、左から3場面を並べる。
  1. 1文字を登録: 置換辞書のページに「P」が1文字だけ書かれている
  2. 中に当たる: 「Payment」の札の頭の P が光る
  3. 別の語に化ける: P がパイナップルに置き換わり、「ayment」の前にくっつく

  python3 scripts/eyecatch/partial-match-replace-pitfall.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas, glyph_rows, ART  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "partial-match-replace-pitfall", "overview.png")

cv = Canvas(184, 46)


def text_width(s):
    """文字列の幅（絵のマス）"""
    return (len(glyph_rows(s)[0]) + ART - 1) // ART


def tag(x, y, w, h=12):
    cv.rect(x + 1, y + 1, w, h, "black")
    cv.rect(x, y, w, h, "white")


PINE_LEAF = [
    "...#.#.#...",
    "...#.#.#...",
    "..#######..",
    "....###....",
]
PINE_BODY = [
    "...#####...",
    "..#######..",
    ".#########.",
    ".#########.",
    ".#########.",
    ".#########.",
    ".#########.",
    "..#######..",
    "...#####...",
]


def pineapple(x, y):
    """11x13 のパイナップル"""
    cv.sprite(x, y, PINE_LEAF, "dgreen")
    cv.sprite(x, y + 4, PINE_BODY, "orange")
    for j in range(1, 8):                        # うろこ模様
        for i in range(2 + (j % 2), 9, 2):
            if PINE_BODY[j][i] == "#":
                cv.put(x + i, y + 4 + j, "brown")


# 背景の星
for sx, sy in [(3, 4), (30, 2), (58, 28), (90, 30), (124, 1), (150, 29), (180, 3), (2, 30), (176, 27)]:
    cv.put(sx, sy, "lav")

# 場面の区切り（細い点線）
for gx in (62, 120):
    for y in range(5, 44, 3):
        cv.put(gx, y, "navy2")

# --- 1: 1文字を登録（開いた辞書） ---
bx, by = 17, 7
cv.rect(bx + 1, by + 1, 28, 18, "black")
cv.rect(bx, by, 28, 18, "brown")                 # 表紙
cv.rect(bx + 1, by + 1, 12, 16, "white")         # 左のページ
cv.rect(bx + 15, by + 1, 12, 16, "white")        # 右のページ
cv.rect(bx + 13, by + 1, 2, 16, "dgray")         # 背
for k in range(4):                               # 左のページ: 既存の登録（行）
    cv.rect(bx + 3, by + 4 + k * 3, 8 - (k % 2) * 3, 1, "gray")
cv.rect(bx + 17, by + 4, 8, 1, "gray")           # 右のページ: 1行だけ…
cv.text(bx + 18, by + 7, "P", "red", shadow=None)  # …新しく登録した「P」
cv.sprite(bx + 26, by - 4, ["..#..", "..#..", "#####", "..#..", "..#.."], "yellow")  # 追加

# --- 2: 中に当たる（Payment の P が光る） ---
w2 = text_width("Payment") + 4
tx2 = 91 - w2 // 2
ty2 = 11
tag(tx2, ty2, w2)
cv.rect(tx2 + 1, ty2 + 1, 6, 10, "yellow")       # 光っている P
cv.text(tx2 + 2, ty2 + 2, "Payment", "black", shadow=None)
for sx, sy in [(tx2 - 2, ty2 - 3), (tx2 + 3, ty2 - 5), (tx2 + 8, ty2 - 3), (tx2 - 4, ty2 + 3)]:
    cv.sprite(sx, sy, [".#.", "###", ".#."], "yellow")  # きらめき

# --- 3: 別の語に化ける（P がパイナップルに） ---
w3 = text_width("ayment") + 3
total = 11 + w3
px3 = 152 - total // 2
ty3 = 11
tag(px3 + 11, ty3, w3)
cv.text(px3 + 12, ty3 + 2, "ayment", "black", shadow=None)
pineapple(px3, ty3 - 4)                          # 札の P の位置に、パイナップルがくっつく

for cx_, label in [(31, "1文字を登録"), (91, "中に当たる"), (152, "別の語に化ける")]:
    cv.text_center(cx_, 33, label, "white")

cv.save(OUT)
