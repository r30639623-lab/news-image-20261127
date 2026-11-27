#!/usr/bin/env python3
"""Build News 27 v5 — v4 with the markets strip fixed to fit (1024x1024).
Written from scratch for v4. No old build code was read.
Content: same 35 verified stories as v3 (3 features + 10 cards + 22 map list).
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/home/hatch/workspace/makefun/news-entry-20261127/news-v5.png"

# ---- palette: premium navy + gold on cream ----
PAPER = (247, 242, 231)
NAVY = (15, 42, 68)
NAVY_DK = (8, 28, 48)
GOLD = (201, 162, 39)
GOLD_DK = (158, 124, 22)
INK = (26, 26, 26)
MUTED = (90, 86, 76)
RED = (140, 29, 24)          # tiny accent only (CONFLICT tags)
SEA = (216, 228, 236)
LAND = (238, 229, 208)
LINE = (15, 42, 68)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

f_mast = F(SERIF_B, 62)
f_date = F(SERIF_B, 25)
f_ed = F(SANS_B, 11)
f_num = F(SERIF_B, 28)
f_numcap = F(SANS, 9)
f_region = F(SANS_B, 11)
f_fhead = F(SANS_B, 11)
f_ftitle = F(SERIF_B, 21)
f_body = F(SANS, 12)
f_src = F(SERIF_I, 10)
f_cardhead = F(SANS_B, 10)
f_ctitle = F(SERIF_B, 13)
f_cbody = F(SANS, 10)
f_quote = F(SERIF_I, 15)
f_qattr = F(SANS_B, 10)
f_mkt = F(SANS_B, 12)
f_maph = F(SERIF_B, 19)
f_list = F(SANS, 10)
f_listb = F(SANS_B, 10)
f_dc = F(SANS, 10)
f_foot = F(SANS, 10)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def tracked(draw, cx, y, text, font, fill, tracking=2):
    """Draw centred text with letter tracking."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, wd in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += wd + tracking

def hline(y, fill, width=1, x0=12, x1=1012):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)

# ============ MASTHEAD ============
tracked(d, 512, 10, "THE WORLD TODAY", f_mast, NAVY, tracking=3)
hline(84, GOLD, 2)
hline(88, NAVY, 1)
d.text((512, 96), "FRIDAY, 27 NOVEMBER 2026", font=f_date, fill=NAVY, anchor="ma")
tracked(d, 512, 126, "FRIDAY EDITION  ·  35 STORIES FROM 7 REGIONS  ·  COMPILED FROM WIRE REPORTS",
        f_ed, GOLD_DK, tracking=1)

# ============ NUMBERS STRIP ============
NUMS = [
    ("2", "Italians killed in\nKuwait drone attack"),
    ("168", "dead in Hong Kong\nestate fire"),
    ("13", "dead in Indonesia\nmine flood"),
    ("12,000", "Congo Ebola\ncases passed"),
    ("800m", "floating bridge\nin China drill"),
    ("1", "seat short of NZ\nmajority"),
]
nx, ny, nw, nh, gap = 12, 146, 162, 56, 8
for i, (n, cap) in enumerate(NUMS):
    x0 = nx + i * (nw + gap)
    d.rectangle([x0, ny, x0 + nw, ny + nh], outline=NAVY, width=1)
    d.line([(x0, ny), (x0 + nw, ny)], fill=GOLD, width=3)
    d.text((x0 + nw / 2, ny + 2), n, font=f_num, fill=NAVY, anchor="ma")
    for j, ln in enumerate(cap.split("\n")):
        d.text((x0 + nw / 2, ny + 33 + j * 11), ln, font=f_numcap, fill=INK, anchor="ma")

tracked(d, 512, 202, "AMERICAS 8  ·  EUROPE 6  ·  MIDDLE EAST 4  ·  ASIA 5  ·  AFRICA 5  ·  OCEANIA 5  ·  GLOBAL 2",
        f_region, NAVY, tracking=1)

# ============ FEATURE ILLUSTRATIONS ============
def grad_sky(x0, y0, x1, y1, top, bot):
    for i in range(y1 - y0):
        t = i / max(1, y1 - y0 - 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)

def illo_f1(x0, y0, x1, y1):
    grad_sky(x0, y0, x1, y1, (10, 26, 46), (30, 58, 92))
    d.ellipse([x1 - 52, y0 + 6, x1 - 30, y0 + 28], fill=(232, 226, 196))
    # skyline with lit windows
    import random
    rnd = random.Random(7)
    bx = x0
    while bx < x1 - 20:
        bw, bh = rnd.randint(16, 30), rnd.randint(14, 34)
        d.rectangle([bx, y1 - bh, bx + bw, y1], fill=(6, 16, 30))
        for wy in range(y1 - bh + 4, y1 - 3, 7):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if rnd.random() < 0.45:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=GOLD)
        bx += bw + 3
    # drone with lights
    cx, cy = (x0 + x1) // 2 - 30, y0 + 26
    d.ellipse([cx - 12, cy - 4, cx + 12, cy + 4], fill=(20, 20, 20))
    d.line([(cx - 20, cy - 6), (cx + 20, cy - 6)], fill=(200, 200, 200), width=2)
    d.ellipse([cx - 21, cy - 9, cx - 15, cy - 3], fill=(255, 80, 60))
    d.ellipse([cx + 15, cy - 9, cx + 21, cy - 3], fill=(120, 255, 120))
    # explosion starburst
    ex, ey = (x0 + x1) // 2 + 52, y0 + 30
    for r, col in ((22, (255, 120, 40)), (15, (255, 180, 60)), (8, (255, 230, 140))):
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
    for a in range(0, 360, 30):
        import math
        r1, r2 = 20, 25
        x_1, y_1 = ex + r1 * math.cos(math.radians(a)), ey + r1 * math.sin(math.radians(a))
        x_2, y_2 = ex + r2 * math.cos(math.radians(a)), ey + r2 * math.sin(math.radians(a))
        d.line([(x_1, y_1), (x_2, y_2)], fill=(255, 160, 50), width=3)
    # smoke
    for sx, sy, sr in ((ex - 34, ey - 12, 9), (ex + 36, ey - 6, 8), (ex - 26, ey + 16, 7)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 118, 112))

def illo_f2(x0, y0, x1, y1):
    grad_sky(x0, y0, x1, y1, (232, 170, 90), (250, 226, 180))
    d.ellipse([x0 + 18, y0 + 8, x0 + 44, y0 + 34], fill=(255, 214, 120))
    # coastline hills
    d.polygon([(x1 - 90, y1), (x1 - 60, y0 + 34), (x1 - 20, y1)], fill=(120, 130, 90))
    d.polygon([(x1 - 130, y1), (x1 - 105, y0 + 44), (x1 - 80, y1)], fill=(100, 112, 78))
    # sea
    sy = y0 + 26
    for i in range(y1 - sy):
        t = i / max(1, y1 - sy - 1)
        c = tuple(int((38, 92, 130)[k] + ((16, 52, 84)[k] - (38, 92, 130)[k]) * t) for k in range(3))
        d.line([(x0, sy + i), (x1, sy + i)], fill=c)
    # waves
    for wy in (sy + 6, sy + 16, sy + 25):
        for wx in range(x0 + 4, x1 - 8, 18):
            d.arc([wx, wy, wx + 14, wy + 8], 180, 360, fill=(220, 235, 245), width=1)
    # floating bridge: 5 barges
    bx = x0 + 22
    for i in range(5):
        bw = 46
        d.rectangle([bx, sy + 2, bx + bw, sy + 12], fill=(52, 52, 52))
        d.rectangle([bx + 6, sy - 4, bx + 18, sy + 2], fill=(70, 70, 70))
        d.rectangle([bx + 26, sy - 2, bx + 40, sy + 2], fill=(84, 84, 84))
        d.line([(bx, sy + 12), (bx + bw, sy + 12)], fill=GOLD, width=2)
        bx += bw + 6
    d.line([(x0 + 22, sy + 7), (bx - 6, sy + 7)], fill=(255, 255, 255), width=1)

def illo_f3(x0, y0, x1, y1):
    grad_sky(x0, y0, x1, y1, (8, 24, 44), (24, 48, 80))
    # city lights row
    import random
    rnd = random.Random(11)
    for lx in range(x0 + 4, x1 - 4, 9):
        if rnd.random() < 0.6:
            d.rectangle([lx, y1 - 4, lx + 4, y1 - 1], fill=GOLD)
    # transmission towers
    def tower(tx):
        d.line([(tx, y1 - 4), (tx, y0 + 12)], fill=(180, 190, 200), width=2)
        d.line([(tx - 16, y0 + 22), (tx + 16, y0 + 22)], fill=(180, 190, 200), width=2)
        d.line([(tx - 11, y0 + 32), (tx + 11, y0 + 32)], fill=(180, 190, 200), width=2)
        d.line([(tx - 16, y0 + 22), (tx, y0 + 12)], fill=(160, 170, 182), width=1)
        d.line([(tx + 16, y0 + 22), (tx, y0 + 12)], fill=(160, 170, 182), width=1)
        d.line([(tx - 11, y0 + 32), (tx, y0 + 22)], fill=(160, 170, 182), width=1)
        d.line([(tx + 11, y0 + 32), (tx, y0 + 22)], fill=(160, 170, 182), width=1)
    tower(x0 + 42)
    tower(x1 - 42)
    # cables sagging between towers
    for cy in (y0 + 24, y0 + 34):
        d.arc([x0 + 42, cy - 8, x1 - 42, cy + 14], 20, 160, fill=(140, 150, 160), width=1)
    # lightning bolt
    bx, by = (x0 + x1) // 2, y0 + 8
    d.polygon([(bx + 6, by), (bx - 8, by + 26), (bx + 1, by + 26), (bx - 6, by + 48),
               (bx + 10, by + 20), (bx + 1, by + 20)], fill=(255, 214, 60))

# ============ FEATURES ============
FEATS = [
    ("1", "CONFLICT", "KUWAIT CITY",
     "Kuwait drone attack kills two Italians",
     "Kuwait says it intercepted a drone assault; two Italian technicians died and four were hurt by falling debris. Rome blames Iran; Tehran denies any role.",
     "— Reuters", illo_f1, True),
    ("2", "POLITICS", "TAIPEI",
     "China tests new Taiwan landing tactics",
     "Beijing runs weeks-long drills off its coast, linking civilian ships into an 800m floating bridge in Dacheng Bay, 280km from Taiwan. Satellite images show it forming and breaking apart.",
     "— Reuters", illo_f2, False),
    ("3", "CONFLICT", "KYIV",
     "Zelensky warns of mass attack on power grid",
     "Russia is preparing another mass strike on energy sites, Kyiv says, after 113 drones and ballistic missiles hit overnight. Crews are restoring power in six regions as winter nears.",
     "— AP", illo_f3, False),
]
fx, fy, fw, fh, fgap = 12, 218, 326, 196, 8
for i, (num, cat, city, title, body, src, illo, dropcap) in enumerate(FEATS):
    x0 = fx + i * (fw + fgap)
    d.rectangle([x0, fy, x0 + fw, fy + 17], fill=NAVY)
    d.line([(x0, fy), (x0 + fw, fy)], fill=GOLD, width=2)
    d.text((x0 + 6, fy + 3), f"{num}  {cat}", font=f_fhead, fill=GOLD)
    d.text((x0 + fw - 6, fy + 3), city, font=f_fhead, fill=(255, 255, 255), anchor="ra")
    ty = fy + 21
    for ln in wrap(title, f_ftitle, fw - 12):
        d.text((x0 + 6, ty), ln, font=f_ftitle, fill=INK)
        ty += 24
    by = ty + 2
    if dropcap:
        d.text((x0 + 6, by - 4), "K", font=F(SERIF_B, 38), fill=NAVY)
        rest = body[1:]
        lines = wrap(rest, f_body, fw - 12 - 30)
        for j, ln in enumerate(lines[:4]):
            d.text((x0 + 36 if j < 3 else x0 + 6, by + j * 15), ln, font=f_body, fill=INK)
        by = by + min(4, len(lines)) * 15
    else:
        for ln in wrap(body, f_body, fw - 12)[:4]:
            d.text((x0 + 6, by), ln, font=f_body, fill=INK)
            by += 15
    d.text((x0 + 6, fy + fh - 66), src, font=f_src, fill=MUTED)
    illo(x0, fy + fh - 54, x0 + fw, fy + fh)

# ============ PULL QUOTE BAND ============
qy = fy + fh + 8
d.rectangle([12, qy, 1012, qy + 40], outline=GOLD, width=1)
d.rectangle([12, qy, 17, qy + 40], fill=GOLD)
d.text((28, qy + 6), "\u201cWe will rebuild what is ours and retaliate against every Russian strike.\u201d",
       font=f_quote, fill=NAVY)
d.text((28, qy + 25), "— VOLODYMYR ZELENSKYY, IN HIS NIGHTLY ADDRESS, 26 NOVEMBER 2026 (VIA REUTERS)",
       font=f_qattr, fill=MUTED)

# ============ CARDS ============
CARDS = [
    ("4", "POLITICS", "WASHINGTON", "Trump widens tariffs to 14 partners",
     "Washington proposes duties of 20-40% on 14 partners to fight excess capacity. China faces the top rate, 20%.", "— Reuters", "pol"),
    ("5", "DISASTER", "HONG KONG", "Hong Kong marks year since fire killed 168",
     "Mourners mark the first anniversary of the Wang Fuk Court blaze; 168 died. An Oct 29 report found wide safety failures.", "— Reuters", "dis"),
    ("6", "POLITICS", "PYONGYANG", "Kim orders more tactical nukes",
     "Kim tours nuclear plants and calls tactical deployment \u2018important and urgent\u2019. He says the arsenal \u2018is now a reality\u2019.", "— Reuters", "pol"),
    ("7", "POLITICS", "BRUSSELS", "EU budget talks end without a deal",
     "Leaders end a Brussels summit with no deal on the \u20ac1.78tn 2028-34 budget. Talks resume Dec 17-18.", "— Reuters", "pol"),
    ("8", "DISASTER", "JAKARTA", "Indonesia mine flood toll rises to 13",
     "Thirteen miners are dead and 13 still missing after a gold-mine flood in Bogor. Rain halted the search of two 100m shafts.", "— Reuters", "dis"),
    ("9", "ECONOMY", "BRASILIA", "Trabuco to take Brazil finance job",
     "Bradesco chairman Luiz Carlos Trabuco, 75, agrees to be finance minister as Lula starts a fourth term in January.", "— Reuters", "eco"),
    ("10", "HEALTH", "KINSHASA", "Congo Ebola outbreak passes 12,000",
     "Cases top 12,021 and nearly half have died. Fighting near Bunia blocks teams as responders pull out.", "— AP", "hea"),
    ("11", "POLITICS", "PARIS", "Depardieu to face rape trial",
     "Depardieu will stand trial for rape over a 2018 assault on Charlotte Arnould. He denies it and faces 15-20 years.", "— Reuters", "pol"),
    ("12", "MARKETS", "FRANKFURT", "Audi profit slumps on weak China sales",
     "Audi\u2019s Q3 net profit fell 87% to \u20ac95m as China sales slid 24.5%. It cut its 2026 revenue outlook to \u20ac55-59bn.", "— Reuters", "eco"),
    ("13", "AVIATION", "SYDNEY", "Qantas and Air NZ jets in near-miss",
     "A Qantas jet aborted its landing as an Air NZ plane crossed the runway, about 90m up. The ATSB opened a probe.", "— ATSB", "avi"),
]

def icon(kind, x, y):
    if kind == "pol":
        for i in range(3):
            d.rectangle([x + i * 6, y + 8 - i * 2, x + i * 6 + 4, y + 10], fill=NAVY)
        d.line([(x - 1, y + 10), (x + 17, y + 10)], fill=NAVY, width=1)
    elif kind == "dis":
        d.polygon([(x + 8, y), (x + 16, y + 12), (x, y + 12)], outline=NAVY, width=1)
        d.text((x + 6, y + 3), "!", font=F(SANS_B, 9), fill=NAVY)
    elif kind == "eco":
        for i, h in enumerate((4, 7, 10)):
            d.rectangle([x + i * 6, y + 11 - h, x + i * 6 + 4, y + 11], fill=NAVY)
    elif kind == "hea":
        d.rectangle([x + 6, y, x + 10, y + 12], fill=NAVY)
        d.rectangle([x + 2, y + 4, x + 14, y + 8], fill=NAVY)
    elif kind == "avi":
        d.polygon([(x + 2, y + 6), (x + 16, y + 6), (x + 9, y + 2)], fill=NAVY)
        d.line([(x + 9, y + 2), (x + 9, y + 11)], fill=NAVY, width=2)

cw, ch, cgap = 193, 126, 8
cx0, cy0 = 12, 468
for idx, (num, cat, city, title, body, src, kind) in enumerate(CARDS):
    r, c = divmod(idx, 5)
    x0 = cx0 + c * (cw + cgap)
    y0 = cy0 + r * (ch + cgap)
    d.rectangle([x0, y0, x0 + cw, y0 + ch], outline=NAVY, width=1)
    d.line([(x0, y0), (x0 + cw, y0)], fill=GOLD, width=2)
    d.rectangle([x0, y0 + 2, x0 + cw, y0 + 16], fill=NAVY)
    d.text((x0 + 5, y0 + 4), f"{num}  {cat}", font=f_cardhead, fill=GOLD)
    d.text((x0 + cw - 5, y0 + 4), city, font=f_cardhead, fill=(255, 255, 255), anchor="ra")
    ty = y0 + 19
    for ln in wrap(title, f_ctitle, cw - 10):
        d.text((x0 + 5, ty), ln, font=f_ctitle, fill=INK)
        ty += 16
    by = ty + 2
    for ln in wrap(body, f_cbody, cw - 10)[:4]:
        d.text((x0 + 5, by), ln, font=f_cbody, fill=INK)
        by += 13
    icon(kind, x0 + 5, y0 + ch - 14)
    d.text((x0 + cw - 5, y0 + ch - 14), src, font=f_src, fill=MUTED, anchor="ra")

# ============ MARKETS STRIP (v5 fix: measure first, fit inside the strip) ============
my = 734
d.rectangle([12, my, 1012, my + 24], fill=NAVY_DK)
d.text((20, my + 6), "MARKETS AT A GLANCE  ·  THU 26 NOV CLOSE", font=f_mkt, fill=GOLD)
f_mkti = F(SANS_B, 11)  # items one point smaller so all four fit with room
ITEMS = (("BRENT", "$95.09", "+0.5%", True), ("GOLD", "$3,570", "-0.5%", False),
         ("BITCOIN", "$60,500", "+0.2%", True), ("WTI", "$83.75", "+2.8%", True))
def item_w(name, val, chg, up):
    arrow = "\u25b2" if up else "\u25bc"
    return (d.textlength(name, font=f_mkti) + 8 + d.textlength(val, font=f_mkti)
            + 6 + d.textlength(arrow + chg, font=f_mkti))
total = sum(item_w(*it) for it in ITEMS)
START_X, END_X = 372, 1004  # right margin 8px inside the strip edge (1012)
gap = (END_X - START_X - total) / (len(ITEMS) - 1)
assert gap >= 8, f"markets strip does not fit: gap {gap:.1f}"
mx = START_X
for name, val, chg, up in ITEMS:
    d.text((mx, my + 6), name, font=f_mkti, fill=(255, 255, 255))
    nw_ = d.textlength(name, font=f_mkti)
    vw = d.textlength(val, font=f_mkti)
    d.text((mx + nw_ + 8, my + 6), val, font=f_mkti, fill=GOLD)
    col = (110, 220, 130) if up else (255, 110, 100)
    d.text((mx + nw_ + 8 + vw + 6, my + 6), ("\u25b2" if up else "\u25bc") + chg, font=f_mkti, fill=col)
    mx += item_w(name, val, chg, up) + gap
print("markets strip: total", round(total, 1), "gap", round(gap, 1), "ends at", round(mx - gap, 1), "<= 1004")

# ============ MAP + LIST ============
d.text((12, 764), "WHERE IT HAPPENED", font=f_maph, fill=NAVY)
hline(786, GOLD, 2)
MAPX, MAPY, MAPW, MAPH = 12, 792, 300, 170
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], outline=GOLD, width=2, fill=SEA)
CONT = {
    "NA": [(20, 26), (40, 14), (70, 8), (105, 12), (120, 26), (108, 38), (92, 44), (96, 54), (78, 50), (60, 58), (40, 52), (24, 40)],
    "SA": [(76, 92), (96, 88), (110, 102), (104, 128), (94, 152), (84, 132), (74, 108)],
    "EU": [(138, 20), (168, 12), (186, 22), (178, 38), (158, 42), (144, 34)],
    "AF": [(138, 56), (166, 54), (184, 64), (182, 92), (168, 116), (152, 98), (140, 74)],
    "AS": [(188, 14), (258, 8), (292, 22), (288, 50), (252, 64), (222, 56), (196, 38)],
    "OC": [(250, 130), (282, 126), (292, 144), (272, 156), (252, 146)],
}
for poly in CONT.values():
    d.polygon([(MAPX + x, MAPY + y) for x, y in poly], fill=LAND, outline=(200, 190, 165))
for lbl, lx, ly in (("AMERICAS", 22, 30), ("EUROPE", 146, 6), ("AFRICA", 146, 88),
                    ("ASIA", 232, 28), ("OCEANIA", 238, 160)):
    d.text((MAPX + lx, MAPY + ly), lbl, font=F(SANS_B, 8), fill=(120, 110, 90))
# (dot_x, dot_y, label_dx, label_dy) — leader lines declutter crowded clusters
MARK = {14: (48, 56, -14, 8), 15: (66, 50, 14, 12), 16: (54, 62, 12, 12), 17: (70, 34, 16, -12),
        18: (64, 24, -4, -16), 19: (238, 56, 0, 0), 20: (148, 24, 14, -10), 21: (172, 32, 16, 8),
        22: (168, 52, -14, 10), 23: (186, 46, 14, -8), 24: (180, 64, 12, 12), 25: (80, 46, 16, 10),
        26: (168, 96, 0, 0), 27: (138, 76, -14, -6), 28: (148, 92, 12, 12), 29: (164, 102, 0, 0),
        30: (286, 162, -16, -8), 31: (270, 148, 0, 0), 32: (244, 144, 0, 0), 33: (272, 164, 14, 6)}
for n, (mx_, my_, dx, dy) in MARK.items():
    x, y = MAPX + mx_, MAPY + my_
    lx, ly = x + dx, y + dy
    d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=NAVY)
    if dx or dy:
        d.line([(x, y), (lx, ly)], fill=NAVY, width=1)
    d.ellipse([lx - 7, ly - 7, lx + 7, ly + 7], fill=NAVY, outline=GOLD, width=1)
    d.text((lx, ly - 5), str(n), font=F(SANS_B, 8), fill=(255, 255, 255), anchor="ma")
d.text((MAPX + 6, MAPY + MAPH - 12), "34-35  GLOBAL · NO SINGLE LOCATION", font=F(SANS_B, 8), fill=NAVY)

LIST = [
    (14, "MEXICO CITY", "Protests over US extradition refusal"),
    (15, "MIAMI", "FAA halts flights after FedEx jet off runway"),
    (16, "SAN SALVADOR", "Mega-prison sweep nets region\u2019s gangs"),
    (17, "WASHINGTON", "Kushner hails Putin as \u2018diplomatic genius\u2019"),
    (18, "OTTAWA", "EU and Canada plan closer AI cooperation"),
    (19, "NEW DELHI", "India rejects US \u2018overcapacity\u2019 claims"),
    (20, "LONDON", "BBC appeals ruling in Trump\u2019s $10bn libel case"),
    (21, "TBILISI", "Georgia: Russia plans to absorb occupied land"),
    (22, "GAZA", "Israel strikes kill 10 in Gaza"),
    (23, "BAGHDAD", "Iraq seals Iran border crossing at Pashta"),
    (24, "JAZAN", "Nepal mourns worker killed in refinery strike"),
    (25, "WASHINGTON", "US approves $622m F-16 sale"),
    (26, "NAIROBI", "Kenya court halts US-funded Ebola centre"),
    (27, "BISSAU", "Guinea-Bissau delays vote, extends army rule"),
    (28, "CONAKRY", "Guinea orders clean-up after dump collapse"),
    (29, "GOMA", "DR Congo seeks answers over Ugandan general"),
    (30, "WELLINGTON", "NZ coalition one seat short of majority"),
    (31, "CANBERRA", "Australia sanctions two \u2018Iranian agents\u2019"),
    (32, "PERTH", "Lyon set to be axed from Test squad"),
    (33, "HOBART", "Stadium to proceed despite blowout fears"),
    (34, "GLOBAL", "Russia-Ukraine prisoner swap due by Christmas"),
    (35, "GLOBAL", "N. Korea halts missile shipments to Russia"),
]
for i, (n, city, txt) in enumerate(LIST):
    col = 0 if i < 11 else 1
    lx = 322 if col == 0 else 664
    ly = 794 + (i % 11) * 15
    d.text((lx, ly), f"{n}.", font=f_listb, fill=NAVY)
    d.text((lx + 24, ly), city, font=f_listb, fill=INK)
    cw_ = d.textlength(city + "  ", font=f_listb)
    d.text((lx + 24 + cw_, ly), "\u2014 " + txt, font=f_list, fill=INK)

# ============ DATE CHECK + FOOTER ============
d.rectangle([12, 968, 1012, 994], outline=GOLD, width=1)
d.text((20, 972), "DATE CHECK \u2014 Hong Kong fire broke out 26 Nov 2025 (toll 168); mourners marked its first",
       font=f_dc, fill=INK)
d.text((20, 983), "anniversary 26\u201327 Nov. Jazan refinery was struck Thu 26 Nov; Nepal\u2019s condolences and the coalition response came Fri 27 Nov. All else reported Fri 27 Nov 2026.",
       font=f_dc, fill=INK)
d.text((512, 1000), "Compiled from Reuters, AP, AFP, Bloomberg and other wire reports \u2014 27 November 2026  ·  Page 1 of 1",
       font=f_foot, fill=MUTED, anchor="ma")

img.save(OUT)
data = open(OUT, "rb").read()
print("saved", OUT, len(data), "bytes")
print("sha256", hashlib.sha256(data).hexdigest())
print("size", Image.open(OUT).size)
print("stories 35 = 3 features + 10 cards + 22 list; regions 8+6+4+5+5+5+2 = 35")
