"""The list at /legal/: the eight apps, each with its pages. Called by build.py.

Each app's name is set in the face and colour of its own legal pages, from a font file that holds
only the letters of that name (legal/fonts/hub-<app>.woff2, cut here when missing). The rest of the
page is in Archivo, the face of the site's front page, also served from legal/fonts/.
"""
import html
from pathlib import Path

SRC = Path(__file__).resolve().parent
LEGAL = SRC.parent
PROJECTS = LEGAL.parent.parent

# what each app is, in one line checked against the app; then the face its name is set in:
# (font file, axis limits for a variable font, CSS for the name)
ROWS = {
    "aimystic": ("Tarot readings written by an AI model, for reflection and entertainment.",
                 "aimystic/assets/google_fonts/EBGaramond-Medium.ttf", None,
                 "font-weight:500;font-size:1.72rem;color:#10111D"),
    "bluehour": ("A home screen for car head units and for phones in a dashboard mount.",
                 "bluehour/assets/fonts/Saira-Variable.ttf", {"wdth": 100, "wght": 600},
                 "font-weight:600;color:#1B3C86"),
    "cascade": ("A drop-and-merge puzzle game played with orbs.",
                "cascade/assets/fonts/BricolageGrotesque-ExtraBold.ttf", None,
                "font-weight:800;color:#141A2E;text-shadow:2px 2px 0 #FF5C9E"),
    "dhikr": ("Tasbih counter, azkar, prayer times, Qibla and the Quran, with a Wear OS watch app.",
              "dhikr/assets/fonts/Amiri-Bold.ttf", None,
              "font-weight:700;font-size:1.72rem;color:#0F4D3A"),
    "minime": ("A tiny you that lives on your phone, your home screen and your watch.",
               "minime/assets/fonts/grandstander/Grandstander-Variable.ttf", {"wght": 800},
               "font-weight:800;color:#1F1B2D;text-decoration:underline #FF5FA2 3px;text-underline-offset:.2em"),
    "relicrevival": ("A cleaning game: wipe the grime off relics and fill a museum with them.",
                     "relicrevival/assets/fonts/Cinzel.ttf", {"wght": 700},
                     "font-weight:700;font-size:1.42rem;color:#1F3A3A"),
    "sortflow": ("A colour-sort puzzle game played with test tubes.",
                 "sortflow/assets/fonts/Alegreya-ExtraBold.ttf", None,
                 "font-weight:800;font-size:1.62rem;color:#7A5325"),
    "zellia": ("A triple tile match puzzle set in zellige mosaics.",
               "zellia/assets/fonts/Cinzel.ttf", {"wght": 700},
               "font-weight:700;font-size:1.42rem;color:#115674"),
}
ARCHIVO = "Mehdi-Snoussi.github.io/_brand/youtube-banner-2026-10/fonts/Archivo-var.ttf"
PAGE = {"privacy": "Privacy policy", "terms": "Terms of service", "delete-account": "Delete your Friends account"}


def cut(src, out, chars, limits=None):
    from fontTools import subset
    from fontTools.ttLib import TTFont
    font = TTFont(PROJECTS / src)
    if "reserved font name" in (font["name"].getDebugName(0) or "").lower():
        return False        # may only be passed on unchanged: the name then stays in Archivo
    opts = subset.Options()
    opts.layout_features = ["kern", "liga", "mark", "mkmk"]
    opts.notdef_outline = True
    opts.glyph_names = False
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=sorted(set(chars)))
    sub.subset(font)
    if limits:
        from fontTools.varLib import instancer
        font = instancer.instantiateVariableFont(font, {k: (tuple(v) if isinstance(v, list) else v) for k, v in limits.items()})
    font.flavor = "woff2"
    font.save(out)
    return True


def build_hub(apps, font_faces, updated, publisher, mail):
    fonts = LEGAL / "fonts"
    latin = list(range(0x20, 0x7F)) + [0xA9, 0x2018, 0x2019, 0x201C, 0x201D]
    if not (fonts / "Archivo.woff2").exists():
        cut(ARCHIVO, fonts / "Archivo.woff2", latin, {"wdth": 100, "wght": [400, 700]})
    faces = ['@font-face{font-family:"Archivo";src:url(fonts/Archivo.woff2) format("woff2");'
             "font-weight:400 700;font-style:normal;font-display:swap}"]
    rows = []
    for app in apps:
        slug = app["slug"]
        what, src, limits, css = ROWS[slug]
        out = fonts / f"hub-{slug}.woff2"
        if not out.exists():
            cut(src, out, [ord(c) for c in app["name"]], limits)
        if out.exists():
            faces.append(f'@font-face{{font-family:"hub-{slug}";src:url(fonts/hub-{slug}.woff2) format("woff2");font-display:swap}}')
            css = f'font-family:"hub-{slug}","Archivo",sans-serif;{css}'
        links = "".join(f'<li><a href="{slug}/{k}.html">{PAGE[k]}</a></li>' for k in app["pages"])
        play = f"https://play.google.com/store/apps/details?id={app['package']}"
        rows.append(f"""<li class="app" id="{slug}">
<img src="../assets/apps/{slug}.webp" alt="" width="56" height="56" loading="lazy">
<div>
<h2 style='{css}'>{html.escape(app['name'])}</h2>
<p>{html.escape(what)}</p>
<ul>{links}<li><a class="play" href="{play}">On Google Play</a></li></ul>
</div>
</li>""")
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Privacy and terms for Carthage Studio's apps</title>
<meta name="description" content="The privacy policy and the terms of service of each of the eight apps Carthage Studio publishes on Google Play: AI Mystic, Blue Hour, Cascade, Dhikr, Mini Me, Relic Revival, SortFlow and Zellia.">
<meta name="theme-color" content="#E7E8E2">
<meta name="color-scheme" content="light">
<style>
{chr(10).join(faces)}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:#E7E8E2;color:#14161A;font:400 1.06rem/1.58 "Archivo","Segoe UI",system-ui,sans-serif}}
a{{color:#1A33DC;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.18em}}
a:hover{{text-decoration-thickness:2px}}
:focus-visible{{outline:2px solid #1A33DC;outline-offset:3px}}
header,main,footer{{max-width:46rem;margin-inline:auto;padding-inline:1.125rem}}
header{{padding-top:2.6rem}}
h1{{margin:0;font-size:clamp(2.1rem,7.5vw,3rem);line-height:1.08;font-weight:700;letter-spacing:-.02em}}
header p{{margin:1rem 0 0;max-width:36rem}}
.apps{{list-style:none;margin:2.2rem 0 0;padding:0;border-top:2px solid #14161A}}
.app{{display:grid;grid-template-columns:56px 1fr;gap:0 1.1rem;padding:1.35rem 0 1.4rem;border-bottom:1px solid #14161A}}
.app img{{border-radius:13px;display:block;margin-top:.15rem}}
.app h2{{margin:0;font-size:1.5rem;line-height:1.2;font-weight:700}}
.app p{{margin:.3rem 0 0;color:#3F454C}}
.app ul{{list-style:none;margin:.7rem 0 0;padding:0;display:flex;flex-wrap:wrap;gap:.35rem 1.4rem}}
.app .play{{color:#14161A}}
.ask{{margin-top:2.4rem}}
.ask h2{{margin:0;font-size:1.25rem}}
.ask p{{margin:.5rem 0 0;max-width:38rem}}
footer{{margin-top:2.8rem;padding-block:1.3rem 3rem;border-top:1px solid #14161A;font-size:.95rem;color:#3F454C}}
footer p{{margin:0 0 .4rem}}
@media (max-width:26rem){{.app{{grid-template-columns:44px 1fr;gap:0 .85rem}}.app img{{width:44px;height:44px;border-radius:10px}}}}
@media print{{body{{background:#fff}}a{{color:#000}}.app a::after{{content:" (" attr(href) ")";font-size:.8em}}}}
</style>
</head>
<body>
<header>
<h1>Privacy and terms</h1>
<p>Carthage Studio publishes eight apps on Google Play. Each one has its own privacy policy and its own terms of service, written from what that app does with your data. Pick the app you installed.</p>
</header>
<main>
<ul class="apps">
{chr(10).join(rows)}
</ul>
<section class="ask">
<h2>Questions and requests</h2>
<p>For a question about any of these pages, or to ask what we hold about you and have it deleted, write to <a href="mailto:{mail}">{mail}</a>. We answer within 30 days.</p>
</section>
</main>
<footer>
<p>The eight apps are published by {publisher}.</p>
<p>This list was last changed on {updated}. Each page carries its own date. <a href="/">The developer's site</a></p>
</footer>
</body>
</html>
"""
    (LEGAL / "index.html").write_text(page, encoding="utf-8", newline="\n")
    print("index.html  the list of", len(rows), "apps")
