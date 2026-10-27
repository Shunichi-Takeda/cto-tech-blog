"""タイムアウトしても検索がディスクを読み続ける — イメージ図

左から3場面を並べる。
  1. CPUは暇: 使用率のメーターはほぼ0で、CPUは居眠りしている
  2. 切っても読む: タイムアウトの砂時計には×が付いたのに、ディスクは赤く回り続ける
  3. 温めておく: ディスクを下から温めておく（暖機）と、緑で落ち着いている

  python3 scripts/eyecatch/filtered-knn-exact-fallback-iops.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "filtered-knn-exact-fallback-iops", "overview.png")

cv = Canvas(184, 46)

DISK = [
    ".....#####.....",
    "...##.....##...",
    "..#.........#..",
    ".#...........#.",
    ".#...........#.",
    "#.............#",
    "#......#......#",
    "#.....###.....#",
    "#......#......#",
    "#.............#",
    ".#...........#.",
    ".#...........#.",
    "..#.........#..",
    "...##.....##...",
    ".....#####.....",
]


def disk(x, y, body, rim):
    """ディスクの円盤（15x15）。中を塗ってから縁と軸を描く"""
    for j, row in enumerate(DISK):
        first, last = row.find("#"), row.rfind("#")
        if first != -1:
            cv.rect(x + first, y + j, last - first + 1, 1, body)
    cv.sprite(x, y, DISK, rim)


# 背景の星
for sx, sy in [(3, 4), (30, 2), (58, 28), (90, 31), (124, 1), (150, 29), (180, 3), (2, 30), (176, 27)]:
    cv.put(sx, sy, "lav")

# 場面の区切り（細い点線）
for gx in (62, 120):
    for y in range(5, 44, 3):
        cv.put(gx, y, "navy2")

# --- 1: CPUは暇 ---
# 使用率のメーター（針はほぼ0）
mx, my = 4, 9
GAUGE = [
    "......#######......",
    "....##.......##....",
    "...#...........#...",
    "..#.............#..",
    ".#...............#.",
    ".#...............#.",
    "#.................#",
    "#.................#",
    "#.................#",
    "###################",
]
for j, row in enumerate(GAUGE):                  # 中を塗る
    first, last = row.find("#"), row.rfind("#")
    cv.rect(mx + first, my + j, last - first + 1, 1, "navy2")
cv.sprite(mx, my, GAUGE, "white")
for (gx_, gy_, c) in [(2, 7, "green"), (3, 4, "green"), (5, 2, "green"), (9, 1, "yellow"),
                      (13, 2, "orange"), (15, 4, "red"), (16, 7, "red")]:
    cv.put(mx + gx_, my + gy_, c)                # 目盛り（左が0、右が上限）
cv.sprite(mx + 3, my + 7, ["##....", "..###.", ".....#"], "yellow")  # 針（左に倒れている）
cv.rect(mx + 8, my + 8, 3, 1, "orange")          # 針の軸

# CPU（居眠り）
cx, cy = 32, 10
for i in range(1, 14, 3):                        # ピン
    cv.put(cx + i, cy - 1, "gray")
    cv.put(cx + i, cy + 14, "gray")
    cv.put(cx - 1, cy + i, "gray")
    cv.put(cx + 14, cy + i, "gray")
cv.rect(cx + 1, cy + 1, 14, 14, "black")
cv.rect(cx, cy, 14, 14, "dgray")
cv.rect(cx + 2, cy + 2, 10, 10, "navy2")
cv.rect(cx + 3, cy + 6, 3, 1, "white")           # 閉じた目
cv.rect(cx + 8, cy + 6, 3, 1, "white")
cv.rect(cx + 6, cy + 9, 2, 1, "pink")            # 口
cv.sprite(cx + 15, cy - 6, ["####", "...#", "..#.", ".#..", "####"], "lav")
cv.sprite(cx + 20, cy - 9, ["###", "..#", ".#.", "###"], "lav")

# --- 2: 切っても読む ---
hx, hy = 68, 8                                   # 砂時計
cv.sprite(hx, hy, [
    "#########",
    ".#.....#.",
    ".#.....#.",
    "..#...#..",
    "...#.#...",
    "....#....",
    "...#.#...",
    "..#...#..",
    ".#.....#.",
    ".#.....#.",
    "#########",
], "yellow")
cv.rect(hx + 3, hy + 3, 3, 1, "orange")          # 上に残った砂
cv.put(hx + 4, hy + 4, "orange")
cv.rect(hx + 2, hy + 9, 5, 1, "orange")          # 下に落ちた砂
BADGE = [".#####.", "#######", "#######", "#######", "#######", "#######", ".#####."]
cv.sprite(hx + 6, hy + 7, BADGE, "black")        # ×の札（タイムアウトで切った）
cv.sprite(hx + 5, hy + 6, BADGE, "red")
cv.sprite(hx + 6, hy + 7, ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"], "white")

dx, dy = 88, 8                                   # 回り続けるディスク
disk(dx, dy, "red", "white")
cv.put(dx + 7, dy + 7, "white")
for ax, ay, n in [(dx + 17, dy + 3, 3), (dx + 18, dy + 7, 4), (dx + 17, dy + 11, 3),
                  (dx - 5, dy + 4, 3), (dx - 6, dy + 10, 3)]:
    cv.rect(ax, ay, n, 1, "orange")              # 回り続ける線

# --- 3: 温めておく ---
gx3, gy3 = 144, 5
disk(gx3, gy3, "dgreen", "white")
cv.put(gx3 + 7, gy3 + 7, "white")
cv.sprite(gx3 - 1, gy3 + 16, [                   # 小さな火（暖機）
    "..#.....#.....#..",
    ".##....###...##..",
    ".###..#####.####.",
    "#################",
], "orange")
cv.sprite(gx3 + 1, gy3 + 18, ["..#....###...#.", "###############"], "yellow")

for cx_, label in [(31, "CPUは暇"), (91, "切っても読む"), (152, "温めておく")]:
    cv.text_center(cx_, 33, label, "white")

cv.save(OUT)
