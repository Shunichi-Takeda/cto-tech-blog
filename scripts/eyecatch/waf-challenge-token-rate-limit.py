"""IPを使い捨てる攻撃者に、IP単位のレート制限は効かない — イメージ図

左に流れ（2場面）、右に見どころ（金色の枠）。
  流れ1 IPは使い捨て: 仮面（IP）を次々付け替える攻撃者。外した仮面が散らばる
  流れ2 全体で止める: 1つの大きな門（全体で1つの枠）の前で、攻撃の要求が溜まって止まる
  見どころ 迂回にも上限:
    ✗ 札を持てば通れる脇の門。札を持った攻撃者が何人も並んで抜けていく
    ✓ 脇の門に数を数える表示。上限に達すると棒が下り、正規ユーザーだけが通った後

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


ATK = [".###.", "#####", "#####", ".###.", "#####", "#####", "##.##"]   # 札を持った攻撃者（小）


def small_attacker(x, y):
    cv.sprite(x, y, ATK, "dgray")
    cv.rect(x + 1, y + 1, 3, 1, "pink")                           # 仮面
    cv.rect(x + 4, y + 4, 2, 2, "yellow")                         # 手に札


# 背景の星
for sx, sy in [(3, 4), (30, 2), (58, 33), (90, 3), (118, 36), (2, 36), (110, 8)]:
    cv.put(sx, sy, "lav")

# --- 流れ: IPは使い捨て → 全体で止める ---
attacker(23, 12)
mask(7, 6, "orange")
mask(9, 20, "green")
mask(39, 5, "lav")
mask(41, 18, "blue")
cv.sprite(36, 13, ["#..", ".#.", "..#"], "lav")                    # 付け替える動き
cv.sprite(18, 15, ["..#", ".#.", "#.."], "lav")
cv.text_center(30, 33, "IPは使い捨て", "white")

gate(91, 6, 22, 22)
for rx, ry in [(83, 24), (76, 24), (69, 24), (83, 19), (76, 19), (83, 14), (65, 19)]:
    cv.sprite(rx + 1, ry + 1, REQUEST, "black")
    cv.sprite(rx, ry, REQUEST, "red")
cv.text_center(88, 33, "全体で止める", "white")

# --- 見どころ: 札があれば素通りの迂回路 / 迂回路にも上限 ---
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

GY = PY + 16                                     # 小さな門の上端
# 左: 札を持てば通れる脇の門 → 攻撃者が並んで抜けていく
gate(PX + 11, GY, 11, 10, "brown", closed=False)
for ax in (PX + 2, PX + 8, PX + 14):
    small_attacker(ax, GY + 3)
cv.sprite(PX + 3, PY + 3, ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"], "red")
for y in range(PY + 4, PY + 28, 2):              # 左右の仕切り
    cv.put(PX + 25, y, "lav")

# 右: 脇の門に数を数える表示 → 上限で棒が下り、攻撃者は止まる
gate(PX + 33, GY, 11, 10, "brown", closed=False)
cv.rect(PX + 34, GY - 6, 9, 4, "black")         # 数を数える表示（上限に達した）
for i, c in enumerate(("green", "green", "red")):
    cv.rect(PX + 35 + i * 3, GY - 5, 1, 2, c)
cv.rect(PX + 33, GY + 5, 11, 1, "red")           # 下りた棒
small_attacker(PX + 27, GY + 3)
cv.sprite(PX + 46, GY + 1, PERSON, "white")       # 先に通った正規ユーザー
cv.rect(PX + 51, GY + 5, 2, 2, "yellow")
cv.sprite(PX + 46, PY + 3, ["......#", ".....##", "#...##.", "##.##..", ".###..."], "green")
cv.text_center(PX + PW // 2, 33, "迂回にも上限", "yellow")

cv.save(OUT)
