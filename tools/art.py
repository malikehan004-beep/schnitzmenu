"""Original flat food illustrations for schnitzmenu.com, drawn as SVG.

No photos of Schnitz products are used (copyright + trademark safety); every
image is drawn here and rendered to WebP by tools/images.py.
"""
import math
import random

GOLD_DARK = "#C9781F"
CHIP = "#F7D154"
CHIP_EDGE = "#DDAE33"
LETTUCE = "#6DBE5B"
LETTUCE_DARK = "#4E9F43"
TOMATO = "#E8543A"
CHEESE = "#FFC93C"
LEMON = "#F7E15A"
NAVY = "#1A1A2E"
BRAND = "#D4471A"

DEFS = """
<defs>
  <linearGradient id="crumb" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#F9CB66"/><stop offset=".55" stop-color="#EBA544"/><stop offset="1" stop-color="#D0832B"/>
  </linearGradient>
  <linearGradient id="crumbHi" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFE3A1" stop-opacity=".9"/><stop offset="1" stop-color="#FFE3A1" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="chip" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FBE07A"/><stop offset=".6" stop-color="#F5CB4A"/><stop offset="1" stop-color="#E5B23A"/>
  </linearGradient>
  <linearGradient id="bun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#F2B65E"/><stop offset="1" stop-color="#D98B32"/>
  </linearGradient>
  <linearGradient id="wrap" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#FBEBD0"/><stop offset="1" stop-color="#EBCB98"/>
  </linearGradient>
  <linearGradient id="can" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#1F3FA8"/><stop offset=".35" stop-color="#3C63D6"/><stop offset="1" stop-color="#16307F"/>
  </linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#CFEFFF" stop-opacity=".9"/><stop offset=".4" stop-color="#FFFFFF" stop-opacity=".95"/><stop offset="1" stop-color="#A9DBF5" stop-opacity=".9"/>
  </linearGradient>
  <radialGradient id="plate" cx=".45" cy=".4" r=".7">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset=".85" stop-color="#FBF6F3"/><stop offset="1" stop-color="#EFE4DE"/>
  </radialGradient>
  <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#7A2E10" flood-opacity=".22"/>
  </filter>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#5A2A10" flood-opacity=".25"/>
  </filter>
</defs>
"""


def _rng(seed):
    return random.Random(seed)


def blob_path(cx, cy, rx, ry, seed=1, wobble=0.07, points=28):
    """A wobbly ellipse - looks like a hand-crumbed schnitzel edge."""
    r = _rng(seed)
    pts = []
    for i in range(points):
        a = 2 * math.pi * i / points
        k = 1 + r.uniform(-wobble, wobble) + 0.05 * math.sin(3 * a + seed)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    # Smooth closed curve through the points (Catmull-Rom -> cubic Bezier).
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    n = len(pts)
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + "Z"


def crumbs(cx, cy, rx, ry, n, seed, size=1.0):
    r = _rng(seed)
    out = []
    for _ in range(n):
        a = r.uniform(0, 2 * math.pi)
        d = math.sqrt(r.uniform(0, 0.85))
        x, y = cx + rx * d * math.cos(a), cy + ry * d * math.sin(a)
        col = r.choice([GOLD_DARK, GOLD_DARK, "#B86A1A", "#FBD98A", "#FFE6A8"])
        rad = r.uniform(1.2, 3.4) * size
        out.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{rad:.1f}' fill='{col}' opacity='{r.uniform(.55, .95):.2f}'/>")
    return "".join(out)


def schnitzel(cx, cy, rx, ry, seed=3, rot=0):
    return (
        f"<g transform='rotate({rot} {cx} {cy})' filter='url(#soft)'>"
        f"<path d='{blob_path(cx, cy + 4, rx, ry, seed)}' fill='#B9701E'/>"
        f"<path d='{blob_path(cx, cy, rx, ry, seed)}' fill='url(#crumb)'/>"
        f"<path d='{blob_path(cx - rx * .12, cy - ry * .2, rx * .6, ry * .42, seed + 7, .1)}' fill='url(#crumbHi)' opacity='.7'/>"
        f"{crumbs(cx, cy, rx, ry, int(rx * ry / 140), seed)}"
        "</g>"
    )


def parma(cx, cy, rx, ry, seed=4, rot=0):
    """Schnitzel topped with napoli and melted cheese."""
    sauce = blob_path(cx, cy - 4, rx * .82, ry * .74, seed + 2, .12)
    cheese = blob_path(cx + 4, cy - 8, rx * .7, ry * .6, seed + 5, .16)
    r = _rng(seed)
    basil = "".join(
        f"<ellipse cx='{cx + r.uniform(-rx * .4, rx * .4):.0f}' cy='{cy + r.uniform(-ry * .35, ry * .25):.0f}' rx='9' ry='5' "
        f"fill='{LETTUCE_DARK}' transform='rotate({r.randint(0, 180)} {cx} {cy})'/>" for _ in range(3))
    return (schnitzel(cx, cy, rx, ry, seed, rot)
            + f"<g transform='rotate({rot} {cx} {cy})'><path d='{sauce}' fill='#C93A22'/><path d='{cheese}' fill='#FFD966'/>"
            + f"<path d='{blob_path(cx - 10, cy - 18, rx * .35, ry * .22, seed + 9, .2)}' fill='#FFF0B8' opacity='.8'/>{basil}</g>")


def chip(x, y, length=70, width=15, rot=0):
    return (f"<g transform='rotate({rot} {x} {y})'><rect x='{x - width / 2:.1f}' y='{y - length / 2:.1f}' width='{width}' "
            f"height='{length}' rx='4' fill='url(#chip)' stroke='{CHIP_EDGE}' stroke-width='1.5'/>"
            f"<rect x='{x - width / 2 + 3:.1f}' y='{y - length / 2 + 4:.1f}' width='3' height='{length - 14}' rx='1.5' fill='#FFF3B0' opacity='.7'/></g>")


def chips_pile(cx, cy, n=9, spread=60, seed=5, length=70):
    r = _rng(seed)
    return "".join(chip(cx + r.uniform(-spread, spread), cy + r.uniform(-spread * .35, spread * .35),
                        length * r.uniform(.8, 1.1), 14, r.uniform(-70, 70)) for _ in range(n))


def lemon(cx, cy, r=26):
    spokes = "".join(
        f"<path d='M{cx},{cy} L{cx + (r - 6) * math.cos(a):.1f},{cy + (r - 6) * math.sin(a):.1f}' stroke='#E8CC3A' stroke-width='2'/>"
        for a in [i * math.pi / 4 for i in range(8)])
    return (f"<g filter='url(#soft)'><circle cx='{cx}' cy='{cy}' r='{r}' fill='#F2D33E'/>"
            f"<circle cx='{cx}' cy='{cy}' r='{r - 4}' fill='{LEMON}'/>{spokes}<circle cx='{cx}' cy='{cy}' r='3' fill='#FFF6B8'/></g>")


def leaf(x, y, s=1, rot=0, col=LETTUCE):
    return (f"<g transform='translate({x} {y}) rotate({rot}) scale({s})'><path d='M0,0 C18,-22 52,-20 64,0 C52,20 18,22 0,0Z' fill='{col}'/>"
            "<path d='M4,0 L58,0' stroke='#3E8A36' stroke-width='2' opacity='.6'/></g>")


def plate(cx, cy, r):
    return (f"<g filter='url(#shadow)'><circle cx='{cx}' cy='{cy}' r='{r}' fill='url(#plate)'/></g>"
            f"<circle cx='{cx}' cy='{cy}' r='{r * .8:.0f}' fill='none' stroke='#EFE2DA' stroke-width='3'/>")


def slaw(cx, cy, seed=8, k=1.0):
    r = _rng(seed)
    bits = "".join(
        f"<path d='M{cx + r.uniform(-34, 34) * k:.0f},{cy + r.uniform(-18, 18) * k:.0f} q{r.uniform(-12, 12) * k:.0f},{r.uniform(-8, 8) * k:.0f} {r.uniform(10, 22) * k:.0f},{r.uniform(-4, 4) * k:.0f}' "
        f"stroke='{r.choice(['#B05AA8', '#F4F1E6', '#F08A3E', '#9BD27F'])}' stroke-width='{5 * k:.1f}' stroke-linecap='round' fill='none'/>"
        for _ in range(int(26 * k * k)))
    return f"<g filter='url(#soft)'><ellipse cx='{cx}' cy='{cy}' rx='{46 * k:.0f}' ry='{28 * k:.0f}' fill='#F7F2E8'/>{bits}</g>"


def dip(cx, cy, col="#FFF1C9", rim="#E9E2D8", k=1.0):
    return (f"<g transform='translate({cx} {cy}) scale({k}) translate({-cx} {-cy})'>" +f"<g filter='url(#soft)'><ellipse cx='{cx}' cy='{cy + 14}' rx='38' ry='12' fill='#D9CFC4'/>"
            f"<path d='M{cx - 38},{cy} L{cx - 32},{cy + 16} Q{cx},{cy + 26} {cx + 32},{cy + 16} L{cx + 38},{cy} Z' fill='#FFFFFF'/>"
            f"<ellipse cx='{cx}' cy='{cy}' rx='38' ry='12' fill='{rim}'/><ellipse cx='{cx}' cy='{cy + 1}' rx='32' ry='9' fill='{col}'/>"
            f"<path d='M{cx - 14},{cy - 1} q8,-5 18,0' stroke='#FFFFFF' stroke-width='3' fill='none' opacity='.7'/></g></g>")


def burger(cx, cy, s=1.0):
    """Schnitzel burger: bun, lettuce, tomato, cheese, schnitzel."""
    w = 150 * s
    sesame = "".join(f"<ellipse cx='{cx + dx * s:.0f}' cy='{cy - 72 * s + dy * s:.0f}' rx='{4 * s:.1f}' ry='{2.2 * s:.1f}' fill='#FFF4D6' "
                     f"transform='rotate({rot} {cx + dx * s:.0f} {cy - 72 * s + dy * s:.0f})'/>"
                     for dx, dy, rot in [(-40, 6, 20), (-18, -8, -10), (6, 2, 30), (30, -6, -25), (48, 10, 15), (-56, 18, -30), (-4, 16, 5), (22, 14, -15)])
    return (
        f"<g filter='url(#shadow)'>"
        f"<path d='M{cx - w * .5:.0f},{cy + 30 * s:.0f} h{w:.0f} q0,{30 * s:.0f} -{w * .12:.0f},{34 * s:.0f} h-{w * .76:.0f} q-{w * .12:.0f},-4 -{w * .12:.0f},-{34 * s:.0f}z' fill='url(#bun)'/>"
        f"<path d='{blob_path(cx, cy + 14 * s, w * .56, 22 * s, 11, .05)}' fill='url(#crumb)'/>"
        f"{crumbs(cx, cy + 14 * s, w * .5, 16 * s, 30, 12, s)}"
        f"<path d='M{cx - w * .5:.0f},{cy - 4 * s:.0f} l{w * .12:.0f},{22 * s:.0f} l{w * .14:.0f},-{18 * s:.0f} l{w * .14:.0f},{20 * s:.0f} l{w * .14:.0f},-{20 * s:.0f} l{w * .14:.0f},{20 * s:.0f} l{w * .14:.0f},-{18 * s:.0f} l{w * .12:.0f},{18 * s:.0f} v-{14 * s:.0f}z' fill='{CHEESE}'/>"
        f"<rect x='{cx - w * .48:.0f}' y='{cy - 18 * s:.0f}' width='{w * .96:.0f}' height='{12 * s:.0f}' rx='{6 * s:.0f}' fill='{TOMATO}'/>"
        f"<path d='M{cx - w * .56:.0f},{cy - 16 * s:.0f} q{w * .1:.0f},-{16 * s:.0f} {w * .2:.0f},0 q{w * .1:.0f},-{16 * s:.0f} {w * .2:.0f},0 q{w * .1:.0f},-{16 * s:.0f} {w * .2:.0f},0 q{w * .1:.0f},-{16 * s:.0f} {w * .2:.0f},0 q{w * .1:.0f},-{16 * s:.0f} {w * .2:.0f},0 q{w * .06:.0f},6 {w * .12:.0f},4 v{8 * s:.0f} h-{w * 1.12:.0f}z' fill='{LETTUCE}'/>"
        f"<path d='M{cx - w * .52:.0f},{cy - 20 * s:.0f} q0,-{70 * s:.0f} {w * .52:.0f},-{72 * s:.0f} q{w * .52:.0f},2 {w * .52:.0f},{72 * s:.0f}z' fill='url(#bun)'/>"
        f"<path d='M{cx - w * .3:.0f},{cy - 62 * s:.0f} q{w * .2:.0f},-{22 * s:.0f} {w * .44:.0f},-{6 * s:.0f}' stroke='#FFD99A' stroke-width='{6 * s:.1f}' fill='none' stroke-linecap='round' opacity='.7'/>"
        f"{sesame}</g>"
    )


def wrap(cx, cy, s=1.0, rot=-18):
    w, h = 110 * s, 230 * s
    return (
        f"<g transform='rotate({rot} {cx} {cy})' filter='url(#shadow)'>"
        f"<rect x='{cx - w / 2:.0f}' y='{cy - h / 2 + 40 * s:.0f}' width='{w:.0f}' height='{h - 40 * s:.0f}' rx='{w * .45:.0f}' fill='url(#wrap)'/>"
        f"<ellipse cx='{cx}' cy='{cy - h / 2 + 46 * s:.0f}' rx='{w / 2:.0f}' ry='{30 * s:.0f}' fill='#F3DDB5'/>"
        f"<ellipse cx='{cx}' cy='{cy - h / 2 + 44 * s:.0f}' rx='{w / 2 - 8 * s:.0f}' ry='{22 * s:.0f}' fill='#E9A443'/>"
        f"{crumbs(cx, cy - h / 2 + 44 * s, w / 2 - 14 * s, 16 * s, 18, 21, s)}"
        f"{leaf(cx - 40 * s, cy - h / 2 + 34 * s, s * .7, -30)}{leaf(cx + 4 * s, cy - h / 2 + 30 * s, s * .6, -10, LETTUCE_DARK)}"
        f"<circle cx='{cx + 22 * s:.0f}' cy='{cy - h / 2 + 40 * s:.0f}' r='{9 * s:.0f}' fill='{TOMATO}'/>"
        f"<path d='M{cx - w / 2:.0f},{cy + 20 * s:.0f} h{w:.0f} v{56 * s:.0f} h-{w:.0f}z' fill='{BRAND}' opacity='.92'/>"
        f"<path d='M{cx - w / 2:.0f},{cy + 30 * s:.0f} h{w:.0f}' stroke='#FFFFFF' stroke-width='{3 * s:.1f}' stroke-dasharray='{6 * s:.0f} {6 * s:.0f}' opacity='.6'/>"
        f"<path d='M{cx - w * .3:.0f},{cy - h / 2 + 80 * s:.0f} v{h * .45:.0f}' stroke='#FFF7E6' stroke-width='{8 * s:.0f}' stroke-linecap='round' opacity='.5'/>"
        "</g>"
    )


def tender(cx, cy, rot=0, seed=30, s=1.0):
    return schnitzel(cx, cy, 58 * s, 24 * s, seed, rot)


def box(cx, cy, w, h, col=BRAND, label=""):
    return (
        f"<g filter='url(#shadow)'><path d='M{cx - w / 2},{cy - h / 2} h{w} l-{w * .08:.0f},{h} h-{w * .84:.0f}z' fill='{col}'/>"
        f"<path d='M{cx - w / 2},{cy - h / 2} h{w} v{h * .16:.0f} h-{w}z' fill='#000' opacity='.12'/>"
        f"<path d='M{cx - w * .3:.0f},{cy + h * .1:.0f} h{w * .6:.0f}' stroke='#FFFFFF' stroke-width='6' stroke-linecap='round' opacity='.85'/>"
        f"<path d='M{cx - w * .2:.0f},{cy + h * .26:.0f} h{w * .4:.0f}' stroke='#FFFFFF' stroke-width='6' stroke-linecap='round' opacity='.55'/>{label}</g>"
    )


def salad_bowl(cx, cy, s=1.0):
    r = _rng(41)
    greens = "".join(leaf(cx + r.uniform(-150, 90) * s, cy - 40 * s + r.uniform(-40, 14) * s, s * r.uniform(.9, 1.3),
                          r.uniform(-60, 60), r.choice([LETTUCE, LETTUCE_DARK, '#8ACD6E'])) for _ in range(26))
    toms = "".join(f"<circle cx='{cx + r.uniform(-90, 90) * s:.0f}' cy='{cy - 36 * s + r.uniform(-16, 10) * s:.0f}' r='{12 * s:.0f}' fill='{TOMATO}'/>"
                   f"<circle cx='{cx + r.uniform(-90, 90) * s:.0f}' cy='{cy - 30 * s:.0f}' r='{6 * s:.0f}' fill='#F1F1E6'/>" for _ in range(4))
    strips = "".join(f"<g transform='rotate({r.uniform(-25, 25):.0f} {cx + dx * s} {cy - 50 * s})'>"
                     f"<rect x='{cx + dx * s - 40 * s:.0f}' y='{cy - 62 * s:.0f}' width='{80 * s:.0f}' height='{22 * s:.0f}' rx='{10 * s:.0f}' fill='url(#crumb)'/>"
                     f"{crumbs(cx + dx * s, cy - 51 * s, 36 * s, 8 * s, 10, int(dx) + 50, s)}</g>"
                     for dx in (-70, -10, 50))
    back = f"<ellipse cx='{cx}' cy='{cy - 30 * s:.0f}' rx='{170 * s:.0f}' ry='{34 * s:.0f}' fill='#F3E6DE'/>"
    front = (f"<g filter='url(#shadow)'><path d='M{cx - 172 * s:.0f},{cy - 30 * s:.0f} q{172 * s:.0f},{70 * s:.0f} {344 * s:.0f},0 q-{20 * s:.0f},{160 * s:.0f} -{172 * s:.0f},{168 * s:.0f} q-{152 * s:.0f},-{8 * s:.0f} -{172 * s:.0f},-{168 * s:.0f}z' fill='#FFFFFF'/>"
             f"<path d='M{cx - 160 * s:.0f},{cy + 10 * s:.0f} q{160 * s:.0f},{50 * s:.0f} {320 * s:.0f},0' stroke='{BRAND}' stroke-width='{12 * s:.0f}' fill='none' opacity='.9'/></g>")
    return back + greens + toms + strips + front

def can(cx, cy, s=1.0, col="url(#can)"):
    w, h = 80 * s, 150 * s
    return (
        f"<g filter='url(#shadow)'><rect x='{cx - w / 2:.0f}' y='{cy - h / 2:.0f}' width='{w:.0f}' height='{h:.0f}' rx='{10 * s:.0f}' fill='{col}'/>"
        f"<ellipse cx='{cx}' cy='{cy - h / 2 + 2:.0f}' rx='{w / 2 - 4:.0f}' ry='{8 * s:.0f}' fill='#C9D3E6'/>"
        f"<rect x='{cx - w / 2:.0f}' y='{cy - 10 * s:.0f}' width='{w:.0f}' height='{36 * s:.0f}' fill='#FFFFFF' opacity='.9'/>"
        f"<circle cx='{cx - 14 * s:.0f}' cy='{cy + 8 * s:.0f}' r='{7 * s:.0f}' fill='{BRAND}'/><circle cx='{cx + 4 * s:.0f}' cy='{cy + 4 * s:.0f}' r='{5 * s:.0f}' fill='#F2B33D'/><circle cx='{cx + 18 * s:.0f}' cy='{cy + 12 * s:.0f}' r='{4 * s:.0f}' fill='{BRAND}'/>"
        f"<circle cx='{cx - 6 * s:.0f}' cy='{cy - 34 * s:.0f}' r='{4 * s:.0f}' fill='#FFFFFF' opacity='.5'/><circle cx='{cx + 12 * s:.0f}' cy='{cy - 46 * s:.0f}' r='{3 * s:.0f}' fill='#FFFFFF' opacity='.4'/>"
        f"<rect x='{cx - w / 2 + 10 * s:.0f}' y='{cy - h / 2 + 14 * s:.0f}' width='{8 * s:.0f}' height='{h - 30 * s:.0f}' rx='4' fill='#FFFFFF' opacity='.25'/></g>"
    )


def bottle(cx, cy, s=1.0):
    return (
        f"<g filter='url(#shadow)'><path d='M{cx - 14 * s:.0f},{cy - 110 * s:.0f} h{28 * s:.0f} v{30 * s:.0f} q{30 * s:.0f},{20 * s:.0f} {30 * s:.0f},{60 * s:.0f} v{110 * s:.0f} q0,{14 * s:.0f} -{14 * s:.0f},{14 * s:.0f} h-{60 * s:.0f} q-{14 * s:.0f},0 -{14 * s:.0f},-{14 * s:.0f} v-{110 * s:.0f} q0,-{40 * s:.0f} {30 * s:.0f},-{60 * s:.0f}z' fill='url(#glass)' stroke='#9CCFEA' stroke-width='2'/>"
        f"<rect x='{cx - 16 * s:.0f}' y='{cy - 126 * s:.0f}' width='{32 * s:.0f}' height='{18 * s:.0f}' rx='4' fill='{NAVY}'/>"
        f"<rect x='{cx - 44 * s:.0f}' y='{cy + 0 * s:.0f}' width='{88 * s:.0f}' height='{44 * s:.0f}' fill='{BRAND}'/>"
        f"<path d='M{cx - 30 * s:.0f},{cy + 22 * s:.0f} h{60 * s:.0f}' stroke='#FFFFFF' stroke-width='{5 * s:.0f}' stroke-linecap='round'/></g>"
    )


def kids_box(cx, cy, s=1.0):
    w, h = 220 * s, 150 * s
    stars = "".join(
        f"<path transform='translate({cx + dx * s:.0f} {cy + dy * s:.0f}) scale({s * .9:.2f})' d='M0,-12 L3.5,-4 12,-3.5 5.5,2.5 7.5,11 0,6.5 -7.5,11 -5.5,2.5 -12,-3.5 -3.5,-4Z' fill='#FFE07A'/>"
        for dx, dy in ((-70, 30), (70, 46), (0, 62)))
    handle = f"<path d='M{cx - 60 * s:.0f},{cy - h / 2:.0f} q{60 * s:.0f},-{80 * s:.0f} {120 * s:.0f},0' stroke='#3346A8' stroke-width='{12 * s:.0f}' fill='none' stroke-linecap='round'/>"
    return (
        handle + f"<g filter='url(#shadow)'><path d='M{cx - w / 2:.0f},{cy - h / 2:.0f} h{w:.0f} l-{14 * s:.0f},{h:.0f} h-{w - 28 * s:.0f}z' fill='#4E66D6'/>"
        f"<path d='M{cx - w / 2:.0f},{cy - h / 2:.0f} h{w:.0f} v{22 * s:.0f} h-{w:.0f}z' fill='#3346A8'/>{stars}</g>"
    )


def nugget(cx, cy, seed, s=1.0):
    return schnitzel(cx, cy, 26 * s, 20 * s, seed, 0)


def pop_top(cx, cy, s=1.0):
    return (
        f"<g filter='url(#shadow)'><rect x='{cx - 34 * s:.0f}' y='{cy - 60 * s:.0f}' width='{68 * s:.0f}' height='{120 * s:.0f}' rx='{8 * s:.0f}' fill='#7CC36A'/>"
        f"<path d='M{cx - 34 * s:.0f},{cy - 10 * s:.0f} h{68 * s:.0f} v{40 * s:.0f} h-{68 * s:.0f}z' fill='#FFFFFF' opacity='.9'/>"
        f"<circle cx='{cx:.0f}' cy='{cy + 10 * s:.0f}' r='{12 * s:.0f}' fill='#F2913B'/>"
        f"<path d='M{cx + 12 * s:.0f},{cy - 60 * s:.0f} l{14 * s:.0f},-{50 * s:.0f}' stroke='#FF6FA0' stroke-width='{7 * s:.0f}' stroke-linecap='round'/></g>"
    )


def chips_cone(cx, cy, s=1.0):
    r = _rng(60)
    fries = "".join(chip(cx + r.uniform(-60, 60) * s, cy - 70 * s + r.uniform(-30, 20) * s, 120 * s, 16 * s, r.uniform(-22, 22)) for _ in range(16))
    return (
        fries + f"<g filter='url(#shadow)'><path d='M{cx - 90 * s:.0f},{cy - 30 * s:.0f} h{180 * s:.0f} l-{24 * s:.0f},{150 * s:.0f} h-{132 * s:.0f}z' fill='{BRAND}'/>"
        f"<path d='M{cx - 90 * s:.0f},{cy - 30 * s:.0f} h{180 * s:.0f} l-{3 * s:.0f},{20 * s:.0f} h-{174 * s:.0f}z' fill='#000' opacity='.15'/>"
        f"<circle cx='{cx:.0f}' cy='{cy + 46 * s:.0f}' r='{30 * s:.0f}' fill='#FFFFFF'/><path d='M{cx - 14 * s:.0f},{cy + 46 * s:.0f} h{28 * s:.0f} M{cx:.0f},{cy + 32 * s:.0f} v{28 * s:.0f}' stroke='{BRAND}' stroke-width='{7 * s:.0f}' stroke-linecap='round'/></g>"
    )


def background(w, h, seed=1, base="#FFF3EE"):
    """Warm background with soft circles and scattered crumbs."""
    r = _rng(seed)
    circles = "".join(
        f"<circle cx='{r.uniform(0, w):.0f}' cy='{r.uniform(0, h):.0f}' r='{r.uniform(60, 180):.0f}' fill='#FFE2D3' opacity='{r.uniform(.35, .7):.2f}'/>"
        for _ in range(5))
    specks = "".join(
        f"<circle cx='{r.uniform(0, w):.0f}' cy='{r.uniform(0, h):.0f}' r='{r.uniform(2, 4.5):.1f}' fill='{r.choice(['#F2B66B', '#E99A55', '#F7CF8F'])}' opacity='.6'/>"
        for _ in range(int(w * h / 9000)))
    return f"<rect width='{w}' height='{h}' fill='{base}'/>{circles}{specks}"


def svg(w, h, body):
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'>{DEFS}{body}</svg>"


# ---------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------

def scene_hero(w=1000, h=800):
    cx, cy = 500, 410
    body = (background(w, h, 2)
            + plate(cx, cy, 330)
            + schnitzel(cx - 40, cy - 40, 210, 135, 3, -8)
            + chips_pile(cx + 70, cy + 170, 13, 110, 9, 110)
            + slaw(cx - 200, cy + 150, 8, 1.7)
            + lemon(cx + 210, cy - 150, 44)
            + leaf(cx - 260, cy - 120, 1.2, -40) + leaf(cx - 230, cy - 160, 1.0, -70, LETTUCE_DARK)
            + dip(cx + 300, cy + 255, '#FFF1C9', '#E9E2D8', 1.8))
    return svg(w, h, body)


def scene_plates(w=800, h=500):
    return svg(w, h, background(w, h, 11) + plate(400, 260, 220) + parma(360, 220, 150, 92, 4, -6)
               + chips_pile(470, 360, 10, 80, 13, 80) + lemon(570, 170, 30) + leaf(200, 330, .9, 20))


def scene_wraps(w=800, h=500):
    return svg(w, h, background(w, h, 12) + wrap(560, 250, 1.05, 18) + burger(300, 300, 1.25)
               + chips_pile(470, 440, 5, 50, 3, 60))


def scene_tenders(w=800, h=500):
    pieces = "".join(tender(330 + dx, 200 + dy, rot, 30 + i) for i, (dx, dy, rot) in enumerate(
        ((-60, 10, -20), (40, -10, 15), (-10, 60, -5), (90, 60, 25), (-90, 90, 10))))
    return svg(w, h, background(w, h, 13) + box(330, 310, 300, 170) + pieces + dip(600, 320, "#FFE8A8") + dip(640, 400, "#F28B54"))


def scene_salads(w=800, h=500):
    return svg(w, h, background(w, h, 14) + salad_bowl(400, 300, 1.15) + lemon(660, 140, 30))


def scene_kids(w=800, h=500):
    nuggets = "".join(nugget(310 + dx, 220 + dy, 70 + i) for i, (dx, dy) in enumerate(((-50, 0), (10, -18), (60, 4), (-20, 30), (40, 34))))
    return svg(w, h, background(w, h, 15) + nuggets + kids_box(320, 320) + pop_top(590, 300) + chips_pile(470, 420, 5, 40, 17, 55))


def scene_chips(w=800, h=500):
    return svg(w, h, background(w, h, 16) + chips_cone(330, 300, 1.1) + dip(560, 330, "#FFF1C9") + dip(660, 400, "#E04B2E") + dip(580, 430, "#F6E27A"))


def scene_drinks(w=800, h=500):
    return svg(w, h, background(w, h, 17) + can(300, 290, 1.3) + bottle(480, 300, 1.2) + can(620, 320, 1.0, "#2E9E5B"))


SCENES = {
    "hero-schnitzel-plate": (scene_hero, 1000, 800),
    "cat-plates": (scene_plates, 800, 500),
    "cat-wraps-burgers": (scene_wraps, 800, 500),
    "cat-tenders-schnacks": (scene_tenders, 800, 500),
    "cat-salads": (scene_salads, 800, 500),
    "cat-kids": (scene_kids, 800, 500),
    "cat-chips-dips": (scene_chips, 800, 500),
    "cat-drinks": (scene_drinks, 800, 500),
}
