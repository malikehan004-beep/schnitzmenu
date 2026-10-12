"""Render every site image and export optimised WebP/JPG/PNG files into the theme.

    python3 tools/images.py

Needs Node + Playwright (Chromium) and Pillow. Outputs to
astra-child-schnitzmenu/assets/img/.
"""
import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from art import SCENES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
THEME = ROOT / "astra-child-schnitzmenu"
OUT = THEME / "assets" / "img"
FONTS = THEME / "assets" / "fonts"

# Responsive widths exported for each illustration.
WIDTHS = {"hero-schnitzel-plate": (520, 1000)}
DEFAULT_WIDTHS = (400, 800)

# Social share cards: slug -> (title, subtitle, illustration)
OG_CARDS = {
    "home": ("Schnitz Menu Australia 2026", "Prices, calories, allergens & deals", "hero-schnitzel-plate"),
    "schnitz-menu": ("The Full Schnitz Menu", "Every wrap, burger, plate & side", "cat-plates"),
    "schnitz-menu-prices": ("Schnitz Prices 2026", "Full price list in AUD", "cat-wraps-burgers"),
    "schnitz-calories": ("Schnitz Calories", "Calorie chart & nutrition guide", "cat-salads"),
    "schnitz-allergen-menu": ("Schnitz Allergen Guide", "Gluten, egg, milk, soy & sesame", "cat-tenders-schnacks"),
    "schnitz-kids-menu": ("Schnitz Kids Menu", "Little Rascals meals & prices", "cat-kids"),
    "schnitz-coupons": ("Schnitz Deals 2026", "Bundles, specials & coupons", "cat-chips-dips"),
}


def font_face():
    faces = []
    for family, weight, file in (("Montserrat", 800, "montserrat-latin-800-normal.woff2"),
                                 ("Montserrat", 700, "montserrat-latin-700-normal.woff2"),
                                 ("Open Sans", 600, "open-sans-latin-600-normal.woff2")):
        data = base64.b64encode((FONTS / file).read_bytes()).decode()
        faces.append(f"@font-face{{font-family:'{family}';font-weight:{weight};src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return "".join(faces)


def og_html(title, subtitle, scene_svg, w=1200, h=630, updated="Updated October 2026"):
    return f"""<html><head><style>{font_face()}
body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;font-family:'Open Sans';background:#D4471A}}
.wrap{{position:relative;width:100%;height:100%;background:linear-gradient(135deg,#D4471A,#B83A12)}}
.art{{position:absolute;right:-40px;top:50%;transform:translateY(-50%);width:{int(w * .5)}px;border-radius:28px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.25)}}
.art svg{{display:block;width:100%;height:auto}}
.txt{{position:absolute;left:70px;top:0;bottom:0;width:{int(w * .47)}px;display:flex;flex-direction:column;justify-content:center;color:#fff}}
.badge{{align-self:flex-start;background:#fff;color:#A8360F;font-weight:600;font-size:22px;padding:8px 20px;border-radius:99px}}
h1{{font-family:Montserrat;font-weight:800;font-size:{64 if len(title) < 24 else 54}px;line-height:1.05;margin:26px 0 18px;letter-spacing:-1px}}
p{{font-size:28px;margin:0;color:#FFE1D4;font-weight:600}}
.url{{position:absolute;left:70px;bottom:40px;font-family:Montserrat;font-weight:700;font-size:26px;color:#fff}}
.url b{{color:#1A1A2E;background:#fff;border-radius:8px;padding:2px 10px;margin-right:10px}}
.ring{{position:absolute;border-radius:50%;background:rgba(255,255,255,.08)}}
</style></head><body><div class="wrap">
<div class="ring" style="width:420px;height:420px;left:-140px;top:-160px"></div><div class="ring" style="width:300px;height:300px;left:380px;bottom:-180px"></div>
<div class="art">{scene_svg}</div>
<div class="txt"><span class="badge">{updated}</span><h1>{title}</h1><p>{subtitle}</p></div>
<div class="url"><b>SM</b>schnitzmenu.com</div></div></body></html>"""


def pin_html(scene_svg):
    return f"""<html><head><style>{font_face()}
body{{margin:0;width:1000px;height:1500px;font-family:'Open Sans';background:#FFF3EE}}
.top{{background:linear-gradient(135deg,#D4471A,#B83A12);color:#fff;padding:70px 80px 56px;text-align:center}}
.badge{{display:inline-block;background:#fff;color:#A8360F;font-weight:600;font-size:30px;padding:10px 26px;border-radius:99px}}
h1{{font-family:Montserrat;font-weight:800;font-size:96px;line-height:1.02;margin:34px 0 20px;letter-spacing:-2px}}
p{{font-size:38px;margin:0;color:#FFE1D4;font-weight:600}}
.art svg{{display:block;width:1000px;height:auto}}
.list{{display:flex;justify-content:center;gap:12px;flex-wrap:nowrap;padding:24px 30px}}
.list span{{font-family:Montserrat;font-weight:700;font-size:27px;white-space:nowrap;background:#fff;color:#1A1A2E;border-radius:99px;padding:14px 28px;box-shadow:0 0 0 3px #F3D5C6}}
.url{{text-align:center;font-family:Montserrat;font-weight:800;font-size:44px;color:#D4471A;padding:10px 0 40px}}
</style></head><body>
<div class="top"><span class="badge">Updated October 2026</span><h1>Full Schnitz Menu Prices</h1><p>Australia 2026 &middot; Calories &middot; Allergens</p></div>
<div class="art">{scene_svg}</div>
<div class="list"><span>Wraps &amp; Burgers</span><span>Plates</span><span>Tenders</span><span>Kids Meals</span></div>
<div class="url">schnitzmenu.com</div></body></html>"""


def icon_html(size=512):
    return f"""<html><body style="margin:0;background:transparent"><svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 48 48">
<rect width="48" height="48" rx="11" fill="#D4471A"/>
<path d="M8 27c0-10 9-15 18-14 8 1 12 7 11 12-1 7-9 11-17 10-7-1-12-3-12-8z" fill="#9C5212" transform="translate(0 1.5)"/>
<path d="M8 27c0-10 9-15 18-14 8 1 12 7 11 12-1 7-9 11-17 10-7-1-12-3-12-8z" fill="#F0B04F"/>
<g fill="#C9781F"><circle cx="17" cy="23" r="1.4"/><circle cx="25" cy="20" r="1.2"/><circle cx="31" cy="25" r="1.4"/><circle cx="21" cy="29" r="1.2"/><circle cx="28" cy="31" r="1.1"/></g>
<circle cx="37" cy="13" r="5" fill="#F7E15A" stroke="#fff" stroke-width="1.5"/></svg></body></html>"""


def logo_html():
    svg = (THEME / "assets" / "img" / "logo.svg").read_text()
    return f"<html><head><style>{font_face()}body{{margin:0;background:transparent}}</style></head><body>{svg.replace('width=\"240\" height=\"60\"', 'width=\"480\" height=\"120\"')}</body></html>"


def render(jobs):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(jobs, f)
    subprocess.run(["node", str(ROOT / "tools" / "render.js"), f.name], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "og").mkdir(exist_ok=True)
    tmp = Path(tempfile.mkdtemp())
    jobs = []
    scenes = {}
    for name, (fn, w, h) in SCENES.items():
        scenes[name] = fn(w, h)
        jobs.append({"html": f"<html><body style='margin:0'>{scenes[name]}</body></html>", "width": w, "height": h,
                     "out": str(tmp / f"{name}.png")})
    for slug, (title, sub, scene) in OG_CARDS.items():
        jobs.append({"html": og_html(title, sub, scenes[scene]), "width": 1200, "height": 630, "out": str(tmp / f"og-{slug}.png")})
    jobs.append({"html": pin_html(scenes["hero-schnitzel-plate"]), "width": 1000, "height": 1500, "out": str(tmp / "pin.png")})
    jobs.append({"html": icon_html(), "width": 512, "height": 512, "out": str(tmp / "icon.png"), "transparent": True})
    jobs.append({"html": logo_html(), "width": 480, "height": 120, "out": str(tmp / "logo.png"), "transparent": True})
    render(jobs)

    report = []

    def save(img, path, **kw):
        img.save(path, **kw)
        report.append((path.relative_to(THEME), path.stat().st_size))

    for name in SCENES:
        src = Image.open(tmp / f"{name}.png").convert("RGB")
        for width in WIDTHS.get(name, DEFAULT_WIDTHS):
            h = round(src.height * width / src.width)
            save(src.resize((width, h), Image.LANCZOS), OUT / f"{name}-{width}.webp", quality=80, method=6)

    for slug in OG_CARDS:
        # JPG: Facebook/WhatsApp/LinkedIn previews don't all accept WebP.
        save(Image.open(tmp / f"og-{slug}.png").convert("RGB"), OUT / "og" / f"og-{slug}.jpg", quality=82, optimize=True, progressive=True)
    save(Image.open(tmp / "pin.png").convert("RGB"), OUT / "pin-schnitz-menu-prices.jpg", quality=82, optimize=True, progressive=True)

    icon = Image.open(tmp / "icon.png").convert("RGBA")
    save(icon, OUT / "site-icon-512.png", optimize=True)
    save(icon.resize((180, 180), Image.LANCZOS), OUT / "apple-touch-icon.png", optimize=True)
    icon.resize((48, 48), Image.LANCZOS).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    report.append((Path("assets/img/favicon.ico"), (OUT / "favicon.ico").stat().st_size))

    logo = Image.open(tmp / "logo.png").convert("RGBA")
    save(logo, OUT / "logo-480.png", optimize=True)

    total = 0
    for path, size in report:
        total += size
        print(f"  {str(path):55} {size / 1024:6.1f} KB")
    print(f"  {'TOTAL':55} {total / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
