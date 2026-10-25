"""Render the five proposals and an overview sheet (desktop band + phone view each).

usage: py -I render_all.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

here = pathlib.Path(__file__).parent
names = sorted(here.glob("s*_*.html"))
out = here / "out"
out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    pg = b.new_page(viewport={"width": 2048, "height": 1152}, device_scale_factor=1)
    for f in names:
        pg.goto(f.resolve().as_uri())
        pg.wait_for_timeout(1500)
        pg.screenshot(path=str(out / f"{f.stem}.png"))
        print(f.stem, pg.evaluate("() => [...document.fonts].filter(x => x.status === 'loaded').length"), "fonts loaded")
    b.close()

# overview: per option, the desktop band (2048x338 -> 1600x264) and the phone view (1236x338 -> 600x164)
font = ImageFont.truetype(str(here.parent / "fonts" / "IBMPlexMono-SemiBold.ttf"), 30)
W, row_h = 1600 + 40 + 600 + 80, 264 + 70
sheet = Image.new("RGB", (W, row_h * len(names) + 40), "#202226")
d = ImageDraw.Draw(sheet)
for i, f in enumerate(names):
    im = Image.open(out / f"{f.stem}.png").convert("RGB")
    im.save(out / f"{f.stem}.jpg", quality=92)
    y = 40 + i * row_h
    d.text((40, y), f"{i + 1}. {f.stem.split('_', 1)[1]}      desktop", fill="#F3F4EF", font=font)
    d.text((40 + 1600 + 40, y), "phone", fill="#F3F4EF", font=font)
    sheet.paste(im.crop((0, 407, 2048, 745)).resize((1600, 264), Image.LANCZOS), (40, y + 44))
    sheet.paste(im.crop((406, 407, 1642, 745)).resize((600, 164), Image.LANCZOS), (40 + 1600 + 40, y + 44))
sheet.save(out / "overview.png")
print(out / "overview.png")
