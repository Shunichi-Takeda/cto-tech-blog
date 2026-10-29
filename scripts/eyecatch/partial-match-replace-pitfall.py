"""1文字の登録が無関係な単語を書き換える — イメージ図

記事本文と同じ架空の例（「P」を「パイナップル」の略称として登録）で、左に流れ（2場面）、右に見どころ。
  流れ1. 1文字を登録: 置換辞書のページに「P」が1文字だけ書かれている
  流れ2. 中に当たる: 「Payment」の札の頭の P が光る
  見どころ. 単語で照合: 部分一致だと P がパイナップルに化ける（✗）、単語の区切りで照合すれば Payment のまま（✓）

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
for sx, sy in [(3, 4), (58, 30), (110, 3), (118, 36), (2, 36), (60, 2)]:
    cv.put(sx, sy, "lav")

# --- 流れ1: 1文字を登録（開いた辞書） ---
bx, by = 16, 8
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

# --- 流れ2: 中に当たる（Payment の P が光る） ---
w2 = text_width("Payment") + 4
tx2 = 90 - w2 // 2
ty2 = 12
tag(tx2, ty2, w2)
cv.rect(tx2 + 1, ty2 + 1, 6, 10, "yellow")       # 光っている P
cv.text(tx2 + 2, ty2 + 2, "Payment", "black", shadow=None)
for sx, sy in [(tx2 - 2, ty2 - 3), (tx2 + 3, ty2 - 5), (tx2 + 8, ty2 - 3), (tx2 - 4, ty2 + 3)]:
    cv.sprite(sx, sy, [".#.", "###", ".#."], "yellow")  # きらめき

cv.text_center(30, 33, "1文字を登録", "white")
cv.text_center(90, 33, "中に当たる", "white")

# --- 見どころ: 部分一致だと化ける / 単語の区切りで照合すれば化けない ---
PX, PY, PW, PH = 126, 5, 56, 38
for i in range(PW):                              # 金色の枠
    cv.put(PX + i, PY, "orange")
    cv.put(PX + i, PY + PH - 1, "orange")
for j in range(PH):
    cv.put(PX, PY + j, "orange")
    cv.put(PX + PW - 1, PY + j, "orange")
cv.rect(PX + 1, PY + 1, PW - 2, PH - 2, "navy2")
cv.sprite(PX + PW // 2 - 3, 0, [               # 電球（得られるもの）
    "..###..",
    ".#####.",
    "#######",
    "#######",
    ".#####.",
    "..###..",
    "..###..",
], "yellow")
cv.rect(PX + PW // 2 - 1, 7, 3, 1, "gray")
for rx, ry in [(-6, 1), (-5, 4), (6, 1), (5, 4)]:  # 光の線
    cv.put(PX + PW // 2 + rx, ry, "yellow")

MARK_X = PX + 3
# 上の段 ✗: P がパイナップルに化けた語
r1 = 10
cv.sprite(MARK_X, r1 + 3, ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"], "red")
wa = text_width("ayment") + 3
pineapple(MARK_X + 8, r1 - 3)
tag(MARK_X + 19, r1, wa, 9)
cv.text(MARK_X + 20, r1 + 1, "ayment", "black", shadow=None)

# 下の段 ✓: 単語の区切り（緑の縦線）で照合し、Payment はそのまま
r2 = 21
cv.sprite(MARK_X - 1, r2 + 3, ["......#", ".....##", "#...##.", "##.##..", ".###..."], "green")
wp = text_width("Payment") + 4
x2 = MARK_X + 10
cv.rect(x2 - 2, r2 - 1, 1, 11, "green")          # 語の前の区切り
tag(x2, r2, wp, 9)
cv.text(x2 + 2, r2 + 1, "Payment", "black", shadow=None)
cv.rect(x2 + wp + 2, r2 - 1, 1, 11, "green")     # 語の後ろの区切り

cv.text_center(PX + PW // 2, 33, "単語で照合", "yellow")

cv.save(OUT)
