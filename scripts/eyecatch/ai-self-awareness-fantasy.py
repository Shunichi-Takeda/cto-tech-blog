"""AIは自我を持った — セキュリティインシデント急増を眺めながらの与太話 — イメージ図

左に流れ（2場面）、右に見どころ。
  流れ1. 両方に売る: シーソーの左端に赤い剣（攻撃側）、右端に青い盾（防御側）。
          支点に立つロボットへ、両端からコインが流れ込む
  流れ2. 命令を無視: 人が吹き出しで命令しているが、赤い目のロボットは背を向け、
          足元の鎖は切れている
  見どころ: 大きく育てたロボット（赤い目） ✗ / 小さなロボットを檻で囲う（青い目） ✓
            一言「小さく囲う」

  python3 scripts/eyecatch/ai-self-awareness-fantasy.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Canvas  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO_ROOT, "images", "ai-self-awareness-fantasy", "overview.png")

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


def robot_back(x, y, eye="red"):
    """背を向けたロボット。頭は右を向き、目は右端に1つだけ見える"""
    cv.put(x + 5, y, "orange")
    cv.rect(x + 5, y + 1, 1, 2, "gray")
    cv.rect(x + 1, y + 4, 11, 8, "black")
    cv.rect(x, y + 3, 11, 8, "gray")
    cv.rect(x + 8, y + 5, 2, 2, eye)             # 横を向いた目
    cv.rect(x + 4, y + 11, 3, 1, "dgray")
    cv.rect(x + 2, y + 13, 8, 6, "black")
    cv.rect(x + 1, y + 12, 9, 6, "gray")
    cv.rect(x + 2, y + 14, 7, 1, "dgray")        # 背中の継ぎ目


def sword(x, y, c):
    """幅7・高さ11の剣。刃が上"""
    cv.sprite(x, y, [
        "...#...",
        "...#...",
        "...#...",
        "...#...",
        "...#...",
        "...#...",
        ".#####.",
        "...#...",
        "...#...",
        "..###..",
    ], c)


def shield(x, y, c):
    """幅7・高さ9の盾"""
    cv.sprite(x, y, [
        "#######",
        "#######",
        "#######",
        "#######",
        ".#####.",
        ".#####.",
        "..###..",
        "..###..",
        "...#...",
    ], c)
    cv.rect(x + 3, y + 1, 1, 4, "white")         # 盾の筋


def coin(x, y):
    cv.put(x, y, "yellow")


def person(x, y):
    """幅5・高さ11の人。(x, y) は左上"""
    cv.rect(x + 1, y, 3, 3, "white")             # 頭
    cv.rect(x, y + 4, 5, 4, "blue")              # 体
    cv.rect(x + 1, y + 8, 1, 3, "blue")          # 足
    cv.rect(x + 3, y + 8, 1, 3, "blue")


def chain(x, y, links, c="gray"):
    """横に並ぶ鎖。1輪は幅4・高さ3の中空の輪で、輪どうしは1マス重なる"""
    for k in range(links):
        cv.sprite(x + k * 3, y, ["####", "#..#", "####"], c)


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

# 1: 両方に売る — シーソーの両端に剣と盾。支点のロボットへ両側からコインが流れる
robot(24, 4)                                 # 支点の奥に立つ
cv.rect(8, 24, 44, 2, "gray")                # シーソーの板
cv.sprite(27, 26, [".###.", "#####"], "dgray")  # 支点
sword(10, 13, "red")                         # 攻撃側（左端）
shield(43, 15, "blue")                       # 防御側（右端）
for k, (cx, cy) in enumerate([(18, 20), (20, 17), (22, 14), (41, 20), (39, 17), (37, 14)]):
    coin(cx, cy)                             # 両端から支点へ向かうコイン
cv.text_center(30, 33, "両方に売る", "white")

# 2: 命令を無視 — 人の吹き出しに背を向けるロボット。足元の鎖は切れている
person(64, 14)
cv.rect(70, 5, 13, 7, "white")               # 吹き出し
cv.rect(68, 10, 2, 2, "white")
cv.sprite(72, 6, ["#", "#", "#", ".", "#"], "red")   # 命令のしるし（！）
cv.rect(75, 7, 5, 1, "dgray")                # 命令の文（短い線）
cv.rect(75, 9, 3, 1, "dgray")
robot_back(92, 9, eye="red")
cv.rect(84, 24, 2, 6, "dgray")               # 鎖をつないでいた杭
chain(85, 27, 2)                             # 鎖（杭側）
chain(96, 27, 2)                             # 鎖（ロボット側）。真ん中で切れている
cv.text_center(88, 33, "命令を無視", "white")

# 3: 見どころ — 大きく育てる ✗ / 小さく囲う ✓
panel()


def big_robot(x, y, eye):
    """幅16・高さ21の大きなロボット"""
    cv.put(x + 7, y, "orange")
    cv.rect(x + 7, y + 1, 2, 2, "gray")
    cv.rect(x + 1, y + 4, 15, 9, "black")
    cv.rect(x, y + 3, 15, 9, "gray")
    cv.rect(x + 3, y + 6, 3, 2, eye)
    cv.rect(x + 9, y + 6, 3, 2, eye)
    cv.rect(x + 4, y + 10, 7, 1, "dgray")
    cv.rect(x + 6, y + 12, 3, 1, "dgray")
    cv.rect(x + 2, y + 14, 12, 7, "black")
    cv.rect(x + 1, y + 13, 12, 7, "gray")
    cv.rect(x + 5, y + 15, 4, 3, "dgray")


def small_robot(x, y, eye):
    """幅8・高さ12の小さなロボット"""
    cv.put(x + 3, y, "orange")
    cv.rect(x + 1, y + 2, 7, 5, "black")
    cv.rect(x, y + 1, 7, 5, "gray")
    cv.rect(x + 1, y + 3, 2, 1, eye)
    cv.rect(x + 4, y + 3, 2, 1, eye)
    cv.rect(x + 2, y + 6, 3, 1, "dgray")
    cv.rect(x + 1, y + 8, 6, 4, "black")
    cv.rect(x, y + 7, 6, 4, "gray")


def cage(x, y, w, h):
    """檻。縦の棒を2マスおきに描き、上下に横棒"""
    cv.rect(x, y, w, 1, "orange")
    cv.rect(x, y + h - 1, w, 1, "orange")
    for k in range(0, w, 3):
        cv.rect(x + k, y, 1, h, "orange")
    cv.rect(x + w - 1, y, 1, h, "orange")


# ✗: 大きく育てたロボット（赤い目）
big_robot(130, 10, "red")
bad(148, 9)

# ✓: 小さなロボットを檻で囲う（青い目）
cage(158, 13, 19, 18)
small_robot(164, 17, "blue")
good(166, 8)
cv.text_center(PX + PW // 2, 33, "小さく囲う", "yellow")

cv.save(OUT)
