#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261125 entry.

Draws a newspaper-style one-page summary of Wednesday 25 November 2026
world news as a 1024x1024 PNG. Deterministic: same input, same bytes
(PIL PNG encoder is deterministic for identical pixel data).

Stories verified against Reuters (via DevDiscourse), BBC, Al Jazeera
summaries of 25 Nov 2026.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 236)
INK = (17, 17, 17)
RED = (185, 28, 28)
GREY = (90, 86, 80)
RULE = (17, 17, 17)
CARD_BG = (255, 255, 255)
DARK = (26, 26, 26)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width."""
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
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # margin

    # ---------- masthead ----------
    y = 26
    d.rectangle([mx, y, W - mx, y + 4], fill=RED)
    y += 16
    title = "THE WORLD IN ONE PAGE"
    tf = font(SERIF_B, 56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 70
    sub = "WORLD NEWS  •  WEDNESDAY, 25 NOVEMBER 2026"
    sf = font(SANS_B, 21)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, y), sub, font=sf, fill=RED)
    y += 34
    d.rectangle([mx, y, W - mx, y + 5], fill=RULE)
    y += 16

    # ---------- lead story: Ukraine ----------
    tag_f = font(SANS_B, 19)
    d.text((mx, y), "EUROPE  —  WAR AT SEA", font=tag_f, fill=RED)
    y += 30
    head_f = font(SANS_B, 39)
    y = draw_wrapped(d, mx, y,
                     "Zelenskiy confirms Ukraine hit a Russian ship in the Gulf of Finland",
                     head_f, W - 2 * mx, INK, 47)
    y += 8
    deck_f = font(SANS, 22)
    y = draw_wrapped(d, mx, y,
                     "Kyiv claims the drone strike on a Russian cargo ship; Putin warns "
                     "retaliation is \u201cinevitable\u201d after attacks on Russian oil plants. "
                     "NATO will send early-warning aircraft to Poland.",
                     deck_f, W - 2 * mx, (51, 51, 51), 30)
    y += 14
    d.line([mx, y, W - mx, y], fill=(190, 184, 174), width=2)
    y += 16

    # ---------- 2x2 story grid ----------
    cards = [
        ("MIDDLE EAST", "Houthis hit Riyadh\u2019s tallest tower",
         "A drone attack wounds 11 in the Saudi capital. The Saudi-led coalition "
         "condemns a \u201cterrorist attack\u201d as rebels close in on Aden."),
        ("TECH", "Huawei convicted in US trial",
         "A jury finds the Chinese firm guilty of stealing trade secrets, in a "
         "sprawling case over its Iran business; it is acquitted of racketeering."),
        ("AMERICAS", "Trump gives Giuliani the Medal of Freedom",
         "The former New York mayor receives the United States\u2019 highest civilian "
         "honour at the White House."),
        ("EUROPE", "Sarkozy ordered to stand trial",
         "The former French president and his wife Carla Bruni face a corruption "
         "trial; the first hearing is set for 1 April 2027."),
    ]
    gap = 16
    cw = (W - 2 * mx - gap) // 2
    ch = 196
    for i, (tag, head, body) in enumerate(cards):
        cx = mx + (i % 2) * (cw + gap)
        cy = y + (i // 2) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD_BG,
                    outline=(200, 194, 184), width=2)
        px, py = cx + 18, cy + 14
        d.text((px, py), tag, font=tag_f, fill=RED)
        py += 28
        py = draw_wrapped(d, px, py, head, font(SANS_B, 25), cw - 36, INK, 30)
        py += 6
        draw_wrapped(d, px, py, body, font(SANS, 18), cw - 36, (51, 51, 51), 24)

    y = y + 2 * ch + gap + 16

    # ---------- footer: also today ----------
    fh = H - y - 28
    d.rectangle([mx, y, W - mx, y + fh], fill=DARK)
    fy = y + 16
    d.text((mx + 18, fy), "ALSO TODAY", font=font(SANS_B, 19), fill=(232, 196, 120))
    fy += 30
    fy = draw_wrapped(d, mx + 18, fy,
                      "NATO plans early-warning jets for Poland  •  Nvidia\u2019s Huang returns "
                      "as CEO as shares jump 31%  •  Today is the International Day for the "
                      "Elimination of Violence against Women",
                      font(SANS, 19), W - 2 * mx - 36, (235, 232, 226), 26)
    fy += 10
    d.line([mx + 18, fy, W - mx - 18, fy], fill=(90, 86, 80), width=1)
    fy += 10
    d.text((mx + 18, fy), "Headlines: Reuters, BBC, Al Jazeera  —  25 November 2026",
           font=font(SANS, 16), fill=(170, 166, 158))

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
