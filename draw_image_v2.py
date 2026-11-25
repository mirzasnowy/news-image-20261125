#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261125 entry, v2 (polish pass).

Draws a dense, infographic-style one-page summary of Tuesday 25 November
2026 world news as a 1024x1024 PNG. Deterministic: same input, same bytes.

Layout (1024x1024, flow top to bottom):
  masthead -> 3-headline sub-deck -> big-number strip -> world map with
  numbered pins -> 12 illustrated top stories (2-col grid) -> UTC timeline
  -> region bar -> ALSO ON (28 one-liners, 2 cols) -> DATE CHECK + legend.

Stories verified against Reuters, AP, AFP, Al Jazeera, WSJ, CMSA/Xinhua
summaries of 25 Nov 2026 (see STORIES / ALSO below; each carries its
source and a confidence label). Stories dated 24 Nov or earlier are NOT
headlines here: they are listed in the DATE CHECK box instead.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MX = 30                      # side margin
CW = W - 2 * MX              # content width = 964
PAPER = (247, 243, 236)
INK = (17, 17, 17)
RED = (185, 28, 28)
GREY = (90, 86, 80)
LGREY = (200, 194, 184)
RULE = (17, 17, 17)
CARD_BG = (255, 255, 255)
DARK = (26, 26, 26)
GREEN = (28, 122, 48)
AMBER = (176, 118, 0)
OCEAN = (214, 228, 238)
LAND = (232, 222, 196)
LAND_LINE = (150, 140, 110)

CONF_COLOR = {"CONFIRMED": GREEN, "REPORTED": AMBER, "CLAIM": RED}

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, fnt, max_w):
    """Truncate text with an ellipsis so it fits max_w pixels."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    ell = "\u2026"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if draw.textlength(text[:mid] + ell, font=fnt) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo] + ell


def wrap_to(draw, text, fnt, max_w, max_lines):
    """Greedy word wrap, capped at max_lines (last line ellipsised)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = fit(draw, lines[-1], fnt, max_w)
    return lines


# ---------------------------------------------------------------- stories
# n, region, tag, headline, deck, confidence, source, icon, (lon, lat) pin
TOP = [
    (1, "ASIA", "SPACE",
     "Pakistan's first astronaut docks at China's Tiangong station",
     "Shenzhou-24 launched 00:18 UTC; Zeeshan Ali is the first foreigner aboard Tiangong.",
     "CONFIRMED", "Reuters", "rocket", (100, 41)),
    (2, "ASIA", "MARKETS",
     "Asia's chip rout: Kospi plunges 6.2% as AI doubts return",
     "Samsung -9.9%, SK Hynix -11.1%; Nikkei -2.8%, Taiex -5%. Nvidia falls 5.9%.",
     "CONFIRMED", "AP", "chart", (127, 37.5)),
    (3, "MIDDLE EAST", "ENERGY",
     "Two tankers hit mines and burn in the Strait of Hormuz",
     "IRGC says the ships used an unauthorised route; fires broke out in engine rooms.",
     "CLAIM", "Reuters", "tanker", (58, 25)),
    (4, "PACIFIC", "SECURITY",
     "Solomons sign security pact with Australia, shut out China",
     "Canberra becomes defence partner of choice; Honiara vows no foreign military base.",
     "CONFIRMED", "Reuters", "treaty", (160, -9.5)),
    (5, "ASIA", "DISASTER",
     "26 miners trapped in flooded Java gold mine; 3 bodies found",
     "Rain burst the Ciseureuh river into illegal shafts at Pongkor, Bogor, on Monday.",
     "CONFIRMED", "Reuters", "mine", (106.8, -6.6)),
    (6, "ASIA", "LABOUR",
     "Bangladesh raises garment wages 36% after weeks of protests",
     "Minimum pay rises to 17,000 taka ($139); workers had demanded it be doubled.",
     "CONFIRMED", "Reuters", "factory", (90.4, 23.8)),
    (7, "EUROPE", "WAR",
     "Zelenskiy confirms Ukraine hit a Russian ship off Finland",
     "Kyiv claims the Sparta II drone strike; Norway urges caution in such operations.",
     "CONFIRMED", "Reuters", "ship", (25, 60)),
    (8, "MIDDLE EAST", "WAR",
     "Houthis claim Ras Tanura refinery hit; Riyadh toll now 11",
     "Coalition says it downed 4 drones; Tuesday's tower strike hurt 11, two critical.",
     "CLAIM", "Reuters", "refinery", (49, 28)),
    (9, "MIDDLE EAST", "WAR",
     "Israeli strike kills Hamas security chief, wife and children",
     "Mohammad Abuelouf died in an airstrike on his Gaza apartment early Wednesday.",
     "REPORTED", "Reuters", "building", (34.5, 31.5)),
    (10, "EUROPE", "WAR",
     "Russian strikes cut power in five Ukraine regions",
     "Energy and gas sites damaged overnight; Odesa attack kills two, injures a child.",
     "REPORTED", "Reuters", "bolt", (30.7, 46.5)),
    (11, "AFRICA", "WAR",
     "Sudan drone strikes kill 19 civilians in Blue Nile",
     "Rights group Emergency Lawyers blames RSF paramilitaries for strikes on two cities.",
     "REPORTED", "Reuters", "drone", (34, 11)),
    (12, "EUROPE", "POLITICS",
     "Puigdemont to end exile and return to Spain on 12 December",
     "Catalan separatist leader announces comeback after this weekend's election.",
     "REPORTED", "Reuters", "plane", (2.2, 41.4)),
]

# n, text, source, confidence
ALSO = [
    (13, "Ramaphosa wins court reprieve over Phala Phala impeachment report", "Reuters", "REPORTED"),
    (14, "Colombia frees supermarket hostages in Cartagena siege; one captor killed", "Reuters", "REPORTED"),
    (15, "Pope Leo calls COP31 failure \u2018troubling\u2019, urges climate action", "AP", "REPORTED"),
    (16, "Dell posts record Q3: revenue $54.9bn, AI servers $22bn", "Dell", "REPORTED"),
    (17, "Nvidia falls 5.9% a day after its 31.5% surge on Huang's return", "AP", "CONFIRMED"),
    (18, "Poland seeks permanent US base after Russian airspace incursions", "Reports", "REPORTED"),
    (19, "NATO jets scrambled as Baltic states warn of drones", "Reuters", "REPORTED"),
    (20, "Lebanon to open a second airport next month", "Reuters", "REPORTED"),
    (21, "UK RAF moves jets to hangars at night over drone fears", "UK media", "REPORTED"),
    (22, "Xi graft probe hits a Shanghai rising star", "Reuters", "REPORTED"),
    (23, "Canada's foreign-student curbs test Carney's talent drive", "Reuters", "REPORTED"),
    (24, "Ukraine drones hit two Rosneft refineries in Samara, one killed", "Reports", "CLAIM"),
    (25, "Odesa strike kills two, injures child; Kyiv flat fire hurts two", "Just Security", "REPORTED"),
    (26, "Dow closes above 50,000 for the first time, at 50,018.70", "WSJ", "CONFIRMED"),
    (27, "Today is the International Day for the Elimination of Violence against Women", "UN", "CONFIRMED"),
    (28, "Samsung's market value slips below 1,000 trillion won", "SE Daily", "CONFIRMED"),
    (29, "SoftBank -14.8% and Kioxia -14.2% in Tokyo sell-off", "AP", "CONFIRMED"),
    (30, "Shanghai -2.0%, Shenzhen -3.45%, ChiNext -4.2%", "WSJ", "CONFIRMED"),
    (31, "Micron -11% as BNP cuts its rating on DRAM outlook", "SE Daily", "CONFIRMED"),
    (32, "Taiwan Taiex -5%: TSMC -3.6%, MediaTek -10%", "AP", "CONFIRMED"),
    (33, "Hong Kong Hang Seng -1.1% to 21,966", "AP", "CONFIRMED"),
    (34, "Nasdaq -1.5%, S&P 500 -0.5%, its 8th loss in 9 days", "WSJ", "CONFIRMED"),
    (35, "Norway urges caution after Kyiv's ship strikes", "Reuters", "REPORTED"),
    (36, "Saudi defences down four Houthi drones over Ras Tanura", "Reuters", "REPORTED"),
    (37, "Antam: Bogor mine was unauthorised, not part of our operations", "Reuters", "REPORTED"),
    (38, "Wage board voted 4-2; workers had wanted 18,000 taka", "Reuters", "REPORTED"),
    (39, "Solomons pact: Australia to spend $740m over a decade", "Australian media", "REPORTED"),
    (40, "First China-foreign \u2018space handshake\u2019 aboard Tiangong, 06:35 UTC", "CMSA", "CONFIRMED"),
]

NUMBERS = [
    ("-6.2%", "KOSPI \u00b7 SEOUL", "worst day in 10 mo"),
    ("+36%", "DHAKA WAGES", "17,000 taka / mo"),
    ("26", "MINERS TRAPPED", "Bogor, Java"),
    ("50,000", "DOW JONES", "first close above"),
]

TIMELINE = [
    ("20:00 TUE", "Dhaka wage board approves +36%"),
    ("00:18", "Shenzhou-24 launches"),
    ("03:56", "Docking at Tiangong"),
    ("06:35", "First space handshake"),
    ("07:31", "Kospi closes -6.2%"),
    ("09:46", "Hormuz mine blasts reported"),
]

REGIONS = [  # name, count, colour
    ("ASIA", 13, (185, 28, 28)),
    ("EUROPE", 10, (36, 84, 160)),
    ("AMERICAS", 7, (28, 122, 48)),
    ("MIDDLE EAST", 5, (222, 120, 20)),
    ("PACIFIC", 2, (0, 130, 135)),
    ("AFRICA", 2, (120, 80, 40)),
    ("WORLD", 1, (110, 110, 110)),
]

DATE_CHECK = [
    ("Huawei convicted in US trial", "24 Nov"),
    ("Giuliani Medal of Freedom", "24 Nov"),
    ("Sarkozy & Bruni to trial", "24 Nov"),
    ("ICJ: Myanmar guilty of Rohingya genocide", "19 Nov"),
    ("COP31 climate talks collapse", "22 Nov"),
    ("Huang returns as Nvidia CEO", "24 Nov"),
    ("Ukraine ships hit off Libya", "23 Nov"),
]

# Simplified continent polygons (lon, lat), equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73),
     (-65, 60), (-55, 52), (-60, 47), (-75, 43), (-80, 35), (-85, 30),
     (-90, 20), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
     (-140, 60), (-158, 58), (-168, 66)],
    [(-55, 60), (-45, 60), (-40, 64), (-30, 68), (-20, 70), (-25, 76),
     (-40, 80), (-55, 76), (-60, 70), (-55, 60)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-50, -30), (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-73, -25),
     (-77, -12), (-80, 10)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (9, 0), (9, 4), (-8, 5), (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (30, 70), (25, 71),
     (18, 69), (12, 65), (5, 60), (-5, 58), (-10, 54), (-10, 43), (-10, 36)],
    [(30, 62), (40, 68), (60, 69), (75, 73), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (150, 45),
     (140, 40), (130, 35), (127, 33), (120, 30), (110, 20), (105, 10),
     (100, 8), (95, 15), (90, 22), (85, 20), (80, 15), (75, 10), (72, 20),
     (66, 25), (60, 25), (55, 26), (50, 29), (48, 30), (43, 29), (40, 31),
     (35, 36), (30, 36), (30, 42), (30, 62)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -27), (150, -22),
     (146, -19), (142, -15), (142, -11), (136, -12), (132, -12), (126, -14),
     (122, -17), (118, -20), (113, -22)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41), (143, 43),
     (140, 44), (138, 40), (135, 36), (132, 33), (130, 31)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-5, 50)],
]
MAP_LABELS = [("N. AMERICA", -100, 47), ("S. AMERICA", -60, -15),
              ("AFRICA", 20, 5), ("EUROPE", 15, 52), ("ASIA", 95, 52),
              ("AUSTRALIA", 134, -25)]


# ---------------------------------------------------------------- icons
def draw_icon(d, kind, x, y, s):
    """Draw a small pictogram for a story inside the (x, y, s, s) box."""
    cx, cy = x + s // 2, y + s // 2
    if kind == "rocket":
        d.polygon([(cx, y + 3), (cx + 7, y + 16), (cx + 7, y + 34),
                   (cx - 7, y + 34), (cx - 7, y + 16)], fill=(200, 205, 210))
        d.polygon([(cx - 7, y + 26), (cx - 13, y + 36), (cx - 7, y + 36)],
                  fill=RED)
        d.polygon([(cx + 7, y + 26), (cx + 13, y + 36), (cx + 7, y + 36)],
                  fill=RED)
        d.ellipse([cx - 3, y + 12, cx + 3, y + 18], fill=(36, 84, 160))
        d.polygon([(cx - 4, y + 36), (cx + 4, y + 36), (cx, y + 44)],
                  fill=(230, 130, 20))
        for sx, sy in [(x + 4, y + 6), (x + s - 6, y + 10), (x + 8, y + 38)]:
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(120, 120, 120))
    elif kind == "chart":
        d.line([x + 5, y + 5, x + 5, y + s - 6, x + s - 4, y + s - 6],
               fill=INK, width=2)
        pts = [(x + 7, y + 10), (x + 15, y + 16), (x + 22, y + 14),
               (x + 30, y + 26), (x + 38, y + 36)]
        d.line(pts, fill=RED, width=3)
        for px, py in pts:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    elif kind == "tanker":
        d.rectangle([x + 4, y + 22, x + s - 4, y + 32], fill=(90, 60, 40))
        d.rectangle([x + 8, y + 14, x + 16, y + 22], fill=(120, 120, 120))
        d.rectangle([x + 20, y + 16, x + 30, y + 22], fill=(36, 84, 160))
        for i in range(3):
            d.line([x + 4 + i * 14, y + 36, x + 12 + i * 14, y + 36],
                   fill=(36, 84, 160), width=2)
        for dx, dy in [(0, -6), (7, -9), (-7, -9), (0, 0)]:
            d.line([cx + dx, y + 8 + dy, cx + dx, y + 16 + dy],
                   fill=(230, 130, 20), width=2)
        d.ellipse([cx - 3, y + 2, cx + 3, y + 8], fill=(230, 130, 20))
    elif kind == "treaty":
        d.rectangle([x + 10, y + 6, x + s - 10, y + s - 8], fill=CARD_BG,
                    outline=INK, width=2)
        for i in range(3):
            d.line([x + 14, y + 14 + i * 6, x + s - 14, y + 14 + i * 6],
                   fill=GREY, width=2)
        d.ellipse([cx - 6, y + s - 14, cx + 6, y + s - 2], fill=RED)
        d.ellipse([cx - 2, y + s - 10, cx + 2, y + s - 6], fill=(255, 220, 120))
    elif kind == "mine":
        d.polygon([(x + 10, y + 4), (x + s - 10, y + 4), (x + s - 6, y + s - 4),
                   (x + 6, y + s - 4)], fill=(96, 78, 58))
        d.line([x + 14, y + 10, x + 14, y + s - 6], fill=(190, 160, 110), width=2)
        d.line([x + s - 14, y + 10, x + s - 14, y + s - 6], fill=(190, 160, 110),
               width=2)
        for i in range(4):
            d.line([x + 12, y + 14 + i * 8, x + s - 12, y + 14 + i * 8],
                   fill=(190, 160, 110), width=2)
        d.ellipse([cx - 7, cy - 3, cx + 7, cy + 11], fill=(230, 190, 40))
        d.ellipse([cx - 2, cy + 1, cx + 2, cy + 5], fill=(255, 240, 150))
    elif kind == "factory":
        d.rectangle([x + 6, y + 18, x + s - 6, y + s - 6], fill=(120, 120, 125))
        d.polygon([(x + 6, y + 18), (x + 14, y + 10), (x + 22, y + 18),
                   (x + 30, y + 10), (x + s - 6, y + 18)], fill=(90, 90, 95))
        d.rectangle([x + 10, y + 6, x + 14, y + 16], fill=(90, 90, 95))
        d.rectangle([x + 12, y + 28, x + 18, y + 34], fill=(255, 220, 120))
        d.rectangle([x + 26, y + 28, x + 32, y + 34], fill=(255, 220, 120))
        d.rectangle([x + 12, y + 38, x + 32, y + s - 6], fill=(70, 70, 75))
    elif kind == "ship":
        d.rectangle([x + 4, y + 26, x + s - 4, y + 34], fill=(40, 60, 90))
        d.rectangle([x + 10, y + 18, x + 26, y + 26], fill=(36, 84, 160))
        d.rectangle([x + 28, y + 14, x + 34, y + 26], fill=(200, 205, 210))
        d.line([x + 30, y + 8, x + 30, y + 14], fill=INK, width=2)
        d.line([x + 8, y + 38, x + 16, y + 38], fill=(36, 84, 160), width=2)
        d.line([x + 22, y + 38, x + 34, y + 38], fill=(36, 84, 160), width=2)
        d.ellipse([cx + 6, y + 2, cx + 12, y + 8], fill=(90, 90, 90))
        d.line([cx + 9, y + 8, cx + 9, y + 12], fill=(90, 90, 90), width=2)
    elif kind == "refinery":
        d.rectangle([x + 8, y + 14, x + 14, y + s - 6], fill=(120, 120, 125))
        d.rectangle([x + 18, y + 20, x + 24, y + s - 6], fill=(120, 120, 125))
        d.rectangle([x + 28, y + 10, x + 34, y + s - 6], fill=(150, 150, 155))
        d.ellipse([x + 30, y + 2, x + 36, y + 8], fill=(230, 130, 20))
        d.line([x + 6, y + s - 6, x + s - 4, y + s - 6], fill=INK, width=2)
        d.line([x + 14, y + 24, x + 28, y + 24], fill=(90, 90, 90), width=2)
    elif kind == "building":
        d.rectangle([x + 10, y + 8, x + s - 10, y + s - 6], fill=(150, 140, 130))
        for r in range(3):
            for c in range(3):
                d.rectangle([x + 14 + c * 9, y + 12 + r * 10,
                             x + 20 + c * 9, y + 18 + r * 10],
                            fill=(255, 220, 120))
        d.polygon([(cx, y + 2), (cx + 3, y + 6), (cx, y + 10), (cx - 3, y + 6)],
                  fill=RED)
    elif kind == "bolt":
        d.polygon([(cx + 4, y + 4), (cx - 6, y + 24), (cx - 1, y + 24),
                   (cx - 4, y + s - 4), (cx + 7, y + 20), (cx + 1, y + 20)],
                  fill=(230, 180, 20))
        d.rectangle([x + 8, y + s - 8, x + s - 8, y + s - 4], fill=GREY)
    elif kind == "drone":
        d.ellipse([x + 2, y + 2, x + 14, y + 8], fill=(70, 70, 70))
        d.ellipse([x + s - 14, y + 2, x + s - 2, y + 8], fill=(70, 70, 70))
        d.ellipse([x + 2, y + s - 10, x + 14, y + s - 4], fill=(70, 70, 70))
        d.ellipse([x + s - 14, y + s - 10, x + s - 2, y + s - 4],
                  fill=(70, 70, 70))
        d.rectangle([cx - 9, cy - 6, cx + 9, cy + 6], fill=(50, 50, 50))
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    elif kind == "plane":
        d.polygon([(x + 4, cy + 2), (x + s - 8, cy - 6), (x + s - 4, cy - 2),
                   (x + s - 8, cy + 2), (x + 12, cy + 6), (x + 6, cy + 8)],
                  fill=(36, 84, 160))
        d.polygon([(cx - 2, cy - 2), (cx + 6, cy - 14), (cx + 10, cy - 12),
                   (cx + 4, cy)], fill=(36, 84, 160))


# ---------------------------------------------------------------- build
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 12

    # ---------- masthead ----------
    d.rectangle([MX, y, W - MX, y + 4], fill=RED)
    y += 12
    tf = font(SERIF_B, 38)
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 48
    sf = font(SANS_B, 15)
    sub = "WEDNESDAY, 25 NOVEMBER 2026  \u2022  40 STORIES  \u2022  ALL TIMES UTC"
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, y), sub, font=sf, fill=RED)
    y += 22
    d.rectangle([MX, y, W - MX, y + 4], fill=RULE)
    y += 10

    # ---------- sub-deck: top 3 headlines ----------
    deck_f = font(SANS_B, 14)
    top3 = [
        "1  Pakistan's first astronaut docks at China's Tiangong station",
        "2  Asia's chip rout: Kospi plunges 6.2% as AI doubts return",
        "3  Two tankers hit mines and burn in the Strait of Hormuz",
    ]
    for line in top3:
        d.text((MX, y), line, font=deck_f, fill=INK)
        y += 16
    y += 4

    # ---------- big-number strip ----------
    strip_y = y
    bw = (CW - 3 * 8) // 4
    for i, (num, lab, sub2) in enumerate(NUMBERS):
        bx = MX + i * (bw + 8)
        d.rectangle([bx, strip_y, bx + bw, strip_y + 40], fill=DARK)
        nf = font(SANS_B, 24)
        d.text((bx + 10, strip_y + 7), num, font=nf,
               fill=(255, 214, 90) if i != 2 else (255, 255, 255))
        nx = bx + 10 + d.textlength(num, font=nf) + 10
        lf = font(SANS_B, 11)
        d.text((nx, strip_y + 8), lab, font=lf, fill=(232, 196, 120))
        sf2 = font(SANS, 10)
        d.text((nx, strip_y + 23), sub2, font=sf2, fill=(190, 186, 176))
    y = strip_y + 40 + 8

    # ---------- world map (label inside, top-left over the Atlantic) ----------
    map_x, map_y, map_w, map_h = MX, y, CW, 104
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=OCEAN,
                outline=LGREY, width=1)

    def project(lon, lat):
        px = map_x + (lon + 180) / 360.0 * map_w
        py = map_y + (80 - lat) / 135.0 * map_h
        return px, py

    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for name, lon, lat in MAP_LABELS:
        px, py = project(lon, lat)
        lf = font(SANS_B, 9)
        d.text((px - d.textlength(name, font=lf) / 2, py - 5), name,
               font=lf, fill=(110, 105, 90))
    d.text((map_x + 8, map_y + 6), "WHERE IT HAPPENED \u2014 TOP 12, PINNED",
           font=font(SANS_B, 11), fill=RED)
    for (n, _reg, _tag, _h, _de, conf, _s, _ic, (lon, lat)) in TOP:
        px, py = project(lon, lat)
        col = CONF_COLOR[conf]
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col,
                  outline=(255, 255, 255), width=2)
        nf = font(SANS_B, 9 if n < 10 else 8)
        t = str(n)
        d.text((px - d.textlength(t, font=nf) / 2, py - 5), t, font=nf,
               fill=(255, 255, 255))
    y = map_y + map_h + 8

    # ---------- illustrated top-12 grid ----------
    gap = 10
    colw = (CW - gap) // 2
    card_h, card_gap = 58, 4
    for i, (n, region, tag, head, deck, conf, src, icon, _pin) in enumerate(TOP):
        cx = MX + (i % 2) * (colw + gap)
        cy = y + (i // 2) * (card_h + card_gap)
        d.rectangle([cx, cy, cx + colw, cy + card_h], fill=CARD_BG,
                    outline=LGREY, width=1)
        # icon
        ix, iy = cx + 4, cy + 5
        d.rectangle([ix, iy, ix + 46, iy + 46], fill=(244, 240, 232),
                    outline=LGREY, width=1)
        draw_icon(d, icon, ix, iy, 46)
        tx = cx + 56
        twd = colw - 56 - 8
        # tag line: number, region, confidence badge
        col = CONF_COLOR[conf]
        tag_f = font(SANS_B, 10)
        d.text((tx, cy + 4), f"{n} \u00b7 {region} \u2014 {tag}", font=tag_f,
               fill=RED)
        badge = conf
        bf = font(SANS_B, 9)
        bw2 = d.textlength(badge, font=bf) + 8
        d.rectangle([cx + colw - 8 - bw2, cy + 4, cx + colw - 8, cy + 15],
                    fill=col)
        d.text((cx + colw - 8 - bw2 + 4, cy + 5), badge, font=bf,
               fill=(255, 255, 255))
        # source, bottom right of card
        srf = font(SANS, 9)
        st = f"Source: {src}"
        sw_st = d.textlength(st, font=srf)
        d.text((cx + colw - 8 - sw_st, cy + card_h - 12), st, font=srf,
               fill=GREY)
        # headline (max 2 lines) then deck on the next free line
        hf = font(SANS_B, 13)
        lines = wrap_to(d, head, hf, twd, 2)
        ly = cy + 17
        for ln in lines:
            d.text((tx, ly), ln, font=hf, fill=INK)
            ly += 15
        df = font(SANS, 10)
        d.text((tx, ly), fit(d, deck, df, twd - sw_st - 10), font=df,
               fill=(70, 66, 60))
    y = y + 6 * (card_h + card_gap) - card_gap + 8

    # ---------- UTC timeline ----------
    # header sits at the left; the dot-line starts after it so the first
    # time label can never collide with the header text
    d.text((MX, y), "THE DAY IN UTC", font=font(SANS_B, 11), fill=RED)
    y += 13
    tl_y = y + 14
    tl_x0 = MX + 110
    d.line([tl_x0 + 4, tl_y, W - MX - 4, tl_y], fill=LGREY, width=2)
    seg = (CW - 110) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        px = tl_x0 + seg * i + seg / 2
        d.ellipse([px - 4, tl_y - 4, px + 4, tl_y + 4], fill=RED,
                  outline=(255, 255, 255), width=1)
        tf2 = font(SANS_B, 10)
        d.text((px - d.textlength(t, font=tf2) / 2, tl_y - 13), t, font=tf2,
               fill=INK)
        lf = font(SANS, 9)
        lab = fit(d, label, lf, seg - 8)
        d.text((px - d.textlength(lab, font=lf) / 2, tl_y + 6), lab,
               font=lf, fill=(70, 66, 60))
    y = tl_y + 15

    # ---------- region bar ----------
    d.text((MX, y), "WHERE THE NEWS CAME FROM \u2014 40 STORIES BY REGION",
           font=font(SANS_B, 11), fill=RED)
    y += 14
    total = sum(c for _n, c, _c in REGIONS)
    bx = MX
    for name, count, col in REGIONS:
        wseg = round(CW * count / total)
        d.rectangle([bx, y, bx + wseg, y + 16], fill=col)
        lf = font(SANS_B, 10)
        lab = f"{name} {count}"
        if wseg > d.textlength(lab, font=lf) + 8:
            d.text((bx + 6, y + 3), lab, font=lf, fill=(255, 255, 255))
        else:
            d.text((bx + 2, y + 3), str(count), font=lf, fill=(255, 255, 255))
        bx += wseg
    y += 16 + 4

    # ---------- ALSO ON ----------
    d.text((MX, y), "ALSO ON \u2014 28 MORE STORIES IN ONE LINE EACH",
           font=font(SANS_B, 12), fill=RED)
    y += 15
    per_col = 14
    colw2 = (CW - 20) // 2
    lf = font(SANS, 11)
    bf = font(SANS_B, 10)
    for i, (n, text, src, conf) in enumerate(ALSO):
        col_i = i // per_col
        row = i % per_col
        lx = MX + col_i * (colw2 + 20)
        ly = y + row * 11
        col = CONF_COLOR[conf]
        d.ellipse([lx, ly, lx + 12, ly + 12], fill=col)
        nf = font(SANS_B, 8)
        t = str(n)
        d.text((lx + 6 - d.textlength(t, font=nf) / 2, ly + 2), t, font=nf,
               fill=(255, 255, 255))
        sfx = f" \u00b7 {src}"
        avail = colw2 - 16 - d.textlength(sfx, font=lf)
        d.text((lx + 16, ly + 1), fit(d, text, lf, avail), font=lf, fill=INK)
        d.text((lx + 16 + d.textlength(fit(d, text, lf, avail), font=lf), ly + 1),
               sfx, font=lf, fill=GREY)
    y = y + per_col * 11 + 6

    # ---------- footer: DATE CHECK + legend + sources ----------
    d.rectangle([MX, y, W - MX, y + 44], fill=DARK)
    fy = y + 5
    d.text((MX + 10, fy), "DATE CHECK \u2014 LEFT OUT ON PURPOSE:",
           font=font(SANS_B, 10), fill=(232, 196, 120))
    fy += 13
    items = "  \u2022  ".join(f"{t} \u2014 {dt}" for t, dt in DATE_CHECK)
    df2 = font(SANS, 10)
    ilines = wrap_to(d, items, df2, CW - 20, 2)
    for ln in ilines:
        d.text((MX + 10, fy), ln, font=df2, fill=(235, 232, 226))
        fy += 12
    y += 44 + 6
    # legend
    lf2 = font(SANS_B, 10)
    lx = MX
    d.text((lx, y), "HOW SURE:", font=lf2, fill=INK)
    lx += d.textlength("HOW SURE: ", font=lf2)
    for conf, note in [("CONFIRMED", "two wires or an official record"),
                       ("REPORTED", "one named source"),
                       ("CLAIM", "one side's claim")]:
        col = CONF_COLOR[conf]
        d.ellipse([lx, y + 2, lx + 8, y + 10], fill=col)
        lx += 11
        seg_t = f"{conf} \u2014 {note}    "
        d.text((lx, y), seg_t, font=font(SANS, 10), fill=INK)
        lx += d.textlength(seg_t, font=font(SANS, 10))
    y += 13
    d.text((MX, y), "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 Al Jazeera \u00b7 WSJ \u00b7 CMSA/Xinhua \u00b7 UN \u2014 All stories dated Tuesday 25 November 2026.",
           font=font(SANS, 10), fill=GREY)

    print("final y:", y)
    img.save("entry-v2.png", format="PNG", optimize=True)
    print("saved entry-v2.png", img.size)


if __name__ == "__main__":
    main()
