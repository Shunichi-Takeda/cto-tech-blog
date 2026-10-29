"""記事のイメージ図（ドット絵）を描くための共通処理。

外部ライブラリに依存しない（Pillow なしで動く）ことを条件にしている。
PNG は標準ライブラリの zlib と struct で書き出す。

座標は「絵の1マス」を単位にする。1マスは出力で DOT * ART 画素の正方形になる。
文字だけは半分の細かさ（1マスを ART 分割した点）で描く。日本語を絵の1マスで描くと
潰れて読めないため。点の大きさが半分でも、アンチエイリアスを切った点の並びなので、
ドット絵の中で浮かない。

文字の点の並びは、macOS の CoreText で描かせる（glyph.swift）。
既定のフォントは macOS に標準で入っている BIZ UDゴシック Bold。
"""
import os
import struct
import subprocess
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))

# PICO-8 パレット。色はこの中から選ぶ（記事ごとに配色を変えない）
PALETTE = {
    "bg": (29, 43, 83), "navy2": (35, 52, 98), "white": (255, 241, 232),
    "gray": (194, 195, 199), "dgray": (95, 87, 79), "red": (255, 0, 77),
    "orange": (255, 163, 0), "yellow": (255, 236, 39), "green": (0, 228, 54),
    "dgreen": (0, 135, 81), "blue": (41, 173, 255), "lav": (131, 118, 156),
    "pink": (255, 119, 168), "brown": (171, 82, 54), "black": (0, 0, 0),
}

FONT = "BIZUDGothic-Bold"
FONT_PX = 16       # 文字の点の高さ（細かい方の点で数える）
ART = 2            # 絵の1マス = 細かい点 ART x ART
DOT = 5            # 細かい点1つ = 出力 DOT x DOT 画素


class Canvas:
    def __init__(self, w, h, bg="bg"):
        self.w, self.h = w, h                     # 絵のマス数
        self.fw, self.fh = w * ART, h * ART       # 細かい点の数
        self.px = [[PALETTE[bg]] * self.fw for _ in range(self.fh)]

    # --- 絵（1マス単位） ---
    def put(self, x, y, c):
        for j in range(ART):
            for i in range(ART):
                self._fine(x * ART + i, y * ART + j, c)

    def rect(self, x, y, w, h, c):
        for j in range(h):
            for i in range(w):
                self.put(x + i, y + j, c)

    def sprite(self, x, y, rows, c):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == "#":
                    self.put(x + i, y + j, c)

    # --- 文字（細かい点単位で描く。位置は絵のマスで指定） ---
    def text(self, x, y, s, c, font=FONT, px=FONT_PX, shadow="black"):
        rows = glyph_rows(s, font, px)
        fx, fy = x * ART, y * ART
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == "#":
                    if shadow:
                        self._fine(fx + i + 1, fy + j + 1, shadow)
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == "#":
                    self._fine(fx + i, fy + j, c)

    def text_center(self, cx, y, s, c, **kw):
        """cx を中心に置く（cx は絵のマス）"""
        width = len(glyph_rows(s, kw.get("font", FONT), kw.get("px", FONT_PX))[0])
        self.text(cx - width / ART / 2, y, s, c, **kw)

    def _fine(self, fx, fy, c):
        fx, fy = int(fx), int(fy)
        if 0 <= fx < self.fw and 0 <= fy < self.fh:
            self.px[fy][fx] = PALETTE[c]

    def save(self, path):
        raw = bytearray()
        for y in range(self.fh * DOT):
            raw.append(0)
            row = self.px[y // DOT]
            for x in range(self.fw * DOT):
                raw.extend(row[x // DOT])
        png = (b"\x89PNG\r\n\x1a\n"
               + _chunk(b"IHDR", struct.pack(">IIBBBBB", self.fw * DOT, self.fh * DOT, 8, 2, 0, 0, 0))
               + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
               + _chunk(b"IEND", b""))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(png)
        print("生成: %s（%dx%d, %d bytes）" % (path, self.fw * DOT, self.fh * DOT, len(png)))


_cache = {}


def glyph_rows(s, font=FONT, px=FONT_PX):
    """文字列を '#' と '.' の行に変換する。上下の空行は落とす。"""
    key = (s, font, px)
    if key not in _cache:
        out = subprocess.run(["swift", os.path.join(HERE, "glyph.swift"), font, str(px), s],
                             check=True, capture_output=True, text=True).stdout.splitlines()
        while out and "#" not in out[0]:
            out.pop(0)
        while out and "#" not in out[-1]:
            out.pop()
        _cache[key] = out
    return _cache[key]


def _chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
