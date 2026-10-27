"""「ありません」と言い切るAIを疑う — イメージ図

左から3場面を並べる。
  1. 見た所に無い: ロボットが懐中電灯で箱を1つだけ照らし、その箱は空
  2. 他の所に有る: 照らした箱は空のまま、照らしていない隣の箱から宝石がはみ出している
  3. 見た所を書く: チェックリストに、見た所はチェック、見ていない所は「?」

  python3 scripts/eyecatch/distrust-ai-agent-absence-claims.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "distrust-ai-agent-absence-claims", "overview.png")

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


def open_box(x, y, lit):
    """幅13・高さ11の、ふたの開いた箱。lit なら明るい色、そうでなければ暗い色"""
    side, inner = ("orange", "brown") if lit else ("dgray", "black")
    cv.rect(x + 1, y + 1, 13, 11, "black")
    cv.rect(x, y, 13, 11, side)
    cv.rect(x + 2, y + 1, 9, 3, inner)           # 中（空）
    cv.rect(x - 2, y - 2, 5, 2, side)            # 開いたふた（左）
    cv.rect(x + 10, y - 2, 5, 2, side)           # 開いたふた（右）


def beam(x0, y0, x1, top, bottom):
    """(x0, y0) から x1 まで広がる光。市松の点で描く"""
    for x in range(x0, x1 + 1):
        t = (x - x0) / max(1, x1 - x0)
        ya = round(y0 + (top - y0) * t)
        yb = round(y0 + (bottom - y0) * t)
        for y in range(ya, yb + 1):
            if (x + y) % 2 == 0:
                cv.put(x, y, "yellow")


def gem(x, y):
    cv.sprite(x, y, [".###.", "#####", ".###.", "..#.."], "blue")
    cv.put(x + 1, y, "white")


def sparkle(x, y, c):
    cv.sprite(x, y, [".#.", "###", ".#."], c)


# 背景の星
for sx, sy in [(3, 4), (30, 2), (58, 30), (88, 2), (118, 31), (176, 2), (2, 30), (110, 4)]:
    cv.put(sx, sy, "lav")

# 場面の区切り（細い点線）
for gx in (62, 120):
    for y in range(5, 44, 3):
        cv.put(gx, y, "navy2")

# 1: 見た所に無い — 懐中電灯で1つだけ照らす。中は空
robot(6, 10)
cv.rect(16, 21, 3, 1, "gray")                # 腕
cv.rect(19, 20, 4, 3, "dgray")               # 懐中電灯
cv.put(23, 21, "yellow")
beam(24, 21, 38, 12, 28)
open_box(40, 17, lit=True)

# 2: 他の所に有る — 照らした箱は空、隣の暗い箱から宝石
beam(64, 20, 70, 12, 28)
open_box(72, 17, lit=True)
open_box(92, 17, lit=False)
gem(96, 13)
sparkle(103, 10, "white")
sparkle(91, 9, "pink")

# 3: 見た場所を書く — チェックリスト
cv.rect(133, 4, 34, 26, "black")
cv.rect(132, 3, 34, 26, "white")             # 紙
cv.rect(144, 1, 10, 4, "dgray")              # クリップ
for k, mark in enumerate(["ok", "ok", "q"]):
    yy = 7 + k * 7
    if mark == "ok":
        cv.sprite(135, yy, ["....#", "...##", "#.##.", "###..", ".#..."], "dgreen")
    else:
        cv.sprite(136, yy - 1, [".##.", "#..#", "..#.", ".#..", "....", ".#.."], "orange")
    cv.rect(143, yy + 2, 19 - k * 3, 1, "gray")
    if mark == "q":
        cv.rect(143, yy + 2, 16, 1, "orange")    # 見ていない場所の行を目立たせる

# ラベル
cv.text_center(34, 33, "見た所に無い", "white")
cv.text_center(92, 33, "他の所に有る", "white")
cv.text_center(150, 33, "見た所を書く", "white")

cv.save(OUT)
