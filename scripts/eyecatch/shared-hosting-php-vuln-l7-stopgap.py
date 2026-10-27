"""パッチを当てられない側の脆弱性対応 — イメージ図

左に流れ（2場面）、右に見どころ（金色の枠）。
  流れ1 直せない: 鍵のかかったサーバー（自分ではパッチを当てられない）と砂時計
  流れ2 手前で止める: 攻撃の要求（赤い封筒）が、盾（CDN）に当たって弾かれる
  見どころ 入口で止める:
    ✗ フォームの入口だけ板で塞いだサーバー。別の入口から封筒が入る
    ✓ 盾がサーバー全体の前に立ち、封筒はどこからも入らない

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


def mini_server(x, y):
    cv.rect(x + 1, y + 1, 10, 14, "black")
    cv.rect(x, y, 10, 14, "gray")
    cv.rect(x, y, 10, 2, "lav")
    for k in range(3):
        cv.rect(x + 2, y + 3 + k * 4, 6, 2, "dgray")


def mini_envelope(x, y):
    cv.rect(x, y, 6, 4, "red")
    cv.sprite(x, y, ["#....#", ".#..#.", "..##.."], "white")


def mini_shield(x, y):
    cv.sprite(x, y, [
        "#######",
        "#######",
        "#######",
        "#######",
        "#######",
        ".#####.",
        ".#####.",
        "..###..",
        "...#...",
    ], "blue")
    cv.sprite(x + 2, y + 2, ["..#..", ".###.", "#####"], "white")


# 背景の星
for sx, sy in [(3, 4), (30, 2), (58, 33), (90, 3), (118, 36), (2, 36), (110, 8)]:
    cv.put(sx, sy, "lav")

# --- 流れ: 直せない → 手前で止める ---
server(8, 12)
lock(12, 5)
hourglass(31, 13)
cv.text_center(30, 33, "直せない", "white")

envelope(63, 17)
cv.rect(74, 20, 5, 1, "red")                                      # 飛んでくる軌跡
spark(80, 14)
shield(88, 10)
envelope(67, 3)                                                   # 弾かれた封筒
cv.sprite(78, 6, ["..#", ".#.", "#.."], "lav")
cv.text_center(88, 33, "手前で止める", "white")

# --- 見どころ: フォームだけ塞いでも入られる / 全体の前で止めれば入らない ---
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

my = PY + 9
# 左: フォームの入口だけ板で塞ぐ → 別の入口から入られる
sx = PX + 14
mini_server(sx, my)
cv.rect(sx - 2, my + 2, 14, 4, "brown")                          # 上の入口（フォーム）に板
cv.put(sx - 1, my + 3, "dgray")
cv.put(sx + 10, my + 3, "dgray")
mini_envelope(PX + 3, my + 9)                                     # 下の入口から入る
cv.rect(PX + 9, my + 10, 4, 1, "red")
cv.sprite(PX + 14, my - 7, ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"], "red")

# 右: 盾がサーバー全体の前に立つ → どこからも入らない
mini_shield(PX + 31, my + 2)
mini_server(PX + 41, my)
mini_envelope(PX + 30, my - 5)                                     # 盾に弾かれた封筒
cv.sprite(PX + 38, my - 7, ["......#", ".....##", "#...##.", "##.##..", ".###..."], "green")
cv.text_center(PX + PW // 2, 33, "入口で止める", "yellow")

cv.save(OUT)
