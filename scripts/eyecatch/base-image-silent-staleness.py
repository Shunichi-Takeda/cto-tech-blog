"""ビルドが落ちたものだけが見える — イメージ図

左に流れ（2場面）、右に見どころ。
  流れ1. 落ちると鳴る: ビルドが落ちたコンテナには赤い×が付き、ベルが鳴る
  流れ2. 静かに古びる: 普通に動いている（緑ランプ）コンテナに、クモの巣とほこりと古いカレンダー
  見どころ. 日付で棚卸し: ベルの鳴った順に並べると、ほこりの箱は最後尾（✗）。
           日付の古い順に並べると、ほこりの箱が先頭に来る（✓）

  python3 scripts/eyecatch/base-image-silent-staleness.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "base-image-silent-staleness", "overview.png")

cv = Canvas(184, 46)


def container(x, y, w=18, h=13, body="gray", lamp=None):
    """輸送用コンテナの形の箱（縦の溝つき）"""
    cv.rect(x + 1, y + 1, w, h, "black")
    cv.rect(x, y, w, h, body)
    cv.rect(x, y, w, 1, "white")
    for i in range(2, w - 1, 3):
        cv.rect(x + i, y + 2, 1, h - 3, "dgray")
    if lamp:
        cv.rect(x + w - 4, y + h - 3, 2, 1, lamp)


def calendar(x, y, w=7, h=7, page="white"):
    cv.rect(x + 1, y + 1, w, h, "black")
    cv.rect(x, y, w, h, page)
    cv.rect(x, y, w, 2, "red")
    for j in range(3, h - 1, 2):
        for i in range(1, w - 1, 2):
            cv.put(x + i, y + j, "gray")


# 背景の星
for sx, sy in [(3, 4), (58, 30), (110, 3), (118, 36), (2, 36), (60, 2)]:
    cv.put(sx, sy, "lav")

# --- 流れ1: 落ちると鳴る ---
container(8, 13)
BADGE = [".#######.", "#########", "#########", "#########", "#########",
         "#########", "#########", "#########", ".#######."]
cv.sprite(13, 16, BADGE, "black")                # 赤い×の札（ビルド失敗）
cv.sprite(12, 15, BADGE, "red")
cv.sprite(14, 17, ["##...##", ".##.##.", "..###..", ".##.##.", "##...##"], "white")
bx, by = 35, 9                                   # 鳴っているベル
cv.sprite(bx, by, [
    "....#....",
    "...###...",
    "..#####..",
    "..#####..",
    "..#####..",
    ".#######.",
    "#########",
    "....#....",
], "yellow")
cv.sprite(bx - 4, by + 1, ["..#", ".#.", "#..", ".#.", "..#"], "orange")   # 揺れの線
cv.sprite(bx + 10, by + 1, ["#..", ".#.", "..#", ".#.", "#.."], "orange")
cv.sprite(bx + 13, by + 2, ["#..", ".#.", "..#"], "orange")

# --- 流れ2: 静かに古びる ---
cx2, cy2 = 72, 13
container(cx2, cy2, lamp="green")
cv.sprite(cx2 + 12, cy2 + 1, [                   # 右上の隅のクモの巣
    "######",
    ".#..##",
    "..#.#.",
    "...###",
    "....##",
    ".....#",
], "white")
for i in range(1, 17, 2):                        # 天板のほこり
    cv.put(cx2 + i, cy2 - 1, "dgray")
cv.put(cx2 + 4, cy2 - 2, "dgray")
cv.put(cx2 + 9, cy2 - 2, "dgray")
calendar(cx2 + 22, cy2 - 3, 9, 10)               # 古いカレンダー（めくられていない）
cv.rect(cx2 + 22, cy2 - 3, 9, 2, "brown")
for i in range(0, 9, 2):                         # 天辺のほこり
    cv.put(cx2 + 22 + i, cy2 - 4, "dgray")

cv.text_center(30, 33, "落ちると鳴る", "white")
cv.text_center(88, 33, "静かに古びる", "white")

# --- 見どころ: ベルの順では古い箱が最後 / 日付の順なら先頭 ---
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


def mini(x, y, kind, cal=None):
    """小さなコンテナ。kind: "broken"（×の札）/ "plain" / "dusty"（ほこり）"""
    container(x, y, w=11, h=7)
    if kind == "broken":                         # 赤い×の札
        cv.rect(x + 3, y + 1, 5, 5, "red")
        cv.sprite(x + 4, y + 2, ["#.#", ".#.", "#.#"], "white")
    if kind == "dusty":
        for i in range(0, 11, 2):
            cv.put(x + i, y - 1, "dgray")
    if cal:                                      # 右上に小さなカレンダー（古いものは灰色で茶色の帯）
        page, top = cal
        cv.rect(x + 7, y - 3, 5, 5, page)
        cv.rect(x + 7, y - 3, 5, 1, top)


MARK_X = PX + 3
COLS = [PX + 11, PX + 25, PX + 39]
# 上の段 ✗: ベルの鳴った順 → ほこりの箱が最後尾
r1 = 11
cv.sprite(MARK_X, r1 + 1, ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"], "red")
for x, kind in zip(COLS, ["broken", "plain", "dusty"]):
    mini(x, r1, kind)

# 下の段 ✓: 日付の古い順 → ほこりの箱が先頭（黄色で囲む）
r2 = 23
cv.sprite(MARK_X - 1, r2 + 1, ["......#", ".....##", "#...##.", "##.##..", ".###..."], "green")
for x, kind, cal in zip(COLS, ["dusty", "plain", "broken"],
                        [("gray", "brown"), ("white", "red"), ("white", "red")]):
    mini(x, r2, kind, cal)
ox = COLS[0] - 2                                 # いちばん古い箱を囲む
for i in range(15):
    cv.put(ox + i, r2 - 5, "yellow")
    cv.put(ox + i, r2 + 8, "yellow")
for j in range(-5, 9):
    cv.put(ox, r2 + j, "yellow")
    cv.put(ox + 14, r2 + j, "yellow")

cv.text_center(PX + PW // 2, 33, "日付で棚卸し", "yellow")

cv.save(OUT)
