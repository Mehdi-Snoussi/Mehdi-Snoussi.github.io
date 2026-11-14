"""Builds the legal pages of the eight apps from the text in this folder.

    py -I legal/_src/build.py            every page (and the copies kept in the app repos)
    py -I legal/_src/build.py dhikr      one app
    py -I legal/_src/build.py --fonts    cut the fonts again from the app repos (needs fonttools, brotli)

Each app has a folder here: app.json (names, dates, fonts), theme.css (its look), head.html
(its header), privacy.txt and terms.txt (the words). The pages written to legal/<app>/ are
whole files with their CSS inside; fonts are served from legal/fonts/, never from another site.

The words are plain text with a few marks:
    key: value lines, then ---          facts about the page (title, description, summary)
    ## Heading                          a numbered section
    ### Heading                         a part of a section
    - item                              a list
    | a | b |                           a table, first row the column names
    > text                              a note
    **bold**, [words](https://...), [[Heading]] (a link to that section, written "section 3")
Everything before the first ## is the summary shown at the top of the page.
"""
import html
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
LEGAL = SRC.parent
SITE = LEGAL.parent
PROJECTS = SITE.parent
UPDATED = "14 November 2026"   # the day these pages go live; change it on the day of the push
PUBLISHER = "Carthage Studio (Mehdi Snoussi), Tunisia"
MAIL = "apps.contact.supports@gmail.com"
BASE_URL = "https://mehdi-snoussi.github.io/legal"

LATIN = (list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) +
         [0x2013, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x2192, 0x20AC, 0x2212])

# Marks and phrases that have no place in these pages; the build stops on them.
BANNED = ["\u2014", " \u00b7 ", "plain language", "we action", "seamless", "robust", "leverage",
          "delve", "utilize", "rest assured", "takes your privacy seriously", "committed to",
          "in order to", "at any time and for any reason", "state-of-the-art", "cutting-edge"]


# ---------------------------------------------------------------- fonts
def font_out(spec):
    src = PROJECTS / spec[3]
    return src, src.stem


def cut_fonts(apps):
    from fontTools import subset
    from fontTools.ttLib import TTFont
    out_dir = LEGAL / "fonts"
    out_dir.mkdir(exist_ok=True)
    notices = {}
    for app in apps:
        for spec in app["fonts"]:
            src, stem = font_out(spec)
            font = TTFont(src)
            copyright_ = (font["name"].getDebugName(0) or "").strip()
            notices.setdefault(spec[0], copyright_)
            if "reserved font name" in copyright_.lower():
                # A font that reserves its name may only be passed on unchanged.
                (out_dir / (stem + ".ttf")).write_bytes(src.read_bytes())
                print("  kept whole:", stem)
                continue
            opts = subset.Options()
            opts.flavor = "woff2"
            opts.layout_features = ["*"]
            opts.name_IDs = ["*"]
            opts.name_languages = ["*"]
            opts.notdef_outline = True
            opts.glyph_names = False
            sub = subset.Subsetter(opts)
            chars = [ord(c) for c in spec[4]] if len(spec) > 4 and spec[4] else LATIN
            sub.populate(unicodes=chars)
            sub.subset(font)
            if len(spec) > 5 and spec[5]:
                # A variable font carries every weight and width; keep only the range the page uses.
                from fontTools.varLib import instancer
                limits = {k: (tuple(v) if isinstance(v, list) else v) for k, v in spec[5].items()}
                font = instancer.instantiateVariableFont(font, limits)
            font.flavor = "woff2"
            font.save(out_dir / (stem + ".woff2"))
            print("  cut:", stem, (out_dir / (stem + ".woff2")).stat().st_size // 1024, "KB")
    ofl = (PROJECTS / "bluehour/assets/fonts/OFL-Barlow.txt").read_text(encoding="utf-8")
    body = ofl[ofl.index("This Font Software is licensed under"):]
    lines = ["The fonts in this folder are the ones the apps themselves use. Each is under the SIL",
             "Open Font License 1.1, printed below. All but the .ttf files are cut down to the Latin",
             "letters these pages need.", ""]
    lines += [f"{fam}: {note}" for fam, note in sorted(notices.items())]
    (out_dir / "OFL.txt").write_text("\n".join(lines) + "\n\n" + body, encoding="utf-8")


def font_faces(app, prefix):
    out = []
    for spec in app["fonts"]:
        _, stem = font_out(spec)
        woff = LEGAL / "fonts" / (stem + ".woff2")
        name, fmt = (stem + ".woff2", "woff2") if woff.exists() else (stem + ".ttf", "truetype")
        out.append(f'@font-face{{font-family:"{spec[0]}";src:url({prefix}fonts/{name}) format("{fmt}");'
                   f"font-weight:{spec[1]};font-style:{spec[2]};font-display:swap}}")
    return "\n".join(out)


# ---------------------------------------------------------------- the words
def curly(s):
    s = re.sub(r'(^|[\s(\[])"', "\\1\u201c", s)
    s = s.replace('"', "\u201d")
    return s.replace("'", "\u2019")


def parse(text):
    head, _, body = text.partition("\n---\n")
    meta = {}
    for ln in head.splitlines():
        if ln.strip():
            k, _, v = ln.partition(":")
            meta[k.strip()] = v.strip()
    blocks, lines, i = [], body.splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
        elif ln.startswith("### "):
            blocks.append(("h3", ln[4:].strip())); i += 1
        elif ln.startswith("## "):
            blocks.append(("h2", ln[3:].strip())); i += 1
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            blocks.append(("table", rows))
        elif ln.startswith("- "):
            items = []
            while i < len(lines) and (lines[i].startswith("- ") or lines[i].startswith("  ")):
                if lines[i].startswith("- "):
                    items.append(lines[i][2:].strip())
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            blocks.append(("ul", items))
        elif ln.startswith("> "):
            blocks.append(("note", ln[2:].strip())); i += 1
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(#|\||- |> )", lines[i]):
                para.append(lines[i].strip()); i += 1
            blocks.append(("p", " ".join(para)))
    return meta, blocks


class Page:
    def __init__(self, app, kind, text):
        self.app, self.kind = app, kind
        self.meta, self.blocks = parse(text)
        self.titles = [b[1] for b in self.blocks if b[0] == "h2"]
        for bad in BANNED:
            if bad in text.lower() or bad in text:
                raise SystemExit(f"{app['slug']}/{kind}: banned mark or phrase {bad!r}")

    def ref(self, m):
        title = m.group(1)
        if title not in self.titles:
            raise SystemExit(f"{self.app['slug']}/{self.kind}: no section called {title!r}")
        n = self.titles.index(title) + 1
        return f'<a href="#s{n}">section {n}</a>'

    def inline(self, s):
        s = html.escape(curly(s), quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\[\[(.+?)\]\]", self.ref, s)
        return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)

    def block(self, b):
        kind, data = b
        if kind == "p":
            return f"<p>{self.inline(data)}</p>"
        if kind == "note":
            return f'<p class="note">{self.inline(data)}</p>'
        if kind == "h3":
            return f"<h3>{self.inline(data)}</h3>"
        if kind == "ul":
            return "<ul>" + "".join(f"<li>{self.inline(x)}</li>" for x in data) + "</ul>"
        heads = data[0]
        out = ["<table><thead><tr>" + "".join(f'<th scope="col">{self.inline(h)}</th>' for h in heads)
               + "</tr></thead><tbody>"]
        for row in data[1:]:
            cells = [f'<th scope="row">{self.inline(row[0])}</th>']
            cells += [f'<td data-th="{html.escape(heads[j])}">{self.inline(c)}</td>'
                      for j, c in enumerate(row) if j]
            out.append("<tr>" + "".join(cells) + "</tr>")
        return "".join(out) + "</tbody></table>"

    def body(self):
        first = next((i for i, b in enumerate(self.blocks) if b[0] == "h2"), len(self.blocks))
        summary = "\n".join(self.block(b) for b in self.blocks[:first])
        out, n = [], 0
        for b in self.blocks[first:]:
            if b[0] == "h2":
                if n:
                    out.append("</section>")
                n += 1
                out.append(f'<section id="s{n}"><h2><span class="n">{n}</span> {self.inline(b[1])}</h2>')
            else:
                out.append(self.block(b))
        out.append("</section>")
        contents = "".join(f'<li><a href="#s{i + 1}">{self.inline(t)}</a></li>'
                           for i, t in enumerate(self.titles))
        return summary, contents, "\n".join(out)

    def markdown(self):
        app, out = self.app, []
        out.append(f"# {self.meta['title']} for {app['name']}\n")
        out.append(f"{app['store_title']}. In force since {app['effective']}. Last changed {UPDATED}.\n")
        out.append(f"This file is a copy of {BASE_URL}/{app['slug']}/{self.kind}.html, written by "
                   "`legal/_src/build.py` in the site's repo. Change the words there, not here.\n")
        out.append(f"## {self.meta['summary']}\n")
        n = 0

        def md(s):
            return re.sub(r"\[\[(.+?)\]\]", lambda m: f"section {self.titles.index(m.group(1)) + 1}", curly(s))
        for kind, data in self.blocks:
            if kind == "h2":
                n += 1
                out.append(f"## {n}. {md(data)}\n")
            elif kind == "h3":
                out.append(f"### {md(data)}\n")
            elif kind == "p":
                out.append(md(data) + "\n")
            elif kind == "note":
                out.append("> " + md(data) + "\n")
            elif kind == "ul":
                out.append("\n".join("- " + md(x) for x in data) + "\n")
            else:
                rows = ["| " + " | ".join(md(c) for c in r) + " |" for r in data]
                rows.insert(1, "|" + " --- |" * len(data[0]))
                out.append("\n".join(rows) + "\n")
        return "\n".join(out)


# ---------------------------------------------------------------- the page
PAGE_NAMES = {"privacy": "Privacy", "terms": "Terms", "delete-account": "Delete account"}


def render(app, kind, page, base_css):
    slug = app["slug"]
    summary, contents, sections = page.body()
    title = page.meta["title"]
    theme = (SRC / slug / "theme.css").read_text(encoding="utf-8")
    fill = {"title": title, "name": app["name"], "store_title": html.escape(app["store_title"]),
            "effective": app["effective"], "updated": UPDATED, "day": UPDATED.split()[0],
            "month_year": " ".join(UPDATED.split()[1:]), "icon": f"../../assets/apps/{slug}.webp",
            "kind": kind}
    # A page that is not a policy (Mini Me's account deletion) has no "in force since" date of its own.
    since = "" if kind == "delete-account" else f"In force since {app['effective']}. "
    fill["dates"] = f"{since}Last changed {UPDATED}. Published by Carthage Studio."
    head = (SRC / slug / "head.html").read_text(encoding="utf-8")
    for k, v in fill.items():
        head = head.replace("{{" + k + "}}", v)
    pages = "".join(
        f'<a href="{k}.html"' + (' aria-current="page"' if k == kind else "") + f">{PAGE_NAMES[k]}</a>"
        for k in app["pages"])
    others = "".join(f'<a href="{k}.html">{page_title(app, k)}</a>' for k in app["pages"] if k != kind)
    play = f"https://play.google.com/store/apps/details?id={app['package']}"
    script = app.get("script", "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} for {app['name']}</title>
<meta name="description" content="{html.escape(page.meta['description'])}">
<meta name="theme-color" content="{app['theme_color']}">
<meta name="color-scheme" content="{app['scheme']}">
<link rel="icon" href="../../assets/apps/{slug}.webp">
<style>
{font_faces(app, "../")}
{base_css}
{theme}
</style>
</head>
<body class="{kind}">
<a class="skip" href="#main">Skip to the text</a>
<nav class="top" aria-label="Legal pages">
<a href="../index.html">All eight apps</a>
<span class="pages">{pages}</span>
</nav>
<header class="head">
{head.strip()}
</header>
<main id="main">
<section class="summary" aria-labelledby="sum">
<h2 id="sum">{page.inline(page.meta['summary'])}</h2>
{summary}
</section>
<nav class="contents" aria-labelledby="con">
<h2 id="con">On this page</h2>
<ol>{contents}</ol>
</nav>
<article>
{sections}
</article>
</main>
<footer class="foot">
<p>{app['name']} is published by {PUBLISHER}. Write to <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<p class="links">{others}<a href="../index.html">All eight apps</a><a href="{play}">{app['name']} on Google Play</a></p>
<p class="colophon">{app['colophon']}</p>
</footer>
{script}
</body>
</html>
"""


def page_title(app, kind):
    text = (SRC / app["slug"] / f"{kind}.txt").read_text(encoding="utf-8")
    return parse(text)[0]["title"]


def load_apps(only):
    apps = []
    for folder in sorted(p for p in SRC.iterdir() if (p / "app.json").exists()):
        if only and folder.name not in only:
            continue
        app = json.loads((folder / "app.json").read_text(encoding="utf-8"))
        app["slug"] = folder.name
        apps.append(app)
    return apps


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apps = load_apps(args)
    if "--fonts" in sys.argv:
        cut_fonts(load_apps([]))
    base_css = (SRC / "base.css").read_text(encoding="utf-8")
    for app in apps:
        for kind in app["pages"]:
            page = Page(app, kind, (SRC / app["slug"] / f"{kind}.txt").read_text(encoding="utf-8"))
            out = LEGAL / app["slug"] / f"{kind}.html"
            out.write_text(render(app, kind, page, base_css), encoding="utf-8", newline="\n")
            words = len(re.sub(r"<[^>]+>", " ", "".join(page.body())).split())
            print(f"{app['slug']}/{kind}.html  {words} words, {len(page.titles)} sections")
            if kind == "privacy" and app.get("md_copy"):
                target = PROJECTS / app["md_copy"]
                target.write_text(page.markdown(), encoding="utf-8", newline="\n")
                print("   copy:", app["md_copy"])
    hub = SRC / "hub.py"
    if hub.exists() and not args:
        ns = {"__file__": str(hub)}
        exec(compile(hub.read_text(encoding="utf-8"), str(hub), "exec"), ns)
        ns["build_hub"](load_apps([]), font_faces, UPDATED, PUBLISHER, MAIL)


if __name__ == "__main__":
    main()
