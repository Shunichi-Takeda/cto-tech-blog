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
for sx, sy in [(3, 4), (30, 2), (60, 30), (90, 31), (124, 1), (150, 30), (180, 3), (2, 30), (176, 28)]:
    cv.put(sx, sy, "lav")

# 場面の区切り（細い点線）
for gx in (62, 120):
    for y in range(5, 44, 3):
        cv.put(gx, y, "navy2")

TY = 15          # カードと環境の上端
SCENES = [
    (8, "red", "run", "日中は動く"),
    (66, "blue", "sleep", "夜は止める"),
    (124, "orange", "done", "完了で消える"),
]
for gx, tab, state, caption in SCENES:
    ticket(gx, TY, tab, done=(state == "done"))
    arrow(gx + 21, TY + 6, 13, "yellow")
    sx = gx + 36
    if state == "done":
        ghost(sx, TY)
    else:
        server(sx, TY, tab, state)
    cv.text_center(gx + 26, 33, caption, "white")

# 1: 太陽（日中は稼働）
cv.sprite(8 + 40, 3, [
    "#..#..#",
    ".#.#.#.",
    "..###..",
    "#######",
    "..###..",
    ".#.#.#.",
    "#..#..#",
], "orange")
# 2: 月と Z（夜は停止）
cv.sprite(66 + 39, 3, ["..###", ".##..", "##...", "##...", "##...", ".##..", "..###"], "yellow")
cv.sprite(66 + 46, 1, ["####", "...#", "..#.", ".#..", "####"], "lav")

cv.save(OUT)
