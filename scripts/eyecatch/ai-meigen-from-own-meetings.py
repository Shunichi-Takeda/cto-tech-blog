"""自分の会議録音から「偉人の名言」を作らせたら — イメージ図

左から3場面を並べる。
  1. 会議の一言: マイクと音の波形、点々だけの吹き出し
  2. 真顔で解説: ロボットが羽ペンを持ち、真顔（口は一文字）で紙に書く
  3. 名言になる: 額縁に入った、かぎ括弧つきの札とキラキラ

  python3 scripts/eyecatch/ai-meigen-from-own-meetings.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "ai-meigen-from-own-meetings", "overview.png")

cv = Canvas(184, 46)


def robot(x, y, eye="blue"):
    """幅12・高さ19のロボット。(x, y) は左上。口は一文字（真顔）"""
    cv.put(x + 5, y, "orange")                   # アンテナの先
    cv.rect(x + 5, y + 1, 1, 2, "gray")
    cv.rect(x + 1, y + 4, 11, 8, "black")        # 頭の影
    cv.rect(x, y + 3, 11, 8, "gray")             # 頭
    cv.rect(x + 2, y + 5, 2, 2, eye)             # 目
    cv.rect(x + 7, y + 5, 2, 2, eye)
    cv.rect(x + 3, y + 8, 5, 1, "dgray")         # 口（一文字）
    cv.rect(x + 4, y + 11, 3, 1, "dgray")        # 首
    cv.rect(x + 2, y + 13, 8, 6, "black")        # 胴の影
    cv.rect(x + 1, y + 12, 9, 6, "gray")         # 胴
    cv.rect(x + 4, y + 14, 3, 2, "dgray")        # 胸のパネル


def sparkle(x, y, c):
    cv.sprite(x, y, ["..#..", "..#..", "##.##", "..#..", "..#.."], c)


# 背景の星
for sx, sy in [(3, 4), (28, 2), (58, 30), (88, 2), (118, 31), (176, 2), (2, 30), (104, 29)]:
    cv.put(sx, sy, "lav")

# 場面の区切り（細い点線）
for gx in (62, 120):
    for y in range(5, 44, 3):
        cv.put(gx, y, "navy2")

# 1: 会議の一言 — マイク、波形、点々の吹き出し
cv.rect(15, 9, 7, 10, "black")               # マイクの影
cv.rect(14, 8, 7, 10, "dgray")               # マイクの頭
for j in range(9, 17, 2):                    # 網目
    cv.rect(15, j, 5, 1, "gray")
cv.rect(16, 18, 3, 2, "gray")                # 首
cv.rect(17, 20, 1, 7, "gray")                # 支柱
cv.rect(13, 27, 9, 2, "gray")                # 台
for i, h in enumerate([2, 5, 8, 4, 10, 6, 3, 7, 4, 2]):   # 音の波形
    cv.rect(26 + i * 2, 18 - h // 2, 1, h, "blue")
cv.rect(36, 3, 19, 9, "white")               # 吹き出し（点々だけ）
cv.rect(38, 12, 2, 2, "white")
for i in range(3):
    cv.rect(40 + i * 4, 7, 2, 2, "dgray")

# 2: 真顔で解説 — ロボットが羽ペンを持って、紙に書く
robot(70, 9)
cv.rect(87, 23, 17, 8, "black")              # 紙の影
cv.rect(86, 22, 17, 8, "white")              # 紙
for k in range(2):
    cv.rect(91, 24 + k * 3, 10 - k * 4, 1, "gray")
cv.rect(80, 21, 6, 1, "gray")                # 腕
cv.sprite(85, 9, [                           # 羽ペン（右上が羽、左下がペン先）
    "........##",
    ".......###",
    "......###.",
    ".....###..",
    "....###...",
    "...###....",
    "..###.....",
    "..##......",
    ".##.......",
    ".#........",
    ".#........",
    "#.........",
], "white")
cv.put(85, 20, "dgray")                      # ペン先（インク）
cv.rect(86, 18, 2, 2, "gray")                # 手

# 3: 名言になる — 額縁の札とキラキラ
cv.rect(132, 6, 36, 22, "black")             # 額の影
cv.rect(131, 5, 36, 22, "orange")            # 額縁
cv.rect(133, 7, 32, 18, "brown")
cv.rect(134, 8, 30, 16, "white")             # 札
cv.sprite(136, 10, ["####", "#...", "#...", "#..."], "dgray")     # 「
cv.sprite(158, 18, ["...#", "...#", "...#", "####"], "dgray")     # 」
for k in range(3):                           # 札の文字の行
    cv.rect(142, 12 + k * 3, 14 - k * 4, 1, "gray")
sparkle(125, 2, "yellow")
sparkle(169, 6, "yellow")
sparkle(170, 22, "pink")
cv.put(127, 26, "yellow")
cv.put(176, 15, "yellow")

# ラベル
cv.text_center(34, 33, "会議の一言", "white")
cv.text_center(92, 33, "真顔で解説", "white")
cv.text_center(150, 33, "名言になる", "white")

cv.save(OUT)
