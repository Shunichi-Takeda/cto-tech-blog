"""ビルドが落ちたものだけが見える — イメージ図

左から3場面を並べる。
  1. 落ちると鳴る: ビルドが落ちたコンテナには赤い×が付き、ベルが鳴る
  2. 静かに古びる: 普通に動いている（緑ランプ）コンテナに、クモの巣とほこりと古いカレンダー
  3. 日付で棚卸し: 箱を古い順に並べ、いちばん古い箱を矢印で指す

  python3 scripts/eyecatch/base-image-silent-staleness.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "base-image-silent-staleness", "overview.png")

cv = Canvas(184, 46)


def container(x, y, w=18, h=13, body="gray", lamp=None):
    """輸送用コンテナの形の箱（縦の溝つき）"""
    cv.rect(x + 1, y + 1, w, h, "black")
    cv.rect(x, y, w, h, body)
    cv.rect(x, y, w, 1, "white")
    for i in range(2, w - 1, 3):
        cv.rect(x + i, y + 2, 1, h - 3, "dgray")
    if lamp:
        cv.rect(x + w - 4, y + h - 3, 2, 1, lamp)


def calendar(x, y, w=7, h=7, page="white"):
    cv.rect(x + 1, y + 1, w, h, "black")
    cv.rect(x, y, w, h, page)
    cv.rect(x, y, w, 2, "red")
    for j in range(3, h - 1, 2):
        for i in range(1, w - 1, 2):
            cv.put(x + i, y + j, "gray")


# 背景の星
for sx, sy in [(3, 4), (30, 2), (58, 28), (90, 30), (124, 1), (150, 29), (180, 3), (2, 30), (176, 27)]:
    cv.put(sx, sy, "lav")

# 場面の区切り（細い点線）
for gx in (62, 120):
    for y in range(5, 44, 3):
        cv.put(gx, y, "navy2")

# --- 1: 落ちると鳴る ---
container(12, 12)
BADGE = [".#######.", "#########", "#########", "#########", "#########",
         "#########", "#########", "#########", ".#######."]
cv.sprite(17, 15, BADGE, "black")                # 赤い×の札（ビルド失敗）
cv.sprite(16, 14, BADGE, "red")
cv.sprite(18, 16, ["##...##", ".##.##.", "..###..", ".##.##.", "##...##"], "white")
bx, by = 37, 8                                   # 鳴っているベル
cv.sprite(bx, by, [
    "....#....",
    "...###...",
    "..#####..",
    "..#####..",
    "..#####..",
    ".#######.",
    "#########",
    "....#....",
], "yellow")
cv.sprite(bx - 4, by + 1, ["..#", ".#.", "#..", ".#.", "..#"], "orange")   # 揺れの線
cv.sprite(bx + 10, by + 1, ["#..", ".#.", "..#", ".#.", "#.."], "orange")
cv.sprite(bx + 13, by + 2, ["#..", ".#.", "..#"], "orange")

# --- 2: 静かに古びる ---
cx2, cy2 = 78, 12
container(cx2, cy2, lamp="green")
cv.sprite(cx2 + 12, cy2 + 1, [                   # 右上の隅のクモの巣
    "######",
    ".#..##",
    "..#.#.",
    "...###",
    "....##",
    ".....#",
], "white")
for i in range(1, 17, 2):                        # 天板のほこり
    cv.put(cx2 + i, cy2 - 1, "dgray")
cv.put(cx2 + 4, cy2 - 2, "dgray")
cv.put(cx2 + 9, cy2 - 2, "dgray")
calendar(cx2 + 22, cy2 - 3, 9, 10)               # 古いカレンダー（めくられていない）
cv.rect(cx2 + 22, cy2 - 3, 9, 2, "brown")
for i in range(0, 9, 2):                         # 天辺のほこり
    cv.put(cx2 + 22 + i, cy2 - 4, "dgray")

# --- 3: 日付で棚卸し ---
boxes = [
    (127, "gray", "brown", True),    # いちばん古い
    (145, "gray", "red", False),
    (163, "gray", "red", False),
]
for x, body, cal_top, oldest in boxes:
    container(x, 16, w=14, h=11, body=body)
    calendar(x + 3, 6, 8, 8, page="gray" if oldest else "white")
    cv.rect(x + 3, 6, 8, 2, cal_top)
    if oldest:
        for i in range(1, 14, 2):
            cv.put(x + i, 15, "dgray")           # ほこり
cv.sprite(130, 0, ["...#...", "...#...", "#######", ".#####.", "..###..", "...#..."], "yellow")  # いちばん古い箱を指す

for cx_, label in [(31, "落ちると鳴る"), (91, "静かに古びる"), (152, "日付で棚卸し")]:
    cv.text_center(cx_, 33, label, "white")

cv.save(OUT)
