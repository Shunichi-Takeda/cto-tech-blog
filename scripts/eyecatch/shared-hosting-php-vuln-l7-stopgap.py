"""パッチを当てられない側の脆弱性対応 — イメージ図

左から3場面を並べる。
  1. 直せない: 鍵のかかったサーバー（自分ではパッチを当てられない）と砂時計
  2. 手前で止める: 攻撃の要求（赤い封筒）が、雲の形の盾（CDN）に当たって弾かれる
  3. 更新まで凌ぐ: 盾の後ろでサーバーが無事。上に更新の矢印

  python3 scripts/eyecatch/shared-hosting-php-vuln-l7-stopgap.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "shared-hosting-php-vuln-l7-stopgap", "overview.png")

cv = Canvas(184, 46)


def server(x, y, lamps=True):
    cv.rect(x + 1, y + 1, 16, 14, "black")
    cv.rect(x, y, 16, 14, "gray")
    cv.rect(x, y, 16, 2, "lav")
    for k in range(3):
        yy = y + 3 + k * 4
        cv.rect(x + 2, yy, 12, 3, "dgray")
        if lamps:
            cv.put(x + 12, yy + 1, "green")


def lock(x, y):
    cv.sprite(x + 1, y, [".###.", "#...#", "#...#"], "white")      # つる
    cv.rect(x, y + 3, 7, 5, "yellow")
    cv.rect(x + 3, y + 4, 1, 2, "black")                          # 鍵穴


def hourglass(x, y):
    cv.rect(x, y, 9, 1, "brown")
    cv.rect(x, y + 12, 9, 1, "brown")
    cv.sprite(x + 1, y + 1, [
        "#######",
        ".#...#.",
        "..#.#..",
        "...#...",
        "..#.#..",
        ".#...#.",
        "#.....#",
        "#.....#",
        "#.....#",
        "#.....#",
        "#######",
    ], "white")
    cv.sprite(x + 2, y + 2, [".....", ".###.", "..#..", ".....", "..#..", ".....",
                             "..#..", ".###.", "#####", "#####"], "orange")


def envelope(x, y):
    cv.rect(x, y, 10, 7, "red")
    cv.sprite(x, y, ["#........#", ".#......#.", "..#....#..", "...####..."], "white")


def shield(x, y):
    """盾（CDN）。表に雲の印"""
    rows = [
        "##############",
        "##############",
        "##############",
        "##############",
        "##############",
        "##############",
        ".############.",
        ".############.",
        "..##########..",
        "...########...",
        "....######....",
        ".....####.....",
        "......##......",
    ]
    cv.sprite(x + 1, y + 1, rows, "black")
    cv.sprite(x, y, rows, "blue")
    cv.sprite(x + 3, y + 3, ["...##...", ".######.", "########", ".######."], "white")


def spark(x, y, c="yellow"):
    cv.sprite(x, y, ["#...#", ".#.#.", ".....", ".#.#.", "#...#"], c)


# 背景の星
for sx, sy in [(3, 4), (30, 2), (60, 30), (90, 31), (124, 1), (150, 30), (180, 3), (2, 30), (176, 28)]:
    cv.put(sx, sy, "lav")

# 場面の区切り（細い点線）
for gx in (62, 120):
    for y in range(5, 44, 3):
        cv.put(gx, y, "navy2")

# 1: 直せない
server(14, 11)
lock(18, 4)
hourglass(37, 12)

# 2: 手前で止める（左から来た封筒が、盾に当たって左上へ弾かれる）
envelope(66, 17)
cv.rect(77, 20, 5, 1, "red")                                      # 飛んでくる軌跡
spark(83, 14)
shield(90, 10)
envelope(70, 3)                                                   # 弾かれた封筒
cv.sprite(81, 6, ["..#", ".#.", "#.."], "lav")

# 3: 更新まで凌ぐ（盾の後ろでサーバーが無事）
shield(126, 10)
server(148, 12)
cv.sprite(151, 2, [                                               # 更新の矢印
    "..#####...",
    ".#.....#..",
    "#.......#.",
    "#......###",
    "#.......#.",
    ".#........",
    "..####....",
], "green")

for cx, label in [(31, "直せない"), (91, "手前で止める"), (152, "更新まで凌ぐ")]:
    cv.text_center(cx, 33, label, "white")

cv.save(OUT)
