"""
CoreMotion — gerador oficial da identidade visual.

Produz os SVGs (e opcionalmente PNGs) do sistema de marca:
  logotipo  · isotipo · imagotipo · isologo  + ícone de app

Requisitos (opcional, apenas para regenerar):
  python3 -m pip install fonttools brotli
  fontes (SIL OFL): Montserrat 800/900 e Barlow Condensed 900
    npm pack @fontsource/montserrat && npm pack @fontsource/barlow-condensed

Uso:
  python3 brand/tools/generate.py            # escreve brand/svg/*.svg
  python3 brand/tools/generate.py --png      # + brand/png/*.png (precisa @resvg/resvg-js)
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                 # brand/
FONT_DIR = os.environ.get('COREMOTION_FONTS', os.path.join(HERE, 'fonts'))

# ───────────────────────────────────────────────────────────── utilities
def fmt(v):
    s = f"{v:.2f}"
    return s.rstrip('0').rstrip('.') if '.' in s else s

def pts(seq):
    return "".join(f"L{fmt(x)} {fmt(y)}" for x, y in seq)

def poly(seq):
    return f"M{fmt(seq[0][0])} {fmt(seq[0][1])}" + pts(seq[1:])

def closed(seq):
    return poly(seq) + "Z"

def pchip(keys, s):
    xs = [k[0] for k in keys]; ys = [k[1] for k in keys]
    if s <= xs[0]: return ys[0]
    if s >= xs[-1]: return ys[-1]
    i = 0
    while i < len(xs) - 2 and s > xs[i + 1]: i += 1
    t = (s - xs[i]) / (xs[i + 1] - xs[i])
    y0 = ys[i - 1] if i > 0 else ys[i]
    y1, y2 = ys[i], ys[i + 1]
    y3 = ys[i + 2] if i + 2 < len(ys) else ys[i + 1]
    m1, m2 = (y2 - y0) / 2, (y3 - y1) / 2
    t2, t3 = t * t, t * t * t
    return ((2*t3-3*t2+1)*y1 + (t3-2*t2+t)*m1 + (-2*t3+3*t2)*y2 + (t3-t2)*m2)

# ───────────────────────────────────────────────────────────── typography
FONTS = {
    'mont900': 'montserrat-latin-900-normal.woff2',
    'mont800': 'montserrat-latin-800-normal.woff2',
    'mont700': 'montserrat-latin-700-normal.woff2',
    'barlow900': 'barlow-condensed-latin-900-normal.woff2',
}
_ttcache = {}

def _tt(name):
    from fontTools.ttLib import TTFont
    if name not in _ttcache:
        _ttcache[name] = TTFont(os.path.join(FONT_DIR, FONTS[name]))
    return _ttcache[name]

def text_path(text, font='mont900', size=100, tracking=0.0, skew=0.0):
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.misc.transform import Transform
    tt = _tt(font)
    cmap, gs = tt.getBestCmap(), tt.getGlyphSet()
    sc = size / tt['head'].unitsPerEm
    x, out = 0.0, []
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            x += size * .4; continue
        pen = SVGPathPen(gs)
        t = Transform(sc, 0, 0, -sc, x, 0)
        if skew:
            t = t.transform(Transform(1, 0, skew, 1, 0, 0))
        gs[g].draw(TransformPen(pen, t))
        d = pen.getCommands()
        if d: out.append(d)
        x += tt['hmtx'][g][0] * sc + tracking * size
    return " ".join(out), x - tracking * size

def cap_height(font='mont900', size=100):
    tt = _tt(font)
    ch = getattr(tt['OS/2'], 'sCapHeight', 0) or tt['head'].unitsPerEm * .7
    return ch * size / tt['head'].unitsPerEm

def arc_text(text, font='mont700', size=36, radius=200, cx=0, cy=0,
             start_deg=-90, direction=1, tracking=0.12):
    """Texto sobre arco circular, convertido em curvas (sem depender de <text>)."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.misc.transform import Transform
    tt = _tt(font)
    cmap, gs = tt.getBestCmap(), tt.getGlyphSet()
    sc = size / tt['head'].unitsPerEm
    items, total = [], 0.0
    for ch in text:
        g = cmap.get(ord(ch))
        w = tt['hmtx'][g][0] * sc if g else size * .4
        items.append((ch, g, w)); total += w + tracking * size
    total -= tracking * size
    th = math.radians(start_deg) - direction * (total / 2) / radius
    out = []
    for ch, g, w in items:
        dth = (w + tracking * size) / radius
        th += direction * dth / 2
        if g:
            ct, st = math.cos(th), math.sin(th)
            tx_, ty_ = direction * -st, direction * ct
            ux, uy = direction * ct, direction * st
            px, py = cx + radius * ct, cy + radius * st
            m = Transform(tx_ * sc, ty_ * sc, ux * sc, uy * sc,
                          px - tx_ * w / 2, py - ty_ * w / 2)
            pen = SVGPathPen(gs)
            gs[g].draw(TransformPen(pen, m))
            d = pen.getCommands()
            if d: out.append(d)
        th += direction * dth / 2
    return " ".join(out)

# ───────────────────────────────────────────────────────────── the mark
CX = CY = 256
R = 118
A_TAIL, A_HEAD = -44.0, -316.0
PROFILE = [(0.0, 1.2), (0.05, 5.4), (0.12, 14.5), (0.22, 26.5), (0.33, 36.2),
           (0.45, 41.4), (0.53, 42.6), (0.62, 41.6), (0.72, 38.4),
           (0.82, 33.4), (0.91, 25.4), (1.0, 12.2)]

def band(r=R, a0=A_TAIL, a1=A_HEAD, profile=PROFILE, n=400, head_trim=0.10, swell=0.010):
    outer, inner = [], []
    for k in range(n + 1):
        s = k / n
        a = math.radians(a0 + (a1 - a0) * s)
        h = pchip(profile, s)
        rr = r * (1 + swell * math.sin(math.pi * s))
        ux, uy = math.cos(a), -math.sin(a)
        px, py = CX + rr * ux, CY + rr * uy
        outer.append((px + ux * h, py + uy * h))
        inner.append((px - ux * h, py - uy * h))
    inner = inner[:int(n * (1 - head_trim)) + 1]
    return outer, inner

def taper(outer, inner):
    return poly(outer) + f"L{fmt(inner[-1][0])} {fmt(inner[-1][1])}" + pts(list(reversed(inner))) + "Z"

OUTER, INNER = band()
CORE = taper(OUTER, INNER)

def spiral_trail(r0=112, a0=-46, turns=0.58, r1=28, w0=6.2, w1=0.85, n=320, root=0.10):
    top, bot = [], []
    for k in range(n + 1):
        t = k / n
        a = math.radians(a0 - 360 * turns * (t ** 0.85))
        r = r0 + (r1 - r0) * (t ** 0.9)
        w = w0 * (1 - t) ** 0.9 + w1
        if t < root:
            w *= (t / root) ** 0.65
        ux, uy = math.cos(a), -math.sin(a)
        top.append((CX + (r + w) * ux, CY + (r + w) * uy))
        bot.append((CX + (r - w) * ux, CY + (r - w) * uy))
    return taper(top, bot)

TRAIL = spiral_trail()

def lens(r, a0, a1, w, n=160, pow_=0.55, tin=0.03, tout=0.03):
    top, bot = [], []
    for k in range(n + 1):
        t = k / n
        f = min(1, t / tin if tin else 1, (1 - t) / tout if tout else 1)
        ww = w * (max(f, 0) ** pow_) * math.sin(math.pi * t) ** 0.25
        a = math.radians(a0 + (a1 - a0) * t)
        top.append((CX + (r + ww) * math.cos(a), CY - (r + ww) * math.sin(a)))
        bot.append((CX + (r - ww) * math.cos(a), CY - (r - ww) * math.sin(a)))
    return taper(top, bot)

RIM = lens(116.0, -38, -290, 2.0)
SPEC = lens(133.0, -72, -176, 7.0)

# ───────────────────────────────────────────────────────────── palettes
INK   = '#0B0C10'
INK2  = '#111319'
RED   = '#E50914'
CORAL = '#FF6A45'
SNOW  = '#F8FAFC'
STEEL = '#94A3B8'

GRADS = '''<linearGradient id="{p}red" x1="0.08" y1="0" x2="0.82" y2="1" gradientUnits="objectBoundingBox">
  <stop offset="0" stop-color="#FF8A4C"/><stop offset="0.14" stop-color="#FF4A34"/>
  <stop offset="0.42" stop-color="#EF0F1D"/><stop offset="0.72" stop-color="#C40814"/>
  <stop offset="1" stop-color="#7C0410"/></linearGradient>
<linearGradient id="{p}rim" x1="0.1" y1="0" x2="0.9" y2="1">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/>
  <stop offset="0.4" stop-color="#FFD9C2" stop-opacity="0.5"/>
  <stop offset="1" stop-color="#FF9C6B" stop-opacity="0"/></linearGradient>
<linearGradient id="{p}spec" x1="0" y1="0" x2="0.6" y2="1">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.34"/>
  <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'''

def defs(p=''):
    return f'<defs>{GRADS.format(p=p)}</defs>'

def mark(p='', mode='gradient', detail=True):
    """marca em caixa 512×512. mode: gradient | white | ink | mono(<cor>)"""
    if mode == 'white':
        body = f'<path d="{CORE}" fill="{SNOW}"/>'
        return body
    if mode == 'ink':
        return f'<path d="{CORE}" fill="{INK}"/>'
    if mode.startswith('#'):
        return (f'<path d="{TRAIL}" fill="{mode}" opacity="0.9"/><path d="{CORE}" fill="{mode}"/>') if detail \
            else f'<path d="{CORE}" fill="{mode}"/>'
    out = ''
    if detail:
        out += f'<path d="{TRAIL}" fill="{CORAL}" opacity="0.95"/>'
    out += f'<path d="{CORE}" fill="url(#{p}red)"/>'
    if detail:
        out += f'<path d="{RIM}" fill="url(#{p}rim)" opacity="0.55"/>'
        out += f'<path d="{SPEC}" fill="url(#{p}spec)" opacity="0.55"/>'
    return out

# ───────────────────────────────────────────────────────────── assets
WM_SIZE, WM_TRACK, WM_SKEW = 200, -0.030, -0.13
WORD, WORD_W = text_path('CoreMotion', 'mont900', WM_SIZE, WM_TRACK, WM_SKEW)
CAP = cap_height('mont900', WM_SIZE)

def svg(w, h, body, p='a', title=''):
    t = f'<title>{title}</title>' if title else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{round(w,2)}" height="{round(h,2)}" '
            f'viewBox="0 0 {round(w,2)} {round(h,2)}" role="img" aria-label="{title}">'
            f'{defs(p)}{t}{body}</svg>')

def bg_rect(w, h, color):
    if not color:
        return ''
    return f'<rect width="{round(w,2)}" height="{round(h,2)}" fill="{color}"/>'

# 1 — LOGOTIPO ------------------------------------------------------------
def logotipo(two_tone=True, mono=False, bg=None, rule=False):
    base, x0 = 268, 46
    W, H = x0 + WORD_W + 42, base + 62
    if mono:
        body = bg_rect(W, H, bg) if bg else ''
        body += f'<path d="{WORD}" fill="{SNOW if mono=="white" else INK}" transform="translate({x0},{base})"/>'
    elif two_tone:
        # "Core" branco · "Motion" vermelho = aceleração cromática
        core_d, core_w = text_path('Core', 'mont900', WM_SIZE, WM_TRACK, WM_SKEW)
        motion_d, _ = text_path('Motion', 'mont900', WM_SIZE, WM_TRACK, WM_SKEW)
        body = bg_rect(W, H, bg) if bg else ''
        body += f'<path d="{core_d}" fill="{SNOW}" transform="translate({x0},{base})"/>'
        body += f'<path d="{motion_d}" fill="{RED}" transform="translate({x0+core_w+18},{base})"/>'
    else:
        body = bg_rect(W, H, bg) if bg else ''
        body += f'<path d="{WORD}" fill="{SNOW}" transform="translate({x0},{base})"/>'
    return svg(W, H, body, 'lg', 'CoreMotion — logotipo')

def logotipo_rule(bg=None):
    base, x0 = 250, 46
    W, H = x0 + WORD_W + 42, base + 152
    core_d, core_w = text_path('Core', 'mont900', WM_SIZE, WM_TRACK, WM_SKEW)
    motion_d, _ = text_path('Motion', 'mont900', WM_SIZE, WM_TRACK, WM_SKEW)
    body = bg_rect(W, H, bg)
    body += f'<path d="{core_d}" fill="{SNOW}" transform="translate({x0},{base})"/>'
    body += f'<path d="{motion_d}" fill="{RED}" transform="translate({x0+core_w+18},{base})"/>'
    # régua de velocidade: engrossa para a direita, cortada em 3 segmentos
    y = base + 62
    body += (f'<path d="M{x0} {y}H{x0+640}" stroke="{RIMC}" stroke-width="7" stroke-linecap="round" opacity="0.25"/>')
    body += (f'<path d="M{x0} {y}H{x0+WORD_W-40}" stroke="{RED}" stroke-width="7" stroke-linecap="round"/>')
    return svg(W, H, body, 'lr', 'CoreMotion — logotipo com régua de velocidade')

RIMC = CORAL

# 2 — ISOTIPO -------------------------------------------------------------
def isotipo(mode='gradient', bg=None, detail=True):
    body = bg_rect(512, 512, bg) if bg else ''
    body += mark('is', mode, detail=detail)
    return svg(512, 512, body, 'is', 'CoreMotion — isotipo (C de velocidade)')

def isotipo_badge(bg=INK, size=512, rounded=False, mode='gradient'):
    body = (f'<rect width="512" height="512" rx="112" fill="{bg}"/>' if rounded
            else f'<rect width="512" height="512" fill="{bg}"/>')
    body += (f'<radialGradient id="isglow" cx="0.5" cy="0.45" r="0.58">'
             f'<stop offset="0" stop-color="{RED}" stop-opacity="0.22"/>'
             f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>')
    body += f'<rect width="512" height="512" rx="{112 if rounded else 0}" fill="url(#isglow)"/>'
    s = 0.78
    body += f'<g transform="translate({256-256*s},{256-256*s}) scale({s})">{mark("ib", mode)}</g>'
    return svg(512, 512, body, 'ib', 'CoreMotion — ícone de aplicativo')

# 3 — IMAGOTIPO -----------------------------------------------------------
def imagotipo(vertical=False, bg=None, mode='gradient', tagline=True, color=SNOW, sub=STEEL):
    size = 150
    word, ww = text_path('CoreMotion', 'mont900', size, -0.028, -0.13)
    cap = cap_height('mont900', size)
    subt, sw = (text_path('HUB DE ALTA PERFORMANCE', 'mont700', 31, 0.30) if tagline else ('', 0))
    if not vertical:
        MH = cap * 1.95
        gap = cap * 0.62
        block_h = cap + (44 + 22 if tagline else 0)
        top = (MH - block_h) / 2
        pad = 40
        W = MH + gap + max(ww, sw) + pad * 2
        H = MH + pad * 2
        body = bg_rect(W, H, bg) if bg else ''
        body += f'<g transform="translate({pad},{pad}) scale({MH/512})">{mark("im", mode)}</g>'
        tx = pad + MH + gap
        body += f'<path d="{word}" fill="{color}" transform="translate({tx},{pad+top+cap})"/>'
        if tagline:
            body += f'<path d="{subt}" fill="{sub}" transform="translate({tx+3},{pad+top+cap+50})"/>'
        return svg(W, H, body, 'im', 'CoreMotion — imagotipo horizontal')
    MH = 300
    gap = 46
    pad = 44
    W = max(MH, ww, sw) + pad * 2
    H = MH + gap + cap + (46 if tagline else 0) + pad * 2
    body = bg_rect(W, H, bg) if bg else ''
    body += f'<g transform="translate({(W-MH)/2},{pad}) scale({MH/512})">{mark("iv", mode)}</g>'
    by = pad + MH + gap + cap
    body += f'<path d="{word}" fill="{color}" transform="translate({(W-ww)/2},{by})"/>'
    if tagline:
        body += f'<path d="{subt}" fill="{sub}" transform="translate({(W-sw)/2},{by+44})"/>'
    return svg(W, H, body, 'iv', 'CoreMotion — imagotipo vertical')

# 4 — ISOLOGO -------------------------------------------------------------
def isologo(bg=None, mode='gradient', disc=None, ring=SNOW, color=SNOW, sub=STEEL):
    S = 600
    body = bg_rect(600, 600, bg) if bg else ''
    if disc:
        body += f'<circle cx="300" cy="300" r="296" fill="{disc}"/>'
    # anel de velocidade: traços afilados, com a abertura alinhada à boca do "C"
    for a0, a1 in [(-116, -66), (-52, -14), (14, 62), (78, 126), (142, 190), (206, 232)]:
        body += f'<path d="{lens_r(300, 300, 262, a0, a1, 4.6)}" fill="{ring}" opacity="0.92"/>'
    body += (f'<circle cx="300" cy="300" r="224" fill="none" stroke="{sub}" '
             f'stroke-width="1.2" opacity="0.45"/>')
    body += f'<path d="{arc_text("COREMOTION", "mont800", 46, 191, 300, 300, -90, 1, 0.18)}" fill="{color}"/>'
    body += f'<path d="{arc_text("HUB DE ALTA PERFORMANCE", "mont700", 27, 191, 300, 300, 90, -1, 0.24)}" fill="{sub}"/>'
    ms = 272
    body += f'<g transform="translate({300-ms/2},{300-ms/2}) scale({ms/512})">{mark("io", mode)}</g>'
    return svg(S, S, body, 'io', 'CoreMotion — isologo (emblema circular)')

def lens_r(cx, cy, r, a0, a1, w, n=120):
    """traço de velocidade sobre arco: afila nas duas pontas"""
    top, bot = [], []
    for k in range(n + 1):
        t = k / n
        ww = w * (math.sin(math.pi * t) ** 0.42)
        a = math.radians(a0 + (a1 - a0) * t)
        top.append((cx + (r + ww) * math.cos(a), cy - (r + ww) * math.sin(a)))
        bot.append((cx + (r - ww) * math.cos(a), cy - (r - ww) * math.sin(a)))
    return taper(top, bot)

def _arc(cx, cy, r, a0, a1, n=100):
    p = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
          cy - r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return poly(p)

# ───────────────────────────────────────────────────────────── output
FILES = {
    '01-logotipo-duotone.svg':      lambda: logotipo(two_tone=True),
    '02-logotipo-branco.svg':       lambda: logotipo(mono='white'),
    '03-logotipo-preto.svg':        lambda: logotipo(mono='ink', bg='#FFFFFF'),
    '04-logotipo-com-regua.svg':    logotipo_rule,
    '05-isotipo.svg':               lambda: isotipo('gradient'),
    '06-isotipo-branco.svg':        lambda: isotipo('white'),
    '07-isotipo-mono.svg':          lambda: isotipo('ink', bg='#FFFFFF'),
    '08-isotipo-simplificado.svg':  lambda: isotipo('gradient', detail=False),
    '09-imagotipo-horizontal.svg':  lambda: imagotipo(),
    '10-imagotipo-horizontal-branco.svg': lambda: imagotipo(mode='white', sub='#CBD5E1'),
    '11-imagotipo-vertical.svg':    lambda: imagotipo(vertical=True),
    '12-imagotipo-vertical-branco.svg': lambda: imagotipo(vertical=True, mode='white', sub='#CBD5E1'),
    '13-isologo.svg':               lambda: isologo(),
    '14-isologo-mono.svg':          lambda: isologo(mode='white', ring=SNOW),
    '15-icone-app.svg':             lambda: isotipo_badge(bg=INK, rounded=True),
    '16-favicon.svg':               lambda: isotipo_badge(bg=INK, rounded=False),
}

def main():
    out_svg = os.path.join(ROOT, 'svg')
    os.makedirs(out_svg, exist_ok=True)
    for name, fn in FILES.items():
        with open(os.path.join(out_svg, name), 'w') as f:
            f.write(fn())
    print(f'{len(FILES)} SVGs escritos em {out_svg}')
    print('paths para React:', emit_ts())


# ───────────────────────────────────────────────────────────── React export
def emit_ts():
    """Gera components/brand/marks.generated.ts para uso direto no site."""
    core_d, core_w = text_path('Core', 'mont900', WM_SIZE, WM_TRACK, WM_SKEW)
    motion_d, _ = text_path('Motion', 'mont900', WM_SIZE, WM_TRACK, WM_SKEW)
    lines = [
        '/** GERADO AUTOMATICAMENTE por brand/tools/generate.py — não editar à mão. */',
        f'export const MARK_CORE = {CORE!r};',
        f'export const MARK_TRAIL = {TRAIL!r};',
        f'export const MARK_RIM = {RIM!r};',
        f'export const MARK_SPEC = {SPEC!r};',
        f'export const WORD_ALL = {WORD!r};',
        f'export const WORD_CORE = {core_d!r};',
        f'export const WORD_MOTION = {motion_d!r};',
        f'export const WORD_WIDTH = {round(WORD_W, 2)};',
        f'export const WORD_CAP = {round(CAP, 2)};',
        f'export const WORD_CORE_ADV = {round(core_w, 2)};',
        '',
    ]
    dest = os.path.join(os.path.dirname(ROOT), 'components', 'brand', 'marks.generated.ts')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'w') as f:
        f.write("\n".join(lines).replace("'", '"'))
    return dest

if __name__ == '__main__':
    main()
