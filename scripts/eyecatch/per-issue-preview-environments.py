"""課題ごとに作って消すプレビュー環境 — イメージ図

左から3場面を並べる。どの場面も「課題カード → その課題専用の環境」。
  1. 日中: 環境は稼働中（太陽、ランプ点灯）
  2. 夜間: 環境は停止中（月と Z、ランプ消灯）
  3. 完了: 環境は輪郭だけ残して、粒になって消える（課題にチェック）

  python3 scripts/eyecatch/per-issue-preview-environments.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "per-issue-preview-environments", "overview.png")

cv = Canvas(184, 46)


def ticket(x, y, tab, done=False):
    cv.rect(x + 1, y + 1, 18, 12, "black")       # 影
    cv.rect(x, y, 18, 12, "white")
    cv.rect(x, y, 4, 12, tab)                    # 色の帯 = 課題キー
    for k in range(3):                           # 本文の行
        cv.rect(x + 6, y + 3 + k * 3, 10 - k * 3, 1, "gray")
    if done:                                     # 完了のチェック
        cv.sprite(x + 9, y + 3, [
            "......#",
            ".....##",
            "#...##.",
            "##.##..",
            ".###...",
            "..#....",
        ], "dgreen")


def arrow(x, y, length, c):
    cv.rect(x, y - 1, length - 3, 3, c)
    cv.sprite(x + length - 4, y - 4, [
        "#....", "##...", "###..", "####.", "#####", "####.", "###..", "##...", "#....",
    ], c)


def server(x, y, tab, state):
    body = "dgray" if state == "sleep" else "gray"
    cv.rect(x + 1, y + 1, 16, 12, "black")
    cv.rect(x, y, 16, 12, body)
    cv.rect(x, y, 16, 2, tab)                    # 課題と同じ色の札 = 課題番号付きの名前
    for k in range(2):                           # ラック2段
        yy = y + 4 + k * 4
        cv.rect(x + 2, yy, 12, 3, "navy2" if state == "sleep" else "dgray")
        if state == "run":
            cv.put(x + 12, yy + 1, "green")
            if k == 0:
                cv.put(x + 10, yy + 1, "orange")


def ghost(x, y):
    """消えていく環境: 点線の輪郭と、右上へ散っていく粒"""
    for i in range(0, 16, 2):
        cv.put(x + i, y, "lav")
        cv.put(x + i, y + 11, "lav")
    for j in range(0, 12, 2):
        cv.put(x, y + j, "lav")
        cv.put(x + 15, y + j, "lav")
    cv.put(x + 1, y + 1, "orange")
    cv.put(x + 2, y + 1, "orange")               # 札の名残
    for dx, dy, c in [
        (4, 4, "gray"), (7, 6, "gray"), (9, 3, "orange"), (12, 5, "gray"),
        (17, 3, "gray"), (18, 7, "lav"), (19, 1, "lav"), (20, 5, "lav"),
        (21, -1, "navy2"), (22, 3, "navy2"), (22, -3, "navy2"), (17, 9, "gray"),
    ]:
        cv.put(x + dx, y + dy, c)


# 背景の星
for sx, sy in [(3, 4), (30, 2), (58, 33), (90, 3), (118, 36), (2, 36), (110, 8)]:
    cv.put(sx, sy, "lav")

# --- 流れ: 課題ごとに作る → 完了で消す ---
TY = 15          # カードと環境の上端
ticket(4, TY, "red")
arrow(25, TY + 6, 13, "yellow")
server(40, TY, "red", "run")
cv.text_center(30, 33, "課題ごとに作る", "white")

ticket(62, TY, "orange", done=True)
arrow(83, TY + 6, 13, "yellow")
ghost(98, TY)
cv.text_center(88, 33, "完了で消す", "white")

# --- 見どころ: 1つを使い回すと混ざる / 課題ごとなら混ざらない ---
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

# 左: 1つの環境を使い回す → 色が混ざる
mx, my = PX + 4, PY + 8
cv.rect(mx + 1, my + 1, 20, 14, "black")
cv.rect(mx, my, 20, 14, "gray")
mixed = [["red", "blue", "orange", "blue"], ["orange", "red", "blue", "red"], ["blue", "orange", "red", "orange"]]
for r, row in enumerate(mixed):
    for c, col in enumerate(row):
        cv.rect(mx + 2 + c * 4, my + 2 + r * 4, 3, 3, col)
cv.sprite(mx + 8, my - 6, ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"], "red")

# 右: 課題ごとに分ける → 1色ずつ
for k, col in enumerate(["red", "blue", "orange"]):
    bx = PX + 30 + k * 8
    cv.rect(bx + 1, my + 1, 6, 14, "black")
    cv.rect(bx, my, 6, 14, "gray")
    cv.rect(bx, my, 6, 2, col)
    for r in range(3):
        cv.rect(bx + 1, my + 3 + r * 4, 4, 3, col)
cv.sprite(PX + 37, my - 6, ["......#", ".....##", "#...##.", "##.##..", ".###..."], "green")
cv.text_center(PX + PW // 2, 33, "混ざらない", "yellow")

cv.save(OUT)
