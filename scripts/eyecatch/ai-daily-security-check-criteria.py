"""毎朝のセキュリティ確認をAIに任せる — イメージ図

左に流れ（2場面）、右に見どころ（金色の枠）。
  流れ1 毎朝AIが見る: 朝日の下で、ロボット（AIエージェント）がログの紙束を読む
  流れ2 色を付ける: 判定のランプ4色（赤・黄・緑・青）
  見どころ 人が動くか:
    ✗ ランプが全部赤。毎回赤なので、人は眠ってしまう
    ✓ 色が分かれ、人が立つのは赤と黄のランプの上だけ

  python3 scripts/eyecatch/ai-daily-security-check-criteria.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "ai-daily-security-check-criteria", "overview.png")

cv = Canvas(184, 46)

LAMP = [".###.", "#####", "#####", "#####", ".###."]
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


def robot(x, y):
    cv.put(x + 6, y, "red")                                       # アンテナ
    cv.rect(x + 6, y + 1, 1, 2, "gray")
    cv.rect(x + 1, y + 3, 12, 7, "gray")                          # 頭
    cv.rect(x + 3, y + 5, 2, 2, "blue")                           # 目
    cv.rect(x + 9, y + 5, 2, 2, "blue")
    cv.rect(x + 4, y + 8, 6, 1, "dgray")                          # 口
    cv.rect(x + 2, y + 11, 10, 6, "lav")                          # 胴
    cv.rect(x + 5, y + 13, 4, 2, "yellow")
    cv.rect(x + 12, y + 12, 3, 2, "lav")                          # 紙へ伸ばした腕


def papers(x, y):
    for k, dx in enumerate((2, 1, 0)):
        yy = y + k * 2
        cv.rect(x + dx + 1, yy + 1, 10, 9, "black")
        cv.rect(x + dx, yy, 10, 9, "white")
    for k in range(3):                                            # ログの行
        cv.rect(x + 2, y + 7 + k * 2, 6 - (k % 2) * 2, 1, "gray")


def sunrise(x, y):
    cv.sprite(x, y, [
        "#...#...#",
        ".#..#..#.",
        "...###...",
        "#.#####.#",
        ".#######.",
    ], "orange")
    cv.rect(x - 2, y + 5, 13, 1, "orange")                         # 地平線


def lamp_row(x, y, step):
    for k, c in enumerate(("red", "yellow", "green", "blue")):
        cv.sprite(x + k * step + 1, y + 1, LAMP, "black")
        cv.sprite(x + k * step, y, LAMP, c)


SMALL_LAMP = [".###.", "#####", "#####", ".###."]
SMALL_PERSON = [".###.", ".###.", "..#..", "#####", "..#..", ".#.#.", "#...#"]
SLEEPER = [                                                       # 横になって眠る人
    ".##......",
    ".########",
    "....#####",
    "....#...#",
]


def small_lamps(x, y, colors, step=6):
    for k, c in enumerate(colors):
        cv.sprite(x + k * step + 1, y + 1, SMALL_LAMP, "black")
        cv.sprite(x + k * step, y, SMALL_LAMP, c)


# 背景の星
for sx, sy in [(3, 4), (30, 2), (58, 33), (90, 3), (118, 36), (2, 36), (110, 8)]:
    cv.put(sx, sy, "lav")

# --- 流れ: 毎朝AIが見る → 色を付ける ---
sunrise(34, 3)
robot(8, 10)
papers(27, 14)
cv.text_center(30, 33, "毎朝AIが見る", "white")

cv.rect(68, 12, 43, 15, "black")
cv.rect(67, 11, 43, 15, "dgray")
lamp_row(71, 16, 10)
cv.text_center(88, 33, "色を付ける", "white")

# --- 見どころ: 全部赤だと誰も動かない / 色を分けると人が動く所が決まる ---
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

LY = PY + 21                                     # ランプの上端
# 左: ランプが全部赤 → 人は眠ってしまう
small_lamps(PX + 2, LY, ["red", "red", "red"], step=7)
cv.sprite(PX + 8, LY - 11, PERSON, "lav")
cv.sprite(PX + 16, LY - 14, ["###", "..#", ".#.", "###"], "lav")
cv.sprite(PX + 20, LY - 18, ["##", ".#", "##"], "lav")
cv.sprite(PX + 3, PY + 3, ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"], "red")
for y in range(PY + 4, PY + 28, 2):              # 左右の仕切り
    cv.put(PX + 24, y, "lav")

# 右: 色が分かれ、赤と黄の上にだけ人が立つ
small_lamps(PX + 27, LY, ["red", "yellow", "green", "blue"], step=7)
for k in (0, 1):
    cv.sprite(PX + 26 + k * 7, LY - 10, PERSON, "white")
cv.sprite(PX + 44, PY + 3, ["......#", ".....##", "#...##.", "##.##..", ".###..."], "green")
cv.text_center(PX + PW // 2, 33, "人が動くか", "yellow")

cv.save(OUT)
