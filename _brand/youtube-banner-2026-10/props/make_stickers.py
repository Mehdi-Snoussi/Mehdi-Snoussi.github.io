"""Write the sticker-sheet banner variations (s1..s5) from one template.

usage: py -I make_stickers.py
The words take a box centred on the band (fitted to 880 px wide at most);
the band's stickers keep to its edges, so they never cover a letter.
"""
import json
import pathlib

here = pathlib.Path(__file__).parent

TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="base.css">
<style>
/* A sheet of die-cut stickers: bright plain shapes with a thick white cut
   edge, an ink outline and a hard offset shadow, around the words. */
body {{ background: {bg}; background-image: radial-gradient({dot} 1.6px, transparent 1.8px); background-size: 22px 22px; }}
svg {{ position: absolute; inset: 0; }}
.words h1 {{ font-size: 74px; color: #14161A; }}
.words p {{ margin-top: 16px; font-size: 30px; color: {cta_fg}; background: {cta_bg}; display: inline-block; padding: 11px 20px 10px; transform: rotate(-1.5deg); }}
</style></head>
<body>
<svg id="s" width="2048" height="1152" viewBox="0 0 2048 1152"></svg>
<div class="center words"><h1 class="dsp" id="h">{headline}</h1><p class="mono">Subscribe for the next one</p></div>
<script>
// fit the headline to 820 px at most, once its font has loaded
const h = document.getElementById('h');
document.fonts.ready.then(() => {{
  let size = 74;
  while (h.getBoundingClientRect().width > 820 && size > 40) {{ size -= 1; h.style.fontSize = size + 'px'; }}
}});
const NS = 'http://www.w3.org/2000/svg', s = document.getElementById('s');
const ink = '#14161A';
const items = {items};
function shape(kind, r) {{
  switch (kind) {{
    case 'circle': return `<circle r="${{r}}"/>`;
    case 'square': return `<rect x="${{-r}}" y="${{-r}}" width="${{2 * r}}" height="${{2 * r}}" rx="${{r * 0.28}}"/>`;
    case 'half': return `<path d="M${{-r}} ${{r * 0.35}} A ${{r}} ${{r}} 0 0 1 ${{r}} ${{r * 0.35}} Z"/>`;
    case 'star': {{ let d = ''; for (let i = 0; i < 10; i++) {{ const a = Math.PI / 5 * i - Math.PI / 2, rr = i % 2 ? r * 0.5 : r; d += (i ? 'L' : 'M') + (rr * Math.cos(a)).toFixed(1) + ' ' + (rr * Math.sin(a)).toFixed(1); }} return `<path d="${{d}}Z" stroke-linejoin="round"/>`; }}
    case 'blob': return `<path d="M${{-r}} 0 C ${{-r}} ${{-r * 0.9}}, ${{r * 0.2}} ${{-r * 1.05}}, ${{r * 0.8}} ${{-r * 0.5}} S ${{r * 1.05}} ${{r * 0.8}}, ${{r * 0.1}} ${{r * 0.85}} S ${{-r}} ${{r * 0.6}}, ${{-r}} 0 Z"/>`;
    case 'wave': return `<path d="M${{-r}} ${{-r * 0.3}} q ${{r / 2}} ${{-r * 0.5}} ${{r}} 0 t ${{r}} 0 v ${{r * 0.6}} q ${{-r / 2}} ${{r * 0.5}} ${{-r}} 0 t ${{-r}} 0 Z"/>`;
    case 'bolt': return `<path d="M${{r * 0.2}} ${{-r}} L${{-r * 0.6}} ${{r * 0.15}} H${{0}} L${{-r * 0.2}} ${{r}} L${{r * 0.6}} ${{-r * 0.15}} H${{0}} Z" stroke-linejoin="round"/>`;
    case 'ring': return `<path fill-rule="evenodd" d="M${{-r}} 0 a ${{r}} ${{r}} 0 1 0 ${{2 * r}} 0 a ${{r}} ${{r}} 0 1 0 ${{-2 * r}} 0 Z M${{-r * 0.45}} 0 a ${{r * 0.45}} ${{r * 0.45}} 0 1 1 ${{r * 0.9}} 0 a ${{r * 0.45}} ${{r * 0.45}} 0 1 1 ${{-r * 0.9}} 0 Z"/>`;
    case 'pill': return `<rect x="${{-r}}" y="${{-r * 0.45}}" width="${{2 * r}}" height="${{r * 0.9}}" rx="${{r * 0.45}}"/>`;
    case 'tri': return `<path d="M0 ${{-r}} L${{r * 0.95}} ${{r * 0.7}} L${{-r * 0.95}} ${{r * 0.7}} Z" stroke-linejoin="round"/>`;
    case 'flower': {{ let d = ''; for (let i = 0; i < 6; i++) {{ const a = Math.PI / 3 * i; d += `<circle cx="${{(r * 0.52 * Math.cos(a)).toFixed(1)}}" cy="${{(r * 0.52 * Math.sin(a)).toFixed(1)}}" r="${{r * 0.48}}"/>`; }} return d + `<circle r="${{r * 0.55}}"/>`; }}
  }}
}}
let html = '';
for (const [k, x, y, r, rot, c] of items) {{
  const g = shape(k, r);
  html += `<g transform="translate(${{x}} ${{y}}) rotate(${{rot}})">`
    + `<g transform="translate(9 9)" fill="${{ink}}" stroke="${{ink}}" stroke-width="22">${{g}}</g>`
    + `<g fill="#FFFFFF" stroke="#FFFFFF" stroke-width="22">${{g}}</g>`
    + `<g fill="${{c}}" stroke="${{ink}}" stroke-width="4">${{g}}</g></g>`;
}}
s.innerHTML = html;
</script>
</body></html>
"""

# Sticker places (band ones keep outside x 574-1474, y 500-690 where the words are); colours per sheet.
BAND = [
    ('blob', 200, 560, 120, 12), ('circle', 370, 680, 70, -8), ('star', 455, 478, 50, 10),
    ('half', 1600, 520, 72, -14), ('square', 1560, 700, 52, 18), ('circle', 1840, 600, 110, 0),
    ('wave', 1030, 430, 58, -4), ('bolt', 1700, 700, 46, 8),
]
TV = [
    ('circle', 120, 200, 160, 0), ('square', 520, 240, 120, -10), ('star', 860, 160, 110, 6), ('half', 1260, 220, 140, 20), ('blob', 1700, 180, 170, -12),
    ('blob', 200, 960, 170, 8), ('circle', 640, 960, 130, 0), ('square', 1040, 1000, 120, 14), ('star', 1460, 960, 120, -8), ('wave', 1860, 990, 150, 10),
]


def items(colours, swap=None):
    out = []
    for i, (k, x, y, r, rot) in enumerate(BAND + TV):
        if swap and i in swap:
            k = swap[i]
        out.append([k, x, y, r, rot, colours[i % len(colours)]])
    return out


VARIANTS = [
    dict(name='s1_yellow', headline='Games to play, apps to keep', bg='#FFE45C', dot='#F2C81C', cta_bg='#14161A', cta_fg='#F3F4EF',
         colours=['#3EA3D8', '#FF5FA2', '#C6F35E', '#3550C4', '#FF7A1A', '#2A8A73', '#8A3484', '#FF5FA2'], swap={}),
    dict(name='s2_pink', headline='Fun games and useful apps', bg='#FF9EC9', dot='#F07AB0', cta_bg='#14161A', cta_fg='#FFE45C',
         colours=['#FFE45C', '#3550C4', '#C6F35E', '#2A8A73', '#FF7A1A', '#3EA3D8', '#8A3484', '#FFE45C'], swap={0: 'flower', 2: 'ring', 6: 'pill'}),
    dict(name='s3_sky', headline='Little games, handy apps', bg='#7CC8F0', dot='#5AB3E2', cta_bg='#14161A', cta_fg='#F3F4EF',
         colours=['#FFE45C', '#FF5FA2', '#FF7A1A', '#C6F35E', '#8A3484', '#F3F4EF', '#2A8A73', '#FFE45C'], swap={1: 'ring', 3: 'tri', 5: 'flower'}),
    dict(name='s4_lime', headline='Apps and games worth keeping', bg='#C6F35E', dot='#A9D93E', cta_bg='#3550C4', cta_fg='#FFFFFF',
         colours=['#FF5FA2', '#3550C4', '#FF7A1A', '#8A3484', '#3EA3D8', '#FFE45C', '#2A8A73', '#FF5FA2'], swap={0: 'pill', 4: 'ring', 7: 'star'}),
    dict(name='s5_lilac', headline='Something to play, something to use', bg='#C9B6F2', dot='#B39CE6', cta_bg='#14161A', cta_fg='#C6F35E',
         colours=['#FFE45C', '#FF5FA2', '#2A8A73', '#FF7A1A', '#3EA3D8', '#C6F35E', '#3550C4', '#FFE45C'], swap={2: 'flower', 3: 'tri', 6: 'ring'}),
]

for v in VARIANTS:
    html = TEMPLATE.format(title=v['name'], bg=v['bg'], dot=v['dot'], cta_bg=v['cta_bg'], cta_fg=v['cta_fg'],
                           headline=v['headline'], items=json.dumps(items(v['colours'], v['swap'])))
    (here / f"{v['name']}.html").write_text(html, encoding='utf-8')
    print('wrote', v['name'])
