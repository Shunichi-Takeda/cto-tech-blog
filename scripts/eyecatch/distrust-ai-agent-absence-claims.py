"""「ありません」と言い切るAIを疑う — イメージ図

左に流れ（2場面）、右に見どころ。
  流れ1. 見た所に無い: ロボットが懐中電灯で箱を1つだけ照らし、その箱は空
  流れ2. 他の所に有る: 照らした箱は空のまま、照らしていない隣の箱から宝石がはみ出している
  見どころ: 「無」とだけ言うロボット ✗ / 見た箱はチェック、見ていない箱は「?」の地図 ✓
            一言「見た所を書く」

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
for sx, sy in [(3, 4), (30, 2), (58, 30), (88, 2), (118, 31), (176, 2), (2, 30), (110, 4)]:
    cv.put(sx, sy, "lav")

# 1: 見た所に無い — 懐中電灯で1つだけ照らす。中は空
robot(6, 10)
cv.rect(16, 21, 3, 1, "gray")                # 腕
cv.rect(19, 20, 4, 3, "dgray")               # 懐中電灯
cv.put(23, 21, "yellow")
beam(24, 21, 38, 12, 28)
open_box(40, 17, lit=True)
cv.text_center(30, 33, "見た所に無い", "white")

# 2: 他の所に有る — 照らした箱は空、隣の暗い箱から宝石
beam(64, 20, 70, 12, 28)
open_box(72, 17, lit=True)
open_box(92, 17, lit=False)
gem(96, 13)
sparkle(103, 10, "white")
sparkle(91, 9, "pink")
cv.text_center(88, 33, "他の所に有る", "white")

# 3: 見どころ — 「無」とだけ言う ✗ / 見た所と見ていない所を書く ✓
panel()

# ✗: ロボットの頭と、「無」だけの吹き出し
cv.rect(130, 18, 11, 8, "black")
cv.rect(129, 17, 11, 8, "gray")
cv.rect(131, 19, 2, 2, "blue")
cv.rect(136, 19, 2, 2, "blue")
cv.rect(132, 22, 5, 1, "dgray")
cv.put(134, 16, "orange")
cv.rect(142, 12, 11, 11, "white")            # 吹き出し
cv.rect(141, 20, 2, 2, "white")              # 吹き出しのしっぽ
cv.text_center(147.5, 13, "無", "dgray", shadow=None)
bad(139, 7)

# ✓: 箱の並びの地図。見た箱はチェック、見ていない箱は「?」
for row in range(2):
    for col in range(3):
        bx, by = 156 + col * 8, 14 + row * 8
        cv.rect(bx + 1, by + 1, 6, 6, "black")
        if row == 0:                         # 見た箱
            cv.rect(bx, by, 6, 6, "white")
            cv.sprite(bx + 1, by + 1, ["...#", "..#.", "#.#.", ".#.."], "dgreen")
        else:                                # 見ていない箱
            cv.rect(bx, by, 6, 6, "dgray")
            cv.sprite(bx + 2, by + 1, ["##", ".#", "#.", "..", "#."], "orange")
good(165, 7)
cv.text_center(PX + PW // 2, 33, "見た所を書く", "yellow")

cv.save(OUT)
