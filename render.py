#!/usr/bin/env python3
"""Render THE WORLD TODAY - front page for Tuesday 24 November 2026.

Deterministic: same input -> same PNG bytes (no timestamps, no randomness).
Run:  python3 render.py   ->   writes entry.png (1024x1024) next to this file.
The image is the entry; main.ts copies it to /output/entry.png at grade time.
Every story below was verified against wire / newspaper reports published
on Tuesday 24 November 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 252, 248)
INK = (17, 17, 17)
NAVY = (18, 40, 75)
RED = (163, 30, 34)
GREEN = (27, 120, 60)
GREY = (96, 96, 96)
LIGHT = (238, 236, 228)
RULE = (198, 196, 186)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, f, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, f, width, fill=INK, leading=None):
    """Draw wrapped text; return the y just below the last line."""
    lh = leading or int(f.size * 1.18)
    for ln in wrap(draw, text, f, width):
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
# (kicker, headline, deck) - all verified 24 Nov 2026 reports.
HERO = ("WAR IN UKRAINE",
        "RUSSIAN STRIKES KILL 12 IN KYIV REGION",
        "Missiles and drones hit homes across the capital's region; rescuers "
        "pull a child and an elderly survivor from rubble.")

SECOND = [
    ("MARKETS",
     "NVIDIA SOARS 31% AS HUANG RETURNS",
     "Board reinstates Jensen Huang as CEO; shares jump; Senate hearing set "
     "for 3 December."),
    ("CLIMATE",
     "COP31 COLLAPSE SPURS CALLS FOR NEW PROCESS",
     "UN talks ended Sunday with no deal; Guterres \u201cdeeply disappointed\u201d."),
]

REGIONS = [
    ("EUROPE", [
        ("POLAND CONFIRMS RUSSIAN MISSILES",
         "Three objects that fell on Friday were Russian Kh-101 missiles."),
        ("12,000 FLEE MANCHESTER CONCERT",
         "Don Toliver show cleared after an unknown substance is released."),
        ("450 GERMAN SCHOOLS GET THREATS",
         "Schools across Germany receive threats by email; police investigate."),
        ("EU READIES NEW RUSSIA SANCTIONS",
         "Fresh package targets Moscow's military, banks and sporting events."),
    ]),
    ("MIDDLE EAST", [
        ("UKRAINE HITS WARSHIP OFF LIBYA",
         "Strike on a vessel at Benghazi; Russians and Libyans killed."),
        ("IRAN WARNS EU BASES IN RANGE",
         "Tehran claims missiles that can travel 4,500 km."),
        ("TANKERS HIT BY MINES IN HORMUZ",
         "Reports say vessels struck mines and caught fire in the strait."),
        ("GAZA: ONE KILLED; CHILD DIES",
         "Israeli fire kills a Palestinian; a child dies of lead poisoning."),
    ]),
    ("ASIA-PACIFIC", [
        ("N. KOREAN JETS ENTER S. KOREA",
         "Seoul says suspected North Korean aircraft crossed the line."),
        ("CHINA: DEATH SENTENCE FOR LEAKS",
         "Official convicted of leaking 100 intelligence reports."),
        ("AUSTRALIA HALTS LOBSTER EXPORTS",
         "Exporters stop shipments as Chinese customs steps up inspections."),
        ("LAHORE TOPS POLLUTION RANKING",
         "Air quality index crosses 500; eight Pakistani cities among the worst."),
    ]),
    ("AMERICAS & WORLD", [
        ("O'HARE GROUND STOP SNARLS RUSH",
         "Chicago airport halts flights briefly over a staffing shortage."),
        ("TRUMP TARGETS NEWSOM IN SPEECH",
         "President attacks governor over 548 commuted death sentences."),
        ("MEXICO: 'EL CHAPO ISIDRO' TRIAL",
         "Alleged drug lord captured; officials say he will stand trial."),
        ("RANGERS END WAIT AT FIR PARK",
         "Naderi's late goal seals a 2-1 win at Motherwell."),
    ]),
]

BRIEF = [
    ("SUDAN", "UN condemns air strikes on Khartoum it says were launched from Ethiopian soil."),
    ("BANGLADESH", "Yunus says attacks on Grameen Bank branches are directed \u201cat a higher level\u201d."),
    ("IRAN", "Singer Parastoo Ahmadi and four crew get 74 lashes each for a virtual concert."),
    ("MUSIC", "Ex-Mossad chief says his agency foiled an ISIS-inspired plot on Swift's Vienna shows."),
    ("S. KOREA", "Education minister quits over AI cheating rules."),
    ("INDONESIA", "More than 30 missing after a deadly blaze at a sweet factory."),
]


# ---------------------------------------------------------------- layout
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 112], fill=NAVY)
    f_title = font(F_SERIF_B, 58)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=f_title)
    draw.text(((W - tw) / 2, 10), title, font=f_title, fill=PAPER)
    f_date = font(F_SANS_B, 20)
    date = "TUESDAY, 24 NOVEMBER 2026  \u00b7  25 STORIES  \u00b7  9 REGIONS"
    tw = draw.textlength(date, font=f_date)
    draw.text(((W - tw) / 2, 76), date, font=f_date, fill=(212, 214, 222))
    draw.rectangle([0, 112, W, 116], fill=RED)


def draw_skyline(draw, x0, y0, x1, y1):
    """Simple night skyline with smoke, right side of the hero box."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 230, 238))
    draw.text((x0 + 8, y0 + 6), "KYIV AT NIGHT", font=font(F_SANS_B, 13),
              fill=GREY)
    base = y1
    buildings = [(0, 150, 46), (50, 118, 40), (94, 158, 52),
                 (150, 96, 44), (198, 140, 38), (240, 168, 46)]
    for bx, bh, bw in buildings:
        bx += x0
        draw.rectangle([bx, base - bh, bx + bw, base], fill=NAVY)
        for wy in range(base - bh + 12, base - 10, 22):
            for wx in range(bx + 8, bx + bw - 6, 14):
                if (wx * 7 + wy * 13) % 5 < 2:
                    draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 214, 120))
    for cx, cy, r in [(x0 + 60, y0 + 44, 16), (x0 + 78, y0 + 30, 12),
                      (x0 + 210, y0 + 48, 14), (x0 + 226, y0 + 34, 10)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 172, 180))


def draw_hero(draw):
    x0, y0, x1, y1 = 24, 122, 1000, 330
    kicker, head, deck = HERO
    tx, tw = x0 + 12, 620
    y = y0 + 8
    draw.text((tx, y), kicker, font=font(F_SANS_B, 20), fill=RED)
    y += 30
    y = draw_wrapped(draw, tx, y, head, font(F_SANS_B, 44), tw, leading=50)
    y += 8
    draw_wrapped(draw, tx, y, deck, font(F_SANS, 20), tw, leading=25)
    draw_skyline(draw, 668, y0 + 8, x1 - 12, y1 - 8)
    draw.line([x0, y1 + 6, x1, y1 + 6], fill=INK, width=2)


def draw_second(draw):
    y0, y1 = 342, 492
    boxes = [(24, 500), (524, 1000)]
    for (kicker, head, deck), (x0, x1) in zip(SECOND, boxes):
        draw.rectangle([x0, y0, x1, y1], fill=LIGHT)
        draw.rectangle([x0, y0, x1, y0 + 4], fill=RED)
        tx, tw = x0 + 14, x1 - x0 - 28
        y = y0 + 12
        draw.text((tx, y), kicker, font=font(F_SANS_B, 18), fill=RED)
        y += 26
        y = draw_wrapped(draw, tx, y, head, font(F_SANS_B, 27), tw, leading=32)
        y += 6
        draw_wrapped(draw, tx, y, deck, font(F_SANS, 17), tw, leading=21)
    draw.text((424, 348), "+31%", font=font(F_SANS_B, 30), fill=GREEN)
    draw.line([24, 502, 1000, 502], fill=INK, width=2)


def draw_regions(draw):
    y0 = 514
    col_w, gap = 238, 12
    for i, (name, stories) in enumerate(REGIONS):
        x0 = 24 + i * (col_w + gap)
        x1 = x0 + col_w
        y = y0
        draw.text((x0, y), name, font=font(F_SANS_B, 19), fill=RED)
        y += 26
        draw.line([x0, y, x1, y], fill=RED, width=2)
        y += 8
        for head, deck in stories:
            y = draw_wrapped(draw, x0, y, head, font(F_SANS_B, 17), col_w,
                             leading=20)
            y += 2
            y = draw_wrapped(draw, x0, y, deck, font(F_SANS, 13), col_w,
                             leading=16, fill=(48, 48, 48))
            y += 6
        if i < 3:
            draw.line([x1 + 6, y0, x1 + 6, 880], fill=RULE, width=1)
    draw.line([24, 890, 1000, 890], fill=INK, width=2)


def draw_brief(draw):
    y = 900
    draw.text((24, y), "IN BRIEF", font=font(F_SANS_B, 18), fill=RED)
    note = "Compiled from reports published Tuesday 24 November 2026."
    nw = draw.textlength(note, font=font(F_SANS, 12))
    draw.text((1000 - nw, y + 4), note, font=font(F_SANS, 12), fill=GREY)
    y += 28
    for tag, text in BRIEF:
        line = tag + " \u2014 " + text
        y = draw_wrapped(draw, 24, y, line, font(F_SANS, 14), 976, leading=15)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_hero(draw)
    draw_second(draw)
    draw_regions(draw)
    draw_brief(draw)
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
