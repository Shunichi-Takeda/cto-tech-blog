"""AIに開発を任せる前に、AIに会社を教える — イメージ図

左から3場面を並べる。
  1. 無難な案: ロボットだけが立っていて、出てくるのは灰色の無個性な箱
  2. 会社を教える: ロボットが組織のナレッジの本を読んでいる（付箋つき）
  3. 継ぎ目を見る: 設計・実装・テストのブロックが矢印でつながり、別のロボットが虫眼鏡で継ぎ目を見ている

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


# 背景の星
for sx, sy in [(3, 4), (28, 2), (58, 30), (88, 2), (118, 31), (140, 2), (180, 4), (2, 30), (176, 29)]:
    cv.put(sx, sy, "lav")

# 場面の区切り（細い点線）
for gx in (62, 120):
    for y in range(5, 44, 3):
        cv.put(gx, y, "navy2")

# 1: 無難な案 — ロボットだけ。出てくる箱はどれも同じ灰色
robot(12, 9)
arrow(27, 21, 8, "lav")
for i, (bx, by) in enumerate([(37, 21), (46, 21), (41, 13)]):
    box(bx, by, "gray")

# 2: 会社を教える — ロボットが本を読む
robot(72, 9)
# 開いた本（ロボットの手元から右へ）
cv.rect(86, 15, 17, 12, "black")
cv.rect(85, 14, 8, 11, "white")              # 左ページ
cv.rect(93, 14, 8, 11, "white")              # 右ページ
cv.rect(92, 14, 2, 11, "brown")              # 背
cv.rect(85, 25, 16, 1, "brown")              # 表紙の下端
for k in range(4):                           # 行
    cv.rect(86, 16 + k * 2, 5, 1, "gray")
    cv.rect(95, 16 + k * 2, 5, 1, "gray")
cv.rect(87, 11, 2, 4, "pink")                # 付箋
cv.rect(90, 10, 2, 5, "yellow")
cv.rect(96, 11, 2, 4, "green")
cv.rect(99, 10, 2, 5, "blue")

# 3: 継ぎ目を見る — 設計・実装・テストが矢印でつながり、継ぎ目を虫眼鏡で見る
for bx, c in [(124, "blue"), (138, "orange"), (152, "green")]:
    cv.rect(bx + 1, 7, 10, 8, "black")
    cv.rect(bx, 6, 10, 8, c)
    cv.rect(bx + 2, 8, 6, 1, "white")
    cv.rect(bx + 2, 10, 4, 1, "white")
    cv.rect(bx + 2, 12, 5, 1, "white")
arrow(134, 10, 4, "yellow")
arrow(148, 10, 4, "yellow")
# 虫眼鏡（実装とテストの継ぎ目に重ねる）
cv.sprite(145, 5, [
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
for k in range(5):                           # 柄（右下のロボットへ）
    cv.rect(152 + k, 13 + k, 2, 2, "brown")
# 別のロボット（目の色を変える）
robot(160, 12, eye="green")

# ラベル
cv.text_center(34, 33, "無難な案", "white")
cv.text_center(92, 33, "会社を教える", "white")
cv.text_center(150, 33, "継ぎ目を見る", "white")

cv.save(OUT)
