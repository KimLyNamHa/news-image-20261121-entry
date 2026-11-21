#!/usr/bin/env python3
"""Draw the world-news poster for Saturday 21 November 2026 (1024x1024 PNG).

A fresh newspaper front page, drawn programmatically with PIL and DejaVu
fonts (local build only — the shipped entrypoint, main.py, only copies the
finished entry.png and loads no font at all). Layout: masthead with the day's
three leads in the subhead, a stat bar, a region strip, three big lead
stories with original vector illustrations, ten more stories in a 4-3-3 card
grid, a world map, twenty one-line briefs, a red DATE CHECK box and a footer.

33 stories in all: 3 leads + 10 cards + 20 briefs. Every story happened, or
was first reported, on Saturday 21 November 2026; sources are named beside
each story. Friday 20 November and earlier stories are NOT shown as
Saturday news: the ICJ Myanmar verdict, the Shenzhen summit, the Anthropic
IPO, the PIF Tower strike, the GTA VI launch, the Van Gogh sale, Wall
Street's correction, the Kyiv bridges barrage, the missile in Poland, the
UK-EU deal, Cyclone Akvan's landfall, Voyager 1's light-day, Fiona the
hippo and the Virginia measles death are listed only in the DATE CHECK box
as excluded.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (14, 42, 71)
NIGHT = (10, 28, 58)
RED = (178, 28, 28)
GOLD = (242, 183, 5)
INK = (24, 24, 24)
GREY = (74, 74, 74)
WHITE = (255, 255, 255)
TEAL = (0, 110, 120)
GREEN = (30, 110, 60)
BLUE = (21, 80, 160)
PURPLE = (106, 27, 154)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size, fallback="DejaVuSans.ttf"):
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.truetype(FONT_DIR + fallback, size)


F_SERIF = font("DejaVuSerif-Bold.ttf", 58)
F_SERIF_SM = font("DejaVuSerif.ttf", 17)
F_KICK = font("DejaVuSans-Bold.ttf", 13)
F_KICK_SM = font("DejaVuSans-Bold.ttf", 11)
F_STAT = font("DejaVuSans-Bold.ttf", 25)
F_STAT_L = font("DejaVuSans.ttf", 11)
F_TAG = font("DejaVuSans-Bold.ttf", 12)
F_HEAD = font("DejaVuSans-Bold.ttf", 21)
F_BODY = font("DejaVuSans.ttf", 13)
F_CARD_H = font("DejaVuSans-Bold.ttf", 15)
F_CARD_B = font("DejaVuSans.ttf", 12)
F_BRIEF = font("DejaVuSans.ttf", 11)
F_BRIEF_B = font("DejaVuSans-Bold.ttf", 11)
F_SMALL = font("DejaVuSans.ttf", 11)
F_SMALL_B = font("DejaVuSans-Bold.ttf", 11)
F_NUM = font("DejaVuSans-Bold.ttf", 10)


def wrap(d, text, fnt, width, max_lines=None):
    """Wrap text to pixel width; truncate the last line with an ellipsis."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + " ...", font=fnt) > width:
            lines[-1] = lines[-1][:-1].strip()
        lines[-1] = (lines[-1] + " ...").strip()
    return lines


def one_line(d, text, fnt, width):
    """Fit text to one line, truncating with an ellipsis if needed."""
    if d.textlength(text, font=fnt) <= width:
        return text
    while text and d.textlength(text + "...", font=fnt) > width:
        text = text[:-1].rstrip()
    return text + "..."


def card(d, x, y, w, h, tag, headline, body, colour):
    """A text card under its illustration banner; tag already holds its number."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=WHITE,
                        outline=(205, 195, 175), width=1)
    d.text((x + 10, y + 6), tag, font=F_TAG, fill=colour)
    ly = y + 24
    for line in wrap(d, headline, F_CARD_H, w - 20, 2):
        d.text((x + 10, ly), line, font=F_CARD_H, fill=NAVY)
        ly += 17
    ly += 2
    for line in wrap(d, body, F_CARD_B, w - 20, 2):
        d.text((x + 10, ly), line, font=F_CARD_B, fill=GREY)
        ly += 13


# ------------------------------------------------------------------ art
def art_cop31(d, x, y, w, h):
    """Antalya at dusk: sea, setting sun, summit flags, podium."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 200, 120))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(38, 110, 160))
    d.ellipse([x + w // 2 - 26, y + 8, x + w // 2 + 26, y + 60],
              fill=(255, 150, 40))
    for i, fx in enumerate(range(0, w, 44)):
        col = [(0, 50, 140), (170, 20, 20), (30, 110, 60), (242, 183, 5),
               (106, 27, 154)][i % 5]
        d.rectangle([x + fx + 6, y + 6, x + fx + 34, y + 22], fill=col)
        d.rectangle([x + fx + 18, y + 6, x + fx + 22, y + 22], fill=WHITE)
    d.rectangle([x + 18, y + h - 26, x + w - 18, y + h - 8], fill=NAVY)
    d.text((x + 26, y + h - 24), "COP31 · ANTALYA", font=F_SMALL_B,
           fill=WHITE)
    d.text((x + w - 96, y + h - 24), "NO DEAL", font=F_SMALL_B, fill=GOLD)


def art_riyadh(d, x, y, w, h):
    """Night over Riyadh: skyline, three missile trails, interception bursts."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for sx, sy in [(18, 10), (70, 22), (150, 8), (230, 18), (280, 10),
                   (110, 30), (200, 32)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    for bx, bw, bh in [(10, 30, 34), (60, 22, 26), (120, 26, 44),
                       (180, 20, 30), (240, 28, 38)]:
        d.rectangle([x + bx, y + h - 12 - bh, x + bx + bw, y + h - 12],
                    fill=(30, 55, 90))
    d.rectangle([x + 128, y + h - 52, x + 138, y + h - 12], fill=(30, 55, 90))
    for (tx, ty) in [(60, 14), (160, 10), (250, 16)]:
        d.line([x + tx, y + ty + 26, x + tx + 14, y + ty], fill=GOLD,
               width=2)
        for dx, dy in [(0, 0), (-6, 4), (6, 4), (0, -6), (-5, -4), (5, -4)]:
            d.line([x + tx + 14, y + ty, x + tx + 14 + dx * 2,
                    y + ty + dy * 2], fill=(255, 170, 40), width=2)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 130, 150))


def art_quake(d, x, y, w, h):
    """The Andes shake: peaks, seismic waves, cracked ground."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 196, 150))
    d.polygon([(x, y + h), (x + 60, y + 12), (x + 120, y + h)], fill=(90, 70, 50))
    d.polygon([(x + 90, y + h), (x + 170, y + 4), (x + 250, y + h)],
              fill=(120, 95, 70))
    d.polygon([(x + 150, y + 4), (x + 162, y + 20), (x + 178, y + 20),
               (x + 186, y + 8)], fill=WHITE)
    for wy in (26, 44, 62):
        pts = []
        for px in range(0, w + 1, 12):
            pts.append((x + px, y + wy + (6 if (px // 12) % 2 else -6)))
        d.line(pts, fill=RED, width=2)
    d.text((x + 10, y + h - 20), "M 6.7", font=F_SMALL_B, fill=RED)
    d.line([x + w - 70, y + h - 8, x + w - 40, y + h - 18, x + w - 10,
            y + h - 8], fill=INK, width=2)


def art_kryvyi(d, x, y, w, h):
    """A shelled apartment block in Kryvyi Rih, flames at the break."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 208, 170))
    d.rectangle([x + 30, y + 10, x + w - 30, y + h - 8], fill=(120, 110, 100))
    d.polygon([(x + 30, y + 10), (x + 70, y + 10), (x + 55, y + 26),
               (x + 30, y + 26)], fill=(120, 110, 100))
    for wx in (44, 84, 124):
        for wy in (34, 56):
            d.rectangle([x + wx, y + wy, x + wx + 16, y + wy + 12],
                        fill=(255, 230, 120))
    for fx, fy, r in [(100, 16, 9), (140, 20, 7), (120, 8, 6)]:
        d.ellipse([x + fx - r, y + fy - r, x + fx + r, y + fy + r],
                  fill=(255, 140, 40))
        d.ellipse([x + fx - r // 2, y + fy - r // 2, x + fx + r // 2,
                   y + fy + r // 2], fill=(255, 230, 120))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(90, 90, 80))


def art_capitol(d, x, y, w, h):
    """A white domed capitol on navy, with a tax ledger."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.rectangle([x + 40, y + h - 22, x + w - 40, y + h - 8], fill=WHITE)
    d.rectangle([x + 70, y + h - 38, x + w - 70, y + h - 22], fill=WHITE)
    d.ellipse([x + w // 2 - 22, y + 6, x + w // 2 + 22, y + 40], fill=WHITE)
    d.rectangle([x + w - 52, y + 8, x + w - 16, y + 40], fill=GOLD)
    d.line([x + w - 48, y + 16, x + w - 20, y + 16], fill=NAVY, width=2)
    d.line([x + w - 48, y + 24, x + w - 20, y + 24], fill=NAVY, width=2)
    d.line([x + w - 48, y + 32, x + w - 20, y + 32], fill=NAVY, width=2)


def art_flags_asia(d, x, y, w, h):
    """China red and Japan white, side by side, with a speech mark."""
    d.rectangle([x, y, x + w // 2 - 2, y + h], fill=(170, 20, 20))
    d.ellipse([x + 18, y + 10, x + 34, y + 26], fill=GOLD)
    d.rectangle([x + w // 2 + 2, y, x + w, y + h], fill=WHITE)
    d.ellipse([x + w // 2 + 34, y + 8, x + w // 2 + 62, y + 36], fill=RED)
    d.ellipse([x + w - 52, y + h - 30, x + w - 20, y + h - 6], fill=NAVY)
    d.text((x + w - 46, y + h - 26), "!", font=F_SMALL_B, fill=WHITE)


def art_plane(d, x, y, w, h):
    """A 767 on final approach over the sea, Davao below."""
    d.rectangle([x, y, x + w, y + h], fill=(140, 190, 220))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(38, 110, 160))
    d.ellipse([x + w - 46, y + 6, x + w - 14, y + 30], fill=(255, 220, 120))
    mx, my = x + w // 2, y + h // 2 - 4
    d.polygon([(mx - 70, my), (mx + 50, my - 8), (mx + 70, my),
               (mx + 50, my + 8)], fill=WHITE)
    d.polygon([(mx - 70, my), (mx - 84, my + 8), (mx - 78, my - 2)],
              fill=(200, 40, 40))
    d.polygon([(mx - 10, my - 6), (mx + 6, my - 22), (mx + 16, my - 6)],
              fill=WHITE)
    d.line([x + 8, y + h - 24, x + w - 8, y + h - 24], fill=WHITE, width=2)
    d.text((x + 10, y + h - 14), "DAVAO", font=F_SMALL_B, fill=WHITE)


def art_chart(d, x, y, w, h):
    """Bitcoin falls: a dark board, a red line down, the price in white."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 16, 16))
    for gy in range(1, 4):
        yy = y + h * gy // 4
        d.line([x + 6, yy, x + w - 6, yy], fill=(50, 50, 50), width=1)
    pts = [(x + 10, y + 10), (x + 60, y + 14), (x + 110, y + 24),
           (x + 160, y + 40), (x + 210, y + 50), (x + 260, y + 66)]
    d.line(pts, fill=(255, 70, 70), width=3, joint="curve")
    for (cx, top, bot) in [(40, 14, 26), (90, 18, 32), (140, 28, 42),
                           (190, 44, 58), (240, 54, 68)]:
        d.rectangle([x + cx - 5, y + top, x + cx + 5, y + bot],
                    fill=(200, 40, 40))
    d.text((x + 10, y + h - 20), "$58,983  -3.9%", font=F_SMALL_B,
           fill=WHITE)
    d.text((x + 170, y + h - 20), "ETH $1,625", font=F_SMALL_B,
           fill=(255, 120, 120))


def art_racecar(d, x, y, w, h):
    """A single-seater flat out under the Las Vegas lights."""
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 30))
    for sx in range(0, w, 26):
        d.ellipse([x + sx + 6, y + 8, x + sx + 10, y + 12], fill=GOLD)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(60, 60, 70))
    d.line([x, y + h - 18, x + w, y + h - 18], fill=WHITE, width=2)
    mx, my = x + w // 2, y + h // 2
    d.polygon([(mx - 70, my + 6), (mx + 60, my - 4), (mx + 78, my + 2),
               (mx + 60, my + 10)], fill=(200, 40, 40))
    d.polygon([(mx - 30, my - 4), (mx - 6, my - 18), (mx + 10, my - 4)],
              fill=(200, 40, 40))
    d.ellipse([mx - 52, my + 2, mx - 34, my + 20], fill=INK)
    d.ellipse([mx + 34, my + 2, mx + 52, my + 20], fill=INK)
    d.rectangle([x + 10, y + 12, x + 34, y + 30], fill=WHITE)
    d.rectangle([x + 10, y + 12, x + 22, y + 21], fill=INK)
    d.rectangle([x + 22, y + 21, x + 34, y + 30], fill=INK)


def art_cricket(d, x, y, w, h):
    """A green outfield, a pale pitch, stumps and a bat mid-swing."""
    d.rectangle([x, y, x + w, y + h], fill=(60, 140, 70))
    d.rectangle([x + w // 2 - 60, y, x + w // 2 + 60, y + h],
                fill=(214, 190, 140))
    for sx in (w // 2 - 12, w // 2, w // 2 + 12):
        d.line([x + sx, y + 8, x + sx, y + 22], fill=(255, 230, 160), width=3)
    d.polygon([(x + 30, y + h - 12), (x + 44, y + h - 20),
               (x + 96, y + 18), (x + 84, y + 26)], fill=(150, 100, 50))
    d.polygon([(x + 96, y + 18), (x + 104, y + 10), (x + 112, y + 16),
               (x + 104, y + 24)], fill=(120, 80, 40))
    d.ellipse([x + w - 30, y + 12, x + w - 16, y + 26], fill=RED)
    d.text((x + 10, y + h - 18), "124*", font=F_SMALL_B, fill=WHITE)


def art_space(d, x, y, w, h):
    """BepiColombo closes on Mercury: stars, a cratered world, a probe."""
    d.rectangle([x, y, x + w, y + h], fill=(8, 8, 20))
    for sx, sy in [(16, 8), (60, 22), (120, 6), (200, 16), (280, 10),
                   (330, 24), (90, 34), (240, 36)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    cx, cy, r = x + w - 62, y + h // 2, 18
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 165, 155))
    for ox, oy, orad in [(-8, -6, 4), (6, 5, 3), (-2, 10, 2)]:
        d.ellipse([cx + ox - orad, cy + oy - orad, cx + ox + orad,
                   cy + oy + orad], fill=(130, 125, 115))
    d.rectangle([x + 30, y + h // 2 - 7, x + 50, y + h // 2 + 7],
                fill=(200, 200, 210))
    d.rectangle([x + 10, y + h // 2 - 4, x + 30, y + h // 2 + 4],
                fill=(40, 90, 180))
    d.rectangle([x + 50, y + h // 2 - 4, x + 70, y + h // 2 + 4],
                fill=(40, 90, 180))
    for t in range(0, 11):
        px = x + 76 + (cx - r - 84) * t / 10
        py = y + h // 2 - 5 * math.sin(math.pi * t / 10)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=GOLD)


def art_ballot(d, x, y, w, h):
    """A ballot box in South Africa's colours, one vote in the slot."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 235, 220))
    d.rectangle([x, y, x + w, y + 12], fill=GREEN)
    d.rectangle([x, y + 12, x + w, y + 24], fill=GOLD)
    d.rectangle([x, y + 24, x + w, y + 36], fill=RED)
    d.rectangle([x + w // 2 - 55, y + 8, x + w // 2 + 55, y + h - 6],
                fill=WHITE, outline=INK, width=2)
    d.rectangle([x + w // 2 - 25, y + 12, x + w // 2 + 25, y + 18],
                fill=INK)
    d.rectangle([x + w // 2 - 12, y - 2, x + w // 2 + 12, y + 14],
                fill=(200, 40, 40))
    d.text((x + 10, y + h - 18), "31%", font=F_SMALL_B, fill=RED)


def art_boat(d, x, y, w, h):
    """A capsized funeral boat on a wide brown river in Bayelsa."""
    d.rectangle([x, y, x + w, y + h], fill=(140, 190, 220))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(120, 90, 50))
    for wy in (h // 2 + 10, h // 2 + 22, h - 14):
        for wx in range(0, w, 30):
            d.arc([x + wx, y + wy, x + wx + 26, y + wy + 10], 0, 180,
                  fill=(220, 200, 160), width=2)
    d.polygon([(x + 60, y + h // 2 - 6), (x + 200, y + h // 2 - 6),
               (x + 180, y + h // 2 + 12), (x + 80, y + h // 2 + 12)],
              fill=(90, 60, 30))
    d.polygon([(x + 60, y + h // 2 - 6), (x + 200, y + h // 2 - 6),
               (x + 190, y + h // 2 - 16), (x + 70, y + h // 2 - 16)],
              fill=(120, 80, 40))
    d.ellipse([x + w - 40, y + 8, x + w - 16, y + 32], fill=(255, 220, 120))


def draw_map(d, x, y, w, h):
    """A stylised world map with numbered pins for the lead & card stories."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.polygon([(x + 18, y + 30), (x + 52, y + 18), (x + 88, y + 26),
               (x + 80, y + 48), (x + 48, y + 54), (x + 22, y + 46)],
              fill=(214, 196, 150))
    d.polygon([(x + 62, y + 62), (x + 84, y + 58), (x + 92, y + 80),
               (x + 78, y + 100), (x + 64, y + 84)], fill=(214, 196, 150))
    d.polygon([(x + 128, y + 26), (x + 158, y + 18), (x + 176, y + 30),
               (x + 162, y + 44), (x + 136, y + 42)], fill=(214, 196, 150))
    d.polygon([(x + 140, y + 52), (x + 168, y + 48), (x + 178, y + 70),
               (x + 162, y + 94), (x + 146, y + 76)], fill=(214, 196, 150))
    d.polygon([(x + 184, y + 24), (x + 252, y + 16), (x + 282, y + 32),
               (x + 268, y + 58), (x + 220, y + 62), (x + 192, y + 48)],
              fill=(214, 196, 150))
    d.polygon([(x + 262, y + 92), (x + 282, y + 88), (x + 288, y + 102),
               (x + 272, y + 108), (x + 260, y + 102)], fill=(214, 196, 150))
    pins = {1: (150, 34), 2: (168, 40), 3: (72, 78), 4: (156, 26),
            5: (58, 40), 6: (252, 36), 7: (262, 58), 8: (100, 66),
            9: (36, 42), 10: (282, 100), 12: (150, 88), 13: (140, 58)}
    for n, (px, py) in pins.items():
        d.ellipse([x + px - 7, y + py - 7, x + px + 7, y + py + 7],
                  fill=RED, outline=WHITE, width=1)
        d.text((x + px - 3, y + py - 6), str(n), font=F_NUM, fill=WHITE)
    d.text((x + 10, y + h - 34), "Pins 1-13 mark the lead & card stories.",
           font=F_SMALL, fill=(200, 205, 215))
    d.text((x + 10, y + h - 20), "11 · SPACE — MERCURY, ABOVE",
           font=F_SMALL_B, fill=GOLD)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead.
    d.rectangle([0, 0, W, 6], fill=RED)
    d.text((8, 12), "THE WORLD IN ONE DAY", font=F_KICK, fill=RED)
    right = "33 STORIES · 7 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((W - 8 - d.textlength(right, font=F_KICK_SM), 14), right,
           font=F_KICK_SM, fill=GREY)
    d.text((8, 30), "Saturday 21 November 2026", font=F_SERIF, fill=NAVY)
    d.text((8, 92), "COP31 runs into overtime in Antalya · Three missiles "
           "shot down over Riyadh · Magnitude 6.7 quake shakes Peru",
           font=F_SERIF_SM, fill=GREY)
    d.line([8, 114, W - 8, 114], fill=NAVY, width=2)

    # --- Timeline ribbon: the day's arc, early hours to all day.
    d.text((8, 120), "EARLY HOURS — RIYADH", font=F_SMALL_B, fill=NAVY)
    d.text((330, 120), "→  00:09 UTC — JUNÍN, PERU", font=F_SMALL_B, fill=TEAL)
    d.text((620, 120), "→  ALL DAY — ANTALYA, COP31 OVERTIME", font=F_SMALL_B,
           fill=RED)

    # --- Stat bar, uneven cells.
    stats = [
        ("5", "Houthi missiles down over Saudi", RED, 148),
        ("6.7", "Peru quake, 108 km deep", NAVY, 168),
        ("$58,983", "bitcoin on Saturday", NAVY, 196),
        ("1:34.041", "Russell, Las Vegas practice", NAVY, 168),
        ("124*", "Rahul v New Zealand", NAVY, 148),
        ("$7.25bn", "Roundup settlement", NAVY, 180),
    ]
    sx = 8
    for num, label, col, w in stats:
        d.line([sx, 138, sx, 188], fill=(200, 190, 170), width=1)
        d.text((sx + 8, 136), num, font=F_STAT, fill=col)
        ly = 166
        for line in wrap(d, label, F_STAT_L, w - 14, 2):
            d.text((sx + 8, ly), line, font=F_STAT_L, fill=GREY)
            ly += 12
        sx += w
    d.line([8, 194, W - 8, 194], fill=(200, 190, 170), width=1)

    # --- Region bar.
    regions = [("EUROPE 7", 7, RED), ("ASIA 4", 4, TEAL),
               ("MIDEAST 6", 6, (180, 140, 0)), ("AFRICA 2", 2, GREEN),
               ("AMERICAS 8", 8, BLUE), ("OCEANIA 4", 4, PURPLE),
               ("GLOBAL 2", 2, GREY)]
    rx = 8
    total = sum(n for _, n, _ in regions)
    for name, n, col in regions:
        w = int(1008 * n / total)
        d.rectangle([rx, 198, rx + w - 2, 212], fill=col)
        d.text((rx + 5, 201), name, font=F_SMALL_B, fill=WHITE)
        rx += w

    # --- Leads: one wide, one mid, one narrow.
    leads = [
        (8, 404, art_cop31, "1 · ANTALYA, TÜRKIYE · CLIMATE",
         "COP31 runs into overtime with no deal in sight",
         "Day 13, a day late; a third draft is due on Saturday, with "
         "fossil fuels still unmentioned. (AFP, AP)"),
        (420, 296, art_riyadh, "2 · RIYADH · DEFENCE",
         "Three Houthi missiles shot down over Riyadh",
         "Early on Saturday, the third night of alerts in a row. "
         "(Reuters, AFP)"),
        (724, 292, art_quake, "3 · JUNÍN, PERU · EARTHQUAKE",
         "M6.7 earthquake shakes central Peru",
         "00:09 UTC, 108 km deep; felt in Lima. IGP: no deaths reported. "
         "(USGS, IGP)"),
    ]
    for x, w, art, tag, head, body in leads:
        y0 = 218
        art(d, x, y0, w, 80)
        d.text((x, y0 + 86), tag, font=F_TAG, fill=RED)
        ly = y0 + 104
        for line in wrap(d, head, F_HEAD, w - 4, 2):
            d.text((x, ly), line, font=F_HEAD, fill=NAVY)
            ly += 24
        for line in wrap(d, body, F_BODY, w - 4, 2):
            d.text((x, ly), line, font=F_BODY, fill=GREY)
            ly += 16

    # --- Card rows: 4, then 3, then 3, all with uneven widths.
    rows = [
        (402, [
            (8, 250, art_kryvyi, "4 · KRYVYI RIH · WAR",
             "Russian double strike hits Kryvyi Rih",
             "12 killed, 42 hurt; a boy and a medic among the dead. "
             "(Kyiv Post, AP)", RED),
            (266, 300, art_capitol, "5 · WASHINGTON · TRADE",
             "Trump vows tax on data centres abroad",
             "'Tremendous' penalty, no details yet; upbeat on Putin talks. "
             "(AP)", NAVY),
            (574, 200, art_flags_asia, "6 · CHINA · JAPAN",
             "Japan told to 'correct' Taiwan words",
             "Tokyo says its stance is unchanged. (Reuters)", NAVY),
            (782, 234, art_plane, "7 · DAVAO · AVIATION",
             "Air Niugini 767 lands safely in Davao",
             "Engine fire alert; all 146 on board safe. (AP, CAAP)", NAVY),
        ]),
        (530, [
            (8, 340, art_chart, "8 · MARKETS · CRYPTO",
             "Bitcoin trades below $59,000 on Saturday",
             "$58,983, down 3.9% in 24 hours; ether $1,625. (CoinGecko)",
             RED),
            (356, 300, art_racecar, "9 · LAS VEGAS · FORMULA 1",
             "Russell fastest in final Las Vegas GP practice",
             "1:34.041; Verstappen sent to stewards after contact. "
             "(Formula 1)", NAVY),
            (664, 352, art_cricket, "10 · WELLINGTON · CRICKET",
             "Rahul hits a century in Wellington",
             "124* as India reach 344 for 2 at tea, replying to 368. (AFP)",
             GREEN),
        ]),
        (658, [
            (8, 240, art_space, "11 · MERCURY · SPACE",
             "BepiColombo reaches Mercury",
             "Thrusters fire at 19:24 CET tonight for orbit insertion. "
             "(ESA)", NAVY),
            (256, 330, art_ballot, "12 · SOUTH AFRICA · POLITICS",
             "ANC scrambles after its worst result",
             "Wins 31%, its worst since 1994. (BBC)", RED),
            (594, 422, art_boat, "13 · BAYELSA, NIGERIA · DISASTER",
             "Funeral boat capsizes in Bayelsa",
             "At least 4 dead after the boat overturns. (Reuters)", GREEN),
        ]),
    ]
    for y0, cards in rows:
        for x, w, art, tag, head, body, col in cards:
            art(d, x, y0, w, 40)
            card(d, x, y0 + 40, w, 88, tag, head, body, col)

    # --- Map + also-list.
    yM = 790
    d.text((8, yM), "WHERE IT HAPPENED", font=F_KICK, fill=NAVY)
    draw_map(d, 8, yM + 16, 296, 130)
    d.text((312, yM), "ALSO ON SATURDAY 21 NOVEMBER 2026 — 20 MORE STORIES",
           font=F_KICK, fill=RED)
    briefs = [
        (14, "Iraqi forces retake Jurf al-Sakhar, held since 2014."),
        (15, "Missouri judge approves $7.25bn Roundup settlement."),
        (16, "Medvedev meets Zverev tonight, Turin tennis semi. (ATP)"),
        (17, "Strikes hit Hodeidah port; Houthis warn airlines."),
        (18, "Youth march across Europe — rallies in 400 cities. (AFP)"),
        (19, "LA fire suspect found guilty at retrial; the fire killed 12."),
        (20, "Train derails in South Korea — 5 of 21 freight cars, no injuries."),
        (21, "Iran: uranium stock stays in the country; minister still seeks a 'fair solution'."),
        (22, "Australia and China agree to AI talks; Albanese ends an 11-day trip."),
        (23, "Iran says it shot down a US drone over the Strait of Hormuz."),
        (24, "Zelensky: Crimea bridge 'will not stay'; warns of more double-tap strikes."),
        (25, "Rutte flies to Warsaw for NATO talks."),
        (26, "Panama threatens to block climate deal."),
        (27, "EU warns COP31 risks ending as a 'fossil summit'."),
        (28, "Indonesia PLN signs clean-power deals."),
        (29, "Yemen Houthis threaten Jeddah and Red Sea ports."),
        (30, "Washington: Vance says Iran strikes were Trump's decision."),
        (31, "Texas execution of a man of 70 takes 63 minutes."),
        (32, "Taipei budget and cash payout passed."),
        (33, "Melbourne: Cummins keeps the Australian captaincy."),
    ]
    for cx, items in [(312, briefs[:10]), (668, briefs[10:])]:
        ly = yM + 18
        for n, text in items:
            num = f"{n}  "
            d.text((cx, ly), num, font=F_BRIEF_B, fill=RED)
            tw = d.textlength(num, font=F_BRIEF_B)
            line = one_line(d, text, F_BRIEF, 348 - tw)
            d.text((cx + tw, ly), line, font=F_BRIEF, fill=INK)
            ly += 12

    # --- Date check.
    d.rectangle([8, 946, W - 8, 992], outline=RED, width=2)
    d.text((16, 952), "DATE CHECK", font=F_SMALL_B, fill=RED)
    dc = ("Left out as earlier news — Fri 20 Nov: ICJ Myanmar verdict; Wall "
          "Street correction; Kyiv bridges barrage; missile in Poland; UK-EU "
          "deal; Akvan landfall; Virginia measles death. Thu 19 Nov: "
          "Shenzhen summit; Anthropic IPO; PIF Tower strike; GTA VI launch; "
          "Van Gogh sale; Fiona the hippo. 18 Nov: Voyager 1's light-day.")
    ly = 952
    for line in wrap(d, dc, F_SMALL, W - 8 - 16 - 100, 3):
        d.text((116, ly), line, font=F_SMALL, fill=INK)
        ly += 13

    # --- Footer.
    foot = ("Every story here happened, or was first reported, on Saturday 21 "
            "November 2026. Sources named beside each story · Original drawings")
    d.text(((W - d.textlength(foot, font=F_SMALL)) / 2, 998), foot,
           font=F_SMALL, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
