#!/usr/bin/env python3
"""Wednesday 25 November 2026 -- the world's news in one image.

Pure standard library (Python 3.13): no third-party packages, no fonts, no
network. The program draws everything itself -- an anti-aliased vector
rasteriser, a built-in monoline stroke font, hand-built pictograms -- and
encodes the PNG with zlib. Output is fully deterministic (no randomness, no
timestamps, no metadata), so two runs write byte-identical files.

Usage:  python main.py            -> writes /output/entry.png
        python main.py some.png   -> writes some.png (handy for local tests)

The story texts below were researched on 25 Nov 2026 from the sources listed
in README.md.
"""

import math
import os
import struct
import sys
import zlib

W = 1024
H = 1024
DEFAULT_OUT = "/output/entry.png"

# --------------------------------------------------------------------------
# palette
# --------------------------------------------------------------------------
BG = (8, 14, 28)
CARD = (20, 33, 58)
ICONBG = (11, 19, 37)
WHITE = (246, 248, 251)
MUTED = (188, 200, 220)
AMBER = (255, 193, 59)
RED = (255, 84, 84)
STONE = (226, 231, 241)
STONE_DK = (160, 172, 196)
STEEL = (190, 200, 216)


# --------------------------------------------------------------------------
# tiny anti-aliased rasteriser
# --------------------------------------------------------------------------
def _put(row, i, col, a):
    if a >= 0.999:
        row[i] = col[0]
        row[i + 1] = col[1]
        row[i + 2] = col[2]
    else:
        ia = 1.0 - a
        row[i] = int(row[i] * ia + col[0] * a + 0.5)
        row[i + 1] = int(row[i + 1] * ia + col[1] * a + 0.5)
        row[i + 2] = int(row[i + 2] * ia + col[2] * a + 0.5)


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.rows = [bytearray(bytes(bg) * w) for _ in range(h)]

    # axis-aligned integer rectangle (fast, no anti-aliasing)
    def rect(self, x0, y0, x1, y1, col):
        x0 = max(0, int(round(x0)))
        y0 = max(0, int(round(y0)))
        x1 = min(self.w, int(round(x1)))
        y1 = min(self.h, int(round(y1)))
        if x1 <= x0 or y1 <= y0:
            return
        seg = bytes(col) * (x1 - x0)
        for y in range(y0, y1):
            self.rows[y][x0 * 3:x1 * 3] = seg

    def circle(self, cx, cy, r, col, alpha=1.0):
        x0 = max(0, int(math.floor(cx - r - 1)))
        x1 = min(self.w, int(math.ceil(cx + r + 1)))
        y0 = max(0, int(math.floor(cy - r - 1)))
        y1 = min(self.h, int(math.ceil(cy + r + 1)))
        sqrt = math.sqrt
        for y in range(y0, y1):
            row = self.rows[y]
            dy = y + 0.5 - cy
            for x in range(x0, x1):
                dx = x + 0.5 - cx
                a = r + 0.5 - sqrt(dx * dx + dy * dy)
                if a <= 0:
                    continue
                if a > 1:
                    a = 1
                _put(row, x * 3, col, a * alpha)

    def ring(self, cx, cy, r, w, col, alpha=1.0):
        hw = w / 2.0
        ext = r + hw + 1
        x0 = max(0, int(math.floor(cx - ext)))
        x1 = min(self.w, int(math.ceil(cx + ext)))
        y0 = max(0, int(math.floor(cy - ext)))
        y1 = min(self.h, int(math.ceil(cy + ext)))
        sqrt = math.sqrt
        for y in range(y0, y1):
            row = self.rows[y]
            dy = y + 0.5 - cy
            for x in range(x0, x1):
                dx = x + 0.5 - cx
                a = hw + 0.5 - abs(sqrt(dx * dx + dy * dy) - r)
                if a <= 0:
                    continue
                if a > 1:
                    a = 1
                _put(row, x * 3, col, a * alpha)

    def line(self, x0, y0, x1, y1, w, col, alpha=1.0):
        r = w / 2.0
        bx0 = max(0, int(math.floor(min(x0, x1) - r - 1)))
        bx1 = min(self.w, int(math.ceil(max(x0, x1) + r + 1)))
        by0 = max(0, int(math.floor(min(y0, y1) - r - 1)))
        by1 = min(self.h, int(math.ceil(max(y0, y1) + r + 1)))
        dx = x1 - x0
        dy = y1 - y0
        l2 = dx * dx + dy * dy
        sqrt = math.sqrt
        for y in range(by0, by1):
            row = self.rows[y]
            py = y + 0.5
            for x in range(bx0, bx1):
                px = x + 0.5
                if l2 == 0:
                    t = 0.0
                else:
                    t = ((px - x0) * dx + (py - y0) * dy) / l2
                if t < 0.0:
                    t = 0.0
                elif t > 1.0:
                    t = 1.0
                ex = px - (x0 + t * dx)
                ey = py - (y0 + t * dy)
                a = r + 0.5 - sqrt(ex * ex + ey * ey)
                if a <= 0:
                    continue
                if a > 1:
                    a = 1
                _put(row, x * 3, col, a * alpha)

    def rrect(self, x0, y0, x1, y1, rad, col, alpha=1.0):
        cx = (x0 + x1) / 2.0
        cy = (y0 + y1) / 2.0
        hx = (x1 - x0) / 2.0
        hy = (y1 - y0) / 2.0
        ix = hx - rad
        iy = hy - rad
        bx0 = max(0, int(math.floor(x0 - 1)))
        bx1 = min(self.w, int(math.ceil(x1 + 1)))
        by0 = max(0, int(math.floor(y0 - 1)))
        by1 = min(self.h, int(math.ceil(y1 + 1)))
        sqrt = math.sqrt
        for y in range(by0, by1):
            row = self.rows[y]
            qy = abs(y + 0.5 - cy) - iy
            for x in range(bx0, bx1):
                qx = abs(x + 0.5 - cx) - ix
                ox = qx if qx > 0 else 0.0
                oy = qy if qy > 0 else 0.0
                inner = qx if qx > qy else qy
                if inner > 0:
                    inner = 0.0
                d = sqrt(ox * ox + oy * oy) + inner - rad
                a = 0.5 - d
                if a <= 0:
                    continue
                if a > 1:
                    a = 1
                _put(row, x * 3, col, a * alpha)

    def poly(self, pts, col, alpha=1.0, ss=4):
        """Even-odd polygon fill with vertical super-sampling and exact
        horizontal coverage."""
        n = len(pts)
        xs_all = [p[0] for p in pts]
        ys_all = [p[1] for p in pts]
        bx0 = max(0, int(math.floor(min(xs_all))))
        bx1 = min(self.w - 1, int(math.ceil(max(xs_all))))
        by0 = max(0, int(math.floor(min(ys_all))))
        by1 = min(self.h, int(math.ceil(max(ys_all))))
        width = bx1 - bx0 + 2
        edges = []
        for i in range(n):
            ax, ay = pts[i]
            bx, by = pts[(i + 1) % n]
            if ay != by:
                edges.append((ax, ay, bx, by))
        inv = 1.0 / ss
        for y in range(by0, by1):
            cov = [0.0] * width
            for s in range(ss):
                sy = y + (s + 0.5) * inv
                xs = []
                for ax, ay, bx, by in edges:
                    if (ay <= sy < by) or (by <= sy < ay):
                        xs.append(ax + (sy - ay) * (bx - ax) / (by - ay))
                xs.sort()
                for k in range(0, len(xs) - 1, 2):
                    xa = xs[k]
                    xb = xs[k + 1]
                    ia = int(math.floor(xa))
                    ib = int(math.floor(xb))
                    if ia == ib:
                        j = ia - bx0
                        if 0 <= j < width:
                            cov[j] += (xb - xa) * inv
                    else:
                        j = ia - bx0
                        if 0 <= j < width:
                            cov[j] += (ia + 1 - xa) * inv
                        for m in range(ia + 1, ib):
                            j = m - bx0
                            if 0 <= j < width:
                                cov[j] += inv
                        j = ib - bx0
                        if 0 <= j < width:
                            cov[j] += (xb - ib) * inv
            row = self.rows[y]
            for j in range(width):
                a = cov[j]
                if a <= 0.001:
                    continue
                x = bx0 + j
                if x >= self.w:
                    break
                if a > 1:
                    a = 1
                _put(row, x * 3, col, a * alpha)


# --------------------------------------------------------------------------
# monoline stroke font (A-Z 0-9 and a little punctuation), 6 units tall
# --------------------------------------------------------------------------
GLYPHS = {}


def _g(ch, width, *strokes):
    GLYPHS[ch] = (width, strokes)


_g('A', 4, [(0, 6), (2, 0), (4, 6)], [(0.85, 4), (3.15, 4)])
_g('B', 4, [(0, 6), (0, 0), (2.8, 0), (4, 1), (4, 2.1), (2.8, 3), (0, 3)],
    [(2.8, 3), (4, 3.9), (4, 5), (2.8, 6), (0, 6)])
_g('C', 4, [(4, 1.2), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 4.8)])
_g('D', 4, [(0, 0), (0, 6), (2, 6), (4, 4), (4, 2), (2, 0), (0, 0)])
_g('E', 4, [(4, 0), (0, 0), (0, 6), (4, 6)], [(0, 3), (3.2, 3)])
_g('F', 4, [(4, 0), (0, 0), (0, 6)], [(0, 3), (3.2, 3)])
_g('G', 4, [(4, 1.2), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5),
    (4, 3.2), (2.3, 3.2)])
_g('H', 4, [(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)])
_g('I', 3, [(0.5, 0), (2.5, 0)], [(1.5, 0), (1.5, 6)], [(0.5, 6), (2.5, 6)])
_g('J', 4, [(4, 0), (4, 5), (3, 6), (1, 6), (0, 5)])
_g('K', 4, [(0, 0), (0, 6)], [(4, 0), (0, 3.6)], [(1.1, 2.6), (4, 6)])
_g('L', 4, [(0, 0), (0, 6), (4, 6)])
_g('M', 4.4, [(0, 6), (0, 0), (2.2, 3.6), (4.4, 0), (4.4, 6)])
_g('N', 4, [(0, 6), (0, 0), (4, 6), (4, 0)])
_O = [(1, 0), (3, 0), (4, 1), (4, 5), (3, 6), (1, 6), (0, 5), (0, 1), (1, 0)]
_g('O', 4, _O)
_P = [(0, 6), (0, 0), (2.8, 0), (4, 1), (4, 2.2), (2.8, 3.2), (0, 3.2)]
_g('P', 4, _P)
_g('Q', 4, _O, [(2.6, 4.4), (4.2, 6.3)])
_g('R', 4, _P, [(2.2, 3.2), (4, 6)])
_g('S', 4, [(4, 1.2), (3, 0), (1, 0), (0, 1), (0, 2.2), (1, 3), (3, 3), (4, 3.8),
    (4, 5), (3, 6), (1, 6), (0, 4.8)])
_g('T', 4, [(0, 0), (4, 0)], [(2, 0), (2, 6)])
_g('U', 4, [(0, 0), (0, 5), (1, 6), (3, 6), (4, 5), (4, 0)])
_g('V', 4, [(0, 0), (2, 6), (4, 0)])
_g('W', 4.8, [(0, 0), (1.2, 6), (2.4, 2.4), (3.6, 6), (4.8, 0)])
_g('X', 4, [(0, 0), (4, 6)], [(4, 0), (0, 6)])
_g('Y', 4, [(0, 0), (2, 3), (4, 0)], [(2, 3), (2, 6)])
_g('Z', 4, [(0, 0), (4, 0), (0, 6), (4, 6)])
_g('0', 4, _O)
_g('1', 4, [(0.6, 1.4), (2, 0), (2, 6)], [(0.6, 6), (3.4, 6)])
_g('2', 4, [(0, 1.2), (1, 0), (3, 0), (4, 1), (4, 2.2), (0, 6), (4, 6)])
_g('3', 4, [(0, 1), (1, 0), (3, 0), (4, 1), (4, 2.1), (3, 3), (1.6, 3)],
    [(3, 3), (4, 3.9), (4, 5), (3, 6), (1, 6), (0, 5)])
_g('4', 4, [(3, 6), (3, 0), (0, 4.2), (4, 4.2)])
_g('5', 4, [(4, 0), (0, 0), (0, 3), (3, 3), (4, 3.9), (4, 5), (3, 6), (1, 6), (0, 5)])
_g('6', 4, [(4, 1), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5),
    (4, 4), (3, 3), (0, 3)])
_g('7', 4, [(0, 0), (4, 0), (1.4, 6)])
_g('8', 4, [(1, 0), (3, 0), (4, 1), (4, 2), (3, 3), (1, 3), (0, 2), (0, 1), (1, 0)],
    [(1, 3), (0, 4), (0, 5), (1, 6), (3, 6), (4, 5), (4, 4), (3, 3)])
_g('9', 4, [(0, 5), (1, 6), (3, 6), (4, 5), (4, 1), (3, 0), (1, 0), (0, 1),
    (0, 2), (1, 3), (4, 3)])
_g('.', 1, [(0.5, 5.8)])
_g(',', 1.4, [(0.8, 5.6), (0.3, 7.2)])
_g('-', 3, [(0.4, 3.2), (2.6, 3.2)])
_g(':', 1, [(0.5, 1.9)], [(0.5, 5.1)])
_g(';', 1.4, [(0.8, 1.9)], [(0.8, 5.0), (0.3, 6.6)])
_g('%', 4.6, [(0, 6), (4.6, 0)],
    [(0.2, 0.2), (1.5, 0.2), (1.5, 1.7), (0.2, 1.7), (0.2, 0.2)],
    [(3.1, 4.3), (4.4, 4.3), (4.4, 5.8), (3.1, 5.8), (3.1, 4.3)])
_g('$', 4, [(4, 1.2), (3, 0.3), (1, 0.3), (0, 1.3), (0, 2.3), (1, 3), (3, 3),
    (4, 3.7), (4, 4.7), (3, 5.7), (1, 5.7), (0, 4.8)], [(2, -0.7), (2, 6.7)])
_g('~', 4, [(0, 3.4), (1, 2.4), (3, 3.6), (4, 2.6)])
_g("'", 1, [(0.5, 0), (0.5, 1.5)])
_g('+', 4, [(0.4, 3), (3.6, 3)], [(2, 1.4), (2, 4.6)])
_g('|', 1, [(0.5, -0.6), (0.5, 6.6)])
_g('/', 3.6, [(0, 6), (3.6, 0)])
_g('(', 2, [(1.8, 0), (0.6, 1.5), (0.6, 4.5), (1.8, 6)])
_g(')', 2, [(0.2, 0), (1.4, 1.5), (1.4, 4.5), (0.2, 6)])
_g('?', 4, [(0, 1.2), (1, 0), (3, 0), (4, 1), (4, 2.2), (2, 3.6), (2, 4.4)], [(2, 5.8)])
_g('!', 1, [(0.5, 0), (0.5, 4)], [(0.5, 5.8)])

SX = 0.86  # horizontal squeeze of glyph units
GAP = 1.25  # inter-letter gap, in units
SPACE = 2.3  # word space, in units


def _adv(ch):
    if ch == ' ':
        return SPACE
    return GLYPHS[ch][0] * SX + GAP


def text_width(s, cap):
    u = cap / 6.0
    return sum(_adv(ch) for ch in s.upper()) * u - GAP * u


def text(cv, x, y, s, cap, col, bold=0.14, alpha=1.0):
    """Draw s with its cap-line at y (top of capitals), starting at x."""
    u = cap / 6.0
    sw = max(1.9, cap * bold)
    xx = x
    for ch in s.upper():
        if ch == ' ':
            xx += SPACE * u
            continue
        width, strokes = GLYPHS[ch]
        for st in strokes:
            pts = [(xx + px * SX * u, y + py * u) for px, py in st]
            if len(pts) == 1:
                cv.circle(pts[0][0], pts[0][1], sw / 2.0, col, alpha)
            else:
                for a, b in zip(pts, pts[1:]):
                    cv.line(a[0], a[1], b[0], b[1], sw, col, alpha)
        xx += (width * SX + GAP) * u
    return xx - x - GAP * u


def wrap(s, maxw, cap):
    words = s.split(' ')
    lines = []
    cur = ''
    for w in words:
        trial = w if not cur else cur + ' ' + w
        if text_width(trial, cap) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# --------------------------------------------------------------------------
# pictograms (each is drawn inside roughly an 80 x 80 box around cx, cy)
# --------------------------------------------------------------------------
def icon_ukraine_talks(cv, cx, cy):
    # two flags on poles facing each other, a question mark between/below
    cv.line(cx - 31, cy - 38, cx - 31, cy + 6, 4, STEEL)
    cv.line(cx + 31, cy - 38, cx + 31, cy + 6, 4, STEEL)
    # Ukraine: blue over yellow
    cv.rect(cx - 29, cy - 36, cx - 3, cy - 23, (0, 87, 183))
    cv.rect(cx - 29, cy - 23, cx - 3, cy - 10, (255, 213, 0))
    # Russia: white / blue / red
    cv.rect(cx + 3, cy - 36, cx + 29, cy - 27.7, (245, 245, 245))
    cv.rect(cx + 3, cy - 27.7, cx + 29, cy - 19.3, (0, 57, 166))
    cv.rect(cx + 3, cy - 19.3, cx + 29, cy - 11, (213, 43, 30))
    # table + question mark
    cv.rrect(cx - 36, cy + 28, cx + 36, cy + 35, 3, STEEL)
    text(cv, cx - text_width('?', 30) / 2.0, cy - 2, '?', 30, AMBER, bold=0.16)


def icon_climate(cv, cx, cy):
    cv.circle(cx, cy, 34, (30, 111, 217))
    cv.poly([(cx - 20, cy - 8), (cx - 18, cy - 20), (cx - 4, cy - 26), (cx + 2, cy - 14),
             (cx - 8, cy - 4)], (58, 176, 98))
    cv.poly([(cx + 6, cy + 2), (cx + 22, cy - 6), (cx + 28, cy + 8), (cx + 14, cy + 24),
             (cx + 4, cy + 14)], (58, 176, 98))
    cv.poly([(cx - 26, cy + 10), (cx - 12, cy + 8), (cx - 8, cy + 20), (cx - 20, cy + 26)],
            (58, 176, 98))
    zig = [(cx - 12, cy - 34), (cx + 2, cy - 14), (cx - 8, cy), (cx + 8, cy + 16), (cx, cy + 34)]
    for a, b in zip(zig, zig[1:]):
        cv.line(a[0], a[1], b[0], b[1], 5, RED)
    # failure badge
    cv.circle(cx + 28, cy + 28, 14, RED)
    cv.circle(cx + 28, cy + 28, 14, WHITE, 0.0)
    cv.line(cx + 22, cy + 22, cx + 34, cy + 34, 4, WHITE)
    cv.line(cx + 34, cy + 22, cx + 22, cy + 34, 4, WHITE)


def icon_tariffs(cv, cx, cy):
    cdk = (176, 98, 30)
    cv.rrect(cx - 36, cy - 2, cx + 36, cy + 36, 5, (236, 142, 52))
    for xo in (-14, 14):
        cv.line(cx + xo, cy - 1, cx + xo, cy + 35, 3, cdk)
    cv.line(cx - 35, cy + 16, cx + 35, cy + 16, 3, cdk)
    cv.rrect(cx - 24, cy - 32, cx + 10, cy - 2, 5, (250, 170, 80))
    cv.line(cx - 7, cy - 31, cx - 7, cy - 3, 3, cdk)
    cv.line(cx - 23, cy - 16, cx + 9, cy - 16, 3, cdk)
    cv.circle(cx + 24, cy - 22, 17, RED)
    text(cv, cx + 24 - text_width('%', 17) / 2.0, cy - 22 - 8.5, '%', 17, WHITE, bold=0.16)


def icon_congress(cv, cx, cy):
    # Capitol dome with a "shutdown" alert badge
    dome = []
    for k in range(0, 19):
        a = math.pi + math.pi * k / 18.0
        dome.append((cx + 21 * math.cos(a), cy - 6 + 21 * math.sin(a)))
    cv.poly(dome, STONE)
    cv.rect(cx - 17, cy - 6, cx + 17, cy + 3, STONE_DK)
    cv.line(cx, cy - 27, cx, cy - 40, 3, STONE)
    cv.poly([(cx, cy - 40), (cx + 10, cy - 36), (cx, cy - 33)], RED)
    cv.rect(cx - 38, cy + 3, cx + 38, cy + 10, STONE)
    for k in range(7):
        xx = cx - 33 + k * 11
        cv.line(xx, cy + 10, xx, cy + 30, 5, STONE)
    cv.rect(cx - 40, cy + 30, cx + 40, cy + 37, STONE_DK)
    cv.circle(cx + 31, cy - 24, 14, RED)
    text(cv, cx + 31 - text_width('!', 18) / 2.0, cy - 24 - 9, '!', 18, WHITE, bold=0.2)


def icon_chip(cv, cx, cy):
    pin = STEEL
    for k in range(-2, 3):
        o = k * 9
        cv.line(cx + o, cy - 36, cx + o, cy - 22, 4, pin)
        cv.line(cx + o, cy + 22, cx + o, cy + 36, 4, pin)
        cv.line(cx - 36, cy + o, cx - 22, cy + o, 4, pin)
        cv.line(cx + 22, cy + o, cx + 36, cy + o, 4, pin)
    cv.rrect(cx - 26, cy - 26, cx + 26, cy + 26, 6, (52, 64, 88))
    cv.rrect(cx - 18, cy - 18, cx + 18, cy + 18, 4, (118, 200, 60))
    cv.poly([(cx, cy - 12), (cx + 11, cy + 1), (cx + 4.5, cy + 1), (cx + 4.5, cy + 12),
             (cx - 4.5, cy + 12), (cx - 4.5, cy + 1), (cx - 11, cy + 1)], (14, 24, 40))


def icon_gaza(cv, cx, cy):
    # white flag of truce, cracked
    cv.line(cx - 26, cy - 38, cx - 26, cy + 38, 4, STEEL)
    cv.poly([(cx - 24, cy - 36), (cx - 8, cy - 31), (cx + 10, cy - 36), (cx + 30, cy - 30),
             (cx + 30, cy + 2), (cx + 10, cy + 8), (cx - 8, cy + 3), (cx - 24, cy + 8)], WHITE)
    zig = [(cx + 4, cy - 38), (cx + 14, cy - 22), (cx + 3, cy - 13), (cx + 14, cy - 1),
           (cx + 6, cy + 10)]
    for a, b in zip(zig, zig[1:]):
        cv.line(a[0], a[1], b[0], b[1], 4, RED)
    cv.rrect(cx - 36, cy + 30, cx + 36, cy + 37, 3, STONE_DK)


def icon_virus(cv, cx, cy):
    body = (236, 64, 110)
    tip = (255, 150, 172)
    for k in range(12):
        a = 2 * math.pi * k / 12.0
        x1 = cx + 17 * math.cos(a)
        y1 = cy + 17 * math.sin(a)
        x2 = cx + 29 * math.cos(a)
        y2 = cy + 29 * math.sin(a)
        cv.line(x1, y1, x2, y2, 4, body)
        cv.circle(cx + 32 * math.cos(a), cy + 32 * math.sin(a), 5, tip)
    cv.circle(cx, cy, 21, body)
    cv.ring(cx, cy, 12, 3, tip)
    cv.circle(cx - 5, cy - 4, 3, tip)
    cv.circle(cx + 6, cy + 3, 3.5, tip)
    cv.circle(cx - 2, cy + 8, 2.5, tip)


def icon_drone(cv, cx, cy):
    gold = (232, 172, 60)
    for sx in (-1, 1):
        for sy in (-1, 1):
            rx = cx + sx * 27
            ry = cy + sy * 25
            cv.line(cx + sx * 7, cy + sy * 6, rx, ry, 5, (95, 108, 130))
            cv.circle(rx, ry, 12, gold, 0.30)
            cv.ring(rx, ry, 12, 3, gold)
            cv.line(rx - 8, ry, rx + 8, ry, 2.5, gold)
    cv.rrect(cx - 12, cy - 10, cx + 12, cy + 10, 5, (70, 82, 106))
    cv.circle(cx, cy, 5, RED)


def icon_globe(cv, cx, cy, r, col, w):
    cv.ring(cx, cy, r, w, col)
    for fx in (0.38, 0.74):
        pts = []
        for k in range(0, 49):
            t = 2 * math.pi * k / 48.0
            pts.append((cx + r * fx * math.cos(t), cy + r * math.sin(t)))
        for a, b in zip(pts, pts[1:]):
            cv.line(a[0], a[1], b[0], b[1], w * 0.6, col)
    cv.line(cx, cy - r, cx, cy + r, w * 0.6, col)
    for fy in (-0.5, 0.0, 0.5):
        yy = cy + fy * r
        half = math.sqrt(max(r * r - (fy * r) ** 2, 0.0))
        cv.line(cx - half, yy, cx + half, yy, w * 0.6, col)


# --------------------------------------------------------------------------
# page content (researched 25 Nov 2026 -- see README.md for sources)
# --------------------------------------------------------------------------
STORIES = [
    ("UKRAINE WAR | EUROPE", (84, 160, 255), icon_ukraine_talks,
     "PEACE TALKS STALL, WAR GRINDS ON",
     "US-brokered Abu Dhabi round ended with no major breakthrough."),
    ("CLIMATE | COP31 ANTALYA", (66, 214, 146), icon_climate,
     "COP31 CLIMATE TALKS END WITH NO DEAL",
     "Longest UN climate summit ever ended 22 Nov; EU rejected a text silent on fossil fuels."),
    ("TRADE | UNITED STATES", (255, 160, 70), icon_tariffs,
     "US PLANS TARIFFS ON 16 PARTNERS",
     "China and EU among targets, after the Supreme Court struck down earlier duties (AP)."),
    ("US CONGRESS | IRAN WAR", (255, 107, 107), icon_congress,
     "SHUTDOWN LOOMS OVER IRAN WAR FUNDS",
     "Deadline 11 Dec. Democrats want funds cut off; Republicans weigh a deal."),
    ("TECH | MARKETS", (166, 132, 255), icon_chip,
     "NVIDIA REINSTATES CEO JENSEN HUANG",
     "Board acted after Trump pressure; shares soared about 30% on the news."),
    ("MIDDLE EAST | GAZA", (52, 214, 224), icon_gaza,
     "GAZA CEASEFIRE ON THE BRINK",
     "Board of Peace warns truce may collapse; 74,000+ Palestinians killed since 2023."),
    ("HEALTH | DR CONGO", (255, 92, 150), icon_virus,
     "EBOLA STILL NOT UNDER CONTROL",
     "11,000+ cases and 5,500+ deaths since May, Africa CDC says."),
    ("CONFLICT | SUDAN", (232, 176, 70), icon_drone,
     "DRONE WAR RAGES IN KORDOFAN",
     "2,230+ civilians killed Jan-Oct 2026, 1,630+ of them by drones."),
]

FOOT_1 = "MARKETS 24 NOV:  NASDAQ DOWN ~1.4%   |   BRENT OIL ~$89   |   GOLD ~$3,600"
FOOT_2 = "ALSO: SEOUL SUBWAY STRIKE AVERTED BY WAGE DEAL   |   25 NOV: UN DAY TO END VIOLENCE AGAINST WOMEN"


def fit_cap(s, maxw, cap):
    while cap > 8 and text_width(s, cap) > maxw:
        cap -= 0.5
    return cap


def draw_card(cv, x, y, w, h, story):
    tag, accent, icon, head, detail = story
    cv.rrect(x, y, x + w, y + h, 12, accent)
    cv.rrect(x + 6, y, x + w, y + h, 12, CARD)
    cv.rect(x + 6, y + 4, x + 20, y + h - 4, CARD)

    isz = 100
    ix = x + 20
    iy = y + (h - isz) / 2.0
    cv.rrect(ix, iy, ix + isz, iy + isz, 16, ICONBG)
    icon(cv, ix + isz / 2.0, iy + isz / 2.0)

    tx = ix + isz + 18
    maxw = x + w - tx - 14
    cap_tag, cap_head, cap_det = 12.5, 23.0, 14.5
    head_lines = wrap(head, maxw, cap_head)
    det_lines = wrap(detail, maxw, cap_det)
    pitch_head, pitch_det = 31, 22
    total = (cap_tag + 15
            + (len(head_lines) - 1) * pitch_head + cap_head + 13
            + (len(det_lines) - 1) * pitch_det + cap_det)
    yy = y + (h - total) / 2.0
    text(cv, tx, yy, tag, cap_tag, accent, bold=0.15)
    yy += cap_tag + 15
    for ln in head_lines:
        text(cv, tx, yy, ln, cap_head, WHITE, bold=0.15)
        yy += pitch_head
    yy += 13 - (pitch_head - cap_head)
    for ln in det_lines:
        text(cv, tx, yy, ln, cap_det, MUTED, bold=0.13)
        yy += pitch_det


def build():
    cv = Canvas(W, H, BG)

    # header ---------------------------------------------------------------
    cv.rect(0, 0, W, 8, AMBER)
    text(cv, 28, 26, "WORLD NEWS IN ONE IMAGE   |   THE DAY IN 8 STORIES", 14, AMBER, bold=0.15)
    text(cv, 28, 54, "WEDNESDAY", 26, MUTED, bold=0.15)
    text(cv, 28, 90, "25 NOVEMBER 2026", 58, WHITE, bold=0.14)
    icon_globe(cv, 934, 88, 52, AMBER, 5)
    cv.rect(24, 158, W - 24, 161, AMBER)

    # cards ----------------------------------------------------------------
    cw, ch, gap = 488, 188, 16
    x0, y0, vgap = 24, 170, 10
    for i, story in enumerate(STORIES):
        col = i % 2
        rw = i // 2
        draw_card(cv, x0 + col * (cw + gap), y0 + rw * (ch + vgap), cw, ch, story)

    # footer ---------------------------------------------------------------
    cv.rrect(24, 960, W - 24, 1008, 10, CARD)
    c1 = fit_cap(FOOT_1, W - 24 * 2 - 28, 13.5)
    c2 = fit_cap(FOOT_2, W - 24 * 2 - 28, 13.5)
    text(cv, 38, 969, FOOT_1, c1, AMBER, bold=0.14)
    text(cv, 38, 989, FOOT_2, c2, MUTED, bold=0.13)
    return cv


# --------------------------------------------------------------------------
# deterministic PNG encoder
# --------------------------------------------------------------------------
def _chunk(tag, data):
    body = tag + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def encode_png(rows, w, h):
    raw = bytearray()
    prev = bytes(w * 3)
    for r in rows:
        raw.append(2)  # filter "Up": flat areas become runs of zeros
        raw.extend(bytes((a - b) & 255 for a, b in zip(r, prev)))
        prev = bytes(r)
    comp = zlib.compress(bytes(raw), 9)
    return (b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + _chunk(b"IDAT", comp)
            + _chunk(b"IEND", b""))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT
    cv = build()
    data = encode_png(cv.rows, W, H)
    assert len(data) <= 1024 * 1024, "image exceeds 1 MiB"
    folder = os.path.dirname(out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(out, "wb") as fh:
        fh.write(data)


if __name__ == "__main__":
    main()
