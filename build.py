#!/usr/bin/env python3
"""Build inorganicvii, static multi-page notes site. Run: python3 build.py"""
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

def svg_open(w=760, h=300, vb=None):
    vb = vb or f"0 0 {w} {h}"
    return f'<svg viewBox="{vb}" width="{w}" height="{h}" role="img" xmlns="http://www.w3.org/2000/svg">'
INK="#20242B"; MUT="#5A6470"; ACC="#C2410C"; PAPER="#FFFFFF"; BLUE="#0E7490"; GREEN="#0E7490"; AMBER="#C2410C"

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
    if kind=="bcc":
        s+=dot(195,155,10,ACC)  # body centre (bcc only: fcc has no atom at the cube centre)
    if kind=="fcc":
        # face centres: front, top, right (visible)
        s+=dot(160,160,9,BLUE)  # front face centre
        s+=dot(195,35,9,BLUE)   # top face centre approx
        s+=dot(295,155,9,BLUE)  # right face centre approx
        s+=f'<text x="380" y="90" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">corners: 8 x 1/8 = 1</text><text x="380" y="120" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">faces: 6 x 1/2 = 3</text><text x="380" y="150" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">total = 4 atoms</text>'
    elif kind=="bcc":
        s+=f'<text x="380" y="90" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">corners: 8 x 1/8 = 1</text><text x="380" y="120" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">centre: 1 (unshared)</text><text x="380" y="150" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">total = 2 atoms</text>'
    else:
        s+=f'<text x="380" y="90" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">corners: 8 x 1/8 = 1</text><text x="380" y="150" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">total = 1 atom</text>'
    s+=f'<text x="60" y="290" font-family="Source Sans 3, sans-serif" font-size="14" fill="{MUT}">{title}</text></svg>'
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
    s+=f'<text x="60" y="270" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">Crystalline: long range order</text>'
    import random; random.seed(7)
    for _ in range(20):
        x=430+random.randint(0,260); y=40+random.randint(0,180)
        s+=f'<circle cx="{x}" cy="{y}" r="11" fill="none" stroke="{MUT}" stroke-width="1.5"/>'
    s+=f'<text x="430" y="270" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">Amorphous: short range order only</text></svg>'
    return s

def fig_axes():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/><line x1="180" y1="200" x2="420" y2="200" stroke="{INK}" stroke-width="2"/><line x1="180" y1="200" x2="180" y2="60" stroke="{INK}" stroke-width="2"/><line x1="180" y1="200" x2="330" y2="110" stroke="{INK}" stroke-width="2"/>'
    s+=f'<text x="430" y="205" font-family="Source Sans 3, sans-serif" font-size="16" fill="{INK}">a</text><text x="170" y="45" font-family="Source Sans 3, sans-serif" font-size="16" fill="{INK}">c</text><text x="340" y="105" font-family="Source Sans 3, sans-serif" font-size="16" fill="{INK}">b</text>'
    s+=f'<text x="480" y="90" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">alpha: between b and c</text><text x="480" y="120" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">beta: between a and c</text><text x="480" y="150" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">gamma: between a and b</text><text x="480" y="190" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">6 lattice parameters:</text><text x="480" y="215" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">a, b, c, alpha, beta, gamma</text></svg>'
    return s

def fig_packing():
    s=svg_open(760,320)
    s+=f'<rect width="760" height="320" fill="{PAPER}"/>'
    for i in range(5):
        fill = INK if i == 2 else "none"
        s+=f'<circle cx="{70+i*40}" cy="70" r="20" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<text x="60" y="130" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">1D row: CN = 2</text>'
    for r in range(3):
        for c in range(4): s+=f'<circle cx="{70+c*40}" cy="{180+r*40}" r="20" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<text x="60" y="310" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">Square packing AAA: CN = 4</text>'
    for r in range(3):
        off=20 if r%2 else 0
        for c in range(4): s+=f'<circle class="anim-drop" style="animation-delay:{r*120}ms" cx="{430+off+c*40}" cy="{180+r*35}" r="20" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
    s+=f'<text x="420" y="310" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">Hexagonal ABAB: CN = 6</text></svg>'
    return s

def fig_stacking():
    s=svg_open(760,340)
    s+=f'<rect width="760" height="340" fill="{PAPER}"/>'
    def cluster(cx, cy, colour, label, filled_centre=False, anim=False):
        out = ""
        pts = [(cx, cy)] + [(cx + 32*dx, cy + 32*dy) for dx, dy in
               [(1,0),(0.5,0.866),(-0.5,0.866),(-1,0),(-0.5,-0.866),(0.5,-0.866)]]
        for i,(x,y) in enumerate(pts):
            fill = colour if (filled_centre and i == 0) else "none"
            cls = ' class="anim-drop"' if anim and i else ""
            sty = f' style="animation-delay:{i*90}ms"' if anim and i else ""
            out += f'<circle{cls}{sty} cx="{x:.0f}" cy="{y:.0f}" r="16" fill="{fill}" stroke="{colour}" stroke-width="1.5"/>'
        out += f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="13" fill="#fff">S</text>' if filled_centre else ""
        out += f'<text x="{cx}" y="{cy+64}" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">{label}</text>'
        return out
    s += cluster(150, 100, INK, "A layer", filled_centre=True)
    s += cluster(166, 230, BLUE, "B layer in the notches", anim=True)
    # arrows to the two 3D outcomes
    s += f'<line x1="260" y1="100" x2="330" y2="100" stroke="{INK}" stroke-width="1.5"/><text x="265" y="88" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">ABAB</text>'
    s += f'<line x1="276" y1="230" x2="346" y2="230" stroke="{INK}" stroke-width="1.5"/><text x="281" y="218" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">ABC</text>'
    # hexagonal prism (hcp)
    hx = [(400 + 55*dx, 100 + 55*dy) for dx, dy in [(1,0),(0.5,0.866),(-0.5,0.866),(-1,0),(-0.5,-0.866),(0.5,-0.866)]]
    pts = " ".join(f"{x:.0f},{y:.0f}" for x, y in hx)
    s += f'<polygon points="{pts}" fill="none" stroke="{INK}" stroke-width="2"/>'
    s += f'<text x="400" y="190" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">hcp prism</text>'
    # cube (ccp)
    s += f'<rect x="560" y="180" width="90" height="90" fill="none" stroke="{BLUE}" stroke-width="2"/><polygon points="560,180 590,150 680,150 650,180" fill="none" stroke="{BLUE}" stroke-width="1.5"/><line x1="650" y1="180" x2="680" y2="150" stroke="{BLUE}" stroke-width="1.5"/><line x1="650" y1="270" x2="680" y2="240" stroke="{BLUE}" stroke-width="1.5"/><line x1="680" y1="150" x2="680" y2="240" stroke="{BLUE}" stroke-width="1.5"/>'
    s += f'<text x="605" y="310" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">ccp cube</text></svg>'
    return s

def fig_voids():
    s=svg_open(760,320)
    s+=f'<rect width="760" height="320" fill="{PAPER}"/>'
    # tetrahedral: 3 base + 1 top small
    for (x,y) in [(140,220),(220,220),(180,150)]: s+=f'<circle cx="{x}" cy="{y}" r="42" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<circle cx="180" cy="195" r="12" fill="{ACC}"/><text x="120" y="290" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">Tetrahedral void: 4 spheres</text><text x="120" y="312" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">r(void) = 0.225 R, 2 per sphere</text>'
    # octahedral: three circles in a triangle, as the notes draw it
    for (x,y) in [(480,205),(600,205),(540,105)]: s+=f'<circle cx="{x}" cy="{y}" r="38" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
    s+=f'<circle cx="540" cy="172" r="13" fill="{ACC}"/><text x="450" y="290" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">Octahedral void: 6 spheres</text><text x="450" y="312" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">r(void) = 0.414 R, 1 per sphere</text></svg>'
    return s

def fig_radius():
    s=svg_open(760,320)
    s+=f'<rect width="760" height="320" fill="{PAPER}"/>'
    # 3D cube: front (80,90)-(250,260), back offset (60,-45)
    front=[(80,260),(250,260),(250,90),(80,90)]
    back=[(x+60,y-45) for x,y in front]
    poly=lambda pts: " ".join(f"{x},{y}" for x,y in pts)
    s+=f'<polygon points="{poly(front)}" fill="none" stroke="{INK}" stroke-width="2"/><polygon points="{poly(back)}" fill="none" stroke="{INK}" stroke-width="2"/>'
    for a,b in zip(front, back): s+=f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" stroke-width="1.5"/>'
    # body diagonal, front bottom-left corner through the centre to the back top-right corner
    s+=f'<line x1="80" y1="260" x2="310" y2="45" stroke="{ACC}" stroke-width="2"/>'
    for p in front+back: s+=f'<circle cx="{p[0]}" cy="{p[1]}" r="16" fill="none" stroke="{ACC}" stroke-width="1.5"/>'
    s+=f'<circle cx="195" cy="152" r="14" fill="{BLUE}"/>'
    s+=f'<text x="330" y="60" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Anion: corners</text><text x="330" y="88" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Cation: body centre</text>'
    s+=f'<text x="330" y="130" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">sqrt(3) a = 2r+ + 2r-</text><text x="330" y="160" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">a = 2r-  (anions touch)</text><text x="330" y="190" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">r+/r- = sqrt(3) - 1 = 0.732</text><text x="330" y="230" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">NaCl (octahedral): 0.414</text><text x="330" y="260" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">ZnS (tetrahedral): 0.225</text>'
    # edge arrow a
    s+=f'<line x1="80" y1="290" x2="250" y2="290" stroke="{INK}" stroke-width="1.5"/><line x1="80" y1="284" x2="80" y2="296" stroke="{INK}" stroke-width="1.5"/><line x1="250" y1="284" x2="250" y2="296" stroke="{INK}" stroke-width="1.5"/><text x="155" y="310" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">a = edge of the cube</text></svg>'
    return s

def fig_perovskite():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    # cube front (90,50)-(310,270), back offset (70,-40)
    s+=f'<rect x="90" y="50" width="220" height="220" fill="none" stroke="{INK}" stroke-width="2"/><line x1="90" y1="50" x2="160" y2="10" stroke="{INK}" stroke-width="1.5"/><line x1="310" y1="50" x2="380" y2="10" stroke="{INK}" stroke-width="1.5"/><line x1="90" y1="270" x2="160" y2="230" stroke="{INK}" stroke-width="1.5"/><line x1="310" y1="270" x2="380" y2="230" stroke="{INK}" stroke-width="1.5"/><line x1="160" y1="10" x2="380" y2="10" stroke="{INK}" stroke-width="1.5"/><line x1="380" y1="10" x2="380" y2="230" stroke="{INK}" stroke-width="1.5"/>'
    # TiO6 octahedron: Ti at the body centre (235,140) joined to the six face-centre oxygens
    for (x,y) in [(200,160),(270,120),(235,30),(235,250),(125,140),(345,140)]:
        s+=f'<line x1="235" y1="140" x2="{x}" y2="{y}" stroke="{BLUE}" stroke-width="1.5"/>'
    for (x,y) in [(90,50),(310,50),(90,270),(310,270),(160,10),(380,10),(160,230),(380,230)]: s+=f'<circle cx="{x}" cy="{y}" r="12" fill="{BLUE}"/>'
    for (x,y) in [(200,160),(270,120),(235,30),(235,250),(125,140),(345,140)]: s+=f'<circle cx="{x}" cy="{y}" r="11" fill="none" stroke="{ACC}" stroke-width="1.5"/>'
    s+=f'<circle cx="235" cy="140" r="12" fill="{ACC}"/>'
    s+=f'<text x="450" y="80" font-family="Source Sans 3, sans-serif" font-size="15" fill="{BLUE}">Ca2+ corners: 8 x 1/8 = 1</text><text x="450" y="110" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">O2- face centres: 6 x 1/2 = 3</text><text x="450" y="140" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">Ti4+ body centre: 1</text><text x="450" y="180" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Formula: CaTiO3</text><text x="450" y="210" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Ti CN 6, Ca CN 12</text><text x="450" y="250" font-family="Source Sans 3, sans-serif" font-size="14" fill="{MUT}">Shift origin by (1/2,1/2,1/2):</text><text x="450" y="275" font-family="Source Sans 3, sans-serif" font-size="14" fill="{MUT}">Ca at centre, Ti at corners, O on edges.</text></svg>'
    return s

def fig_tolerance():
    s=svg_open(760,320)
    s+=f'<rect width="760" height="320" fill="{PAPER}"/>'
    s+=f'<line x1="70" y1="250" x2="700" y2="250" stroke="{INK}" stroke-width="2"/>'
    def X(tt): return 70+(tt-0.6)/0.6*630
    for (x0,x1,lab) in [(70,X(0.71),"ilmenite / other"),(X(0.71),X(0.90),"orthorhombic / rhombohedral"),(X(0.90),X(1.0),"cubic"),(X(1.0),700,"hexagonal / tetragonal")]:
        s+=f'<rect x="{x0:.0f}" y="120" width="{x1-x0:.0f}" height="130" fill="{PAPER}" stroke="{MUT}" stroke-width="1"/>'
        s+=f'<text x="{(x0+x1)/2:.0f}" y="190" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">{lab}</text>'
    for tt in [0.71,0.90,1.0]:
        s+=f'<line x1="{X(tt):.0f}" y1="250" x2="{X(tt):.0f}" y2="260" stroke="{INK}" stroke-width="2"/><text x="{X(tt):.0f}" y="280" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">{tt}</text>'
    s+=f'<circle cx="{X(1.0):.0f}" cy="90" r="6" fill="{ACC}"/><text x="{X(1.0):.0f}" y="70" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="14" fill="{ACC}">t = 1 ideal, SrTiO3</text><text x="70" y="40" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">Goldschmidt tolerance factor t, increasing to the right</text></svg>'
    return s

def fig_cfse():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    d_o = 'Δ<tspan baseline-shift="sub" font-size="11">o</tspan>'
    d_t = 'Δ<tspan baseline-shift="sub" font-size="11">t</tspan>'
    # octahedral levels
    s+=f'<text x="60" y="36" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Octahedral</text>'
    s+=f'<line class="anim-line" x1="60" y1="80" x2="220" y2="80" stroke="{ACC}" stroke-width="3"/><line class="anim-line" style="animation-delay:150ms" x1="60" y1="170" x2="220" y2="170" stroke="{ACC}" stroke-width="3"/>'
    s+=f'<text x="235" y="85" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">e<tspan baseline-shift="sub" font-size="11">g</tspan> (+0.6 {d_o})</text>'
    s+=f'<text x="235" y="175" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">t<tspan baseline-shift="sub" font-size="11">2g</tspan> (-0.4 {d_o})</text>'
    s+=f'<line x1="330" y1="80" x2="330" y2="170" stroke="{INK}" stroke-width="1.5"/><line x1="324" y1="80" x2="330" y2="80" stroke="{INK}" stroke-width="1.5"/><line x1="324" y1="170" x2="330" y2="170" stroke="{INK}" stroke-width="1.5"/><text x="342" y="130" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">{d_o}</text>'
    s+=f'<text x="60" y="235" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">d<tspan baseline-shift="super" font-size="11">3</tspan>: t<tspan baseline-shift="sub" font-size="11">2g</tspan><tspan baseline-shift="super" font-size="11">3</tspan>, CFSE = 1.2 {d_o}</text>'
    s+=f'<text x="60" y="262" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">d<tspan baseline-shift="super" font-size="11">5</tspan> high spin: CFSE = 0</text>'
    # tetrahedral levels (inverted, smaller gap)
    s+=f'<text x="460" y="36" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Tetrahedral</text>'
    s+=f'<line class="anim-line" style="animation-delay:300ms" x1="460" y1="100" x2="620" y2="100" stroke="{BLUE}" stroke-width="3"/><line class="anim-line" style="animation-delay:450ms" x1="460" y1="150" x2="620" y2="150" stroke="{BLUE}" stroke-width="3"/>'
    s+=f'<text x="460" y="88" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">t<tspan baseline-shift="sub" font-size="10">2</tspan> (+0.4 {d_t})</text>'
    s+=f'<text x="460" y="178" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">e (-0.6 {d_t})</text>'
    s+=f'<line x1="660" y1="100" x2="660" y2="150" stroke="{INK}" stroke-width="1.5"/><line x1="654" y1="100" x2="660" y2="100" stroke="{INK}" stroke-width="1.5"/><line x1="654" y1="150" x2="660" y2="150" stroke="{INK}" stroke-width="1.5"/><text x="672" y="130" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">{d_t}</text>'
    s+=f'<text x="460" y="235" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">{d_t} = 4/9 {d_o}</text>'
    s+=f'<text x="460" y="262" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">Splitting is inverted and smaller</text></svg>'
    return s

def fig_spinel():
    s=svg_open(760,290)
    s+=f'<rect width="760" height="290" fill="{PAPER}"/>'
    sub = lambda x: f'<tspan baseline-shift="sub" font-size="11">{x}</tspan>'
    s+=f'<text x="60" y="40" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Normal spinel (A){sub("tet")}(B){sub("2oct")}O{sub("4")}</text>'
    for (x,y,lab) in [(120,120,"A2+"),(200,120,"B3+"),(280,120,"B3+")]: s+=f'<circle cx="{x}" cy="{y}" r="26" fill="none" stroke="{INK}" stroke-width="1.5"/><text x="{x}" y="{y+5}" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">{lab}</text>'
    s+=f'<text x="60" y="180" font-family="Source Sans 3, sans-serif" font-size="13" fill="{MUT}">Td hole (1/8 filled) - Oct holes (1/2 filled)</text><text x="60" y="210" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">MgAl{sub("2")}O{sub("4")}, ZnFe{sub("2")}O{sub("4")}, Mn{sub("3")}O{sub("4")}</text>'
    s+=f'<text x="420" y="40" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Inverse spinel B(AB)O{sub("4")}</text>'
    for (x,y,lab) in [(480,120,"B3+"),(560,120,"A2+"),(640,120,"B3+")]:
        cls = ' class="anim-pulse"' if lab == "A2+" else ""
        s+=f'<circle{cls} cx="{x}" cy="{y}" r="26" fill="none" stroke="{INK}" stroke-width="1.5"/><text x="{x}" y="{y+5}" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">{lab}</text>'
    s+=f'<text x="420" y="180" font-family="Source Sans 3, sans-serif" font-size="13" fill="{MUT}">Td: B3+ - Oct: A2+ + B3+</text><text x="420" y="210" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">Fe{sub("3")}O{sub("4")}, CoFe{sub("2")}O{sub("4")}, NiFe{sub("2")}O{sub("4")}</text><text x="420" y="232" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">CuFe{sub("2")}O{sub("4")}</text><text x="60" y="262" font-family="Source Sans 3, sans-serif" font-size="14" fill="{ACC}">O2- forms a ccp / fcc array in both cases.</text></svg>'
    return s

def fig_defects():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    # Schottky: two vacancies, one cation (blue) and one anion (ink), labelled
    for r in range(3):
        for c in range(4):
            if (r,c) in [(1,1),(1,2)]: continue
            col = BLUE if (r+c) % 2 == 0 else ACC
            s+=f'<circle cx="{70+c*52}" cy="{60+r*52}" r="16" fill="none" stroke="{col}" stroke-width="1.5"/>'
    s+=f'<rect x="105" y="95" width="32" height="32" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="4 3"/><rect x="157" y="95" width="32" height="32" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="4 3"/>'
    s+=f'<text x="60" y="215" font-family="Source Sans 3, sans-serif" font-size="13" fill="{BLUE}">cation vacancy</text><text x="180" y="215" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">anion vacancy</text>'
    s+=f'<text x="60" y="250" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">Schottky: paired cation + anion</text><text x="60" y="275" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">vacancies, stoichiometry kept</text>'
    # Frenkel: one lattice site empty (vacancy), the ion in a gap between sites
    for r in range(3):
        for c in range(4):
            if (r,c) == (1,1): continue
            s+=f'<circle cx="{430+c*52}" cy="{60+r*52}" r="16" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
    s+=f'<rect x="465" y="95" width="32" height="32" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="4 3"/><circle cx="516" cy="84" r="9" fill="{ACC}"/>'
    s+=f'<text x="420" y="215" font-family="Source Sans 3, sans-serif" font-size="13" fill="{ACC}">ion in an interstitial gap</text>'
    s+=f'<text x="420" y="250" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">Frenkel: ion leaves its site for</text><text x="420" y="275" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">an interstitial site, vacancy left</text></svg>'
    return s


def fig_lattice():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    # stacked unit cells: 3 columns x 2 rows of small oblique cubes; bottom-left cell highlighted
    for row in range(2):
        for col in range(3):
            x=90+col*130; y=210-row*100
            front=[(x,y),(x+70,y),(x+70,y-70),(x,y-70)]
            back=[(a+22,b-16) for a,b in front]
            poly=lambda pts: " ".join(f"{a},{b}" for a,b in pts)
            hl = (row==0 and col==0)
            wdt = 3 if hl else 1.5
            colr = ACC if hl else INK
            s+=f'<polygon points="{poly(front)}" fill="none" stroke="{colr}" stroke-width="{wdt}"/><polygon points="{poly(back)}" fill="none" stroke="{colr}" stroke-width="{wdt}"/>'
            for a,b in zip(front, back): s+=f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{colr}" stroke-width="{wdt}"/>'
    s+=f'<text x="125" y="235" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">a</text><text x="172" y="180" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">b</text><text x="72" y="180" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">c</text>'
    s+=f'<text x="90" y="275" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">a: bottom edge, b: side edge, c: left edge of the unit cell</text>'
    s+=f'<text x="90" y="14" font-family="Source Sans 3, sans-serif" font-size="14" fill="{ACC}">one unit cell, highlighted</text></svg>'
    return s

def fig_nacl_oct():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    cx, cy = 220, 150
    for (x,y) in [(cx,60),(cx,240),(130,150),(310,150)]:
        s+=f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{INK}" stroke-width="1.5"/>'
        s+=f'<circle cx="{x}" cy="{y}" r="20" fill="none" stroke="{ACC}" stroke-width="1.5"/>'
    s+=f'<circle cx="{cx+55}" cy="{cy-45}" r="14" fill="none" stroke="{ACC}" stroke-width="1.5"/><circle cx="{cx-55}" cy="{cy+45}" r="14" fill="none" stroke="{ACC}" stroke-width="1.5"/>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="12" fill="{BLUE}"/>'
    s+=f'<text x="400" y="90" font-family="Source Sans 3, sans-serif" font-size="15" fill="{BLUE}">Cl- at the six corners of an octahedron</text><text x="400" y="120" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">Na+ at the centre</text><text x="400" y="160" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Na+ is octahedrally surrounded</text><text x="400" y="190" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">by six Cl- ions: coordination 6:6</text></svg>'
    return s

def fig_wurtzite():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    def hexpts(cx, cy, r):
        return [(cx + r*dx, cy + r*dy) for dx, dy in [(1,0),(0.5,0.866),(-0.5,0.866),(-1,0),(-0.5,-0.866),(0.5,-0.866)]]
    top = hexpts(220, 90, 70); bot = hexpts(220, 210, 70)
    poly=lambda pts: " ".join(f"{x:.0f},{y:.0f}" for x,y in pts)
    s+=f'<polygon points="{poly(top)}" fill="none" stroke="{INK}" stroke-width="2"/><polygon points="{poly(bot)}" fill="none" stroke="{INK}" stroke-width="2"/>'
    for a,b in zip(top, bot): s+=f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{INK}" stroke-width="1.5"/>'
    for (x,y) in top+bot: s+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#FFEDD5" stroke="{ACC}" stroke-width="1.5"/>'
    s+=f'<circle cx="250" cy="168" r="10" fill="{ACC}"/>'
    s+=f'<text x="400" y="90" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Wurtzite, ZnS: hexagonal prism</text><text x="400" y="120" font-family="Source Sans 3, sans-serif" font-size="15" fill="{BLUE}">S2- in an hcp array</text><text x="400" y="150" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">Zn2+ in half the tetrahedral holes</text><text x="400" y="180" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Coordination 4:4, as in zinc blende</text></svg>'
    return s

def fig_fluorite():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    # cube divided into 8 small cubes
    s+=f'<rect x="90" y="50" width="200" height="200" fill="none" stroke="{INK}" stroke-width="2"/><line x1="190" y1="50" x2="190" y2="250" stroke="{INK}" stroke-width="1"/><line x1="90" y1="150" x2="290" y2="150" stroke="{INK}" stroke-width="1"/>'
    s+=f'<line x1="90" y1="50" x2="140" y2="20" stroke="{INK}" stroke-width="1.5"/><line x1="290" y1="50" x2="340" y2="20" stroke="{INK}" stroke-width="1.5"/><line x1="290" y1="250" x2="340" y2="220" stroke="{INK}" stroke-width="1.5"/><line x1="140" y1="20" x2="340" y2="20" stroke="{INK}" stroke-width="1.5"/><line x1="340" y1="20" x2="340" y2="220" stroke="{INK}" stroke-width="1.5"/>'
    for (x,y) in [(90,50),(290,50),(90,250),(290,250),(190,150),(215,35),(315,135),(140,20),(340,20),(340,220)]: s+=f'<circle cx="{x}" cy="{y}" r="11" fill="{BLUE}"/>'
    for (x,y) in [(140,100),(240,100),(140,200),(240,200)]: s+=f'<circle cx="{x}" cy="{y}" r="9" fill="{ACC}"/>'
    s+=f'<text x="400" y="90" font-family="Source Sans 3, sans-serif" font-size="15" fill="{BLUE}">Ca2+: corners and face centres</text><text x="400" y="120" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">F-: centres of the eight small cubes</text><text x="400" y="160" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Ca2+ coordinated by 8 F-</text><text x="400" y="190" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">F- coordinated by 4 Ca2+: 8:4</text></svg>'
    return s

def fig_rutile():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    # tetragonal box: one side longer than the others
    s+=f'<rect x="120" y="50" width="130" height="200" fill="none" stroke="{INK}" stroke-width="2"/><line x1="120" y1="50" x2="160" y2="25" stroke="{INK}" stroke-width="1.5"/><line x1="250" y1="50" x2="290" y2="25" stroke="{INK}" stroke-width="1.5"/><line x1="250" y1="250" x2="290" y2="225" stroke="{INK}" stroke-width="1.5"/><line x1="160" y1="25" x2="290" y2="25" stroke="{INK}" stroke-width="1.5"/><line x1="290" y1="25" x2="290" y2="225" stroke="{INK}" stroke-width="1.5"/>'
    for (x,y) in [(120,50),(250,50),(120,250),(250,250),(160,25),(290,25),(160,225),(290,225)]: s+=f'<circle cx="{x}" cy="{y}" r="10" fill="{BLUE}"/>'
    s+=f'<circle cx="185" cy="150" r="10" fill="{BLUE}"/><circle cx="150" cy="110" r="8" fill="{ACC}"/><circle cx="225" cy="190" r="8" fill="{ACC}"/>'
    s+=f'<text x="360" y="90" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Rutile, TiO2: tetragonal cell</text><text x="360" y="120" font-family="Source Sans 3, sans-serif" font-size="15" fill="{BLUE}">Ti4+: corners and body centre</text><text x="360" y="150" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">O2-: inside the cell</text><text x="360" y="190" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Ti octahedral (6), O trigonal (3)</text><text x="360" y="220" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">One side longer: body-centred</text><text x="360" y="250" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">tetragonal, not cubic</text></svg>'
    return s

def fig_diamond():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    front=[(80,250),(280,250),(280,50),(80,50)]
    back=[(x+60,y-40) for x,y in front]
    poly=lambda pts: " ".join(f"{x},{y}" for x,y in pts)
    s+=f'<polygon points="{poly(front)}" fill="none" stroke="{INK}" stroke-width="2"/><polygon points="{poly(back)}" fill="none" stroke="{INK}" stroke-width="2"/>'
    for a,b in zip(front, back): s+=f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" stroke-width="1.5"/>'
    for p in front+back: s+=f'<circle cx="{p[0]}" cy="{p[1]}" r="9" fill="{INK}"/>'
    for (x,y) in [(180,150),(210,30),(310,130)]: s+=f'<circle cx="{x}" cy="{y}" r="9" fill="{BLUE}"/>'
    for (x,y) in [(220,170),(250,100),(130,200),(230,210)]: s+=f'<circle cx="{x}" cy="{y}" r="9" fill="{ACC}"/>'
    s+=f'<text x="400" y="90" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">Diamond cubic: an fcc lattice</text><text x="400" y="120" font-family="Source Sans 3, sans-serif" font-size="15" fill="{ACC}">4 more atoms inside the cell</text><text x="400" y="150" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">at 4 of the 8 tetrahedral holes</text><text x="400" y="190" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">8 atoms per cell, CN 4, 34% filled</text></svg>'
    return s

def fig_bcc_layers():
    s=svg_open(760,300)
    s+=f'<rect width="760" height="300" fill="{PAPER}"/>'
    for r in range(4):
        for c in range(4): s+=f'<circle cx="{70+c*32}" cy="{60+r*32}" r="14" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<text x="60" y="230" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">First layer: square packing</text>'
    s+=f'<line x1="60" y1="50" x2="180" y2="170" stroke="{ACC}" stroke-width="1.5"/>'
    for r in range(4):
        for c in range(4): s+=f'<circle cx="{430+16+c*32}" cy="{76+r*32}" r="14" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
    s+=f'<text x="420" y="230" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">Second layer sits in the notches</text></svg>'
    return s

def fig_hcp_prism():
    s=svg_open(760,340)
    s+=f'<rect width="760" height="340" fill="{PAPER}"/>'
    def hexpts(cx, cy, r):
        return [(cx + r*dx, cy + r*dy) for dx, dy in [(1,0),(0.5,0.866),(-0.5,0.866),(-1,0),(-0.5,-0.866),(0.5,-0.866)]]
    top = hexpts(220, 90, 70); bot = hexpts(220, 230, 70)
    poly=lambda pts: " ".join(f"{x:.0f},{y:.0f}" for x,y in pts)
    s+=f'<polygon points="{poly(top)}" fill="none" stroke="{INK}" stroke-width="2"/><polygon points="{poly(bot)}" fill="none" stroke="{INK}" stroke-width="2"/>'
    for a,b in zip(top, bot): s+=f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<text x="400" y="70" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">A: third layer, top</text><text x="400" y="160" font-family="Source Sans 3, sans-serif" font-size="15" fill="{BLUE}">B: second layer, middle</text><text x="400" y="250" font-family="Source Sans 3, sans-serif" font-size="15" fill="{INK}">A: first layer, bottom</text>'
    s+=f'<line x1="150" y1="30" x2="290" y2="30" stroke="{INK}" stroke-width="1.5"/><line x1="150" y1="24" x2="150" y2="36" stroke="{INK}" stroke-width="1.5"/><line x1="290" y1="24" x2="290" y2="36" stroke="{INK}" stroke-width="1.5"/><text x="205" y="20" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">a</text>'
    s+=f'<line x1="60" y1="90" x2="60" y2="230" stroke="{INK}" stroke-width="1.5"/><line x1="54" y1="90" x2="66" y2="90" stroke="{INK}" stroke-width="1.5"/><line x1="54" y1="230" x2="66" y2="230" stroke="{INK}" stroke-width="1.5"/><text x="45" y="165" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">c</text>'
    for (x,y) in [(480,300),(520,300),(500,265)]: s+=f'<circle cx="{x}" cy="{y}" r="14" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
    s+=f'<text x="560" y="305" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">B: three spheres, a triangle</text></svg>'
    return s

def fig_ccp12():
    s=svg_open(760,430)
    s+=f'<rect width="760" height="430" fill="{PAPER}"/>'
    for (x,y,n) in [(352,52,"7"),(408,52,"8"),(380,98,"9")]:
        s+=f'<circle cx="{x}" cy="{y}" r="18" fill="none" stroke="{INK}" stroke-width="1.5"/><text x="{x}" y="{y+5}" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">{n}</text>'
    s+=f'<text x="450" y="75" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">A layer, above</text>'
    for i,(x,y) in enumerate([(380,178),(434,209),(434,271),(380,302),(326,271),(326,209)]):
        s+=f'<circle cx="{x}" cy="{y}" r="18" fill="none" stroke="{BLUE}" stroke-width="1.5"/><text x="{x}" y="{y+5}" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">{i+1}</text>'
    s+=f'<text x="380" y="245" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="16" fill="{ACC}">★</text>'
    s+=f'<text x="470" y="245" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">B layer: six around the centre</text>'
    for (x,y,n) in [(352,372,"10"),(408,372,"11"),(380,410,"12")]:
        s+=f'<circle cx="{x}" cy="{y}" r="18" fill="none" stroke="{INK}" stroke-width="1.5"/><text x="{x}" y="{y+5}" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="13" fill="{INK}">{n}</text>'
    s+=f'<text x="450" y="380" font-family="Source Sans 3, sans-serif" font-size="14" fill="{INK}">C layer, below</text></svg>'
    return s

# ---- template ----
def page(rel, title, lede, body, crumb=""):
    depth = rel.count("/")
    cls = "home" if rel == "index.html" else "page"
    def hero_cube(x0, label, kind):
        front=[(x0,160),(x0+80,160),(x0+80,80),(x0,80)]
        back=[(a+20,b-20) for a,b in front]
        poly=lambda pts: " ".join(f"{a},{b}" for a,b in pts)
        g=f'<g class="cube"><path d="M{x0} 160 L{x0} 80 L{x0+80} 80 L{x0+80} 160 Z M{x0+20} 140 L{x0+20} 60 L{x0+100} 60 L{x0+100} 140 Z M{x0} 80 L{x0+20} 60 M{x0+80} 80 L{x0+100} 60 M{x0+80} 160 L{x0+100} 140 M{x0} 160 L{x0+20} 140" fill="none" stroke="#FAF7F1" stroke-width="2"/>'
        for (x,y) in front+back: g+=f'<circle cx="{x}" cy="{y}" r="7" fill="#FAF7F1"/>'
        if kind=="bcc": g+=f'<circle cx="{x0+50}" cy="{110}" r="7" fill="#FAF7F1"/>'
        if kind=="fcc":
            g+=f'<circle cx="{x0+40}" cy="{120}" r="7" fill="#FAF7F1"/><circle cx="{x0+50}" cy="{70}" r="7" fill="#FAF7F1"/><circle cx="{x0+90}" cy="{110}" r="7" fill="#FAF7F1"/>'
        g+=f'<text x="{x0}" y="200" fill="#FAF7F1" font-family="Source Sans 3, sans-serif" font-size="15">{label}</text></g>'
        return g
    field = '<figure class="field hero-field"><svg viewBox="0 0 720 220" role="img" aria-label="Simple cubic, body-centred cubic and face-centred cubic unit cells">' + hero_cube(40, "Simple cubic", "sc") + hero_cube(280, "Body-centred cubic", "bcc") + hero_cube(520, "Face-centred cubic", "fcc") + '</svg></figure>'
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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body class="{cls}">
<header class="topbar"><div class="container">
<a class="wordmark" href="{prefix}index.html"><span>Inorganic</span><span>VII</span></a>
<nav aria-label="Main"><a href="{prefix}index.html">Chapters</a><button type="button" class="search-btn" id="search-btn" aria-expanded="false">Search</button><a href="{prefix}chapters/04-solids/index.html">Chapter 4 · Solids</a><a href="{prefix}sources.html">Sources and checks</a></nav>
</div></header>
<main class="container">
<p class="crumb">{crumb}</p>
<div class="hero"><h1>{title}</h1><p class="lede">{lede}</p></div>
{field if cls == "home" else ""}
{body}
</main>
<footer><div class="container">
<p>Transcribed from the handwritten notes in the uploaded 23-page PDF, then checked against the sources listed on the sources page. Where the handwriting was crossed out, cut off, or wrong, the page says so instead of silently copying it.</p>
<p><a href="{prefix}index.html">All chapters</a></p><p><a href="{prefix}sources.html">Sources and checks</a></p>
<p><button type="button" class="motion-toggle" onclick="document.body.classList.toggle('no-motion');this.textContent=document.body.classList.contains('no-motion')?'Resume motion':'Pause motion'">Pause motion</button></p>
</div></footer>
<div class="search-panel" id="search-panel" data-index="{prefix}assets/search.json" hidden>
<div class="search-box"><input type="search" id="search-input" placeholder="Search the notes..." aria-label="Search the notes"><button type="button" id="search-close">Close</button></div>
<ol id="search-results"></ol>
</div>
<script src="{prefix}assets/search.js" defer></script>
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
        pager = '<nav class="pager" aria-label="Topics">' + (f'<a href="{prev[0]}">Previous topic: {prev[1]}</a>' if prev else '<span></span>') + (f'<a href="{nxt[0]}">Next topic: {nxt[1]}</a>' if nxt else '') + '</nav>'
    write(rel, page(rel, title, lede, body + pager, crumb))

def check_box(title, text):
    return f'<aside class="note"><p><strong>{title}.</strong> {text}</p></aside>'

# ---- Chapter 1 topic bodies ----
B01 = f"""
{fig("Regular order against irregular order. The drawing is a schematic, not a photograph of atoms.", fig_order())}
<h2>Crystalline</h2>
<ul><li>Definite, repeating, long range order of particles.</li><li>Definite characteristic shape.</li><li>Sharp and fixed melting point.</li><li>Breaks along a definite plane, giving smooth surfaces.</li><li>A definite value of heat of fusion.</li></ul>
<p>Examples: NaCl, diamond.</p>
<h2>Amorphous</h2>
<ul><li>Irregular; only short range order.</li><li>Irregular shape.</li><li>Softens gradually over a range of temperature.</li><li>Breaks irregularly.</li><li>No definite value of heat of fusion.</li></ul>
<p>Examples: glass, rubber, pitch.</p>
"""
B02 = f"""
{fig("The six lattice parameters: three edge lengths and three angles between them.", fig_axes())}
{fig("The crystal is built by stacking unit cells together, one highlighted here.", fig_lattice())}
<h2>Lattice and unit cells</h2>
<p>A crystal consists of a basic structural unit, or motif, repeated in three dimensions. The basic unit may be a single atom, molecule or ion, or a group of atoms or molecules, which has an identical environment throughout the crystal. It is also called the basis of the crystal. A basis has the same stoichiometric composition as the crystal itself.</p>
<p>The lattice, or space lattice, is the geometrical idealisation of the structure. It is obtained by placing a point at the same location of each basis in the crystal; the resulting three-dimensional distribution of points in space forms the lattice. A crystal structure is generated by associating each lattice point with a basis.</p>
<div class="formula">lattice + basis = crystal structure</div>
<p>A unit cell is the smallest part of the crystal which can generate the whole crystal structure through repetition in three dimensions by simple translational displacement. In effect this is equivalent to constructing the whole crystal structure by stacking the unit cells together along their faces without leaving any space.</p>
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
<p>Combining all possible symmetry elements gives 32 point groups, which fall into the seven crystal systems. Depending on the symmetry of the unit cell crystal may be classified into 7 crystal system represented by 7 primitive unit cell.</p>
<h2>The seven crystal systems</h2>
<table><thead><tr><th>System</th><th class="num">Bravais lattices</th><th>Cell</th><th>Symmetry</th></tr></thead><tbody>
<tr><td>Cubic</td><td class="num">3</td><td>a = b = c, α = β = γ = 90°</td><td>Four C<sub>3</sub> axes</td></tr>
<tr><td>Tetragonal</td><td class="num">2</td><td>a = b ≠ c, α = β = γ = 90°</td><td>One C<sub>4</sub> axis</td></tr>
<tr><td>Orthorhombic</td><td class="num">4</td><td>a ≠ b ≠ c, α = β = γ = 90°</td><td>Three perpendicular C<sub>2</sub> axes</td></tr>
<tr><td>Monoclinic</td><td class="num">2</td><td>a ≠ b ≠ c, α = γ = 90°, β ≠ 90°</td><td>One C<sub>2</sub> axis</td></tr>
<tr><td>Hexagonal</td><td class="num">1</td><td>a = b ≠ c, α = β = 90°, γ = 120°</td><td>One C<sub>6</sub> axis</td></tr>
<tr><td>Rhombohedral</td><td class="num">1</td><td>a = b = c, α = β = γ ≠ 90° (α &lt; 120°)</td><td>One C<sub>3</sub> axis</td></tr>
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
{fig("Face-centred cubic: 14 lattice points in the cell, 4 atoms per cell after sharing is counted.", cube_svg("fcc","Face-centred cubic"))}
<p>In a face-centred cubic lattice the atoms are at all eight corners and at the centre of each face. There is no atom at the centre of the cube. Each face-centre atom is shared by two adjacent cells, so it contributes 1/2.</p>
<div class="formula">Corners: 8 × 1/8 = 1<br>Faces: 6 × 1/2 = 3<br>Total = 4 atoms per unit cell</div>
"""
B05 = f"""
{fig("One dimension, then two: square packing is less efficient than hexagonal packing.", fig_packing())}
<h2>Close packing in one dimension</h2>
<p>Spheres are placed in a row, each touching two neighbours. Coordination number = 2.</p>
<h2>Close packing in two dimensions</h2>
<p><strong>Square packing (AAA type).</strong> Rows are placed one above the other so that spheres sit directly on top of each other. It is less efficient. Coordination number = 4.</p>
<p><strong>Hexagonal packing (ABAB type).</strong> The second row sits in the depressions (holes) of the first row. High efficient, this is the closest packing in two dimensions. Each sphere touches six neighbours. Coordination number = 6.</p>
"""
B06 = f"""
{fig("Third layer repeats the first (ABAB, hcp) or takes a new position (ABCABC, ccp).", fig_stacking())}
<p>To build a crystal in three dimensions, close-packed layers are stacked one on top of the other in a regular way. Consider a sphere S in the first layer: spheres in the next layer nestle in the notches at the positions marked with dots. Three of these will make contact with S. In the second layer there is a notch over S, but there are also notches over the positions marked with crosses. The third layer may repeat the arrangement of the first layer, or it may not.</p>
<p>Such a pattern of packing of spheres in three dimensions is referred to as hexagonal close packing. It is called hexagonal because a six-fold (C<sub>6</sub>) axis runs perpendicular to the plane of the close-packed layer, present in all the stacked layers.</p>
<ul><li><strong>If the third layer repeats the first,</strong> there are only two kinds of layer, A and B, and the pattern is ABAB… This is the hexagonal close-packed (hcp) structure.</li>
<li><strong>If the third layer does not repeat the first,</strong> it is denoted C, and the pattern is ABCABC… This is the cubic close-packed (ccp) structure, also called face-centred cubic (fcc).</li></ul>
<h2>Hexagonal close packing</h2>
{fig("The hexagonal unit cell: A layers top and bottom, B layer in the middle.", fig_hcp_prism())}
<p>This is the relation between the simple hexagonal crystal system and the hexagonal close-packing model. In ABA stacking, the seven spheres in both the first layer (A) and the third layer occupy simple hexagonal lattice points, while the three spheres of the second layer (B) are placed (within the unit cell) at the corners of an equilateral triangle midway between the two parallel hexagonal planes, so that the nearest environment of every sphere becomes identical. The height of the unit cell, c, is the distance between the first and third layers; a is the length of the side of the hexagon.</p>
<p>A sphere is hexagonally surrounded by six spheres in its own plane, and touches three spheres below the plane and three above it. Coordination number = 6 + 3 + 3 = 12.</p>
<p class="figures">Packing efficiency 74%, coordination number 12, stacking ABAB and so on.</p>
<h2>Cubic close packing</h2>
{fig("The 12 nearest neighbours of one sphere: three above, six around it, three below.", fig_ccp12())}
<p>In ccp / fcc the stacking sequence is ABCABC… The structure has cubic symmetry. In addition to the eight spheres at the eight corners of the cube, there is one sphere at the centre of each of the six faces, hence the name face-centred cubic. Each sphere is surrounded by 12 other nearest spheres, so the coordination number is 12. Packing efficiency is 74%.</p>
<h2>Common features of hcp and ccp</h2>
<ul><li>Coordination number is 12 in both.</li><li>Packing efficiency is 74% in both, 74% of the total volume of the unit cell is occupied by the spheres.</li></ul>
<h2>Body-centred cubic, for comparison</h2>
{fig("BCC layers: the second layer sits in the notches of the first.", fig_bcc_layers())}
<p>Another common arrangement in a few metals is body-centred cubic (bcc). The second layer sits in the notches of the first and the pattern repeats ABAB…, but the coordination number is 8, compared with 12 in a close-packed pattern.</p>
""" + check_box("A line to read with care", "The notes say, in the bcc paragraph, that the number of neighbours around any sphere is four. That is the in-plane count in the drawing, not the coordination number of bcc. The coordination number of bcc is 8, as the notes themselves state in the next sentence.")

B07 = f"""
{fig("A tetrahedral void is bounded by four spheres; an octahedral void by six. The drawings are sections through the voids.", fig_voids())}
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
<tr><td class="num">0.225 to 0.414</td><td class="num">4</td><td>Tetrahedral</td><td>ZnS</td></tr>
<tr><td class="num">0.414 to 0.732</td><td class="num">6</td><td>Octahedral</td><td>NaCl</td></tr>
<tr><td class="num">0.732 to 1.000</td><td class="num">8</td><td>Cubic</td><td>CsCl</td></tr>
</tbody></table>
<h2>Worked limits</h2>
<p><strong>CsCl, 8:8.</strong> Side of cube a = 2r<sup>−</sup>. Body diagonal √3 a = 2r<sup>+</sup> + 2r<sup>−</sup>. Hence √3 = (r<sup>+</sup> + r<sup>−</sup>)/r<sup>−</sup>, so r<sup>+</sup>/r<sup>−</sup> = √3 − 1 = 1.732 − 1 = 0.732.</p>
<p><strong>NaCl, octahedral, 6:6.</strong> Face diagonal √2 a = 2r<sup>+</sup> + 2r<sup>−</sup>, with a = 2r<sup>−</sup> (a here is the side of the square of anions around the hole). Hence r<sup>+</sup>/r<sup>−</sup> = √2 − 1 = 0.414.</p>
<p><strong>ZnS, tetrahedral, 4:4.</strong> A quarter of the body diagonal gives r<sup>+</sup> + r<sup>−</sup> = √3 a/4, with the face diagonal √2 a = 4r<sup>−</sup>. Hence r<sup>+</sup>/r<sup>−</sup> = √6/2 − 1 = 0.225.</p>
""" + check_box("Checked, with one correction to the working", "The three limiting values, 0.225, 0.414 and 0.732, are correct and match the standard radius-ratio table. The tetrahedral algebra in the notes is heavily crossed out, and its last legible step gives 0.449, not 0.225, so this page gives the standard working instead. The radius-ratio rule is a guide, not a law. That last sentence is standard knowledge supplied here, because the notes' own limitation item is cut off at the bottom of the page.")

B08 = f"""
{fig("Diamond cubic: an fcc lattice with four extra atoms inside the cell.", fig_diamond())}
<h2>Diamond cubic unit cell</h2>
<p>Diamond is a special type of fcc lattice. Four additional atoms are present within the face-centred cube, distributed symmetrically so that each one has an identical environment. They sit at the centres of alternating small cubes within the fcc cell, that is, at 4 of the 8 alternative tetrahedral holes. In this arrangement every atom is tetrahedrally surrounded.</p>
<p>Total lattice points per diamond cubic unit cell:</p>
<div class="formula">n = 1/8 × Nc + 1/2 × Nf + Ni = 1/8 × 8 + 1/2 × 6 + 4 = 1 + 3 + 4 = 8</div>
<p>The four internal lattice points lie along the four body diagonals of the fcc unit cell, each one a quarter of the way along a body diagonal from a corner. Taking a corner atom and the nearest atom along the body diagonal:</p>
<div class="formula">2r = 1/4 × √3 a<br>a = 8r / √3</div>
<p>Percentage of space actually occupied:</p>
<div class="formula">[8 × (4/3)πr³ × 100] / [(8/√3 r)³] = 34%</div>
<p class="figures">Space occupied 34%, space unoccupied 66%, 8 atoms per unit cell, coordination number 4.</p>
<p>Compare fcc metals at 74%: diamond is much more open, because every atom is held in a directional tetrahedral network rather than in close packing.</p>
"""

B09 = f"""
{fig("NaCl: each Na+ sits in an octahedron of six Cl- ions.", fig_nacl_oct())}
<h2>AB type, four structures</h2>
<p>NaCl, CsCl, ZnS (zinc blende) and ZnS (wurtzite).</p>
<table><thead><tr><th>Structure</th><th class="num">Coordination</th><th>Anion array</th><th>Cation site</th></tr></thead><tbody>
<tr><td><strong>NaCl</strong> (rock salt)</td><td class="num">6:6</td><td>fcc Cl<sup>−</sup></td><td>Na<sup>+</sup> in all octahedral holes; 4 Na<sup>+</sup> and 4 Cl<sup>−</sup> per cell</td></tr>
<tr><td><strong>CsCl</strong></td><td class="num">8:8</td><td>Simple cubic Cl<sup>−</sup></td><td>Cs<sup>+</sup> at the body centre; 1 of each per cell</td></tr>
<tr><td><strong>ZnS, zinc blende</strong></td><td class="num">4:4</td><td>fcc S<sup>2−</sup></td><td>Zn<sup>2+</sup> in half the tetrahedral holes; 4 of each per cell</td></tr>
<tr><td><strong>ZnS, wurtzite</strong></td><td class="num">4:4</td><td>hcp S<sup>2−</sup></td><td>Zn<sup>2+</sup> in half the tetrahedral holes</td></tr>
</tbody></table>
<p>Zinc blende and wurtzite have the same 4:4 coordination and the same stoichiometry; they differ in the stacking of the anion array, ccp in zinc blende, hcp in wurtzite.</p>
{fig("Wurtzite, ZnS: the same 4:4 coordination in a hexagonal cell.", fig_wurtzite())}
"""
B10 = f"""
{fig("Fluorite, CaF2: Ca2+ on corners and faces, F- in the eight small cubes.", fig_fluorite())}
<h2>Fluorite, CaF<sub>2</sub>, 8:4</h2>
<p>Ca<sup>2+</sup> ions are arranged at the corners and at the centres of the faces of a cubic unit cell, and F<sup>−</sup> ions are at the centres of the eight small cubes into which the cell may be divided. Each Ca<sup>2+</sup> is coordinated by 8 F<sup>−</sup> neighbours at the corners of a cube, while each F<sup>−</sup> has 4 Ca<sup>2+</sup> neighbours.</p>
<p>This is the only structure in the notes with 8:4 coordination. The reverse structure, antifluorite, is taken by oxides such as Li<sub>2</sub>O and Na<sub>2</sub>O, with the cation and anion positions exchanged. (Standard material added here; it is not in the notes.)</p>
{fig("Rutile, TiO2: a tetragonal cell, one side longer than the others.", fig_rutile())}
<h2>Rutile, TiO<sub>2</sub>, 6:3</h2>
<p>The unit cell of the rutile lattice is a given figure. The cation is octahedrally surrounded by six anions, while the anion (O<sup>2−</sup>) is trigonally surrounded by three cations. Rutile has a low-symmetry anion sublattice that fits neither a simple cubic nor an fcc lattice. The cation sublattice is a distorted body-centred cube, because one side of the cube differs from the others, the cation sublattice is actually body-centred tetragonal. The unit cell is tetragonal.</p>
"""
B11 = f"""
{fig("Schottky: vacancies in pairs. Frenkel: a displaced ion and the vacancy it leaves.", fig_defects())}
<p>There are different types of imperfection, such as point, surface and volume imperfections. Point defects are zero-dimensional, occurring at a single lattice site; extended defects may be one, two or three-dimensional (for example a stacking fault). Defects can also be classified as intrinsic and extrinsic.</p>
<p>Point defects in ionic crystals fall into two groups: stoichiometric defects (Schottky and Frenkel) and non-stoichiometric defects. Intrinsic defects (Schottky and Frenkel defects) occur in the pure crystal, while extrinsic defects originate from impurities present in the crystal. Defects can largely influence physical properties such as mechanical strength, electrical conductivity, colour and chemical reactivity. In ionic crystals only point imperfections are important.</p>
<h2>Point imperfections</h2>
<p>Point imperfections are very often referred to as zero-dimensional imperfections. They are localised in point-like regions and may arise due to:</p>
<ol><li>A vacancy in a lattice site.</li><li>A substitutional impurity.</li><li>Occurrence of a constituent ion in an interstitial space.</li><li>Non-stoichiometric proportions of the constituent ions.</li></ol>
<table><thead><tr><th>Defect</th><th>What happens</th><th>Stoichiometry</th></tr></thead><tbody>
<tr><td><strong>Schottky</strong></td><td>Equal numbers of cation and anion vacancies</td><td>Kept</td></tr>
<tr><td><strong>Frenkel</strong></td><td>An ion moves to an interstitial site, leaving a vacancy</td><td>Kept</td></tr>
</tbody></table>
""" + check_box("A question in the margin of the notes", "The notes also ask, in a line of their own: n-type, p-type, semiconductor, see note. The note it points to is not in the uploaded pages, so it is kept here as an open question. The notes ask why a KCl crystal looks violet in excess potassium, while excess lithium makes LiCl pink. That is an F-centre (colour centre): excess metal gives electrons trapped in anion vacancies, and the trapped electron absorbs visible light. The colour depends on the size of the vacancy, hence on the host crystal, violet in KCl, pink in LiCl. The notes mark this as a question to return to, so it is kept as a question here, with the standard answer given.")

B12 = f"""
{fig("Perovskite CaTiO3: Ca on the corners, O on the face centres, Ti at the body centre.", fig_perovskite())}
<h2>Perovskite, CaTiO<sub>3</sub></h2>
<p>Named after the mineral CaTiO<sub>3</sub>. O<sup>2−</sup> ions, along with the larger cation (Ca<sup>2+</sup>), form a ccp and fcc array in which the octahedral holes formed by O<sup>2−</sup> are occupied by the smaller cation (Ti<sup>4+</sup>). In the unit cell, the eight corners of the cube are occupied by Ca<sup>2+</sup>, O<sup>2−</sup> are placed at the centres of the six faces, and Ti<sup>4+</sup> is placed at the centre of the cube.</p>
<div class="formula">Ca2+: 8 × 1/8 = 1<br>O2−: 6 × 1/2 = 3<br>Ti4+: 1<br>CaTiO<sub>3</sub></div>
<p>The structure can also be interpreted in terms of ReO<sub>3</sub>: the Re positions are occupied by Ti<sup>4+</sup>, while Ca<sup>2+</sup> occupies the centre of the cube. Ti<sup>4+</sup> is octahedrally surrounded by O<sup>2−</sup>, while Ca<sup>2+</sup> is surrounded by 12 O<sup>2−</sup> ions residing at the centre of the edges of the cube.</p>
<table><thead><tr><th>Charge combination</th><th>Examples</th></tr></thead><tbody>
<tr><td>A<sup>II</sup> B<sup>IV</sup> O<sub>3</sub></td><td>A = Ca, Sr, Ba; B = Ti, Zr, Ge, Sn</td></tr>
<tr><td>A<sup>III</sup> B<sup>III</sup> O<sub>3</sub></td><td>A = La; B = Al, Ti, Cr, Mn</td></tr>
<tr><td>A<sup>I</sup> B<sup>V</sup> O<sub>3</sub></td><td>A = Na, K; B = Nb, Ta</td></tr>
</tbody></table>
""" + check_box("One entry corrected", "The notes list Cr among the A-site cations for A<sup>II</sup>B<sup>IV</sup>O<sub>3</sub>. Chromium is not a normal A-site cation in that family; the A site is Ca, Sr or Ba. The table above uses the corrected list.")
B12 += """
<h2>Ilmenite, FeTiO<sub>3</sub></h2>
<p>Named after the mineral ilmenite. It adopts the structure of corundum (α-Al<sub>2</sub>O<sub>3</sub>). In a hexagonal close-packed array of O<sup>2−</sup> ions, two-thirds of the octahedral holes are occupied, one-third by Fe<sup>2+</sup> and one-third by Ti<sup>4+</sup>, in alternating layers.</p>
<table><thead><tr><th>Charge combination</th><th>Examples</th></tr></thead><tbody>
<tr><td>A<sup>II</sup> B<sup>IV</sup> O<sub>3</sub></td><td>A = Fe, Cd, Mg, Co; B = Ti</td></tr>
<tr><td>A<sup>III</sup> B<sup>III</sup> O<sub>3</sub></td><td>No example given in the notes</td></tr>
<tr><td>A<sup>I</sup> B<sup>V</sup> O<sub>3</sub></td><td>A = Li; B = Nb (LiNbO<sub>3</sub>)</td></tr>
</tbody></table>
""" + check_box("Corrected from the handwriting", "One word in the ilmenite paragraph is crossed out, and it reads as Fe<sup>3+</sup>; the general formula at the end of the paragraph is scribbled out. The rest of the paragraph is legible. Ilmenite is Fe<sup>II</sup>Ti<sup>IV</sup>O<sub>3</sub>: Fe<sup>2+</sup>, not Fe<sup>3+</sup>. The two cations together fill two-thirds of the octahedral holes in the hcp oxide array, as in corundum.")

B13 = f"""
{fig("Goldschmidt tolerance factor: the structure that forms as t moves away from 1.", fig_tolerance())}
<p>The Goldschmidt tolerance factor (t) is a dimensionless number used to predict the stability of a crystal and its symmetry in ABO<sub>3</sub> perovskites. It relates the ionic radii of the A-site cation (r<sub>A</sub>), the B-site cation (r<sub>B</sub>) and the anion (r<sub>O</sub>).</p>
<div class="formula">t = (rA + rO) / [ √2 (rB + rO) ]</div>
<p>When t deviates from the ideal value 1, the crystal lattice experiences a steric mismatch, driving structural distortion to lower-symmetry phases.</p>
<table><thead><tr><th class="num">t</th><th>Structure</th><th>Why</th><th>Example</th></tr></thead><tbody>
<tr><td class="num">&gt; 1</td><td>Hexagonal or tetragonal</td><td>A-site cation too large; A site overbonded</td><td>BaTiO<sub>3</sub> (t ≈ 1.06), BaNiO<sub>3</sub></td></tr>
<tr><td class="num">0.9 to 1</td><td>Cubic</td><td>A, B and O packed ideally; BO<sub>6</sub> octahedra untilted</td><td>SrTiO<sub>3</sub> (t ≈ 1.00), CaTiO<sub>3</sub> (t ≈ 0.97, orthorhombic despite t near 1)</td></tr>
<tr><td class="num">0.71 to 0.9</td><td>Orthorhombic / rhombohedral</td><td>A-site cation too small; BO<sub>6</sub> octahedra tilt and rotate</td><td>GdFeO<sub>3</sub> (t ≈ 0.88)</td></tr>
<tr><td class="num">About 0.8</td><td>Different structures</td><td>Perovskite framework gives way to ilmenite-type structures; the boundary is not sharp</td><td>MgTiO<sub>3</sub> (t = 0.81), FeTiO<sub>3</sub> (t ≈ 0.82)</td></tr>
</tbody></table>
""" + check_box("Checked against the standard table", "The ranges in the table are a guide, not a sharp boundary. The notes give collapse below t = 0.8 or above t = 1.05, with MgTiO<sub>3</sub> (t = 0.81 in the notes) as a non-perovskite example. That limit is arguably closer to where the real ilmenites fall than the 0.71 boundary is: MgTiO<sub>3</sub> (t = 0.81) and FeTiO<sub>3</sub> (t ≈ 0.82) are both ilmenite, even though they lie inside the nominal perovskite range. CaTiO<sub>3</sub> itself is orthorhombic, not cubic, at room temperature, despite t ≈ 0.97.")

B14 = f"""
{fig("Octahedral splitting is larger; tetrahedral splitting is inverted and smaller.", fig_cfse())}
<p>This is the page in the photograph you sent. It is the last page of the notes, and it states the rule that decides normal against inverse spinel.</p>
<p class="quote"><strong>From the notes, transcribed:</strong> “This generally takes place [in] transition metal oxide. Generally the site selection is governed by the relative change of CFSE (Crystal Field Stabilization Energy) in occupying the Oct and Td holes.”</p>
<p>The crossed-out words in the photograph are “crystal” (before CFSE) and “octa” (before “oct”). The sentence is about spinel oxides, AB<sub>2</sub>O<sub>4</sub>.</p>
<p>Structure of mixed metal oxides.</p>
<h2>Normal spinel</h2>
<p>Named after the mineral spinel, MgAl<sub>2</sub>O<sub>4</sub>. It consists of a ccp array of oxide ions in which the divalent metal ion (Mg<sup>2+</sup>) occupies 1/8 of the tetrahedral holes and the trivalent metal ion (Al<sup>3+</sup>) occupies 1/2 of the octahedral holes. In a ccp anion sublattice there is one octahedral hole and two tetrahedral holes per anion. There are four oxides per formula unit, and consequently four octahedral holes and eight tetrahedral holes.</p>
<div class="formula">Normal: (A<sup>II</sup>)<sub>tet</sub> (B<sup>III</sup>)<sub>2oct</sub> O<sub>4</sub></div>
<h2>Inverse spinel</h2>
<p>In an inverse spinel, half of the B ions occupy 1/8 of the tetrahedral holes, and A and the other half of B occupy 1/2 of the octahedral holes in the ccp array of O<sup>2−</sup>. In an inverse spinel the A<sup>2+</sup> ion has a strong tendency to occupy octahedral holes, which is why the B<sup>3+</sup> ion is displaced into the tetrahedral hole.</p>
<div class="formula">Inverse: B<sup>III</sup><sub>tet</sub> [A<sup>II</sup> B<sup>III</sup>]<sub>oct</sub> O<sub>4</sub></div>
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
<tr><td>Mn<sub>3</sub>O<sub>4</sub></td><td>Normal: Mn<sup>II</sup>[Mn<sup>III</sup><sub>2</sub>]O<sub>4</sub></td><td>Mn<sup>2+</sup> is high-spin d<sup>5</sup> (CFSE 0); Mn<sup>3+</sup> is d<sup>4</sup> and takes the octahedral site.</td></tr>
<tr><td>CuFe<sub>2</sub>O<sub>4</sub></td><td>Inverse: Fe<sup>3+</sup>[Cu<sup>2+</sup>Fe<sup>3+</sup>]O<sub>4</sub></td><td>Cu<sup>2+</sup> is d<sup>9</sup> and prefers octahedral (also Jahn-Teller distorted); Fe<sup>3+</sup> is d<sup>5</sup> with no preference.</td></tr>
<tr><td>Fe<sub>3</sub>O<sub>4</sub></td><td>Inverse: Fe<sup>3+</sup>[Fe<sup>2+</sup>Fe<sup>3+</sup>]O<sub>4</sub></td><td>Fe<sup>3+</sup> is d<sup>5</sup> (CFSE 0 in either site); Fe<sup>2+</sup> is d<sup>6</sup> and prefers octahedral.</td></tr>
<tr><td>CoFe<sub>2</sub>O<sub>4</sub>, NiFe<sub>2</sub>O<sub>4</sub></td><td>Inverse</td><td>Co<sup>2+</sup> (d<sup>7</sup>) and Ni<sup>2+</sup> (d<sup>8</sup>) have a strong octahedral preference over Fe<sup>3+</sup> (d<sup>5</sup>).</td></tr>
<tr><td>FeCr<sub>2</sub>O<sub>4</sub></td><td>Normal</td><td>Cr<sup>3+</sup> is d<sup>3</sup>, with the largest octahedral preference (0.84 Δ<sub>o</sub>).</td></tr>
<tr><td>Co<sub>3</sub>O<sub>4</sub></td><td>Normal: Co<sup>II</sup>[Co<sup>III</sup><sub>2</sub>]O<sub>4</sub></td><td>Co<sup>2+</sup> is d<sup>7</sup> (tetrahedral); Co<sup>3+</sup> is low-spin d<sup>6</sup> with very high CFSE in the octahedral site.</td></tr>
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

# ---- Chapter 4 sections: the 14 topics grouped into 6 pages, so the chapter is easy to move through ----
COMING = """
<p class="lead">These parts of the Chapter 4 syllabus are not in the 23 handwritten pages uploaded so far. Upload the pages that cover them and they will be added here, in the same format as the rest of the chapter.</p>
<h2>Types of bonding, lattice energy</h2>
<ul><li>Types of bonding in solids: ionic, covalent, metallic, molecular and hydrogen-bonded solids</li><li>Lattice energy, Born-Haber cycle, Madelung constant</li><li>Crystal field considerations in solids, structure-property correlations</li></ul>
<h2>Silicates</h2>
<ul><li>Classification based on SiO<sub>4</sub> tetrahedral linkage</li><li>Single chain silicates (pyroxenes), double chain silicates (amphiboles)</li><li>Sheet silicates (talc, mica, clay minerals)</li><li>Three-dimensional framework silicates (zeolites)</li><li>Isomorphous substitution, ion exchange properties, structural chemistry and industrial applications</li></ul>
<h2>More defects</h2>
<ul><li>Line defects and dislocations, surface defects and grain boundaries</li><li>Non-stoichiometric compounds, metal excess and metal deficiency defects</li><li>Defect equilibria, defect chemistry and its influence on electrical and optical properties</li></ul>
<h2>Band theory and semiconductors</h2>
<ul><li>Free electron theory, band theory of solids</li><li>Conductors, insulators and semiconductors</li><li>Intrinsic and extrinsic semiconductors; n-type and p-type semiconductors (the notes only ask about n-type and p-type in a margin question, the topic itself is not taught there)</li></ul>
<h2>Superconductivity and magnetism</h2>
<ul><li>Superconductivity, critical temperature, Meissner effect, type I and type II superconductors</li><li>Diamagnetism, paramagnetism, ferromagnetism, antiferromagnetism, ferrimagnetism</li><li>Cooperative magnetism and magnetic domains</li></ul>
<h2>Polarization and liquid crystals</h2>
<ul><li>Polarization mechanisms in solids, ferroelectricity, antiferroelectricity, pyroelectricity, piezoelectricity, dielectric properties</li><li>Liquid crystals (nematic, smectic, cholesteric phases), order parameter and phase transitions</li><li>Structure-property relationships and technological applications</li></ul>
"""

SECTIONS = [
 ("01-crystal-and-lattice", "The crystal and its lattice", B01 + B02 + B03 + B04),
 ("02-close-packing-voids", "Close packing, voids and the radius ratio", B05 + B06 + B07),
 ("03-diamond-ionic-structures", "Diamond and ionic crystal structures", B08 + B09 + B10),
 ("04-perovskite-ilmenite-spinel", "Perovskite, ilmenite, tolerance factor and spinel", B12 + B13 + B14),
 ("05-point-defects", "Point defects", B11),
 ("06-still-to-come", "Still to come in this chapter", COMING),
]

def section_nav(current):
    links = []
    for slug, title, _ in SECTIONS:
        cls = ' class="current"' if slug == current else ""
        links.append(f'<a href="{slug}.html"{cls}>{title}</a>')
    return '<nav class="section-nav" aria-label="Sections in this chapter">' + " · ".join(links) + "</nav>"


import re as _re, json as _json

def _slug(text):
    s = _re.sub(r"<[^>]+>", "", text).lower()
    s = _re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "section"

def _add_ids(body, tag):
    def repl(m):
        inner = m.group(1)
        return f'<{tag} id="{_slug(inner)}">{inner}</{tag}>'
    return _re.sub(rf"<{tag}>(.*?)</{tag}>", repl, body)

def _toc_flat(body):
    entries = _re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    items = "".join(f'<li><a href="#{i}">{_re.sub("<[^>]+>", "", x)}</a></li>' for i, x in entries)
    return f'<details class="toc" open><summary>Contents</summary><ol>{items}</ol></details>'

def _chapter_page(rel, title, lede, body, crumb):
    body2 = _add_ids(body, "h2")
    write(rel, page(rel, title, lede, _toc_flat(body2) + body2, crumb))

def main():
    # chapter 4: ONE page, all six sections, with a collapsible table of contents
    ch4_body = '<p class="lead">Chapter 4 of your syllabus, 15 hours. The first five sections are covered by the 23 handwritten pages you uploaded. The sixth lists what is still missing from those pages, so you can see at a glance what the notes do and do not cover.</p>'
    toc_items = ""
    for slug, title, content in SECTIONS:
        c = _add_ids(content.replace("<h2>", "<h3>").replace("</h2>", "</h3>"), "h3")
        subs = "".join(f'<li><a href="#{i}">{_re.sub("<[^>]+>", "", x)}</a></li>' for i, x in _re.findall(r'<h3 id="([^"]+)">(.*?)</h3>', c))
        toc_items += f'<li><a href="#{slug}">{title}</a><ol>{subs}</ol></li>'
        ch4_body += f'<h2 id="{slug}">{title}</h2>' + c
    toc = f'<details class="toc" open><summary>Contents: Chapter 4</summary><ol>{toc_items}</ol></details>'
    write("chapters/04-solids/index.html", page("chapters/04-solids/index.html", "Structure and properties of solids", "Chapter 4 · 15 hours. Partly covered by your notes; the rest is listed and waiting.", toc + ch4_body, '<a href="../../index.html">Chapters</a> / Chapter 4'))
    # old section pages redirect to the single chapter page, at the right section
    for slug, title, _ in SECTIONS:
        write(f"chapters/04-solids/{slug}.html", f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=index.html#{slug}"><title>Moved</title></head><body><p>This section now lives on <a href="index.html#{slug}">the Chapter 4 page</a>.</p></body></html>')
    # old topic URLs redirect to the new section pages
    old_to_new = {
        "01-crystalline-amorphous": "01-crystal-and-lattice", "02-lattice-unit-cells": "01-crystal-and-lattice",
        "03-symmetry-seven-systems": "01-crystal-and-lattice", "04-atoms-per-unit-cell": "01-crystal-and-lattice",
        "05-close-packing-1d-2d": "02-close-packing-voids", "06-hcp-ccp": "02-close-packing-voids",
        "07-voids-radius-ratio": "02-close-packing-voids", "08-diamond-cubic": "03-diamond-ionic-structures",
        "09-ionic-crystals-ab": "03-diamond-ionic-structures", "10-ionic-crystals-ab2": "03-diamond-ionic-structures",
        "11-point-defects": "05-point-defects", "12-perovskite-ilmenite": "04-perovskite-ilmenite-spinel",
        "13-tolerance-factor": "04-perovskite-ilmenite-spinel", "14-spinel-cfse": "04-perovskite-ilmenite-spinel",
    }
    for old, new in old_to_new.items():
        dest = f"../04-solids/index.html#{new}"
        write(f"chapters/01-solid-state/{old}.html", f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={dest}"><title>Moved</title></head><body><p>This page has moved to <a href="{dest}">the Chapter 4 page</a>.</p></body></html>')
    write("chapters/01-solid-state/index.html", '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=../04-solids/index.html"><title>Moved</title></head><body><p>This chapter has moved to <a href="../04-solids/index.html">Chapter 4 · Structure and properties of solids</a>.</p></body></html>')
    # chapters 1-3: upload soon
    upcoming = [
        ("01-bonding-quantum", "Bonding and properties in chemical system: a quantum chemical approach", "15 hours. The Born-Oppenheimer approximation, the hydrogen molecular ion (H2+), molecular orbital theory, LCAO, LCAO-MO method, MO of homo- and heteronuclear diatomic molecules, MO of polynuclear ABn type molecules, molecular electronic terms, the hydrogen molecule (H2), electron probability density, dipole moment, semiempirical treatment of polyatomic molecules: Hückel method of π-MO calculation, Frost diagram of carbocyclic π-systems."),
        ("02-elements-coordination", "Chemistry of elements and Coordination chemistry: structure, bonding, stereochemistry and properties", "15 hours. Chemistry of elements: structural versatility, design and synthesis, isolation, characterization, spectral, magnetic and catalytic properties. Non-transition and transition metal complexes, inner-transition metals. Coordination chemistry: Orgel diagram, Tanabe-Sugano diagram, ligand symmetry orbitals, spectral properties, Nephelauxetic effect, Racah parameter, vibronic coupling, spin-orbit coupling, magnetic properties, Jahn-Teller and Renner-Teller effects, CFSE and spectroscopy."),
        ("03-organometallic", "Organometallic chemistry-I", "15 hours. Valence electron count, oxidation number and formal ligand charge; carbonyl ligand, pi-ligands, complexes containing M-C, M=C and M≡C bonds, hydride and dihydrogen complexes, phosphines and related ligands, spectral analysis and characterization, Dewar-Chatt-Duncanson bonding model, isolobal analogy, agostic interaction."),
    ]
    for slug, title, desc in upcoming:
        num = slug[:2]
        body = f'<p class="lead">{desc}</p><aside class="note"><p><strong>Upload soon.</strong> No handwritten pages for this chapter have been uploaded yet. Upload them and they will be transcribed, checked and added here in the same format as Chapter 4.</p></aside><p><a class="btn" href="../04-solids/index.html">Read Chapter 4 instead</a></p>'
        _chapter_page(f"chapters/{slug}/index.html", title, "Upload soon. The chapter will be added from your notes.", body, f'<a href="../../index.html">Chapters</a> / Chapter {num}')
    # home
    home_body = """
<p class="lead">Your handwritten inorganic chemistry notes, set as a readable reference: one chapter per subject, one page per section, figures redrawn so they can be checked. Four chapters, 15 hours each. Chapter 4 is partly covered by the 23 pages you uploaded; the other three are waiting for their pages.</p>
<ol class="chapter-list">
<li><div><h2><a href="chapters/01-bonding-quantum/index.html">1. Bonding and properties in chemical system: a quantum chemical approach</a></h2><p>Born-Oppenheimer, H2+, MO theory, LCAO, diatomic and polynuclear molecules, Hückel method, Frost diagrams.</p></div><span class="status">Upload soon · 15 hours</span></li>
<li><div><h2><a href="chapters/02-elements-coordination/index.html">2. Chemistry of elements and Coordination chemistry</a></h2><p>Elements and complexes, inner-transition metals, Orgel and Tanabe-Sugano diagrams, spectra, magnetism, Jahn-Teller.</p></div><span class="status">Upload soon · 15 hours</span></li>
<li><div><h2><a href="chapters/03-organometallic/index.html">3. Organometallic chemistry-I</a></h2><p>Electron count, carbonyls, pi-ligands, M-C bonds, hydrides, phosphines, Dewar-Chatt-Duncanson, isolobal analogy.</p></div><span class="status">Upload soon · 15 hours</span></li>
<li><div><h2><a href="chapters/04-solids/index.html">4. Structure and properties of solids</a></h2><p>Crystalline and amorphous solids, lattices, close packing, ionic structures, perovskite, spinel, defects, and what is still to come.</p></div><span class="status">Partly covered · 15 hours</span></li>
</ol>
<p><a class="btn btn-primary" href="chapters/04-solids/index.html">Start Chapter 4</a></p>
"""
    write("index.html", page("index.html", "Solid state, drawn clearly", "Inorganic chemistry notes, chapter by chapter, with the figures redrawn and the handwriting checked.", home_body, "Home"))
    # sources
    sources_body = """
<p class="lead">Every page was transcribed from the rendered PDF pages first, then checked. Where the handwriting and the standard source disagreed, the site keeps the standard result and says what the notes said.</p>
<h2>What was transcribed</h2>
<p>The uploaded PDF, <span class="num">PDF_Gallery_20261115_202140.pdf</span>, 23 pages of handwritten notes. Page 11 is a duplicate photograph of page 10, so it adds no new topic. The single photograph you sent in chat is page 23 of that PDF.</p>
<h2>What the notes cover in Chapter 4, and what is still missing</h2>
<p><strong>Covered by your notes:</strong> crystalline and amorphous solids, lattice, basis, unit cell, symmetry elements, Bravais lattices, close packing (hcp, ccp), voids, radius ratio rules, AB and AB₂ type structures, perovskite, ilmenite, rutile, tolerance factor and structural distortion, normal and inverse spinel, cation distribution, diamond cubic, zinc blende and wurtzite, point defects (Schottky and Frenkel), F-centres (as a question), n-type and p-type semiconductors (as a margin question only).</p>
<p><strong>Not in your notes yet:</strong> types of bonding in solids, lattice energy, Born-Haber cycle, Madelung constant, crystal field considerations in solids, silicates (pyroxenes, amphiboles, talc, mica, clays, zeolites), line and surface defects, non-stoichiometric compounds, defect equilibria, band theory, conductors, insulators and semiconductors, superconductivity, magnetism (dia-, para-, ferro-, antiferro- and ferrimagnetism), polarization, ferroelectricity, piezoelectricity, liquid crystals. These are listed on the last section page of Chapter 4. Upload the pages that cover them and they will be added there.</p>
<h2>What was checked, and where</h2>
<table><thead><tr><th>Claim in the notes</th><th>Result</th><th>Source</th></tr></thead><tbody>
<tr><td>Normal spinel: A<sup>2+</sup> in 1/8 Td, B<sup>3+</sup> in 1/2 Oct; inverse: B(AB)O<sub>4</sub></td><td>Correct</td><td>LibreTexts, Spinel, Perovskite, and Rutile Structures</td></tr>
<tr><td>Site selection governed by relative CFSE in Oct and Td holes</td><td>Correct, the standard explanation for transition-metal oxide spinels</td><td>LibreTexts, Spinel, Perovskite, and Rutile Structures</td></tr>
<tr><td>OSPE: d<sup>3</sup>/d<sup>8</sup> 0.84, d<sup>4</sup>/d<sup>9</sup> 0.42, d<sup>2</sup>/d<sup>7</sup> 0.27, d<sup>1</sup>/d<sup>6</sup> 0.13, d<sup>0</sup>/d<sup>5</sup>/d<sup>10</sup> 0 (Δ<sub>o</sub>)</td><td>Correct, high spin, Δ<sub>t</sub> = 4/9 Δ<sub>o</sub></td><td>LibreTexts, Octahedral vs. Tetrahedral Geometries</td></tr>
<tr><td>Goldschmidt t: &gt;1 hexagonal/tetragonal, 0.9 to 1 cubic, 0.71 to 0.9 orthorhombic/rhombohedral, about 0.8 ilmenite-type</td><td>Ranges are a guide only; the notes' 0.8 / 1.05 collapse limits are the working rule</td><td>Wikipedia, Goldschmidt tolerance factor</td></tr>
<tr><td>Perovskite: Ca corners, O face centres, Ti body centre; Ti CN 6, Ca CN 12</td><td>Correct</td><td>Wikipedia, Perovskite; University of Sydney, CHEM1902 2007-N-6</td></tr>
<tr><td>Ilmenite FeTiO<sub>3</sub>, corundum-type, 2/3 of octahedral holes filled</td><td>Correct, with Fe<sup>2+</sup> (not Fe<sup>3+</sup> as one crossed-out word suggested)</td><td>LibreTexts / standard corundum description</td></tr>
<tr><td>Radius ratios 0.225 / 0.414 / 0.732</td><td>Correct</td><td>LibreTexts, Structures of Simple Binary Compounds</td></tr>
<tr><td>Diamond packing efficiency 34%</td><td>Correct</td><td>Standard calculation, a = 8r/√3</td></tr>
<tr><td>HCP and CCP packing efficiency 74%, CN 12</td><td>Correct</td><td>Standard close-packing result</td></tr>
</tbody></table>
<h2>Corrections made on the site</h2>
<ul><li>Ilmenite: Fe<sup>2+</sup>, not Fe<sup>3+</sup>.</li><li>Perovskite A-site list: Cr removed from the A<sup>II</sup> list.</li><li>Tetrahedral radius-ratio working: the crossed-out algebra in the notes was not reproduced; the standard limiting value 0.225 is given.</li><li>Tolerance-factor limits: the standard 0.71 to 1.0 ranges are given, with the notes’ 0.8 / 1.05 rule marked as an approximation.</li><li>BCC paragraph: the in-plane neighbour count of four is not the bcc coordination number, which is 8.</li>
<li>Zinc-blende working: the notes' tetrahedral algebra is crossed out and its last legible step gives 0.449, not 0.225. The page gives the standard working instead, a quarter of the body diagonal, r<sup>+</sup> + r<sup>−</sup> = √3a/4.</li>
<li>Tolerance factor: the notes' 0.8 / 1.05 collapse limits are kept as the working rule, and the table now says the ranges are a guide only, because MgTiO<sub>3</sub> (t = 0.81) and FeTiO<sub>3</sub> (t ≈ 0.82) are ilmenite inside the nominal perovskite range, and CaTiO<sub>3</sub> (t ≈ 0.97) is orthorhombic despite t near 1.</li>
<li>The notes write “stacking fold”; the standard term is “stacking fault”.</li>
<li>Antifluorite (Li<sub>2</sub>O, Na<sub>2</sub>O) and the radius-ratio “guide, not a law” sentence are standard material added by the site, not in the notes, and are marked as such on the pages.</li></ul>
<h2>Design</h2>
<p>Redesigned from scratch to a warm lab-notebook look: paper #FAF7F1, deep teal accent, Fraunces heads over Source Sans 3, one 760px column shared by the text and the figures, built with the Hallmark design skill (nutlope/hallmark, installed with <span class="num">npx skills add nutlope/hallmark -g</span>) and checked against the taste and UI/UX skills. The notes' wording is kept word for word, organised into topics; anything added or corrected is flagged in a note on the page. All figures are inline SVG drawn for this site, no photographs of the handwritten pages are reproduced, so the text is searchable. Figures are animated as an extra, with a pause button in the footer and a still version under reduced-motion settings.</p>
"""
    _chapter_page("sources.html", "Sources and checks", "How the handwriting was read, what was verified online, and what was corrected.", sources_body, '<a href="index.html">Chapters</a> / Sources')
    # search index: one entry per heading, from the finished pages
    entries = []
    for rel in ["index.html", "sources.html", "chapters/01-bonding-quantum/index.html", "chapters/02-elements-coordination/index.html", "chapters/03-organometallic/index.html", "chapters/04-solids/index.html"]:
        html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        main = html.split("<main", 1)[1].split("</main>", 1)[0] if "<main" in html else html
        parts = _re.split(r'<h[23] id="([^"]+)">(.*?)</h[23]>', main)
        # parts: [pre, id, title, text, id, title, text, ...]
        for k in range(1, len(parts) - 1, 3):
            anchor, heading, text = parts[k], parts[k+1], parts[k+2]
            plain = _re.sub(r"<[^>]+>", " ", text)
            plain = _re.sub(r"\s+", " ", plain).strip()
            entries.append({"t": _re.sub("<[^>]+>", "", heading).strip(), "u": rel, "a": anchor, "x": plain[:600]})
    with open(os.path.join(ROOT, "assets", "search.json"), "w", encoding="utf-8") as f:
        _json.dump(entries, f, ensure_ascii=False)
    print("search index:", len(entries), "entries")
    # deploy files
    with open(os.path.join(ROOT, "wrangler.toml"), "w", encoding="utf-8") as f:
        f.write('name = "inorganicvii"\ncompatibility_date = "2026-11-15"\npages_build_output_dir = "."\n')
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# inorganicvii

Static multi-page notes site for Cloudflare Pages.
Production URL: https://inorganicvii.pages.dev

## Structure

- `index.html`, chapter list (4 syllabus chapters)
- `chapters/04-solids/`, 6 section pages, transcribed from the 23-page PDF
- `chapters/01-bonding-quantum/`, `02-elements-coordination/`, `03-organometallic/`, upload soon
- `sources.html`, verification log and syllabus coverage
- `assets/style.css`, site theme

## Deploy to Cloudflare Pages

```bash
cd inorganicvii
npx wrangler login
npx wrangler pages deploy . --project-name inorganicvii
```

First time only: `npx wrangler pages project create inorganicvii --production-branch main`

Or in the dashboard: Workers and Pages, then Create, then Pages, then Upload assets, then upload this folder, project name `inorganicvii`.

No build step. No server code.
""")
    print("done")

if __name__ == "__main__":
    main()
