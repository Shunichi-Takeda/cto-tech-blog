"""タイムアウトしても検索がディスクを読み続ける — イメージ図

左に流れ（2場面）、右に見どころ。
  流れ1. CPUは暇: 使用率のメーターはほぼ0で、CPUは居眠りしている
  流れ2. 切っても読む: タイムアウトの砂時計には×が付いたのに、ディスクは赤く回り続ける
  見どころ. 秒単位で見る: 1分平均のなだらかな線（✗）と、上限に何度も張り付く秒単位の線（✓）

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
for sx, sy in [(3, 4), (58, 30), (110, 3), (118, 36), (2, 36), (60, 2)]:
    cv.put(sx, sy, "lav")

# --- 流れ1: CPUは暇 ---
# 使用率のメーター（針はほぼ0）
mx, my = 4, 11
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
cx, cy = 30, 12
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
cv.sprite(cx + 16, cy - 6, ["####", "...#", "..#.", ".#..", "####"], "lav")
cv.sprite(cx + 21, cy - 10, ["###", "..#", ".#.", "###"], "lav")

# --- 流れ2: 切っても読む ---
hx, hy = 66, 10                                  # 砂時計
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

dx, dy = 90, 8                                   # 回り続けるディスク
disk(dx, dy, "red", "white")
cv.put(dx + 7, dy + 7, "white")
for ax, ay, n in [(dx + 17, dy + 3, 3), (dx + 18, dy + 7, 4), (dx + 17, dy + 11, 3),
                  (dx - 4, dy + 4, 2), (dx - 5, dy + 10, 3)]:
    cv.rect(ax, ay, n, 1, "orange")              # 回り続ける線

cv.text_center(30, 33, "CPUは暇", "white")
cv.text_center(90, 33, "切っても読む", "white")

# --- 見どころ: 1分平均では見えない / 秒単位で見ると上限に張り付いている ---
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


def chart(x, y, w, h):
    """小さなグラフの台紙。上の赤い点線が上限"""
    cv.rect(x + 1, y + 1, w, h, "black")
    cv.rect(x, y, w, h, "bg")
    cv.rect(x, y + h - 1, w, 1, "gray")          # 横軸
    cv.rect(x, y, 1, h, "gray")                  # 縦軸
    for i in range(2, w, 2):
        cv.put(x + i, y + 2, "red")              # 上限


my = PY + 8
CW, CH = 22, 15
# 左: 1分平均 → なだらかで低い
lx = PX + 4
chart(lx, my, CW, CH)
for i, v in enumerate([10, 10, 10, 9, 9, 9, 9, 10, 10, 9, 9, 9, 8, 8, 9, 9, 9, 10, 10, 10]):
    cv.put(lx + 1 + i, my + v, "blue")
cv.sprite(lx + 8, my - 6, ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"], "red")

# 右: 秒単位 → 何度も上限に張り付く
rx_ = PX + 30
chart(rx_, my, CW, CH)
spikes = [11, 7, 3, 3, 9, 12, 5, 3, 3, 3, 10, 6, 3, 8, 12, 4, 3, 3, 9, 11]
prev = None
for i, v in enumerate(spikes):
    x = rx_ + 1 + i
    if prev is not None:                         # 縦につないでギザギザにする
        for yy in range(min(prev, v), max(prev, v) + 1):
            cv.put(x, my + yy, "yellow")
    cv.put(x, my + v, "yellow")
    prev = v
cv.sprite(rx_ + 8, my - 6, ["......#", ".....##", "#...##.", "##.##..", ".###..."], "green")
cv.text_center(PX + PW // 2, 33, "秒単位で見る", "yellow")

cv.save(OUT)
