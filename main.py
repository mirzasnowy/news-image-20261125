#!/usr/bin/env python3
"""Sum up Wednesday 25 November 2026 in one image.

A single-file, standard-library-only program. It draws a 1024x1024
newspaper front page (masthead, date, eight story cards, a markets ticker
and a source footer) with a hand-built 5x7 bitmap font and a hand-written
PNG encoder, then writes it to /output/entry.png (or to the path given as
the first argument). No network, no third-party packages, and the output
is deterministic: the same input always produces byte-identical output.

Run:
    python3 main.py                 # writes /output/entry.png
    python3 main.py out.png         # writes out.png (for local testing)
"""

import struct
import sys
import zlib

# ---------------------------------------------------------------------------
# 5x7 bitmap font.
#
# Each glyph is 7 rows of 5 characters. '#' is an ink pixel, '.' is blank.
# The font covers A-Z, a-z, 0-9 and the punctuation the page needs.
# ---------------------------------------------------------------------------
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".###.", "#...#", "#....", "#..##", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "a": (".....", ".....", ".###.", "....#", ".####", "#...#", ".###."),
    "b": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
    "c": (".....", ".....", ".###.", "#....", "#....", "#....", ".###."),
    "d": ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".###."),
    "e": (".....", ".....", ".###.", "#...#", "#####", "#....", ".###."),
    "f": ("..##.", ".#..#", ".#...", "####.", ".#...", ".#...", ".#..."),
    "g": (".....", ".....", ".###.", "#...#", "#...#", ".###.", "###.."),
    "h": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "i": (".....", "..#..", ".....", ".##..", "..#..", "..#..", ".###."),
    "j": ("...#.", ".....", "..##.", "...#.", "...#.", "...#.", ".##.."),
    "k": ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#...#"),
    "l": (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "m": (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
    "n": (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "o": (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
    "p": (".....", ".....", "####.", "#...#", "#...#", "####.", "#...."),
    "q": (".....", ".....", ".####", "#...#", "#...#", ".####", "....#"),
    "r": (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
    "s": (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
    "t": (".#...", ".#...", "####.", ".#...", ".#...", ".#...", "..##."),
    "u": (".....", ".....", "#...#", "#...#", "#...#", "#...#", ".###."),
    "v": (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "w": (".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    "x": (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
    "y": (".....", ".....", "#...#", "#...#", "#...#", ".###.", ".##.."),
    "z": (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
}

FONT.update({
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.#..", "#..##"),
    "~": (".....", ".....", "..##.", ".#..#", ".....", ".....", "....."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "|": ("..#..", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "•": (".....", ".....", ".###.", ".###.", ".###.", ".....", "....."),
})

# Glyph drawn for any character the font does not cover (a hollow box),
# so a missing glyph is visible instead of silently vanishing.
FALLBACK = ("#####", "#...#", "#...#", "#...#", "#...#", "#...#", "#####")


# ---------------------------------------------------------------------------
# Canvas: an RGB image held as a flat bytearray, with rectangle and text
# drawing. All coordinates are in pixels; drawing is clipped to the canvas.
# ---------------------------------------------------------------------------
class Canvas:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.pixels = bytearray(bytes(color) * (width * height))

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width, x + w)
        y1 = min(self.height, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            start = (yy * self.width + x0) * 3
            self.pixels[start:start + len(row)] = row

    def draw_text(self, x, y, text, scale, color):
        """Draw text left-aligned at (x, y). Returns the x of the end."""
        cx = x
        for ch in text:
            glyph = FONT.get(ch, FALLBACK)
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "#":
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, color)
            cx += 6 * scale
        return cx

    def draw_text_centered(self, y, text, scale, color):
        """Draw text centred horizontally on the given y. Returns its x."""
        w = text_width(text, scale)
        x = (self.width - w) // 2
        self.draw_text(x, y, text, scale, color)
        return x


def text_width(text, scale):
    """Pixel width of text at the given scale (no trailing gap)."""
    if not text:
        return 0
    return len(text) * 6 * scale - scale


def wrap_text(text, scale, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if text_width(trial, scale) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ---------------------------------------------------------------------------
# PNG writer (standard library only). Filter: none. Compression: zlib level
# 9, which is deterministic, so identical pixels give identical bytes.
# ---------------------------------------------------------------------------
def _png_chunk(chunk_type, data):
    out = struct.pack(">I", len(data)) + chunk_type + data
    out += struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    return out


def write_png(canvas, path):
    raw = bytearray()
    stride = canvas.width * 3
    for y in range(canvas.height):
        raw.append(0)  # filter type 0: no filtering
        start = y * stride
        raw += canvas.pixels[start:start + stride]
    ihdr = struct.pack(">IIBBBBB", canvas.width, canvas.height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _png_chunk(b"IHDR", ihdr)
    png += _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _png_chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)

import os

# ---------------------------------------------------------------------------
# Page design: a cream newspaper front page, 1024x1024.
# Masthead + date, then eight story cards in a 2x4 grid, then a dark
# markets ticker and a source footer.
# ---------------------------------------------------------------------------
PAPER = (250, 246, 238)
INK = (26, 26, 26)
RED = (178, 34, 34)
CARD = (255, 255, 255)
CARD_BORDER = (210, 205, 195)
BODY = (45, 45, 45)
MUTED = (110, 105, 95)
TICKER_BG = (26, 26, 26)
TICKER_FG = (250, 246, 238)

PAGE_W = 1024
PAGE_H = 1024

# (kicker, title, body) — the verified news of Wednesday 25 November 2026.
STORIES = [
    ("UKRAINE", "Abu Dhabi talks stall",
     "Negotiators end the round with no major breakthrough, and the war grinds on."),
    ("COP31", "Summit ends with no deal",
     "Antalya closes as the longest UN climate summit ever, without an agreement."),
    ("TARIFFS", "Tariffs hit 16 partners",
     "AP sources say new US duties are planned, including on China and the EU."),
    ("SHUTDOWN", "Funds fight splits Congress",
     "Lawmakers divide over Iran war funding as the 11 Dec deadline nears."),
    ("NVIDIA", "Huang returns, shares jump",
     "Jensen Huang is reinstated as CEO after Trump pressure; shares rise about 30%."),
    ("GAZA", "Ceasefire may collapse",
     "The Board of Peace warns the Gaza ceasefire could fall apart."),
    ("EBOLA", "Outbreak not under control",
     "Health officials say Ebola in DR Congo is still not under control."),
    ("SUDAN", "Drone war in Kordofan",
     "A drone war rages as the conflict spreads and civilians pay the price."),
]

TICKER_LINES = [
    "MARKETS (24 NOV): Nasdaq ~-1.4%  |  Brent ~$89  |  Gold ~$3,600",
    "Seoul subway strike averted  \u2022  25 NOV: UN Day to End Violence Against Women",
]

FOOTER = "Sources: AP, UN News, Al Jazeera. Figures marked ~ are single-source."


def draw_card(canvas, x, y, w, h, kicker, title, body):
    """One story card: white face, thin border, red kicker, title, body."""
    canvas.fill_rect(x, y, w, h, CARD_BORDER)
    canvas.fill_rect(x + 1, y + 1, w - 2, h - 2, CARD)
    inner = w - 32
    # Red square + kicker.
    canvas.fill_rect(x + 16, y + 16, 10, 10, RED)
    canvas.draw_text(x + 32, y + 14, kicker, 2, RED)
    # Title (scale 3, up to 2 lines).
    title_lines = wrap_text(title, 3, inner)[:2]
    ty = y + 38
    for line in title_lines:
        canvas.draw_text(x + 16, ty, line, 3, INK)
        ty += 24
    # Body (scale 2, up to 3 lines).
    body_lines = wrap_text(body, 2, inner)[:3]
    by = ty + 10
    for line in body_lines:
        canvas.draw_text(x + 16, by, line, 2, BODY)
        by += 17


def build_page():
    canvas = Canvas(PAGE_W, PAGE_H, PAPER)

    # Masthead.
    canvas.draw_text_centered(28, "THE WORLD IN ONE PAGE", 6, INK)
    canvas.draw_text_centered(80, "Wednesday, 25 November 2026", 2, INK)
    canvas.fill_rect(32, 104, PAGE_W - 64, 3, RED)
    canvas.draw_text_centered(116, "Eight stories that shaped the day", 2, MUTED)

    # Story grid: 2 columns x 4 rows.
    margin = 32
    col_gap = 24
    row_gap = 16
    card_w = (PAGE_W - 2 * margin - col_gap) // 2
    card_h = 168
    grid_top = 140
    for i, (kicker, title, body) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = margin + col * (card_w + col_gap)
        y = grid_top + row * (card_h + row_gap)
        draw_card(canvas, x, y, card_w, card_h, kicker, title, body)

    # Markets ticker: dark band, two centred lines.
    ticker_y = 876
    ticker_h = 80
    canvas.fill_rect(0, ticker_y, PAGE_W, ticker_h, TICKER_BG)
    canvas.draw_text_centered(ticker_y + 14, TICKER_LINES[0], 2, TICKER_FG)
    canvas.draw_text_centered(ticker_y + 40, TICKER_LINES[1], 2, TICKER_FG)

    # Source footer.
    canvas.draw_text_centered(970, FOOTER, 2, MUTED)

    return canvas


def main(argv):
    out = argv[1] if len(argv) > 1 else "/output/entry.png"
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    canvas = build_page()
    write_png(canvas, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
