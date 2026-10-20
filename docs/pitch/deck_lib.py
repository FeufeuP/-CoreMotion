"""Biblioteca de design + animação para o deck do CoreMotion.

Tema: geométrico, pastel, colorido.
Animações: XML de timing nativo do PowerPoint (entradas em cascata).
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml
from lxml import etree

# ------------------------------------------------------------------ paleta
CREAM    = RGBColor(0xFB, 0xF7, 0xF2)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
INK      = RGBColor(0x2E, 0x34, 0x47)
INK2     = RGBColor(0x55, 0x5D, 0x73)
MUTED    = RGBColor(0x8B, 0x92, 0xA6)
LINE     = RGBColor(0xE7, 0xDF, 0xD6)

CORAL    = RGBColor(0xFF, 0x9A, 0xA2)
CORAL_D  = RGBColor(0xF2, 0x6D, 0x76)
MINT     = RGBColor(0xB5, 0xEA, 0xD7)
MINT_D   = RGBColor(0x6F, 0xC9, 0xA5)
LAV      = RGBColor(0xC7, 0xCE, 0xEA)
LAV_D    = RGBColor(0x8E, 0x9B, 0xE0)
BUTTER   = RGBColor(0xFF, 0xE2, 0xA8)
BUTTER_D = RGBColor(0xF2, 0xC1, 0x6B)
PEACH    = RGBColor(0xFF, 0xC9, 0xA3)
SKY      = RGBColor(0xA9, 0xD6, 0xE5)
PINK     = RGBColor(0xF7, 0xC6, 0xE0)
LILAC    = RGBColor(0xE4, 0xC1, 0xF9)

FONT = "Arial"
SW, SH = 13.333, 7.5

SHAPES = {
    "rect": MSO_SHAPE.RECTANGLE,
    "round": MSO_SHAPE.ROUNDED_RECTANGLE,
    "oval": MSO_SHAPE.OVAL,
    "tri": MSO_SHAPE.ISOSCELES_TRIANGLE,
    "hex": MSO_SHAPE.HEXAGON,
    "chev": MSO_SHAPE.CHEVRON,
    "rndtri": MSO_SHAPE.RIGHT_TRIANGLE,
    "pent": MSO_SHAPE.PENTAGON,
    "plus": MSO_SHAPE.MATH_PLUS,
    "diamond": MSO_SHAPE.DIAMOND,
}


# ------------------------------------------------------------------ utilitários
def new_deck():
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    return prs


def blank(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = CREAM
    return slide


def _alpha(shape, pct, target="fill"):
    spPr = shape._element.spPr
    if target == "fill":
        node = spPr.find(qn("a:solidFill"))
    else:
        ln = spPr.find(qn("a:ln"))
        node = ln.find(qn("a:solidFill")) if ln is not None else None
    if node is None:
        return
    clr = node.find(qn("a:srgbClr"))
    if clr is None:
        return
    a = etree.SubElement(clr, qn("a:alpha"))
    a.set("val", str(int(pct * 1000)))


def _soft_shadow(shape, blur=14, dist=5, alpha=10):
    shape.shadow.inherit = False
    spPr = shape._element.spPr
    lst = spPr.find(qn("a:effectLst"))
    if lst is None:
        lst = etree.SubElement(spPr, qn("a:effectLst"))
    for child in list(lst):
        lst.remove(child)
    xml = (
        '<a:outerShdw xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        f'blurRad="{int(blur * 12700)}" dist="{int(dist * 12700)}" dir="5400000" '
        'algn="ctr" rotWithShape="0">'
        f'<a:srgbClr val="2E3447"><a:alpha val="{int(alpha * 1000)}"/></a:srgbClr>'
        "</a:outerShdw>"
    )
    lst.append(parse_xml(xml))


def shape(slide, kind, x, y, w, h, fill=None, line=None, lw=1.0,
          rot=0, alpha=None, line_alpha=None, shadow=False, radius=None,
          shadow_alpha=10):
    s = slide.shapes.add_shape(SHAPES[kind], Inches(x), Inches(y),
                               Inches(w), Inches(h))
    s.shadow.inherit = False
    if kind == "round" and radius is not None:
        try:
            s.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
        if alpha is not None:
            _alpha(s, alpha)
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
        if line_alpha is not None:
            _alpha(s, line_alpha, "line")
    if rot:
        s.rotation = rot
    if shadow:
        _soft_shadow(s, alpha=shadow_alpha)
    if s.has_text_frame:
        s.text_frame.text = ""
    return s


def txt(slide, x, y, w, h, items, size=14, color=INK, bold=False, spc=0,
        align="l", anchor="t", line_spacing=None, italic=False,
        space_after=0, name=None):
    """items: str | list[str | tuple[str, dict]]  (um parágrafo por item)."""
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE,
                          "b": MSO_ANCHOR.BOTTOM}[anchor]
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    if isinstance(items, str):
        items = [items]
    flat = []
    for item in items:
        if isinstance(item, tuple):
            text, opts = item
        else:
            text, opts = item, {}
        for part in str(text).split("\n"):
            flat.append((part, dict(opts)))
    for i, (text, opts) in enumerate(flat):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER,
                       "r": PP_ALIGN.RIGHT}[opts.get("align", align)]
        p.space_after = Pt(opts.get("after", space_after))
        ls = opts.get("line", line_spacing)
        if ls:
            p.line_spacing = ls
        p.space_before = Pt(opts.get("before", 0))
        run = p.add_run()
        run.text = text
        f = run.font
        f.name = opts.get("font", FONT)
        f.size = Pt(opts.get("size", size))
        f.bold = opts.get("bold", bold)
        f.italic = opts.get("italic", italic)
        f.color.rgb = opts.get("color", color)
        sp = opts.get("spc", spc)
        if sp:
            f._rPr.set("spc", str(int(sp * 100)))
    return box


def line(slide, x1, y1, x2, y2, color, lw=1.0, dash=False, alpha=None):
    """Linha reta via conector (horizontal, vertical ou diagonal)."""
    from math import hypot, atan2, degrees
    ln = slide.shapes.add_connector(1, Inches(x1), Inches(y1),
                                    Inches(x2), Inches(y2))
    ln.line.color.rgb = color
    ln.line.width = Pt(lw)
    if dash:
        ln.line.dash_style = 4  # dash
    if alpha is not None:
        _alpha(ln, alpha, "line")
    return ln


def dots(slide, x, y, cols, rows, gap, r, color, alpha=100):
    out = []
    for i in range(cols):
        for j in range(rows):
            out.append(shape(slide, "oval", x + i * gap, y + j * gap, r, r,
                             fill=color, alpha=alpha))
    return out


def card(slide, x, y, w, h, fill=WHITE, radius=0.05, shadow=True, line_c=None,
         lw=1.0):
    return shape(slide, "round", x, y, w, h, fill=fill, line=line_c, lw=lw,
                 radius=radius, shadow=shadow, shadow_alpha=12)


def chip(slide, x, y, w, h, label, fill, color=INK, size=8.5, spc=1.6,
         bold=True, dot_color=None):
    s = shape(slide, "round", x, y, w, h, fill=fill, radius=0.5)
    if dot_color is not None:
        shape(slide, "oval", x + 0.16, y + h / 2 - 0.04, 0.08, 0.08,
              fill=dot_color)
        txt(slide, x + 0.32, y, w - 0.42, h, label, size=size, color=color,
            bold=bold, spc=spc, anchor="m")
    else:
        txt(slide, x, y, w, h, label, size=size, color=color, bold=bold,
            spc=spc, align="c", anchor="m")
    return s


def chrome(slide, idx, total, section, accent=CORAL_D, dark=False):
    ink = WHITE if dark else INK
    muted = RGBColor(0xC9, 0xC3, 0xBB) if dark else MUTED
    shape(slide, "round", 0.62, 0.52, 0.17, 0.17, fill=accent, radius=0.3)
    txt(slide, 0.9, 0.51, 3.2, 0.2, "COREMOTION", size=9, color=ink,
        bold=True, spc=2.6, anchor="m")
    txt(slide, 10.9, 0.51, 1.82, 0.2, f"{idx:02d} / {total:02d}", size=8,
        color=muted, bold=True, spc=1.8, align="r", anchor="m")
    # barra de progresso
    shape(slide, "rect", 0.62, 7.12, 12.1, 0.014,
          fill=RGBColor(0xE9, 0xE1, 0xD8) if not dark else RGBColor(0x4A, 0x51, 0x66))
    shape(slide, "rect", 0.62, 7.12, 12.1 * idx / total, 0.014, fill=accent)


# ------------------------------------------------------------------ animações
def _set_visible(cid, spid):
    return (f'<p:set><p:cBhvr><p:cTn id="{cid}" dur="1" fill="hold">'
            f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
            f'<p:attrNameLst><p:attrName>style.visibility</p:attrName>'
            f"</p:attrNameLst></p:cBhvr><p:to><p:strVal val=\"visible\"/>"
            f"</p:to></p:set>")


def _anim_effect(cid, spid, dur, flt="fade"):
    return (f'<p:animEffect transition="in" filter="{flt}"><p:cBhvr>'
            f'<p:cTn id="{cid}" dur="{dur}"/>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
            f"</p:cBhvr></p:animEffect>")


def _anim_pos(cid, spid, dur, axis="ppt_y", delta=0.18):
    d = float(delta)
    return (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr additive="base">'
            f'<p:cTn id="{cid}" dur="{dur}" fill="hold"/>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
            f"<p:attrNameLst><p:attrName>{axis}</p:attrName></p:attrNameLst>"
            f"</p:cBhvr><p:tavLst>"
            f'<p:tav tm="0"><p:val><p:strVal val="#{axis}{d:+.3f}"/></p:val></p:tav>'
            f'<p:tav tm="100000"><p:val><p:strVal val="#{axis}"/></p:val></p:tav>'
            f"</p:tavLst></p:anim>")


def _anim_pos_over(cid, spid, dur, axis, start, over):
    """Desliza com ultrapassagem (freio de velocidade): 0 -> start -> over -> 0."""
    s, o = float(start), float(over)
    return (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr additive="base">'
            f'<p:cTn id="{cid}" dur="{dur}" fill="hold"/>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
            f"<p:attrNameLst><p:attrName>{axis}</p:attrName></p:attrNameLst>"
            f"</p:cBhvr><p:tavLst>"
            f'<p:tav tm="0"><p:val><p:strVal val="#{axis}{s:+.3f}"/></p:val></p:tav>'
            f'<p:tav tm="62000"><p:val><p:strVal val="#{axis}{o:+.3f}"/></p:val></p:tav>'
            f'<p:tav tm="100000"><p:val><p:strVal val="#{axis}"/></p:val></p:tav>'
            f"</p:tavLst></p:anim>")


def _anim_scale(cid, spid, dur, start=72, start_y=None):
    sx = int(float(start) * 1000)
    sy = int(float(start_y if start_y is not None else start) * 1000)
    return (f'<p:animScale><p:cBhvr><p:cTn id="{cid}" dur="{dur}" fill="hold"/>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr>'
            f'<p:from x="{sx}" y="{sy}"/>'
            f'<p:to x="100000" y="100000"/></p:animScale>')


def _anim_rot(cid, spid, dur, deg_from, deg_to=0):
    return (f'<p:animRot><p:cBhvr><p:cTn id="{cid}" dur="{dur}" fill="hold"/>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr>'
            f'<p:from x="0" y="0" z="{int(deg_from * 60000)}"/>'
            f'<p:to x="0" y="0" z="{int(deg_to * 60000)}"/></p:animRot>')


def _anim_motion(cid, spid, dur, path):
    return (f'<p:animMotion origin="layout" path="{path}" pathEditMode="relative" '
            f'rCtr="0"><p:cBhvr><p:cTn id="{cid}" dur="{dur}" fill="hold"/>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animMotion>')


def animate(slide, specs):
    """specs: [(shape, efeito, atraso_ms, duracao_ms[, extra])]  efeito:

    fade | rise | drop | left | right | zoom | wipe | wipeup |
    whip (chega esticado da esquerda, como rastro) |
    speed (chega da direita com ultrapassagem) |
    boost (chega da esquerda com ultrapassagem) |
    spin (fade + giro de assentamento) |
    race (trajeto de corrida; extra = path "M 0 0 L 0.8 0 E")

    Pode ser chamada mais de uma vez por slide (os grupos são fundidos).
    """
    ids = iter(range(3, 40000))
    groups = []
    for spec in specs:
        shp, effect, delay, dur = spec[:4]
        extra = spec[4] if len(spec) > 4 else None
        spid = shp.shape_id
        e1, e2, e3, e4 = next(ids), next(ids), next(ids), next(ids)
        preset, flt = 10, "fade"
        inner = _set_visible(e1, spid)
        if effect == "fade":
            preset, flt = 10, "fade"
            inner += _anim_effect(e2, spid, dur, flt)
        elif effect in ("rise", "drop", "left", "right"):
            preset, flt = 2, "fade"
            inner += _anim_effect(e2, spid, dur, flt)
            if effect in ("rise", "drop"):
                delta = 0.18 if effect == "rise" else -0.18
                inner += _anim_pos(e3, spid, dur, "ppt_y", delta)
            else:
                delta = -0.2 if effect == "left" else 0.2
                inner += _anim_pos(e3, spid, dur, "ppt_x", delta)
        elif effect == "zoom":
            preset, flt = 23, "fade"
            inner += _anim_effect(e2, spid, dur, flt)
            inner += _anim_scale(e3, spid, dur, 74)
        elif effect == "wipe":
            preset, flt = 22, "wipe(right)"
            inner += _anim_effect(e2, spid, dur, flt)
        elif effect == "wipeup":
            preset, flt = 22, "wipe(up)"
            inner += _anim_effect(e2, spid, dur, flt)
        elif effect == "whip":
            # entra esticado da esquerda e comprime — rastro de velocidade
            preset, flt = 2, "fade"
            inner += _anim_effect(e2, spid, dur, flt)
            inner += _anim_pos(e3, spid, dur, "ppt_x", -0.42)
            inner += _anim_scale(next(ids), spid, dur, 42, 100)
        elif effect in ("speed", "boost"):
            # entra rápido e freia com ultrapassagem
            preset, flt = 2, "fade"
            inner += _anim_effect(e2, spid, dur, flt)
            if effect == "speed":
                inner += _anim_pos_over(e3, spid, dur, "ppt_x", 0.50, -0.045)
            else:
                inner += _anim_pos_over(e3, spid, dur, "ppt_x", -0.48, 0.04)
        elif effect == "spin":
            preset, flt = 23, "fade"
            inner += _anim_effect(e2, spid, dur, flt)
            base = int(shp.rotation or 0)
            inner += _anim_rot(e3, spid, dur, base - 22, base)
        elif effect == "race":
            preset, flt = 2, "fade"
            path = extra or "M 0 0 L 0.35 0 E"
            inner += _anim_motion(e3, spid, dur, path)
        else:
            preset, flt = 10, "fade"
            inner += _anim_effect(e2, spid, dur, flt)

        effect_par = (
            f'<p:par><p:cTn id="{e4}" presetID="{preset}" presetClass="entr" '
            f'presetSubtype="0" fill="hold" grpId="0" nodeType="afterEffect">'
            f'<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
            f"<p:childTnLst>{inner}</p:childTnLst></p:cTn></p:par>"
        )
        groups.append(
            f'<p:par><p:cTn id="{next(ids)}" fill="hold">'
            f'<p:stCondLst><p:cond delay="{int(delay)}"/></p:stCondLst>'
            f"<p:childTnLst><p:par><p:cTn id=\"{next(ids)}\" fill=\"hold\">"
            f'<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
            f"<p:childTnLst>{effect_par}</p:childTnLst></p:cTn></p:par>"
            f"</p:childTnLst></p:cTn></p:par>"
        )

    ns = ('xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
          'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"')
    existing = slide._element.find(qn("p:timing"))
    if existing is not None:
        main = None
        for ctn in existing.iter(qn("p:cTn")):
            if ctn.get("nodeType") == "mainSeq":
                main = ctn
                break
        lst = main.find(qn("p:childTnLst"))
        frag = parse_xml(f"<p:wrap {ns}>{''.join(groups)}</p:wrap>")
        for g in list(frag):
            lst.append(g)
        el = existing
    else:
        root, seq = next(ids), next(ids)
        xml = (
            f"<p:timing {ns}>"
            f'<p:tnLst><p:par><p:cTn id="{root}" dur="indefinite" restart="never" '
            f'nodeType="tmRoot"><p:childTnLst>'
            f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="{seq}" dur="indefinite" '
            f'nodeType="mainSeq"><p:childTnLst>{"".join(groups)}</p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/>'
            '</p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/>'
            "</p:tgtEl></p:cond></p:nextCondLst></p:seq>"
            "</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>"
        )
        el = parse_xml(xml)
        slide._element.append(el)
    # renumerar ids em ordem de documento (como o PowerPoint faz)
    n = 0
    for ctn in el.iter(qn("p:cTn")):
        n += 1
        ctn.set("id", str(n))


# --- transições: PML padrão + extensões p14 (PowerPoint 2010+) + morph (2016+) ---
_P14_FALLBACK = {
    "pan": "push", "flash": "fade", "vortex": "circle", "switch": "wipe",
    "flip": "split", "ripple": "circle", "honeycomb": "dissolve",
    "glitter": "dissolve", "gallery": "cover", "conveyor": "push",
    "warp": "zoom", "flythrough": "zoom", "drape": "cover",
    "curtains": "split", "airplane": "cover", "origami": "dissolve",
    "shred": "strips", "reveal": "wipe", "ferris": "wheel",
    "crush": "fade", "peel": "wipe", "pageCurl": "wipe",
}
_P14_DIR = {"pan", "vortex", "switch", "gallery", "conveyor"}
_NS_MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
_NS_P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
_NS_P159 = "http://schemas.microsoft.com/office/powerpoint/2015/09/main"


def _std_transition(kind, speed, direction, orient):
    at = ""
    if kind in ("push", "cover", "wipe"):
        at = f' dir="{direction or "l"}"'
    elif kind == "split":
        at = f' orient="{orient or "horz"}" dir="{direction or "out"}"'
    elif kind == "zoom":
        at = f' dir="{direction if direction in ("in", "out") else "in"}"'
    elif kind in ("blinds", "checker", "comb", "randomBar"):
        at = f' dir="{orient or "horz"}"'
    elif kind == "strips":
        at = f' dir="{direction or "ld"}"'
    elif kind == "wheel":
        at = ' spokes="3"'
    return (f'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            f'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            f'spd="{speed}"><p:{kind}{at}/></p:transition>')


def transition(slide, kind="fade", speed="slow", dur=None, direction=None, orient=None):
    """Transição de slide.

    Padrão: fade, push, cover, wipe, split, cut, dissolve, zoom, strips, wheel…
    p14 (2010+): flash, pan, vortex, conveyor, gallery, switch, warp, flythrough,
    origami, curtains, ferris, glitter, ripple, shred, drape, airplane…
    p159 (2016+): morph (objetos com o mesmo nome '!!' deslizam entre slides).

    dur em milissegundos; direction em l/u/r/d.
    """
    if kind == "morph":
        dur = int(dur or 1200)
        xml = (
            f'<mc:AlternateContent xmlns:mc="{_NS_MC}" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            f'xmlns:p14="{_NS_P14}">'
            f'<mc:Choice xmlns:p159="{_NS_P159}" Requires="p159">'
            f'<p:transition spd="{speed}" p14:dur="{dur}">'
            '<p159:morph option="byObject"/></p:transition></mc:Choice>'
            f'<mc:Fallback><p:transition spd="{speed}"><p:fade/></p:transition>'
            f"</mc:Fallback></mc:AlternateContent>"
        )
    elif kind in _P14_FALLBACK:
        dur = int(dur or 800)
        inner14 = f"<p14:{kind}"
        if direction and kind in _P14_DIR:
            inner14 += f' dir="{direction}"'
        inner14 += "/>"
        xml = (
            f'<mc:AlternateContent xmlns:mc="{_NS_MC}" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            f'xmlns:p14="{_NS_P14}">'
            f'<mc:Choice Requires="p14">'
            f'<p:transition spd="{speed}" p14:dur="{dur}">{inner14}</p:transition>'
            f"</mc:Choice><mc:Fallback>"
            f"{_std_transition(_P14_FALLBACK[kind], speed, direction, orient)}"
            f"</mc:Fallback></mc:AlternateContent>"
        )
    else:
        attrs = ""
        if dur:
            attrs = (f' xmlns:p14="{_NS_P14}" p14:dur="{int(dur)}"')
        xml = _std_transition(kind, speed, direction, orient)
        xml = xml.replace("spd=", f"{attrs} spd=", 1) if attrs else xml

    el = parse_xml(xml)
    # transition deve vir antes de timing
    timing = slide._element.find(qn("p:timing"))
    if timing is not None:
        timing.addprevious(el)
    else:
        slide._element.append(el)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def cascade(shapes, start=0, step=90, effect="rise", dur=520):
    """Sequência de entrada em cascata."""
    return [(s, effect, start + i * step, dur) for i, s in enumerate(shapes)]
