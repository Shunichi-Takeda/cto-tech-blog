"""IPを使い捨てる攻撃者に、IP単位のレート制限は効かない — イメージ図

左から3場面を並べる。
  1. IPは使い捨て: 仮面（IP）を次々付け替える攻撃者。外した仮面が散らばる
  2. 全体で止める: 1つの大きな門（全体で1つの枠）の前で、攻撃の要求が溜まって止まる
  3. 札で通す: 札（トークン）を持った正規ユーザーだけが、脇の小さな門を通る。門には数を数える表示

  python3 scripts/eyecatch/waf-challenge-token-rate-limit.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "waf-challenge-token-rate-limit", "overview.png")

cv = Canvas(184, 46)

MASK = [".#####.", "#######", "#.#.#.#", "#######", ".##.##."]
PERSON = [
    "..###..",
    ".#####.",
    "..###..",
    "...#...",
    ".#####.",
    "#.###.#",
    "..###..",
    "..#.#..",
    ".##.##.",
]
REQUEST = ["######", "#.##.#", "##..##", "######"]   # 攻撃の要求（封筒）


def mask(x, y, c):
    cv.sprite(x, y, MASK, c)
    cv.put(x + 2, y + 2, "black")
    cv.put(x + 4, y + 2, "black")


def attacker(x, y):
    cv.sprite(x, y, [                                             # フードの人影
        "...#####...",
        "..#######..",
        ".#########.",
        ".#########.",
        ".#########.",
        "..#######..",
        "...#####...",
        ".#########.",
        "###########",
        "###########",
        "###########",
        "####...####",
        "####...####",
    ], "dgray")
    mask(x + 2, y + 2, "pink")                                    # いま付けている仮面


def gate(x, y, w, h, c="brown", closed=True):
    cv.rect(x, y, 3, h, c)                                        # 柱
    cv.rect(x + w - 3, y, 3, h, c)
    cv.rect(x - 1, y, w + 2, 2, c)                                # 梁
    if closed:
        for i in range(x + 4, x + w - 4, 3):                      # 閉じた格子
            cv.rect(i, y + 3, 1, h - 3, "gray")


# 背景の星
for sx, sy in [(3, 4), (30, 2), (60, 30), (90, 31), (124, 1), (150, 30), (180, 3), (2, 30), (176, 28)]:
    cv.put(sx, sy, "lav")

# 場面の区切り（細い点線）
for gx in (62, 120):
    for y in range(5, 44, 3):
        cv.put(gx, y, "navy2")

# 1: IPは使い捨て
attacker(24, 12)
mask(8, 6, "orange")
mask(12, 20, "green")
mask(40, 5, "lav")
mask(44, 18, "blue")
cv.sprite(37, 13, ["#..", ".#.", "..#"], "lav")                    # 付け替える動き
cv.sprite(19, 15, ["..#", ".#.", "#.."], "lav")

# 2: 全体で止める（大きな門の前に、攻撃の要求が溜まる）
gate(92, 6, 22, 22)
for rx, ry in [(84, 24), (77, 24), (70, 24), (84, 19), (77, 19), (84, 14), (66, 19)]:
    cv.sprite(rx + 1, ry + 1, REQUEST, "black")
    cv.sprite(rx, ry, REQUEST, "red")

# 3: 札で通す（札を持った人だけ、数を数える小さな門を通る）
gate(146, 12, 15, 16, "dgray", closed=False)
cv.rect(147, 6, 13, 5, "black")                                   # 数を数える表示
for i in range(3):
    cv.rect(150 + i * 3, 7, 1, 3, "green")
cv.sprite(150, 18, PERSON, "white")                               # 門をくぐる正規ユーザー
cv.rect(156, 20, 4, 3, "yellow")                                  # 札（トークン）
cv.put(157, 21, "orange")
cv.sprite(164, 20, ["#....", ".#...", "..#..", ".#...", "#...."], "yellow")  # 通り抜ける向き
cv.sprite(168, 20, ["#....", ".#...", "..#..", ".#...", "#...."], "yellow")

for cx, label in [(31, "IPは使い捨て"), (91, "全体で止める"), (152, "札で通す")]:
    cv.text_center(cx, 33, label, "white")

cv.save(OUT)
