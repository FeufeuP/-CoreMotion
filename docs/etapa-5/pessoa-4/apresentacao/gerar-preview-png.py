"""Renderiza cada slide de um .pptx em PNG, sem depender de LibreOffice/PowerPoint.

Uso:  python tools/render_pptx_png.py <entrada.pptx> <dir_saida> [--ppi 120]

Desenha retângulos/chapas e texto com Pillow, lendo forma, cor, fonte, tamanho,
negrito, alinhamento, âncora vertical e margens do próprio XML do pacote. As
métricas usam DejaVu (levemente mais largo que Arial), então o texto nunca aparece
otimista demais: se couber aqui, cabe no PowerPoint. Caixa com estouro é marcada com
borda vermelha tracejada e avisada no stdout.
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu

EMU_IN = 914400
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONTS = {
    ("sans", False): "DejaVuSans.ttf",
    ("sans", True): "DejaVuSans-Bold.ttf",
    ("mono", False): "DejaVuSansMono.ttf",
    ("mono", True): "DejaVuSansMono-Bold.ttf",
}
_cache: dict = {}


def pil_font(name: str, size_pt: float, bold: bool):
    fam = "mono" if any(k in (name or "").lower() for k in ("mono", "consol", "courier")) else "sans"
    px = max(1, int(round(size_pt * (100 / 72.0) / (100 / 72.0))))  # placeholder
    return fam, px


def get_font(name: str, size_pt: float, bold: bool, ppi: float) -> ImageFont.FreeTypeFont:
    fam = "mono" if any(k in (name or "").lower() for k in ("mono", "consol", "courier")) else "sans"
    px = int(round(size_pt * ppi / 72.0))
    key = (fam, bold, px)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, FONTS[(fam, bold)]), px)
    return _cache[key]


def rgb(c, default=(0, 0, 0)):
    try:
        if c is None:
            return default
        r, g, b = c[0], c[1], c[2]
        return (r, g, b)
    except Exception:
        return default


def fill_rgb(shape, default=None):
    try:
        f = shape.fill
        if f.type is None:
            return default
        # MSO_FILL.SOLID == 1
        if int(f.type) == 1:
            return rgb(f.fore_color.rgb, default)
        return default
    except Exception:
        return default


def line_rgb(shape, default=None):
    try:
        ln = shape.line
        if ln.fill.type is not None and int(ln.fill.type) != 1:   # sem contorno sólido
            return default
        return rgb(ln.color.rgb, default)
    except Exception:
        return default


def wrap(d: ImageDraw.ImageDraw, segs, width_px, ppi):
    """segs: lista de (texto, fonte, cor). Devolve lista de linhas, cada uma lista de
    (pedaco, fonte, cor), quebrando por palavra."""
    lines, cur, cur_w = [], [], 0.0
    for text, font, color in segs:
        for word in text.split(" "):
            piece = word + " "
            w = d.textlength(piece, font=font)
            if cur_w + w > width_px and cur:
                lines.append(cur)
                cur, cur_w = [], 0.0
                piece = word + " "
                w = d.textlength(piece, font=font)
            cur.append((piece, font, color))
            cur_w += w
        if text.endswith(" "):
            pass
    if cur:
        lines.append(cur)
    return lines or [[("", get_font("Arial", 12, False, ppi), (0, 0, 0))]]


def draw_text(d, shape, box_px, ppi, warn):
    tf = shape.text_frame
    x, y, w, h = box_px
    ml = tf.margin_left / EMU_IN * ppi
    mr = tf.margin_right / EMU_IN * ppi
    mt = tf.margin_top / EMU_IN * ppi
    mb = tf.margin_bottom / EMU_IN * ppi
    inner_w = max(1, w - ml - mr)
    inner_h = max(1, h - mt - mb)

    paras = []
    for p in tf.paragraphs:
        segs = []
        size_max, bold_any, name_any = 12.0, False, "Arial"
        for r in p.runs:
            if not r.text:
                continue
            sz = float(r.font.size.pt) if r.font.size else 12.0
            bd = bool(r.font.bold)
            nm = r.font.name or "Arial"
            col = rgb(r.font.color.rgb if r.font.color and r.font.color.type is not None else None, (17, 23, 36))
            segs.append((r.text + " " if not r.text.endswith(" ") else r.text,
                         get_font(nm, sz, bd, ppi), col))
            size_max = max(size_max, sz)
            bold_any = bold_any or bd
            name_any = nm
        align = {PP_ALIGN.CENTER: "center", PP_ALIGN.RIGHT: "right", PP_ALIGN.LEFT: "left",
                 None: "left"}.get(p.alignment, "left")
        ls = p.line_spacing if isinstance(p.line_spacing, float) else 1.15
        after = (p.space_after.pt if p.space_after else 0.0)
        paras.append((segs, size_max, ls, after, align))

    # altura de cada linha
    laid, total_h = [], 0.0
    for segs, size_max, ls, after, align in paras:
        if not segs:
            total_h += size_max * ppi / 72.0 * 0.5 + after * ppi / 72.0
            laid.append(([], size_max, after, align))
            continue
        lines = wrap(d, segs, inner_w, ppi)
        lh = size_max * ppi / 72.0 * 1.22 * ls
        total_h += len(lines) * lh + after * ppi / 72.0
        laid.append((lines, lh, after, align))

    anchor = tf.vertical_anchor
    if anchor == MSO_ANCHOR.MIDDLE:
        y0 = y + mt + max(0, (inner_h - total_h) / 2)
    elif anchor == MSO_ANCHOR.BOTTOM:
        y0 = y + mt + max(0, inner_h - total_h)
    else:
        y0 = y + mt

    cy = y0
    for lines, lh, after, align in laid:
        for line in lines:
            lw = sum(d.textlength(t, font=f) for t, f, _ in line)
            if align == "center":
                cx = x + ml + max(0, (inner_w - lw) / 2)
            elif align == "right":
                cx = x + ml + max(0, inner_w - lw)
            else:
                cx = x + ml
            for t, f, c in line:
                d.text((cx, cy), t, font=f, fill=c)
                cx += d.textlength(t, font=f)
            cy += lh
        cy += after * ppi / 72.0

    if total_h > inner_h * 1.03 + 2:
        warn.append(round(total_h / ppi * 72, 1))
        return True
    return False


def shape_alpha(shape):
    try:
        from pptx.oxml.ns import qn
        el = shape._element.spPr.find(qn('a:solidFill') + '/' + qn('a:srgbClr') + '/' + qn('a:alpha'))
        return int(el.get('val')) if el is not None else None
    except Exception:
        return None


def geom_of(shape):
    """prstGeom do shape: 'ellipse' | 'roundRect' | 'rect' | outro."""
    try:
        from pptx.oxml.ns import qn
        el = shape._element.spPr.find(qn('a:prstGeom'))
        return (el.get('prst') or 'rect') if el is not None else 'rect'
    except Exception:
        return 'rect'


def rounded(d, box_px, radius_px, fill, outline, geom='rect'):
    x, y, w, h = box_px
    lw = max(1, int(round(1.1)))
    if geom == 'ellipse':
        d.ellipse([x, y, x + w, y + h], fill=fill, outline=outline, width=lw)
        return
    r = min(radius_px, w / 2, h / 2)
    if r <= 1:
        d.rectangle([x, y, x + w, y + h], fill=fill, outline=outline, width=lw)
    else:
        d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=lw)


def render(pptx_path, out_dir, ppi=120, prefix="slide"):
    os.makedirs(out_dir, exist_ok=True)
    prs = Presentation(pptx_path)
    W = int(round(prs.slide_width / EMU_IN * ppi))
    H = int(round(prs.slide_height / EMU_IN * ppi))
    files, report = [], []
    for i, sl in enumerate(prs.slides, 1):
        img = Image.new("RGB", (W, H), (255, 255, 255))
        d = ImageDraw.Draw(img)
        bgrgb = None
        try:
            if int(sl.background.fill.type) == 1:
                bgrgb = rgb(sl.background.fill.fore_color.rgb, None)
        except Exception:
            pass
        if bgrgb:
            d.rectangle([0, 0, W, H], fill=bgrgb)
        over = 0
        for sh in sl.shapes:
            try:
                box_px = (sh.left / EMU_IN * ppi, sh.top / EMU_IN * ppi,
                          sh.width / EMU_IN * ppi, sh.height / EMU_IN * ppi)
            except TypeError:
                continue
            x, y, w, h = box_px
            if x + w < -2 or y + h < -2 or x > W + 2 or y > H + 2:
                continue
            fc = fill_rgb(sh, None)
            lc = line_rgb(sh, None)
            radius = 0
            try:
                if sh.adjustments and len(list(sh.adjustments)):
                    radius = float(list(sh.adjustments)[0]) * min(w, h)
            except Exception:
                radius = 0
            geom = geom_of(sh)
            if fc or lc:
                op = shape_alpha(sh)
                if fc and op is not None and op < 100000:
                    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                    ld = ImageDraw.Draw(lay)
                    rounded(ld, box_px, radius, tuple(list(fc) + [int(255 * op / 100000)]), None, geom)
                    img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")
                    d = ImageDraw.Draw(img)
                    if lc:
                        rounded(d, box_px, radius, None, lc, geom)
                else:
                    rounded(d, box_px, radius, fc, lc, geom)
            if sh.has_text_frame and any(r.text.strip() for p in sh.text_frame.paragraphs for r in p.runs):
                if draw_text(d, sh, box_px, ppi, report):
                    over += 1
                    d.rectangle([x, y, x + w, y + h], outline=(255, 0, 60), width=2)
        fp = os.path.join(out_dir, "%s-%02d.png" % (prefix, i))
        img.save(fp)
        files.append(fp)
    return files, over


def mosaic(files, out_path, cols=3, tw=640):
    imgs = [Image.open(f) for f in files]
    th = int(imgs[0].height * (tw / imgs[0].width))
    rows = (len(imgs) + cols - 1) // cols
    pad, lab = 18, 34
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad, rows * (th + lab) + (rows + 1) * pad), (244, 245, 248))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 20)
    for i, im in enumerate(imgs):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + lab + pad)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
        d.rectangle([x, y, x + tw - 1, y + th - 1], outline=(210, 214, 224), width=1)
        d.text((x + 2, y + th + 6), "%02d" % (i + 1), font=f, fill=(60, 70, 90))
    sheet.save(out_path)
    return out_path, sheet.size


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ppi = 120
    for a in sys.argv[1:]:
        if a.startswith("--ppi"):
            ppi = int(a.split("=")[1])
    src = args[0]
    dst = args[1]
    files, over = render(src, dst, ppi=ppi)
    print("%d pngs em %s (%d px de largura, %d shapes com estouro)" % (len(files), dst, int(13.3333 * ppi), over))
    if len(files) > 1:
        mp, size = mosaic(files, os.path.join(dst, "mosaico.png"))
        print("mosaico: %s %s" % (mp, size))
