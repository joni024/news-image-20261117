#!/usr/bin/env python3
"""Draw the news infographic for make.fun competition news-image-20261117.

Build-time tool only: it renders entry.png (1024x1024) from the verified
events of Tuesday 17 November 2026. The graded entrypoint is main.py, which
simply copies the rendered image to the output directory.

Layout (1024x1024):
  masthead  : date banner, full width
  hero      : U.S. strikes on Iran / Strait of Hormuz, with a drawn scene
  grid 2x2  : Kerch Bridge, Trump Asia trip, U.S. outages, measles status
  also strip: four more verified stories of the day
  footer    : date-coverage statement
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24

PAPER = (250, 246, 239)
INK = (20, 32, 46)
NAVY = (13, 27, 46)
NAVY2 = (27, 51, 84)
RED = (200, 16, 46)
GOLD = (201, 162, 39)
GRAY = (105, 110, 118)
CARD = (255, 255, 255)
BORDER = (214, 207, 192)
LIGHT = (238, 233, 224)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap returning lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, f, fill, max_w, leading):
    """Draw wrapped text; return the y just below the block."""
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def centered(d, y, text, f, fill, cx=W // 2):
    d.text((cx - d.textlength(text, font=f) / 2, y), text, font=f, fill=fill)


# ---------------------------------------------------------------- icons
def icon_bridge(d, cx, cy, s, color):
    """A bridge with a broken middle span, over water."""
    deck_y = cy - s * 0.05
    # towers
    d.rectangle([cx - s * 0.62, cy - s * 0.55, cx - s * 0.48, deck_y], fill=color)
    d.rectangle([cx + s * 0.48, cy - s * 0.55, cx + s * 0.62, deck_y], fill=color)
    # deck, left and right of the gap
    d.rectangle([cx - s * 0.78, deck_y, cx - s * 0.12, deck_y + s * 0.10], fill=color)
    d.rectangle([cx + s * 0.12, deck_y, cx + s * 0.78, deck_y + s * 0.10], fill=color)
    # falling middle span, tilted
    d.polygon([(cx - s * 0.10, deck_y + s * 0.30), (cx + s * 0.10, deck_y + s * 0.18),
               (cx + s * 0.10, deck_y + s * 0.30), (cx - s * 0.10, deck_y + s * 0.42)],
              fill=color)
    # suspension cables
    d.line([cx - s * 0.55, cy - s * 0.55, cx - s * 0.12, deck_y], fill=color, width=max(2, s // 28))
    d.line([cx + s * 0.55, cy - s * 0.55, cx + s * 0.12, deck_y], fill=color, width=max(2, s // 28))
    # water
    for i, wx in enumerate([-0.7, -0.2, 0.3]):
        d.arc([cx + wx * s, cy + s * 0.45, cx + (wx + 0.45) * s, cy + s * 0.75],
              start=0, end=180, fill=color, width=max(2, s // 25))


def icon_globe(d, cx, cy, s, color):
    """A globe with meridians."""
    d.ellipse([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55],
              outline=color, width=max(3, s // 18))
    d.ellipse([cx - s * 0.22, cy - s * 0.55, cx + s * 0.22, cy + s * 0.55],
              outline=color, width=max(2, s // 28))
    d.line([cx - s * 0.55, cy, cx + s * 0.55, cy], fill=color, width=max(2, s // 28))
    d.arc([cx - s * 0.55, cy - s * 0.30, cx + s * 0.55, cy + s * 0.30],
          start=0, end=360, fill=color, width=max(2, s // 28))


def icon_outage(d, cx, cy, s, color):
    """A grounded plane with a warning bolt."""
    # plane silhouette (side view, nose right)
    d.polygon([(cx - s * 0.75, cy + s * 0.05), (cx - s * 0.35, cy - s * 0.15),
               (cx + s * 0.55, cy - s * 0.15), (cx + s * 0.80, cy + s * 0.05),
               (cx + s * 0.55, cy + s * 0.10), (cx - s * 0.35, cy + s * 0.10)],
              fill=color)
    d.polygon([(cx - s * 0.15, cy - s * 0.15), (cx + s * 0.05, cy - s * 0.45),
               (cx + s * 0.20, cy - s * 0.45), (cx + s * 0.25, cy - s * 0.15)],
              fill=color)
    d.polygon([(cx - s * 0.45, cy + s * 0.10), (cx - s * 0.30, cy + s * 0.38),
               (cx - s * 0.15, cy + s * 0.38), (cx - s * 0.25, cy + s * 0.10)],
              fill=color)
    # runway
    d.line([cx - s * 0.85, cy + s * 0.55, cx + s * 0.85, cy + s * 0.55],
           fill=color, width=max(3, s // 20))
    # lightning bolt, yellow
    bolt = [(cx + s * 0.42, cy - s * 0.80), (cx + s * 0.18, cy - s * 0.30),
            (cx + s * 0.38, cy - s * 0.30), (cx + s * 0.22, cy + s * 0.05),
            (cx + s * 0.52, cy - s * 0.45), (cx + s * 0.32, cy - s * 0.45)]
    d.polygon(bolt, fill=(232, 178, 8))


def icon_virus(d, cx, cy, s, color):
    """A virus particle with spikes."""
    r = s * 0.34
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        x1, y1 = cx + math.cos(a) * r, cy + math.sin(a) * r
        x2, y2 = cx + math.cos(a) * (r + s * 0.16), cy + math.sin(a) * (r + s * 0.16)
        d.line([x1, y1, x2, y2], fill=color, width=max(2, s // 28))
        d.ellipse([x2 - s * 0.05, y2 - s * 0.05, x2 + s * 0.05, y2 + s * 0.05],
                  fill=color)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.15, cy + r * 0.15],
              fill=PAPER)
    d.ellipse([cx + r * 0.25, cy + r * 0.25, cx + r * 0.55, cy + r * 0.55],
              fill=PAPER)


def hero_scene(d, x0, y0, w, h):
    """Strait of Hormuz at dusk: burning tanker, warplane overhead."""
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=14, fill=NAVY2)
    # sun low on the horizon
    d.ellipse([x0 + w * 0.62, y0 + h * 0.10, x0 + w * 0.78, y0 + h * 0.10 + w * 0.16],
              fill=(240, 190, 90))
    # sea
    sea_y = y0 + h * 0.62
    d.rounded_rectangle([x0, sea_y, x0 + w, y0 + h], radius=14, fill=(11, 38, 64))
    d.rectangle([x0, sea_y, x0 + w, sea_y + 14], fill=(11, 38, 64))
    # waves
    for i in range(4):
        wx = x0 + 14 + i * (w - 28) / 4
        d.arc([wx, sea_y + 26, wx + (w - 28) / 4, sea_y + 44], start=200, end=340,
              fill=(120, 170, 210), width=3)
    # tanker hull
    hull_y = sea_y - 6
    d.polygon([(x0 + w * 0.08, hull_y), (x0 + w * 0.14, hull_y + 34),
               (x0 + w * 0.86, hull_y + 34), (x0 + w * 0.92, hull_y)],
              fill=(8, 14, 22))
    d.rectangle([x0 + w * 0.10, hull_y - 30, x0 + w * 0.62, hull_y], fill=(16, 28, 42))
    d.rectangle([x0 + w * 0.68, hull_y - 48, x0 + w * 0.82, hull_y], fill=(16, 28, 42))
    d.rectangle([x0 + w * 0.71, hull_y - 58, x0 + w * 0.79, hull_y - 48], fill=(200, 16, 46))
    # flames amidships
    fx = x0 + w * 0.40
    d.polygon([(fx - 34, hull_y - 28), (fx - 12, hull_y - 78), (fx + 2, hull_y - 48),
               (fx + 18, hull_y - 88), (fx + 30, hull_y - 52), (fx + 42, hull_y - 28)],
              fill=(230, 110, 20))
    d.polygon([(fx - 16, hull_y - 28), (fx - 4, hull_y - 58), (fx + 8, hull_y - 38),
               (fx + 18, hull_y - 60), (fx + 24, hull_y - 28)], fill=(245, 200, 60))
    # smoke
    for sx, sy, sr in [(fx - 6, hull_y - 96, 12), (fx + 14, hull_y - 112, 15),
                       (fx + 34, hull_y - 122, 11)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 125, 132))
    # warplane with contrail
    px, py = x0 + w * 0.20, y0 + h * 0.22
    d.line([x0 + 8, py + 26, px - 6, py + 6], fill=(200, 210, 220), width=3)
    d.polygon([(px - 34, py + 8), (px + 6, py - 8), (px + 34, py + 2),
               (px + 6, py + 10)], fill=(220, 228, 236))
    d.polygon([(px - 2, py - 8), (px + 8, py - 26), (px + 16, py - 24),
               (px + 14, py - 6)], fill=(220, 228, 236))


# ---------------------------------------------------------------- layout
def draw_panel(d, x, y, w, h, kicker, kcolor, headline, deck, icon_fn, icon_s=72):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=CARD,
                        outline=BORDER, width=2)
    d.rounded_rectangle([x, y, x + w, y + 8], radius=4, fill=kcolor)
    d.rectangle([x, y + 4, x + w, y + 8], fill=kcolor)
    # icon on the left, kept inside the panel
    icon_fn(d, x + 60, y + h // 2 + 10, icon_s, kcolor)
    tx = x + 124
    tw = w - 124 - 16
    yy = y + 20
    d.text((tx, yy), kicker, font=font(SANS_B, 19), fill=kcolor)
    yy += 28
    yy = text_block(d, tx, yy, headline, font(SANS_B, 25), INK, tw, 30)
    yy += 6
    text_block(d, tx, yy, deck, font(SANS, 19), (52, 60, 70), tw, 24)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.rectangle([0, 146, W, 150], fill=GOLD)
    centered(d, 16, "THE WORLD IN ONE PICTURE", font(SANS_B, 22), GOLD)
    centered(d, 44, "TUESDAY  17  NOVEMBER  2026", font(SERIF_B, 62), (255, 255, 255))
    centered(d, 118, "WORLD NEWS  •  ONE DAY  •  ONE IMAGE", font(SANS, 19),
             (170, 185, 205))

    # ---- hero ----
    hx, hy, hw, hh = MARGIN, 166, W - 2 * MARGIN, 240
    d.rounded_rectangle([hx, hy, hx + hw, hy + hh], radius=12, fill=CARD,
                        outline=BORDER, width=2)
    d.rectangle([hx, hy, hx + 10, hy + hh], fill=RED)
    tx = hx + 30
    d.text((tx, hy + 18), "MIDDLE EAST  •  STRAIT OF HORMUZ", font=font(SANS_B, 20),
           fill=RED)
    yy = text_block(d, tx, hy + 46, "U.S. STRIKES IRAN AFTER\nTANKER ATTACKS",
                    font(SANS_B, 42), INK, 620, 48)
    text_block(d, tx, yy + 10,
               "U.S. warplanes hit missile sites on Qeshm Island after attacks "
               "on commercial ships. A gas tanker burned off Oman; 24 seafarers "
               "were evacuated.",
               font(SANS, 22), (52, 60, 70), 610, 28)
    hero_scene(d, hx + hw - 330, hy + 20, 300, hh - 40)

    # ---- grid 2x2 ----
    gx, gy = MARGIN, 418
    gw = (W - 2 * MARGIN - 16) // 2
    gh = 196
    draw_panel(d, gx, gy, gw, gh,
               "EUROPE  •  UKRAINE", (31, 111, 235),
               "KERCH BRIDGE SPAN COLLAPSES",
               "Ukraine struck the bridge to Crimea; a road section fell into "
               "the sea. Russia hit bridges in Kyiv.",
               icon_bridge)
    draw_panel(d, gx + gw + 16, gy, gw, gh,
               "ASIA  •  DIPLOMACY", (46, 139, 87),
               "TRUMP OPENS ASIA TRIP IN MANILA",
               "ASEAN and Quad meetings under way; a summit with Xi and Putin "
               "is set for Thursday in China.",
               icon_globe)
    draw_panel(d, gx, gy + gh + 12, gw, gh,
               "UNITED STATES", (124, 58, 237),
               "OUTAGES HIT AIRPORTS, BANKS, TECH",
               "Flights grounded, Apple and Microsoft services disrupted. "
               "Officials deny a cyberattack.",
               icon_outage, icon_s=62)
    draw_panel(d, gx + gw + 16, gy + gh + 12, gw, gh,
               "HEALTH", (14, 116, 144),
               "U.S. LOSES MEASLES-FREE STATUS",
               "First loss of elimination status since 2000 as cases surge and "
               "vaccination rates fall.",
               icon_virus)

    # ---- also strip ----
    ax, ay, aw, ah = MARGIN, 834, W - 2 * MARGIN, 88
    d.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=12, fill=LIGHT,
                        outline=BORDER, width=2)
    d.text((ax + 20, ay + 12), "ALSO TODAY", font=font(SANS_B, 19), fill=INK)
    text_block(d, ax + 20, ay + 38,
               "Winter rains deepen Gaza's shelter crisis  •  Japan scrambles jets "
               "as Russian planes enter its airspace  •  Depardieu admits sexual "
               "assault charge in Paris  •  Five EU states plan a migrant return "
               "hub in Rwanda",
               font(SANS, 20), (52, 60, 70), aw - 40, 26)

    # ---- footer ----
    centered(d, 938, "All events happened or were first reported on Tuesday 17 November 2026.",
             font(SANS_I, 20), GRAY)
    centered(d, 966, "As reported by Reuters, AP, CNN and the UN  •  Drawn for make.fun",
             font(SANS, 17), GRAY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
