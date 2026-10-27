"""自分の会議録音から「偉人の名言」を作らせたら — イメージ図

左に流れ（2場面）、右に見どころ。
  流れ1. 会議の一言: マイクと音の波形、点々だけの吹き出し
  流れ2. 真顔で解説: ロボットが羽ペンを持ち、真顔（口は一文字）で紙に書く
  見どころ: にやけたロボットとただの紙 ✗ / 真顔のロボットとキラキラの額縁 ✓
            一言「真顔が効く」

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


# --- 見どころ: 金色の枠と電球 ---
PX, PY, PW, PH = 126, 5, 56, 38


def panel():
    for i in range(PW):                          # 金色の枠
        cv.put(PX + i, PY, "orange")
        cv.put(PX + i, PY + PH - 1, "orange")
    for j in range(PH):
        cv.put(PX, PY + j, "orange")
        cv.put(PX + PW - 1, PY + j, "orange")
    cv.rect(PX + 1, PY + 1, PW - 2, PH - 2, "navy2")
    cv.sprite(PX + PW // 2 - 3, 0, [           # 電球（得られるもの）
        "..###..",
        ".#####.",
        "#######",
        "#######",
        ".#####.",
        "..###..",
        "..###..",
    ], "yellow")
    cv.rect(PX + PW // 2 - 1, 7, 3, 1, "gray")
    for rx, ry in [(-6, 1), (-5, 4), (6, 1), (5, 4)]:   # 光の線
        cv.put(PX + PW // 2 + rx, ry, "yellow")


def bad(x, y):
    cv.sprite(x, y, ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"], "red")


def good(x, y):
    cv.sprite(x, y, ["......#", ".....##", "#...##.", "##.##..", ".###..."], "green")


# 背景の星
for sx, sy in [(3, 4), (28, 2), (58, 30), (88, 2), (118, 31), (176, 2), (2, 30), (104, 29)]:
    cv.put(sx, sy, "lav")

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
cv.text_center(30, 33, "会議の一言", "white")

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
cv.text_center(88, 33, "真顔で解説", "white")

# 3: 見どころ — にやけると台無し ✗ / 真顔で名言になる ✓
panel()


def head(x, y, smile):
    """幅11・高さ8のロボットの頭"""
    cv.rect(x + 1, y + 1, 11, 8, "black")
    cv.rect(x, y, 11, 8, "gray")
    cv.rect(x + 2, y + 2, 2, 2, "blue")
    cv.rect(x + 7, y + 2, 2, 2, "blue")
    if smile:                                # にやけた口
        cv.sprite(x + 2, y + 5, ["#.....#", ".#####."], "dgray")
    else:                                    # 一文字の口（真顔）
        cv.rect(x + 3, y + 5, 5, 1, "dgray")
    cv.put(x + 5, y - 1, "orange")           # アンテナ


def sparkle(x, y, c):
    cv.sprite(x, y, [".#.", "###", ".#."], c)


# ✗: にやけたロボットと、ただの紙
head(129, 16, smile=True)
cv.rect(143, 16, 9, 11, "black")
cv.rect(142, 15, 9, 11, "white")
for k in range(3):
    cv.rect(143, 18 + k * 3, 6 - k * 2, 1, "gray")
bad(137, 7)

# ✓: 真顔のロボットと、キラキラの額縁の名言
head(155, 16, smile=False)
cv.rect(169, 15, 11, 12, "black")
cv.rect(168, 14, 11, 12, "orange")           # 額縁
cv.rect(169, 15, 9, 10, "white")
cv.sprite(170, 16, ["##", "#."], "dgray")    # 「
cv.sprite(175, 22, [".#", "##"], "dgray")    # 」
cv.rect(172, 19, 4, 1, "gray")
sparkle(166, 27, "yellow")
sparkle(177, 10, "yellow")
good(162, 7)
cv.text_center(PX + PW // 2, 33, "真顔が効く", "yellow")

cv.save(OUT)
