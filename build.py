#!/usr/bin/env python3
"""Build inorganicvii — static multi-page notes site. Run: python3 build.py"""
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

def svg_open(w=760, h=300, vb="0 0 760 300"):
    return f'<svg viewBox="{vb}" width="{w}" height="{h}" role="img" xmlns="http://www.w3.org/2000/svg">'
INK="#1c2430"; MUT="#5a6572"; ACC="#a4134a"; PAPER="#f2f4f6"; BLUE="#2b5f8a"; GREEN="#2e6b4f"; AMBER="#9a6a00"

def cube_svg(kind="sc", title=""):
    # front face (60,60)-(260,260), depth offset 70,-50 ; schematic isometric-ish cube
    def pt(x,y,dx=70,dy=-50): return (x+dx, y+dy)
    front=[(60,260),(260,260),(260,60),(60,60)]
    back=[pt(*p) for p in front]
    lines=""
    for a,b in zip(front, back): lines+=f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" stroke-width="1.5"/>'
    poly=lambda pts: " ".join(f"{x},{y}" for x,y in pts)
    s=svg_open(760,300,"0 0 760 300")
    s+=f'<rect x="0" y="0" width="760" height="300" fill="{PAPER}"/>'
    s+=f'<polygon points="{poly(front)}" fill="none" stroke="{INK}" stroke-width="2"/><polygon points="{poly(back)}" fill="none" stroke="{INK}" stroke-width="2"/>{lines}'
    def dot(x,y,r=9,fill=INK): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="#fff" stroke-width="1.5"/>'
    # corners front + back
    for p in front+back: s+=dot(*p)
    if kind in ("bcc","fcc"):
        s+=dot(195,155,10,ACC)  # body centre (only bcc)
    if kind=="fcc":
        # face centres: front, top, right (visible)
        s+=dot(160,160,9,BLUE)  # front face centre
        s+=dot(195,35,9,BLUE)   # top face centre approx
        s+=dot(295,155,9,BLUE)  # right face centre approx
        s+='<text x="380" y="90" font-family="IBM Plex Mono, monospace" font-size="15" fill="#1c2430">corners: 8 x 1/8 = 1</text><text x="380" y="120" font-family="IBM Plex Mono, monospace" font-size="15" fill="#1c2430">faces: 6 x 1/2 = 3</text><text x="380" y="150" font-family="IBM Plex Mono, monospace" font-size="15" fill="#a4134a">total = 4 atoms</text>'
    elif kind=="bcc":
        s+='<text x="380" y="90" font-family="IBM Plex Mono, monospace" font-size="15" fill="#1c2430">corners: 8 x 1/8 = 1</text><text x="380" y="120" font-family="IBM Plex Mono, monospace" font-size="15" fill="#1c2430">centre: 1 (unshared)</text><text x="380" y="150" font-family="IBM Plex Mono, monospace" font-size="15" fill="#a4134a">total = 2 atoms</text>'
    else:
        s+='<text x="380" y="90" font-family="IBM Plex Mono, monospace" font-size="15" fill="#1c2430">corners: 8 x 1/8 = 1</text><text x="380" y="150" font-family="IBM Plex Mono, monospace" font-size="15" fill="#a4134a">total = 1 atom</text>'
    s+=f'<text x="60" y="290" font-family="IBM Plex Mono, monospace" font-size="14" fill="{MUT}">{title}</text></svg>'
    return s

def fig(caption, inner):
    return f'<figure>{inner}<figcaption>{caption}</figcaption></figure>'

# ---- individual figures ----
def fig_order():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    for r in range(4):
        for c in range(5):
            s+=f'<circle cx="{70+c*52}" cy="{60+r*48}" r="11" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<text x="60" y="270" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Crystalline: long range order</text>'
    import random; random.seed(7)
    for _ in range(20):
        x=430+random.randint(0,260); y=40+random.randint(0,180)
        s+=f'<circle cx="{x}" cy="{y}" r="11" fill="none" stroke="{MUT}" stroke-width="1.5"/>'
    s+=f'<text x="430" y="270" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Amorphous: short range order only</text></svg>'
    return s

def fig_axes():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/><line x1="180" y1="200" x2="420" y2="200" stroke="{INK}" stroke-width="2"/><line x1="180" y1="200" x2="180" y2="60" stroke="{INK}" stroke-width="2"/><line x1="180" y1="200" x2="330" y2="110" stroke="{INK}" stroke-width="2"/>'
    s+=f'<text x="430" y="205" font-family="IBM Plex Mono, monospace" font-size="16" fill="{INK}">a</text><text x="170" y="45" font-family="IBM Plex Mono, monospace" font-size="16" fill="{INK}">c</text><text x="340" y="105" font-family="IBM Plex Mono, monospace" font-size="16" fill="{INK}">b</text>'
    s+=f'<text x="480" y="90" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">alpha: between b and c</text><text x="480" y="120" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">beta: between a and c</text><text x="480" y="150" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">gamma: between a and b</text><text x="480" y="190" font-family="IBM Plex Mono, monospace" font-size="15" fill="{ACC}">6 lattice parameters:</text><text x="480" y="215" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">a, b, c, alpha, beta, gamma</text></svg>'
    return s

def fig_packing():
    s=svg_open(760,320)
    s+=f'<rect width="760" height="320" fill="{PAPER}"/>'
    for i in range(5): s+=f'<circle cx="{70+i*48}" cy="70" r="20" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<text x="60" y="130" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">1D row: CN = 2</text>'
    for r in range(3):
        for c in range(4): s+=f'<circle cx="{70+c*48}" cy="{180+r*44}" r="20" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<text x="60" y="310" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Square packing AAA: CN = 4</text>'
    for r in range(3):
        off=24 if r%2 else 0
        for c in range(4): s+=f'<circle cx="{430+off+c*48}" cy="{180+r*40}" r="20" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
    s+=f'<text x="420" y="310" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Hexagonal ABAB: CN = 6</text></svg>'
    return s

def fig_stacking():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    for i,(lab,y) in enumerate([("A",60),("B",130),("A",200)]):
        for c in range(5): s+=f'<circle cx="{80+c*44}" cy="{y}" r="16" fill="none" stroke="{INK}" stroke-width="1.5"/>'
        s+=f'<text x="330" y="{y+6}" font-family="IBM Plex Mono, monospace" font-size="16" fill="{INK}">{lab}</text>'
    s+=f'<text x="60" y="270" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">ABAB... = hcp</text>'
    for i,(lab,y) in enumerate([("A",60),("B",130),("C",200)]):
        off=18 if lab=="C" else 0
        for c in range(5): s+=f'<circle cx="{450+off+c*44}" cy="{y}" r="16" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
        s+=f'<text x="700" y="{y+6}" font-family="IBM Plex Mono, monospace" font-size="16" fill="{INK}">{lab}</text>'
    s+=f'<text x="430" y="270" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">ABCABC... = ccp / fcc</text></svg>'
    return s

def fig_voids():
    s=svg_open(760,320)
    s+=f'<rect width="760" height="320" fill="{PAPER}"/>'
    # tetrahedral: 3 base + 1 top small
    for (x,y) in [(140,220),(220,220),(180,150)]: s+=f'<circle cx="{x}" cy="{y}" r="42" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<circle cx="180" cy="195" r="12" fill="{ACC}"/><text x="120" y="290" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Tetrahedral void: 4 spheres</text><text x="120" y="312" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">r(void) = 0.225 R, 2 per sphere</text>'
    for (x,y) in [(480,120),(560,120),(480,220),(560,220),(520,170)]: pass
    # octahedral: 4 in plane + top/bottom
    for (x,y) in [(480,170),(600,170),(540,110),(540,230)]: s+=f'<circle cx="{x}" cy="{y}" r="38" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
    s+=f'<circle cx="540" cy="170" r="13" fill="{ACC}"/><text x="450" y="290" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Octahedral void: 6 spheres</text><text x="450" y="312" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">r(void) = 0.414 R, 1 per sphere</text></svg>'
    return s

def fig_radius():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    # CsCl cube schematic
    s+='<rect x="80" y="60" width="180" height="180" fill="none" stroke="#1c2430" stroke-width="2"/><line x1="80" y1="60" x2="260" y2="240" stroke="#a4134a" stroke-width="2"/>'
    for (x,y) in [(80,60),(260,60),(80,240),(260,240)]: s+=f'<circle cx="{x}" cy="{y}" r="16" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
    s+=f'<circle cx="170" cy="150" r="16" fill="{ACC}"/><text x="80" y="275" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">CsCl: body diagonal = 2r+ + 2r-</text><text x="330" y="100" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">sqrt(3) a = 2r+ + 2r-</text><text x="330" y="130" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">a = 2r-  (anions touch)</text><text x="330" y="160" font-family="IBM Plex Mono, monospace" font-size="15" fill="{ACC}">r+/r- = sqrt(3) - 1 = 0.732</text><text x="330" y="200" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">NaCl (octahedral): 0.414</text><text x="330" y="230" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">ZnS (tetrahedral): 0.225</text></svg>'
    return s

def fig_perovskite():
    s=svg_open(760,320)
    s+=f'<rect width="760" height="320" fill="{PAPER}"/>'
    # cube front
    s+='<rect x="90" y="50" width="220" height="220" fill="none" stroke="#1c2430" stroke-width="2"/><line x1="90" y1="50" x2="160" y2="10" stroke="#1c2430" stroke-width="1.5"/><line x1="310" y1="50" x2="380" y2="10" stroke="#1c2430" stroke-width="1.5"/><line x1="310" y1="270" x2="380" y2="230" stroke="#1c2430" stroke-width="1.5"/><line x1="160" y1="10" x2="380" y2="10" stroke="#1c2430" stroke-width="1.5"/><line x1="380" y1="10" x2="380" y2="230" stroke="#1c2430" stroke-width="1.5"/>'
    for (x,y) in [(90,50),(310,50),(90,270),(310,270),(160,10),(380,10),(380,230)]: s+=f'<circle cx="{x}" cy="{y}" r="12" fill="{BLUE}"/>'
    for (x,y) in [(200,50),(200,270),(90,160),(310,160)]: s+=f'<circle cx="{x}" cy="{y}" r="11" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<circle cx="200" cy="160" r="12" fill="{ACC}"/>'
    s+=f'<text x="450" y="80" font-family="IBM Plex Mono, monospace" font-size="15" fill="{BLUE}">Ca2+ corners: 8 x 1/8 = 1</text><text x="450" y="110" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">O2- face centres: 6 x 1/2 = 3</text><text x="450" y="140" font-family="IBM Plex Mono, monospace" font-size="15" fill="{ACC}">Ti4+ body centre: 1</text><text x="450" y="180" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">Formula: CaTiO3</text><text x="450" y="210" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">Ti CN 6, Ca CN 12</text><text x="450" y="250" font-family="IBM Plex Mono, monospace" font-size="14" fill="{MUT}">Shift origin by (1/2,1/2,1/2):</text><text x="450" y="275" font-family="IBM Plex Mono, monospace" font-size="14" fill="{MUT}">Ca at centre, O on edges - same cell.</text></svg>'
    return s

def fig_tolerance():
    s=svg_open(760,320)
    s+=f'<rect width="760" height="320" fill="{PAPER}"/>'
    # axis
    s+='<line x1="70" y1="250" x2="700" y2="250" stroke="#1c2430" stroke-width="2"/>'
    bands=[(70,0.71,"#dfe6ea","< 0.71"),(200,0.90,"#eef1f3","0.71-0.90"),(430,1.00,"#f2f4f6","0.90-1.00"),(560,1.10,"#eef1f3","> 1")]
    # simple bands by x mapping t 0.6->70, 1.2->700
    def X(t): return 70+(t-0.6)/0.6*630
    for (x0,x1,lab) in [(70,X(0.71),"ilmenite / other"),(X(0.71),X(0.90),"orthorhombic / rhombohedral"),(X(0.90),X(1.0),"cubic"),(X(1.0),700,"hexagonal / tetragonal")]:
        s+=f'<rect x="{x0:.0f}" y="120" width="{x1-x0:.0f}" height="130" fill="#eef1f3" stroke="#5a6572" stroke-width="1"/>'
        s+=f'<text x="{(x0+x1)/2:.0f}" y="190" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="13" fill="#1c2430">{lab}</text>'
    for t in [0.71,0.90,1.0]:
        s+=f'<line x1="{X(t):.0f}" y1="250" x2="{X(t):.0f}" y2="260" stroke="#1c2430" stroke-width="2"/><text x="{X(t):.0f}" y="280" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="14" fill="#1c2430">{t}</text>'
    s+=f'<circle cx="{X(1.0):.0f}" cy="90" r="6" fill="{ACC}"/><text x="{X(1.0):.0f}" y="70" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="14" fill="{ACC}">t = 1 ideal, SrTiO3</text><text x="70" y="40" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Goldschmidt tolerance factor t, increasing to the right</text></svg>'
    return s

def fig_cfse():
    s=svg_open(760,340)
    s+=f'<rect width="760" height="340" fill="{PAPER}"/>'
    # octahedral levels
    s+=f'<text x="80" y="40" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">Octahedral</text><line x1="80" y1="90" x2="240" y2="90" stroke="{ACC}" stroke-width="3"/><line x1="80" y1="190" x2="240" y2="190" stroke="{ACC}" stroke-width="3"/><text x="260" y="95" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">eg (+0.6 Delt_o)</text><text x="260" y="195" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">t2g (-0.4 Delt_o)</text><text x="80" y="140" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Delt_o</text>'
    s+=f'<text x="80" y="260" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">d3: t2g3, CFSE = 1.2 Delt_o</text><text x="80" y="285" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">d5 high spin: CFSE = 0</text>'
    # tetrahedral levels (inverted)
    s+=f'<text x="480" y="40" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">Tetrahedral</text><line x1="480" y1="90" x2="640" y2="90" stroke="{BLUE}" stroke-width="3"/><line x1="480" y1="150" x2="640" y2="150" stroke="{BLUE}" stroke-width="3"/><text x="480" y="115" font-family="IBM Plex Mono, monospace" font-size="13" fill="{INK}">t2 (+0.4 Delt_t)</text><text x="480" y="175" font-family="IBM Plex Mono, monospace" font-size="13" fill="{INK}">e (-0.6 Delt_t)</text><text x="480" y="260" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Delt_t = 4/9 Delt_o</text><text x="480" y="285" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Splitting is inverted</text><text x="480" y="310" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">and smaller than oct.</text></svg>'
    return s

def fig_spinel():
    s=svg_open(760,320)
    s+=f'<rect width="760" height="320" fill="{PAPER}"/>'
    s+=f'<text x="60" y="40" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">Normal spinel (A)tet(B)2oct O4</text>'
    for (x,y,lab) in [(120,120,"A2+"),(200,120,"B3+"),(280,120,"B3+")]: s+=f'<circle cx="{x}" cy="{y}" r="26" fill="none" stroke="{INK}" stroke-width="1.5"/><text x="{x}" y="{y+5}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="12" fill="{INK}">{lab}</text>'
    s+=f'<text x="60" y="180" font-family="IBM Plex Mono, monospace" font-size="13" fill="{MUT}">Td hole (1/8 filled) - Oct holes (1/2 filled)</text><text x="60" y="210" font-family="IBM Plex Mono, monospace" font-size="13" fill="{INK}">MgAl2O4, ZnFe2O4, Mn3O4</text>'
    s+=f'<text x="420" y="40" font-family="IBM Plex Mono, monospace" font-size="15" fill="{INK}">Inverse spinel B(AB)O4</text>'
    for (x,y,lab) in [(480,120,"B3+"),(560,120,"A2+"),(640,120,"B3+")]: s+=f'<circle cx="{x}" cy="{y}" r="26" fill="none" stroke="{BLUE}" stroke-width="1.5"/><text x="{x}" y="{y+5}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="12" fill="{INK}">{lab}</text>'
    s+=f'<text x="420" y="180" font-family="IBM Plex Mono, monospace" font-size="13" fill="{MUT}">Td: B3+ - Oct: A2+ + B3+</text><text x="420" y="210" font-family="IBM Plex Mono, monospace" font-size="13" fill="{INK}">Fe3O4, CoFe2O4, NiFe2O4</text><text x="60" y="270" font-family="IBM Plex Mono, monospace" font-size="14" fill="{ACC}">O2- forms a ccp / fcc array in both cases.</text></svg>'
    return s

def fig_defects():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    for r in range(3):
        for c in range(4):
            if r==1 and c==1: continue
            s+=f'<circle cx="{70+c*52}" cy="{60+r*52}" r="16" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<rect x="105" y="95" width="32" height="32" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="4 3"/><text x="60" y="250" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Schottky: paired cation + anion</text><text x="60" y="275" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">vacancies, stoichiometry kept</text>'
    for r in range(3):
        for c in range(4): s+=f'<circle cx="{430+c*52}" cy="{60+r*52}" r="16" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
    s+=f'<circle cx="534" cy="112" r="10" fill="{ACC}"/><text x="420" y="250" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">Frenkel: ion leaves its site for</text><text x="420" y="275" font-family="IBM Plex Mono, monospace" font-size="14" fill="{INK}">an interstitial site, vacancy left</text></svg>'
    return s


# ---- template ----
def page(rel, title, lede, body, crumb=""):
    depth = rel.count("/")
    prefix = "../" * depth if depth else ""
    # rel like chapters/01.../x.html -> depth 2, prefix ../../ ; index at root depth 0
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Inorganic VII</title>
<meta name="description" content="{lede}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<header class="topbar"><div class="container">
<a class="wordmark" href="{prefix}index.html">Inorganic <span>VII</span></a>
<nav><a href="{prefix}index.html">Chapters</a><a href="{prefix}chapters/01-solid-state/index.html">Solid state</a><a href="{prefix}sources.html">Sources and checks</a></nav>
</div></header>
<main class="container">
<p class="crumb">{crumb}</p>
<div class="hero"><h1>{title}</h1><p class="lede">{lede}</p></div>
{body}
</main>
<footer><div class="container">
<p>Transcribed from the handwritten notes in the uploaded 23-page PDF, then checked against the sources listed on the sources page. Where the handwriting was crossed out, cut off, or wrong, the page says so instead of silently copying it.</p>
<p><a href="{prefix}index.html">All chapters</a> · <a href="{prefix}sources.html">Sources and checks</a></p>
</div></footer>
</body>
</html>
"""

def write(rel, html):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f: f.write(html)
    print("wrote", rel)

def topic_page(rel, title, lede, body, crumb, prev=None, nxt=None):
    pager = ""
    if prev or nxt:
        pager = '<nav class="pager">' + (f'<a href="{prev[0]}">← {prev[1]}</a>' if prev else '<span></span>') + (f'<a href="{nxt[0]}">{nxt[1]} →</a>' if nxt else '') + '</nav>'
    write(rel, page(rel, title, lede, body + pager, crumb))

def check_box(title, text):
    return f'<div class="check"><h3>{title}</h3><p>{text}</p></div>'

# ---- Chapter 1 topic bodies ----
B01 = f"""
{fig("Regular order against irregular order. The drawing is a schematic, not a photograph of atoms.", fig_order())}
<div class="sheet"><h2>Crystalline</h2>
<ul><li>Definite, repeating, long range order of particles.</li><li>Definite characteristic shape.</li><li>Sharp and fixed melting point.</li><li>Breaks along a definite plane, giving smooth surfaces.</li><li>A definite value of heat of fusion.</li></ul>
<p>Examples: NaCl, diamond.</p>
<h2>Amorphous</h2>
<ul><li>Irregular; only short range order.</li><li>Irregular shape.</li><li>Softens gradually over a range of temperature.</li><li>Breaks irregularly.</li><li>No definite value of heat of fusion.</li></ul>
<p>Examples: glass, rubber, pitch.</p></div>
<p>Glass is the usual exam example of an amorphous solid: it has no long range order, so it has no sharp melting point.</p>
"""
B02 = f"""
{fig("The six lattice parameters: three edge lengths and three angles between them.", fig_axes())}
<h2>Lattice and unit cells</h2>
<p>A crystal consists of a basic structural unit, or motif, repeated in three dimensions. The basic unit may be a single atom, molecule or ion, or a group of atoms or molecules, which has an identical environment throughout the crystal. It is also called the basis of the crystal. A basis has the same stoichiometric composition as the crystal itself.</p>
<p>The lattice, or space lattice, is the geometrical idealisation of the structure. It is obtained by placing a point at the same location of each basis in the crystal; the resulting three-dimensional distribution of points in space forms the lattice. A crystal structure is generated by associating each lattice point with a basis.</p>
<div class="formula">lattice + basis = crystal structure</div>
<p>A unit cell is the smallest part of the crystal which can generate the whole crystal structure through repetition in three dimensions by simple translational displacement — stacking unit cells together along their faces without leaving any space.</p>
<h2>Lattice parameters</h2>
<p>A unit cell is described by six numbers: <span class="num">a, b, c</span>, the lengths of the three edges, and <span class="num">α, β, γ</span>, the angles between the edges (α between b and c, β between a and c, γ between a and b).</p>
"""
B03 = """
<h2>Symmetry elements</h2>
<p>A symmetry operation is a movement of a crystal after which it looks exactly the same as before. The imaginary point, line or plane about which the operation is carried out is called a symmetry element.</p>
<ol>
<li><strong>Proper rotation axes (n-fold).</strong> Rotation by 360°/n about an axis leaves the crystal unchanged. Only 1, 2, 3, 4 and 6-fold axes are possible in a periodic crystal. A 5-fold axis (and 7, 8-fold) can never exist in a crystal, because space cannot be filled by repeating a pentagon without leaving gaps.</li>
<li><strong>Plane of symmetry (m).</strong> An imaginary plane that divides the crystal into two halves, each a mirror image of the other.</li>
<li><strong>Centre of symmetry (i).</strong> A point such that any line drawn through it meets the crystal at equal distances on both sides. Also called a centre of inversion.</li>
<li><strong>Roto-inversion axes (S<sub>n</sub>).</strong> Combined rotation followed by inversion through a point. These are improper symmetry operations.</li>
</ol>
<p>Combining all possible symmetry elements gives 32 point groups, which fall into the seven crystal systems.</p>
<h2>The seven crystal systems</h2>
<table><thead><tr><th>System</th><th class="num">Bravais lattices</th><th>Cell</th><th>Symmetry</th></tr></thead><tbody>
<tr><td>Cubic</td><td class="num">3</td><td>a = b = c, α = β = γ = 90°</td><td>Four C<sub>3</sub> axes</td></tr>
<tr><td>Tetragonal</td><td class="num">2</td><td>a = b ≠ c, α = β = γ = 90°</td><td>One C<sub>4</sub> axis</td></tr>
<tr><td>Orthorhombic</td><td class="num">4</td><td>a ≠ b ≠ c, α = β = γ = 90°</td><td>Three perpendicular C<sub>2</sub> axes</td></tr>
<tr><td>Monoclinic</td><td class="num">2</td><td>a ≠ b ≠ c, α = γ = 90°, β ≠ 90°</td><td>One C<sub>2</sub> axis</td></tr>
<tr><td>Hexagonal</td><td class="num">1</td><td>a = b ≠ c, α = β = 90°, γ = 120°</td><td>One C<sub>6</sub> axis</td></tr>
<tr><td>Rhombohedral</td><td class="num">1</td><td>a = b = c, α = β = γ ≠ 90°</td><td>One C<sub>3</sub> axis</td></tr>
<tr><td>Triclinic</td><td class="num">1</td><td>a ≠ b ≠ c, α ≠ β ≠ γ ≠ 90°</td><td>None (C<sub>1</sub>)</td></tr>
</tbody></table>
<p>The lattice counts add to 14 Bravais lattices in total: 3 + 2 + 4 + 2 + 1 + 1 + 1 = 14.</p>
"""
B04 = f"""
{fig("Simple cubic: one atom per cell. The cube is a schematic; atoms are drawn as points, not to scale.", cube_svg("sc","Simple cubic (primitive)"))}
<p>In a simple or primitive cubic lattice the atoms are present at all eight corners of the unit cell. Each corner is shared by eight adjacent cubic cells, so each corner contributes 1/8 of an atom.</p>
<div class="formula">8 corners × 1/8 = 1 atom per unit cell</div>
{fig("Body-centred cubic: the centre atom belongs entirely to this cell.", cube_svg("bcc","Body-centred cubic"))}
<p>In a body-centred cubic lattice the atoms are at all the corners and at the centre of the unit cell. The centre atom is not shared by any other cell.</p>
<div class="formula">8 × 1/8 + 1 = 2 atoms per unit cell</div>
{fig("Face-centred cubic: 14 lattice points in the drawing, 4 atoms per cell after sharing is counted.", cube_svg("fcc","Face-centred cubic"))}
<p>In a face-centred cubic lattice the atoms are at all eight corners and at the centre of each face. There is no atom at the centre of the cube. Each face-centre atom is shared by two adjacent cells, so it contributes 1/2.</p>
<div class="formula">Corners: 8 × 1/8 = 1 &nbsp;·&nbsp; Faces: 6 × 1/2 = 3 &nbsp;·&nbsp; Total = 4 atoms per unit cell</div>
"""
B05 = f"""
{fig("One dimension, then two: square packing is less efficient than hexagonal packing.", fig_packing())}
<h2>Close packing in one dimension</h2>
<p>Spheres are placed in a row, each touching two neighbours. Coordination number = 2.</p>
<h2>Close packing in two dimensions</h2>
<p><strong>Square packing (AAA type).</strong> Rows are placed one above the other so that spheres sit directly on top of each other. It is less efficient. Coordination number = 4.</p>
<p><strong>Hexagonal packing (ABAB type).</strong> The second row sits in the depressions (holes) of the first row. This is the closest packing in two dimensions. Each sphere touches six neighbours. Coordination number = 6.</p>
"""
B06 = f"""
{fig("Third layer repeats the first (ABAB, hcp) or takes a new position (ABCABC, ccp).", fig_stacking())}
<p>To build a crystal in three dimensions, close-packed layers are stacked one on top of the other in a regular way. Consider a sphere S in the first layer: spheres in the next layer nestle in the notches around it. In the second layer there is a notch over S, but there are also notches over other positions. The third layer may repeat the arrangement of the first layer, or it may not.</p>
<ul><li><strong>If the third layer repeats the first,</strong> there are only two kinds of layer, A and B, and the pattern is ABAB… This is the hexagonal close-packed (hcp) structure.</li>
<li><strong>If the third layer does not repeat the first,</strong> it is denoted C, and the pattern is ABCABC… This is the cubic close-packed (ccp) structure, also called face-centred cubic (fcc).</li></ul>
<h2>Hexagonal close packing</h2>
<p>In ABA stacking, the seven spheres in both the first layer (A) and the third layer occupy simple hexagonal lattice points, while the three spheres of the second layer (B) are placed at the corners of an equilateral triangle midway between the two parallel hexagonal planes, so that the nearest environment of every sphere becomes identical. The height of the unit cell, c, is the distance between the first and third layers; a is the length of the side of the hexagon.</p>
<p>A sphere is hexagonally surrounded by six spheres in its own plane, and touches three spheres below the plane and three above it. Coordination number = 6 + 3 + 3 = 12.</p>
<div class="kv"><div><span class="num">74%</span><span>Packing efficiency, hcp</span></div><div><span class="num">12</span><span>Coordination number, hcp</span></div><div><span class="num">ABAB…</span><span>Stacking sequence</span></div></div>
<h2>Cubic close packing</h2>
<p>In ccp / fcc the stacking sequence is ABCABC… The structure has cubic symmetry. In addition to the eight spheres at the eight corners of the cube, there is one sphere at the centre of each of the six faces, hence the name face-centred cubic. Each sphere is surrounded by 12 other nearest spheres, so the coordination number is 12. Packing efficiency is 74%.</p>
<h2>Common features of hcp and ccp</h2>
<ul><li>Coordination number is 12 in both.</li><li>Packing efficiency is 74% in both — 74% of the total volume of the unit cell is occupied by the spheres.</li></ul>
<h2>Body-centred cubic, for comparison</h2>
<p>Another common arrangement in a few metals is body-centred cubic (bcc). The second layer sits in the notches of the first and the pattern repeats ABAB…, but the coordination number is 8, compared with 12 in a close-packed pattern.</p>
""" + check_box("A line to read with care", "The notes say, in the bcc paragraph, that the number of neighbours around any sphere is four. That is the in-plane count in the drawing, not the coordination number of bcc. The coordination number of bcc is 8, as the notes themselves state in the next sentence.")

B07 = f"""
{fig("A tetrahedral void is bounded by four spheres; an octahedral void by six.", fig_voids())}
<p>The empty spaces left between packed spheres are called interstitial voids. Two types matter.</p>
<table><thead><tr><th>Void</th><th>Surrounded by</th><th class="num">Per sphere</th><th class="num">Largest sphere that fits</th></tr></thead><tbody>
<tr><td>Tetrahedral</td><td>Four spheres at the corners of a tetrahedron</td><td class="num">2</td><td class="num">0.225 R</td></tr>
<tr><td>Octahedral</td><td>Six spheres at the corners of an octahedron</td><td class="num">1</td><td class="num">0.414 R</td></tr>
</tbody></table>
<p>R is the radius of the packed sphere. An fcc unit cell has 4 atoms, so it has 8 tetrahedral voids and 4 octahedral voids.</p>
{fig("CsCl geometry: the cation touches anions along the body diagonal.", fig_radius())}
<h2>Radius ratio rule</h2>
<p>The radius ratio r<sup>+</sup>/r<sup>−</sup> predicts which hole a cation occupies, and therefore its coordination number. The limits are the ratios at which the cation just touches the surrounding anions.</p>
<table><thead><tr><th class="num">r<sup>+</sup>/r<sup>−</sup></th><th class="num">Coordination</th><th>Geometry</th><th>Example</th></tr></thead><tbody>
<tr><td class="num">0.225 – 0.414</td><td class="num">4</td><td>Tetrahedral</td><td>ZnS</td></tr>
<tr><td class="num">0.414 – 0.732</td><td class="num">6</td><td>Octahedral</td><td>NaCl</td></tr>
<tr><td class="num">0.732 – 1.000</td><td class="num">8</td><td>Cubic</td><td>CsCl</td></tr>
</tbody></table>
<h2>Worked limits, as written in the notes</h2>
<p><strong>CsCl, 8:8.</strong> Side of cube a = 2r<sup>−</sup>. Body diagonal √3 a = 2r<sup>+</sup> + 2r<sup>−</sup>. Hence √3 = (r<sup>+</sup> + r<sup>−</sup>)/r<sup>−</sup>, so r<sup>+</sup>/r<sup>−</sup> = √3 − 1 = 1.732 − 1 = 0.732.</p>
<p><strong>NaCl, octahedral, 6:6.</strong> Face diagonal √2 a = 2r<sup>+</sup> + 2r<sup>−</sup>, with a = 2r<sup>−</sup>. Hence r<sup>+</sup>/r<sup>−</sup> = √2 − 1 = 0.414.</p>
<p><strong>ZnS, tetrahedral, 4:4.</strong> Half the body diagonal gives r<sup>+</sup> + r<sup>−</sup> = √3 a/2, with the face diagonal √2 a = 2r<sup>−</sup>. The limiting ratio is 0.225.</p>
""" + check_box("Checked, with one correction to the working", "The three limiting values — 0.225, 0.414 and 0.732 — are correct and match the standard radius-ratio table. The intermediate algebra on the tetrahedral page of the notes is heavily crossed out and does not cleanly give 0.225 as written, so this page shows the standard result rather than reproducing that crossed-out line. The radius-ratio rule is a guide, not a law: it predicts only about half of the alkali halide structures correctly.")

B08 = """
<h2>Diamond cubic unit cell</h2>
<p>Diamond is a special type of fcc lattice. Four additional atoms are present within the face-centred cube, distributed symmetrically so that each one has an identical environment. They sit at the centres of alternating small cubes within the fcc cell — that is, at 4 of the 8 alternative tetrahedral holes. In this arrangement every atom is tetrahedrally surrounded.</p>
<p>Total lattice points per diamond cubic unit cell:</p>
<div class="formula">n = 1/8 × Nc + 1/2 × Nf + Ni = 1/8 × 8 + 1/2 × 6 + 4 = 1 + 3 + 4 = 8</div>
<p>The four internal lattice points lie along the four body diagonals of the fcc unit cell, each one a quarter of the way along a body diagonal from a corner. Taking a corner atom and the nearest atom along the body diagonal:</p>
<div class="formula">2r = 1/4 × √3 a &nbsp;·&nbsp; a = 8r / √3</div>
<p>Percentage of space actually occupied:</p>
<div class="formula">[8 × (4/3)πr³ × 100] / [(8/√3 r)³] = 34%</div>
<div class="kv"><div><span class="num">34%</span><span>Space occupied, diamond</span></div><div><span class="num">66%</span><span>Space unoccupied</span></div><div><span class="num">8</span><span>Atoms per unit cell</span></div><div><span class="num">4</span><span>Coordination number</span></div></div>
<p>Compare fcc metals at 74%: diamond is much more open, because every atom is held in a directional tetrahedral network rather than in close packing.</p>
"""

B09 = """
<h2>AB type — four structures</h2>
<p>NaCl, CsCl, ZnS (zinc blende) and ZnS (wurtzite).</p>
<table><thead><tr><th>Structure</th><th class="num">Coordination</th><th>Anion array</th><th>Cation site</th></tr></thead><tbody>
<tr><td><strong>NaCl</strong> (rock salt)</td><td class="num">6:6</td><td>fcc Cl<sup>−</sup></td><td>Na<sup>+</sup> in all octahedral holes; 4 Na<sup>+</sup> and 4 Cl<sup>−</sup> per cell</td></tr>
<tr><td><strong>CsCl</strong></td><td class="num">8:8</td><td>Simple cubic Cl<sup>−</sup></td><td>Cs<sup>+</sup> at the body centre; 1 of each per cell</td></tr>
<tr><td><strong>ZnS, zinc blende</strong></td><td class="num">4:4</td><td>fcc S<sup>2−</sup></td><td>Zn<sup>2+</sup> in half the tetrahedral holes; 4 of each per cell</td></tr>
<tr><td><strong>ZnS, wurtzite</strong></td><td class="num">4:4</td><td>hcp S<sup>2−</sup></td><td>Zn<sup>2+</sup> in half the tetrahedral holes</td></tr>
</tbody></table>
<p>Zinc blende and wurtzite have the same 4:4 coordination and the same stoichiometry; they differ in the stacking of the anion array — ccp in zinc blende, hcp in wurtzite.</p>
"""
B10 = """
<h2>Fluorite, CaF<sub>2</sub> — 8:4</h2>
<p>Ca<sup>2+</sup> ions are arranged at the corners and at the centres of the faces of a cubic unit cell, and F<sup>−</sup> ions are at the centres of the eight small cubes into which the cell may be divided. Each Ca<sup>2+</sup> is coordinated by 8 F<sup>−</sup> neighbours at the corners of a cube, while each F<sup>−</sup> has 4 Ca<sup>2+</sup> neighbours.</p>
<p>This is the only structure in the notes with 8:4 coordination. The reverse structure, antifluorite, is taken by oxides such as Li<sub>2</sub>O and Na<sub>2</sub>O, with the cation and anion positions exchanged.</p>
<h2>Rutile, TiO<sub>2</sub> — 6:3</h2>
<p>The cation is octahedrally surrounded by six anions, while the anion (O<sup>2−</sup>) is trigonally surrounded by three cations. Rutile has a low-symmetry anion sublattice that fits neither a simple cubic nor an fcc lattice. The cation sublattice is a distorted body-centred cube, because one side of the cube differs from the others — the cation sublattice is actually body-centred tetragonal. The unit cell is tetragonal.</p>
"""
B11 = f"""
{fig("Schottky: vacancies in pairs. Frenkel: a displaced ion and the vacancy it leaves.", fig_defects())}
<p>There are different types of imperfection, such as point, surface and volume imperfections. Point defects are zero-dimensional, occurring at a single lattice site; extended defects may be one, two or three-dimensional (for example a stacking fault). Defects can also be classified as intrinsic and extrinsic.</p>
<p>Intrinsic defects (Schottky and Frenkel defects) occur in the pure crystal, while extrinsic defects originate from impurities present in the crystal. Defects can largely influence physical properties such as mechanical strength, electrical conductivity, colour and chemical reactivity. In ionic crystals only point imperfections are important.</p>
<h2>Point imperfections</h2>
<p>Point imperfections are very often referred to as zero-dimensional imperfections. They are localised in point-like regions and may arise due to:</p>
<ol><li>A vacancy in a lattice site.</li><li>A substitutional impurity.</li><li>Occurrence of a constituent ion in an interstitial space.</li><li>Non-stoichiometric proportions of the constituent ions.</li></ol>
<table><thead><tr><th>Defect</th><th>What happens</th><th>Stoichiometry</th></tr></thead><tbody>
<tr><td><strong>Schottky</strong></td><td>Equal numbers of cation and anion vacancies</td><td>Kept</td></tr>
<tr><td><strong>Frenkel</strong></td><td>An ion moves to an interstitial site, leaving a vacancy</td><td>Kept</td></tr>
</tbody></table>
""" + check_box("A question in the margin of the notes", "The notes ask why a KCl crystal looks violet in excess potassium, while excess lithium makes LiCl pink. That is an F-centre (colour centre): excess metal gives electrons trapped in anion vacancies, and the trapped electron absorbs visible light. The colour depends on the size of the vacancy, hence on the host crystal — violet in KCl, pink in LiCl. The notes mark this as a question to return to, so it is kept as a question here, with the standard answer given.")

B12 = f"""
{fig("Perovskite CaTiO3: Ca on the corners, O on the face centres, Ti at the body centre.", fig_perovskite())}
<h2>Perovskite, CaTiO<sub>3</sub></h2>
<p>Named after the mineral CaTiO<sub>3</sub>. O<sup>2−</sup> ions, along with the larger cation (Ca<sup>2+</sup>), form a ccp array in which the octahedral holes formed by O<sup>2−</sup> are occupied by the smaller cation (Ti<sup>4+</sup>). In the unit cell, the eight corners of the cube are occupied by Ca<sup>2+</sup>, O<sup>2−</sup> are placed at the centres of the six faces, and Ti<sup>4+</sup> is placed at the centre of the cube.</p>
<div class="formula">Ca2+: 8 × 1/8 = 1 &nbsp;·&nbsp; O2−: 6 × 1/2 = 3 &nbsp;·&nbsp; Ti4+: 1 &nbsp;·&nbsp; CaTiO3</div>
<p>The structure can also be interpreted in terms of ReO<sub>3</sub>: the Re positions are occupied by Ti<sup>4+</sup>, while Ca<sup>2+</sup> occupies the centre of the cube. Ti<sup>4+</sup> is octahedrally surrounded by O<sup>2−</sup>, while Ca<sup>2+</sup> is surrounded by 12 O<sup>2−</sup> ions.</p>
<table><thead><tr><th>Charge combination</th><th>Examples</th></tr></thead><tbody>
<tr><td>A<sup>II</sup> B<sup>IV</sup> O<sub>3</sub></td><td>A = Ca, Sr, Ba; B = Ti, Zr, Ge, Sn</td></tr>
<tr><td>A<sup>III</sup> B<sup>III</sup> O<sub>3</sub></td><td>A = La; B = Al, Ti, Cr, Mn</td></tr>
<tr><td>A<sup>I</sup> B<sup>V</sup> O<sub>3</sub></td><td>A = Na, K; B = Nb, Ta</td></tr>
</tbody></table>
""" + check_box("One entry corrected", "The notes list Cr among the A-site cations for A<sup>II</sup>B<sup>IV</sup>O<sub>3</sub>. Chromium is not a normal A-site cation in that family; the A site is Ca, Sr or Ba. The table above uses the corrected list.")
B12 += """
<h2>Ilmenite, FeTiO<sub>3</sub></h2>
<p>Named after the mineral ilmenite. It adopts the structure of corundum (α-Al<sub>2</sub>O<sub>3</sub>). In a hexagonal close-packed array of O<sup>2−</sup> ions, two-thirds of the octahedral holes are occupied — one-third by Fe<sup>2+</sup> and one-third by Ti<sup>4+</sup>, in alternating layers.</p>
<table><thead><tr><th>Charge combination</th><th>Examples</th></tr></thead><tbody>
<tr><td>A<sup>II</sup> B<sup>IV</sup> O<sub>3</sub></td><td>A = Fe, Cd, Mg, Co; B = Ti</td></tr>
<tr><td>A<sup>III</sup> B<sup>III</sup> O<sub>3</sub></td><td>Corundum-type oxides</td></tr>
<tr><td>A<sup>I</sup> B<sup>V</sup> O<sub>3</sub></td><td>A = Li; B = Nb (LiNbO<sub>3</sub>)</td></tr>
</tbody></table>
""" + check_box("Corrected from the handwriting", "The ilmenite paragraph in the notes is crossed out and partly illegible, and one crossed-out word reads as Fe<sup>3+</sup>. Ilmenite is Fe<sup>II</sup>Ti<sup>IV</sup>O<sub>3</sub>: Fe<sup>2+</sup>, not Fe<sup>3+</sup>. The two cations together fill two-thirds of the octahedral holes in the hcp oxide array, as in corundum.")

B13 = f"""
{fig("Goldschmidt tolerance factor: the structure that forms as t moves away from 1.", fig_tolerance())}
<p>The Goldschmidt tolerance factor (t) is a dimensionless number used to predict the stability of a crystal and its symmetry in ABO<sub>3</sub> perovskites. It relates the ionic radii of the A-site cation (r<sub>A</sub>), the B-site cation (r<sub>B</sub>) and the anion (r<sub>O</sub>).</p>
<div class="formula">t = (rA + rO) / [ √2 (rB + rO) ]</div>
<p>When t deviates from the ideal value 1, the crystal lattice experiences a steric mismatch, driving structural distortion to lower-symmetry phases.</p>
<table><thead><tr><th class="num">t</th><th>Structure</th><th>Why</th><th>Example</th></tr></thead><tbody>
<tr><td class="num">&gt; 1</td><td>Hexagonal or tetragonal</td><td>A-site cation too large; A site overbonded</td><td>BaTiO<sub>3</sub> (t ≈ 1.06), BaNiO<sub>3</sub></td></tr>
<tr><td class="num">0.9 – 1</td><td>Cubic</td><td>A, B and O packed ideally; BO<sub>6</sub> octahedra untilted</td><td>SrTiO<sub>3</sub> (t ≈ 1.00)</td></tr>
<tr><td class="num">0.71 – 0.9</td><td>Orthorhombic / rhombohedral</td><td>A-site cation too small; BO<sub>6</sub> octahedra tilt and rotate</td><td>CaTiO<sub>3</sub>, GdFeO<sub>3</sub></td></tr>
<tr><td class="num">&lt; 0.71</td><td>Different structures</td><td>Perovskite framework cannot be sustained</td><td>Ilmenite, FeTiO<sub>3</sub></td></tr>
</tbody></table>
""" + check_box("Checked against the standard table", "The ranges in the table are the standard Goldschmidt ranges. The notes give a narrower rule of thumb — collapse below t = 0.8 or above t = 1.05, with MgTiO<sub>3</sub> (t = 0.81 in the notes) as a non-perovskite example. That is a usable classroom approximation, but it is not the standard boundary: perovskites are known down to about t = 0.71, and CaTiO<sub>3</sub> itself is orthorhombic, not cubic, at room temperature.")

B14 = f"""
{fig("Octahedral splitting is larger and inverted relative to tetrahedral splitting.", fig_cfse())}
<p>This is the page in the photograph you sent. It is the last page of the notes, and it states the rule that decides normal against inverse spinel.</p>
<div class="sheet"><p><strong>From the notes, transcribed:</strong> “This generally takes place [in] transition metal oxide. Generally the site selection is governed by the relative change of CFSE (Crystal Field Stabilization Energy) in occupying the Oct and Td holes.”</p></div>
<p>The crossed-out words in the photograph are “crystal” (before CFSE) and “octa” (before “oct”). The sentence is about spinel oxides, AB<sub>2</sub>O<sub>4</sub>.</p>
<h2>Normal spinel</h2>
<p>Named after the mineral spinel, MgAl<sub>2</sub>O<sub>4</sub>. It consists of a ccp array of oxide ions in which the divalent metal ion (Mg<sup>2+</sup>) occupies 1/8 of the tetrahedral holes and the trivalent metal ion (Al<sup>3+</sup>) occupies 1/2 of the octahedral holes. In a ccp anion sublattice there is one octahedral hole and two tetrahedral holes per anion. There are four oxides per formula unit, and consequently four octahedral holes and eight tetrahedral holes.</p>
<div class="formula">Normal: (AII)tet (BIII)2oct O4</div>
<h2>Inverse spinel</h2>
<p>In an inverse spinel, half of the B ions occupy 1/8 of the tetrahedral holes, and A and the other half of B occupy 1/2 of the octahedral holes in the ccp array of O<sup>2−</sup>.</p>
<div class="formula">Inverse: BIII tet [ AII BIII ]oct O4</div>
{fig("Normal against inverse: which cation sits in which hole.", fig_spinel())}
<h2>Why CFSE decides it</h2>
<p>For transition-metal oxide spinels, O<sup>2−</sup> is a weak-field ligand, so the ions are usually high spin. The structure that forms is the one with the larger total CFSE. The octahedral site preference energy (OSPE) is CFSE(oct) − CFSE(tet), with Δ<sub>t</sub> = 4/9 Δ<sub>o</sub>. Its size depends on the d-electron count:</p>
<table><thead><tr><th>d count (high spin)</th><th class="num">CFSE oct (Δ<sub>o</sub>)</th><th class="num">CFSE tet (Δ<sub>o</sub>)</th><th class="num">OSPE (Δ<sub>o</sub>)</th></tr></thead><tbody>
<tr><td>d<sup>0</sup>, d<sup>5</sup>, d<sup>10</sup></td><td class="num">0</td><td class="num">0</td><td class="num">0</td></tr>
<tr><td>d<sup>1</sup>, d<sup>6</sup></td><td class="num">0.40</td><td class="num">0.27</td><td class="num">0.13</td></tr>
<tr><td>d<sup>2</sup>, d<sup>7</sup></td><td class="num">0.80</td><td class="num">0.53</td><td class="num">0.27</td></tr>
<tr><td>d<sup>3</sup>, d<sup>8</sup></td><td class="num">1.20</td><td class="num">0.36</td><td class="num">0.84</td></tr>
<tr><td>d<sup>4</sup>, d<sup>9</sup></td><td class="num">0.60</td><td class="num">0.18</td><td class="num">0.42</td></tr>
</tbody></table>
<p>So d<sup>3</sup> and d<sup>8</sup> have the strongest octahedral preference, d<sup>0</sup>, d<sup>5</sup> and d<sup>10</sup> have none, and the rest fall in between.</p>
<h2>Worked examples from the notes</h2>
<table><thead><tr><th>Spinel</th><th>Distribution</th><th>Why</th></tr></thead><tbody>
<tr><td>MgAl<sub>2</sub>O<sub>4</sub></td><td>Normal</td><td>Both non-transition metals; CFSE = 0. The more highly charged Al<sup>3+</sup> prefers the octahedral site.</td></tr>
<tr><td>ZnFe<sub>2</sub>O<sub>4</sub></td><td>Normal</td><td>Zn<sup>2+</sup> is d<sup>10</sup> and Fe<sup>3+</sup> is d<sup>5</sup>; both have zero CFSE, and small Zn<sup>2+</sup> fits the tetrahedral site.</td></tr>
<tr><td>Mn<sub>3</sub>O<sub>4</sub></td><td>Normal</td><td>Mn<sup>2+</sup> is high-spin d<sup>5</sup> (CFSE 0); Mn<sup>3+</sup> is d<sup>4</sup> and takes the octahedral site.</td></tr>
<tr><td>Fe<sub>3</sub>O<sub>4</sub></td><td>Inverse: Fe<sup>3+</sup>[Fe<sup>2+</sup>Fe<sup>3+</sup>]O<sub>4</sub></td><td>Fe<sup>3+</sup> is d<sup>5</sup> (CFSE 0 in either site); Fe<sup>2+</sup> is d<sup>6</sup> and prefers octahedral.</td></tr>
<tr><td>CoFe<sub>2</sub>O<sub>4</sub>, NiFe<sub>2</sub>O<sub>4</sub></td><td>Inverse</td><td>Co<sup>2+</sup> (d<sup>7</sup>) and Ni<sup>2+</sup> (d<sup>8</sup>) have a strong octahedral preference over Fe<sup>3+</sup> (d<sup>5</sup>).</td></tr>
<tr><td>FeCr<sub>2</sub>O<sub>4</sub></td><td>Normal</td><td>Cr<sup>3+</sup> is d<sup>3</sup>, with the largest octahedral preference (0.84 Δ<sub>o</sub>).</td></tr>
<tr><td>Co<sub>3</sub>O<sub>4</sub></td><td>Normal</td><td>Co<sup>3+</sup> is low-spin d<sup>6</sup> with very high CFSE in the octahedral site.</td></tr>
</tbody></table>
""" + check_box("Verified", "The rule on this page is correct and is the standard explanation: for transition-metal oxide spinels, normal against inverse is driven primarily by the CFSE of the ions in tetrahedral and octahedral sites. The worked examples above follow the same rule, with the OSPE values taken from the standard high-spin table.")

TOPICS = [
 ("01-crystalline-amorphous", "Crystalline and amorphous solids", B01),
 ("02-lattice-unit-cells", "Lattice and unit cells", B02),
 ("03-symmetry-seven-systems", "Symmetry and the seven crystal systems", B03),
 ("04-atoms-per-unit-cell", "Atoms per unit cell: SC, BCC, FCC", B04),
 ("05-close-packing-1d-2d", "Close packing in 1D and 2D", B05),
 ("06-hcp-ccp", "HCP and CCP in three dimensions", B06),
 ("07-voids-radius-ratio", "Voids and the radius ratio rule", B07),
 ("08-diamond-cubic", "Diamond cubic", B08),
 ("09-ionic-crystals-ab", "Ionic crystals of AB type", B09),
 ("10-ionic-crystals-ab2", "Ionic crystals of AB2 type", B10),
 ("11-point-defects", "Point defects", B11),
 ("12-perovskite-ilmenite", "Perovskite and ilmenite", B12),
 ("13-tolerance-factor", "Goldschmidt tolerance factor", B13),
 ("14-spinel-cfse", "Normal and inverse spinel: CFSE", B14),
]

def main():
    # chapter 1 index
    items = "".join(f'<li><a href="{slug}.html">{title}</a></li>' for slug, title, _ in TOPICS)
    ch1_body = f"""
<div class="sheet"><p>From the 23-page handwritten PDF: solid state, from crystalline and amorphous solids through close packing, ionic structures, defects, perovskite and spinel. Fourteen topic pages, in the order the notes take them.</p></div>
<ol class="topic-list">{items}</ol>
<p><a class="btn btn-primary" href="01-crystalline-amorphous.html">Start at the first topic</a></p>
"""
    write("chapters/01-solid-state/index.html", page("chapters/01-solid-state/index.html", "Solid state and crystal structures", "Fourteen topics, transcribed from your 23-page notes and checked against standard sources.", ch1_body, '<a href="../../index.html">Chapters</a> / Chapter 1'))
    # topic pages
    for i, (slug, title, body) in enumerate(TOPICS):
        prev = (TOPICS[i-1][0]+".html", TOPICS[i-1][1]) if i>0 else ("index.html", "Chapter 1")
        nxt = (TOPICS[i+1][0]+".html", TOPICS[i+1][1]) if i < len(TOPICS)-1 else (None, None)
        nxt = nxt if nxt[0] else None
        topic_page(f"chapters/01-solid-state/{slug}.html", title, "Chapter 1 · Solid state and crystal structures", body, f'<a href="../../index.html">Chapters</a> / <a href="index.html">Chapter 1 · Solid state</a> / Topic {i+1} of {len(TOPICS)}', prev, nxt)
    # planned chapters
    planned = [
        ("02-crystal-field-theory", "Crystal field theory in depth", "Splitting in octahedral, tetrahedral and square-planar fields, spectrochemical series, high and low spin, CFSE calculations, Jahn-Teller distortion, magnetic moments."),
        ("03-coordination-compounds", "Coordination compounds", "Nomenclature, isomerism, Werner theory, chelate effect, stability constants, substitution mechanisms."),
        ("04-organometallic-catalysis", "Organometallic chemistry and catalysis", "18-electron rule, metal carbonyls, oxidative addition and reductive elimination, homogeneous catalysis."),
        ("05-bioinorganic", "Bioinorganic chemistry", "Metalloproteins, haemoglobin and myoglobin, electron transfer, metal ions in medicine."),
        ("06-solid-state-materials", "Solid-state materials and applications", "Band theory, semiconductors, superconductors, magnetic materials, zeolites and MOFs."),
    ]
    for slug, title, desc in planned:
        num = slug[:2]
        body = f'<div class="sheet"><p>{desc}</p></div><div class="check"><h3>Awaiting notes</h3><p>This chapter is part of the site structure, but no handwritten pages for it were in the upload. Upload the pages for this chapter and they will be transcribed, checked and added as topic pages in the same format as Chapter 1.</p></div><p><a class="btn" href="../01-solid-state/index.html">Read Chapter 1 instead</a></p>'
        write(f"chapters/{slug}/index.html", page(f"chapters/{slug}/index.html", title, "Planned chapter — topic pages will be added from your notes.", body, f'<a href="../../index.html">Chapters</a> / Chapter {num}'))
    # home
    home_body = """
<div class="sheet"><p>Your handwritten inorganic chemistry notes, set as a readable reference: one chapter per subject, one page per topic, figures redrawn so they can be checked. Chapter 1 is complete from the 23 pages you uploaded. The other chapters are ready to fill. Upload their pages and they join the same structure.</p></div>
<div class="kv"><div><span class="num">14</span><span>Topic pages in Chapter 1</span></div><div><span class="num">23</span><span>Handwritten pages transcribed</span></div><div><span class="num">6</span><span>Chapters in the site</span></div></div>
<ol class="chapter-list">
<li><div><h2><a href="chapters/01-solid-state/index.html">1 · Solid state and crystal structures</a></h2><p>Crystalline and amorphous solids, lattices, symmetry, close packing, voids, radius ratio, ionic structures, defects, perovskite, spinel and CFSE.</p></div><span class="status">Complete</span></li>
<li><div><h2><a href="chapters/02-crystal-field-theory/index.html">2 · Crystal field theory in depth</a></h2><p>Splitting, spectrochemical series, spin states, CFSE, Jahn-Teller.</p></div><span class="status">Awaiting notes</span></li>
<li><div><h2><a href="chapters/03-coordination-compounds/index.html">3 · Coordination compounds</a></h2><p>Nomenclature, isomerism, stability, mechanisms.</p></div><span class="status">Awaiting notes</span></li>
<li><div><h2><a href="chapters/04-organometallic-catalysis/index.html">4 · Organometallic chemistry and catalysis</a></h2><p>Carbonyls, the 18-electron rule, catalytic cycles.</p></div><span class="status">Awaiting notes</span></li>
<li><div><h2><a href="chapters/05-bioinorganic/index.html">5 · Bioinorganic chemistry</a></h2><p>Metalloproteins, oxygen transport, electron transfer.</p></div><span class="status">Awaiting notes</span></li>
<li><div><h2><a href="chapters/06-solid-state-materials/index.html">6 · Solid-state materials and applications</a></h2><p>Bands, semiconductors, superconductors, porous solids.</p></div><span class="status">Awaiting notes</span></li>
</ol>
<p><a class="btn btn-primary" href="chapters/01-solid-state/14-spinel-cfse.html">Spinel and CFSE</a> <a class="btn" href="sources.html">How notes were checked</a></p>
"""
    write("index.html", page("index.html", "Solid state, drawn clearly", "Inorganic chemistry notes, chapter by chapter, with the figures redrawn and the handwriting checked.", home_body, "Home"))
    # sources
    sources_body = """
<div class="sheet"><p>Every page was transcribed from the rendered PDF pages first, then checked. Where the handwriting and the standard source disagreed, the site keeps the standard result and says what the notes said.</p></div>
<h2>What was transcribed</h2>
<p>The uploaded PDF, <span class="num">PDF_Gallery_20261115_202140.pdf</span>, 23 pages of handwritten notes. Page 11 is a duplicate photograph of page 10, so it adds no new topic. The single photograph you sent in chat is page 23 of that PDF.</p>
<h2>What was checked, and where</h2>
<table><thead><tr><th>Claim in the notes</th><th>Result</th><th>Source</th></tr></thead><tbody>
<tr><td>Normal spinel: A<sup>2+</sup> in 1/8 Td, B<sup>3+</sup> in 1/2 Oct; inverse: B(AB)O<sub>4</sub></td><td>Correct</td><td>LibreTexts, Spinel, Perovskite, and Rutile Structures</td></tr>
<tr><td>Site selection governed by relative CFSE in Oct and Td holes</td><td>Correct — the standard explanation for transition-metal oxide spinels</td><td>LibreTexts, Spinel, Perovskite, and Rutile Structures</td></tr>
<tr><td>OSPE: d<sup>3</sup>/d<sup>8</sup> 0.84, d<sup>4</sup>/d<sup>9</sup> 0.42, d<sup>2</sup>/d<sup>7</sup> 0.27, d<sup>1</sup>/d<sup>6</sup> 0.13, d<sup>0</sup>/d<sup>5</sup>/d<sup>10</sup> 0 (Δ<sub>o</sub>)</td><td>Correct, high spin, Δ<sub>t</sub> = 4/9 Δ<sub>o</sub></td><td>LibreTexts, Octahedral vs. Tetrahedral Geometries</td></tr>
<tr><td>Goldschmidt t: &gt;1 hexagonal/tetragonal, 0.9–1 cubic, 0.71–0.9 orthorhombic/rhombohedral, &lt;0.71 other</td><td>Correct; the notes’ 0.8 / 1.05 limits are a classroom approximation</td><td>Wikipedia, Goldschmidt tolerance factor</td></tr>
<tr><td>Perovskite: Ca corners, O face centres, Ti body centre; Ti CN 6, Ca CN 12</td><td>Correct</td><td>Wikipedia, Perovskite; University of Sydney, CHEM1902 2007-N-6</td></tr>
<tr><td>Ilmenite FeTiO<sub>3</sub>, corundum-type, 2/3 of octahedral holes filled</td><td>Correct, with Fe<sup>2+</sup> (not Fe<sup>3+</sup> as one crossed-out word suggested)</td><td>LibreTexts / standard corundum description</td></tr>
<tr><td>Radius ratios 0.225 / 0.414 / 0.732</td><td>Correct</td><td>LibreTexts, Structures of Simple Binary Compounds</td></tr>
<tr><td>Diamond packing efficiency 34%</td><td>Correct</td><td>Standard calculation, a = 8r/√3</td></tr>
<tr><td>HCP and CCP packing efficiency 74%, CN 12</td><td>Correct</td><td>Standard close-packing result</td></tr>
</tbody></table>
<h2>Corrections made on the site</h2>
<ul><li>Ilmenite: Fe<sup>2+</sup>, not Fe<sup>3+</sup>.</li><li>Perovskite A-site list: Cr removed from the A<sup>II</sup> list.</li><li>Tetrahedral radius-ratio working: the crossed-out algebra in the notes was not reproduced; the standard limiting value 0.225 is given.</li><li>Tolerance-factor limits: the standard 0.71–1.0 ranges are given, with the notes’ 0.8 / 1.05 rule marked as an approximation.</li><li>BCC paragraph: the in-plane neighbour count of four is not the bcc coordination number, which is 8.</li></ul>
<h2>Design</h2>
<p>Built with the Hallmark design skill (nutlope/hallmark, installed with <span class="num">npx skills add nutlope/hallmark -g</span>), theme Almanac: cool slate stock, pale printed sheet, blue-black ink, Hanken Grotesk heads over Newsreader prose, mono figures, one magenta accent. All figures are inline SVG drawn for this site — no photographs of the handwritten pages are reproduced, so the text is searchable.</p>
"""
    write("sources.html", page("sources.html", "Sources and checks", "How the handwriting was read, what was verified online, and what was corrected.", sources_body, '<a href="index.html">Chapters</a> / Sources'))
    # deploy files
    with open(os.path.join(ROOT, "wrangler.toml"), "w", encoding="utf-8") as f:
        f.write('name = "inorganicvii"\ncompatibility_date = "2026-11-15"\npages_build_output_dir = "."\n')
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write("# inorganicvii\n\nStatic multi-page notes site for Cloudflare Pages.\nProduction URL: https://inorganicvii.pages.dev\n\n## Structure\n\n- `index.html` — chapter list\n- `chapters/01-solid-state/` — 14 topic pages, transcribed from the 23-page PDF\n- `chapters/02-…/06-…/` — planned chapters, awaiting notes\n- `sources.html` — verification log\n- `assets/style.css` — Hallmark Almanac theme\n\n## Deploy to Cloudflare Pages\n\n```bash\ncd inorganicvii\nnpx wrangler login\nnpx wrangler pages deploy . --project-name inorganicvii\n```\n\nFirst time only: `npx wrangler pages project create inorganicvii --production-branch main`\n\nOr in the dashboard: Workers & Pages → Create → Pages → Upload assets → upload this folder, project name `inorganicvii`.\n\nNo build step. No server code.\n")
    print("done")

if __name__ == "__main__":
    main()
