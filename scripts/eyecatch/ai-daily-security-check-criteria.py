"""毎朝のセキュリティ確認をAIに任せる — イメージ図

左から3場面を並べる。
  1. 毎朝AIが見る: 朝日の下で、ロボット（AIエージェント）がログの紙束を読む
  2. 色を付ける: 判定のランプ4色（赤・黄・緑・青）
  3. 人は赤と黄: 人が立つのは赤と黄のランプの所だけ。緑と青には誰もいない

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


# 背景の星
for sx, sy in [(3, 4), (30, 2), (60, 30), (90, 31), (124, 1), (150, 30), (180, 3), (2, 30), (176, 28)]:
    cv.put(sx, sy, "lav")

# 場面の区切り（細い点線）
for gx in (62, 120):
    for y in range(5, 44, 3):
        cv.put(gx, y, "navy2")

# 1: 毎朝AIが見る
sunrise(42, 3)
robot(16, 10)
papers(34, 14)

# 2: 色を付ける（判定のパネル）
cv.rect(70, 12, 43, 15, "black")
cv.rect(69, 11, 43, 15, "dgray")
lamp_row(73, 16, 10)

# 3: 人は赤と黄（人が動くのは赤と黄だけ）
lamp_row(134, 21, 10)
for k in (0, 1):                                                  # 赤と黄の上にだけ人が立つ
    cv.sprite(133 + k * 10 + 1, 10 + 1, PERSON, "black")
    cv.sprite(133 + k * 10, 10, PERSON, "white")

for cx, label in [(31, "毎朝AIが見る"), (91, "色を付ける"), (152, "人は赤と黄")]:
    cv.text_center(cx, 33, label, "white")

cv.save(OUT)
