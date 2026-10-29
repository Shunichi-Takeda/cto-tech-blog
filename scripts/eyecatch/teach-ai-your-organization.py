"""AIに開発を任せる前に、AIに会社を教える — イメージ図

左に流れ（2場面）、右に見どころ。
  流れ1. 無難な案: ロボットだけが立っていて、出てくるのは灰色の無個性な箱
  流れ2. 会社を教える: ロボットが組織のナレッジの本を読んでいる（付箋つき）
  見どころ: 工程のブロック1つだけを虫眼鏡で見る ✗ / ブロックの継ぎ目を見る ✓
            一言「継ぎ目を見る」

  python3 scripts/eyecatch/teach-ai-your-organization.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "teach-ai-your-organization", "overview.png")

cv = Canvas(184, 46)


def robot(x, y, eye="blue"):
    """幅12・高さ19のロボット。(x, y) は左上"""
    cv.put(x + 5, y, "orange")                   # アンテナの先
    cv.rect(x + 5, y + 1, 1, 2, "gray")
    cv.rect(x + 1, y + 4, 11, 8, "black")        # 頭の影
    cv.rect(x, y + 3, 11, 8, "gray")             # 頭
    cv.rect(x + 2, y + 5, 2, 2, eye)             # 目
    cv.rect(x + 7, y + 5, 2, 2, eye)
    cv.rect(x + 3, y + 8, 5, 1, "dgray")         # 口
    cv.rect(x + 4, y + 11, 3, 1, "dgray")        # 首
    cv.rect(x + 2, y + 13, 8, 6, "black")        # 胴の影
    cv.rect(x + 1, y + 12, 9, 6, "gray")         # 胴
    cv.rect(x + 4, y + 14, 3, 2, "dgray")        # 胸のパネル


def box(x, y, c):
    cv.rect(x + 1, y + 1, 8, 7, "black")
    cv.rect(x, y, 8, 7, c)
    cv.rect(x, y, 8, 2, "dgray" if c == "gray" else "white")   # ふた
    cv.rect(x + 3, y, 2, 7, "dgray" if c == "gray" else "white")


def arrow(x, y, length, c):
    cv.rect(x, y, length - 2, 1, c)
    cv.sprite(x + length - 3, y - 2, ["#..", "##.", "###", "##.", "#.."], c)


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
for sx, sy in [(3, 4), (28, 2), (58, 30), (88, 2), (118, 31), (140, 2), (180, 4), (2, 30), (176, 29)]:
    cv.put(sx, sy, "lav")

# 1: 無難な案 — ロボットだけ。出てくる箱はどれも同じ灰色
robot(12, 9)
arrow(27, 21, 8, "lav")
for bx, by in [(37, 21), (46, 21), (41, 13)]:
    box(bx, by, "gray")
cv.text_center(30, 33, "無難な案", "white")

# 2: 会社を教える — ロボットが本を読む
robot(70, 9)
cv.rect(85, 15, 17, 12, "black")
cv.rect(84, 14, 8, 11, "white")              # 左ページ
cv.rect(92, 14, 8, 11, "white")              # 右ページ
cv.rect(91, 14, 2, 11, "brown")              # 背
cv.rect(84, 25, 16, 1, "brown")              # 表紙の下端
for k in range(4):                           # 行
    cv.rect(85, 16 + k * 2, 5, 1, "gray")
    cv.rect(94, 16 + k * 2, 5, 1, "gray")
cv.rect(86, 11, 2, 4, "pink")                # 付箋
cv.rect(89, 10, 2, 5, "yellow")
cv.rect(95, 11, 2, 4, "green")
cv.rect(98, 10, 2, 5, "blue")
cv.text_center(88, 33, "会社を教える", "white")

# 3: 見どころ — 1つだけ見る ✗ / 継ぎ目を見る ✓
panel()


def steps(x, y):
    """設計・実装・テストの3ブロック（幅6、すき間1）"""
    for k, c in enumerate(["blue", "orange", "green"]):
        cv.rect(x + k * 7 + 1, y + 1, 6, 7, "black")
        cv.rect(x + k * 7, y, 6, 7, c)
        cv.rect(x + k * 7 + 1, y + 2, 4, 1, "white")
        cv.rect(x + k * 7 + 1, y + 4, 3, 1, "white")


def lens(cx, cy):
    """中心 (cx, cy) の虫眼鏡。柄は右下"""
    cv.sprite(cx - 4, cy - 4, [
        "..#####..",
        ".#.....#.",
        "#.......#",
        "#.......#",
        "#.......#",
        "#.......#",
        "#.......#",
        ".#.....#.",
        "..#####..",
    ], "yellow")
    for k in range(3):
        cv.rect(cx + 4 + k, cy + 4 + k, 2, 2, "brown")


steps(129, 17)
lens(132, 20)                                # 設計のブロックだけを見ている
bad(137, 8)
steps(156, 17)
lens(169, 20)                                # 実装とテストの継ぎ目を見ている
good(164, 8)
cv.text_center(PX + PW // 2, 33, "継ぎ目を見る", "yellow")

cv.save(OUT)
