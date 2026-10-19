"""Gera a versao animada (transicoes + entradas por clique) do PITCH do CoreMotion.

Uso:  python tools/make_pitch_pptx.py <saida.pptx>

Mesmo motor de XML do deck de pendencias (p:transition / p:timing escritos a mao,
porque nem python-pptx nem a Google Slides API expoe movimento), mas com o conteudo
do pitch do produto: 15 slides que vendem o site para a banca.
"""
from __future__ import annotations

import sys

from lxml import etree
from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p14": "http://schemas.microsoft.com/office/powerpoint/2010/main",
}
EMU_IN = 914400

INK = RGBColor(0x0B, 0x10, 0x20)
PAPER = RGBColor(0xF5, 0xF6, 0xF8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
HAIR = RGBColor(0xE4, 0xE7, 0xF0)
LIME = RGBColor(0xC6, 0xF2, 0x4E)
LIME_T = RGBColor(0xF0, 0xFC, 0xE8)
VIOLET = RGBColor(0x6C, 0x4C, 0xF1)
VIOLET_T = RGBColor(0xEC, 0xE8, 0xFF)
CYAN = RGBColor(0x14, 0xC8, 0xDC)
CYAN_T = RGBColor(0xF1, 0xFC, 0xFD)
AMBER = RGBColor(0xFF, 0xB0, 0x20)
AMBER_T = RGBColor(0xFF, 0xF6, 0xE5)
CORAL = RGBColor(0xFF, 0x3B, 0x5C)
CORAL_T = RGBColor(0xFF, 0xEC, 0xEF)
SLATE = RGBColor(0x4A, 0x54, 0x68)
SLATE_T = RGBColor(0xEA, 0xED, 0xF2)
LIGHT = RGBColor(0xC9, 0xD1, 0xE0)
TXT = INK

DISPLAY = "Arial Black"
BODY = "Arial"
MONO = "Consolas"


def q(tag: str) -> str:
    pre, local = tag.split(":")
    return "{%s}%s" % (NS[pre], local)


# ----------------------------------------------------------------- primitives
def set_alpha(shape, opacity_pct: float) -> None:
    """Torna o preenchimento solido semitransparente (100 = opaco)."""
    from pptx.oxml.ns import qn
    spPr = shape._element.spPr
    sf = spPr.find(qn('a:solidFill'))
    if sf is None:
        return
    clr = sf.find(qn('a:srgbClr'))
    if clr is None:
        return
    for old in clr.findall(qn('a:alpha')):
        clr.remove(old)
    a = clr.makeelement(qn('a:alpha'), {'val': str(int(opacity_pct * 1000))})
    clr.append(a)


def glow(slide, x, y, w, h, color, opacity=22):
    g = box(slide, x, y, w, h, fill=color, shape=MSO_SHAPE.OVAL)
    set_alpha(g, opacity)
    return g


def bg(slide, color: RGBColor) -> None:
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def box(slide, x, y, w, h, fill=None, line=None, radius=None, shape=None):
    shape = slide.shapes.add_shape(
        shape or (MSO_SHAPE.ROUNDED_RECTANGLE if radius is not None else MSO_SHAPE.RECTANGLE),
        Emu(int(x * EMU_IN)), Emu(int(y * EMU_IN)), Emu(int(w * EMU_IN)), Emu(int(h * EMU_IN)),
    )
    if radius is not None and shape is not None and shape.shape_type != MSO_SHAPE.OVAL:
        try:
            shape.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Emu(9525)
    shape.shadow.inherit = False
    shape.text_frame.word_wrap = True
    return shape


def put(shape, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space_after=4,
         ml=0.16, mr=0.14, mt=0.10, mb=0.08):
    tf = shape.text_frame
    tf.margin_left = Emu(int(ml * EMU_IN))
    tf.margin_right = Emu(int(mr * EMU_IN))
    tf.margin_top = Emu(int(mt * EMU_IN))
    tf.margin_bottom = Emu(int(mb * EMU_IN))
    tf.vertical_anchor = anchor
    first = True
    for text, size, bold, color, font, spc in paras:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        p.space_after = Pt(space_after)
        p.line_spacing = spc
        run = p.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = font
    return shape


def kicker(slide, text, color, w=2.9):
    chip = box(slide, 0.5, 0.38, w, 0.28, fill=color)
    put(chip, [(text, 9.5, True, INK, MONO, 1.0)], anchor=MSO_ANCHOR.MIDDLE,
        space_after=0, align=PP_ALIGN.CENTER, ml=0.04, mr=0.04, mt=0.0, mb=0.0)
    return chip


_FONTCACHE = {}


def _font(px, bold, mono=False):
    key = (px, bold, mono)
    if key not in _FONTCACHE:
        fam = "DejaVuSansMono" if mono else "DejaVuSans"
        _FONTCACHE[key] = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/%s-%s.ttf" % (fam, "Bold" if bold else ""), px)
    return _FONTCACHE[key]


def text_in(t, pt, bold=True, mono=False):
    """Largura aproximada do texto em polegadas, medida em DejaVu (mais largo que
    Arial, entao o ajuste e conservador: se couber aqui, cabe no PowerPoint)."""
    return _font(max(6, int(round(pt))), bold, mono).getlength(t) / 72.0


def fit_size(t, size, avail_in, mono=False, minimum=17):
    while size > minimum and text_in(t, size, True, mono) > avail_in - 0.12:
        size -= 0.5
    return size


def title(slide, text, size=28, dark=False, w=12.33):
    size = fit_size(text, size, w)          # nunca deixa o titulo quebrar linha
    t = box(slide, 0.5, 0.76, w, 0.72)
    put(t, [(text, size, True, WHITE if dark else TXT, DISPLAY, 1.0)],
        anchor=MSO_ANCHOR.MIDDLE, space_after=0, ml=0.0, mt=0.0, mb=0.0)
    return t


def card(slide, x, y, w, h, head, lines, fill=WHITE, line=HAIR, body=11,
         head_col=None, spc=1.2, align=PP_ALIGN.LEFT, dark=False, mono_head=True):
    shape = box(slide, x, y, w, h, fill=fill, line=line, radius=0.05)
    paras = []
    if head:
        paras.append((head, head_size(body, mono_head), True,
                      head_col or (TXT if not dark else INK), MONO if mono_head else BODY, 1.1))
    for ln in lines:
        paras.append((ln, body, False, TXT if not dark else INK, BODY, spc))
    put(shape, paras, align=align, space_after=5)
    return shape


def head_size(body, mono_head):
    return body - 1.0 if mono_head else body + 1.0


def grid(slide, items, cols, cw, ch, y0=1.78, gap=0.19, x0=0.5, **kw):
    shapes = []
    for i, (head, lines) in enumerate(items):
        r, c = divmod(i, cols)
        shapes.append(card(slide, x0 + c * (cw + gap), y0 + r * (ch + gap), cw, ch,
                           head, lines, **kw))
    return shapes


def note(slide, text, fill=VIOLET_T, line=None, y=5.95, h=0.8, size=12.5, bold=True,
         color=TXT, font=BODY, anchor=MSO_ANCHOR.MIDDLE):
    shape = box(slide, 0.5, y, 12.33, h, fill=fill, line=line)
    put(shape, [(text, size, bold, color, font, 1.2)], anchor=anchor, space_after=0)
    return shape


def strip(slide, head, lines, fill=CYAN_T, line=None, y=4.75, h=1.15, body=12, dark=False):
    shape = box(slide, 0.5, y, 12.33, h, fill=fill, line=line, radius=0.04)
    paras = [(head, body - 1.5, True, INK, MONO, 1.1)]
    for ln in lines:
        paras.append((ln, body, False, TXT, BODY, 1.22))
    put(shape, paras, space_after=4)
    return shape


# ------------------------------------------------------------------- XML magic
def set_transition(slide, kind="fade", dur=650):
    root = slide._element
    for tag in ("transition", "timing"):
        for el in root.findall(q("p:" + tag)):
            root.remove(el)
    if kind == "none":
        return
    tr = etree.SubElement(root, q("p:transition"), nsmap={"p14": NS["p14"]})
    tr.set("spd", "med")
    if kind == "morph":
        tr.set(q("p14:dur"), str(dur))
        etree.SubElement(tr, q("p14:morph")).set("option", "byObj")
    elif kind == "push":
        etree.SubElement(tr, q("p:push")).set("dir", "u")
    elif kind == "wipe":
        etree.SubElement(tr, q("p:wipe")).set("dir", "l")
    else:
        etree.SubElement(tr, q("p:fade"))
    timing = root.find(q("p:timing"))
    if timing is not None:
        root.remove(timing)
        root.append(tr)
        root.append(timing)


class TimingBuilder:
    def __init__(self):
        self.i = 1

    def nxt(self):
        self.i += 1
        return self.i

    def effect(self, spid, grp, delay, dur, slide_level=False):
        node_type = "afterEffect" if slide_level else "clickEffect"
        c = [self.nxt() for _ in range(5)]
        return f"""<p:par><p:cTn id="{c[0]}" fill="hold"><p:stCondLst><p:cond delay="{'0' if slide_level else 'indefinite'}"/></p:stCondLst><p:childTnLst>
<p:par><p:cTn id="{c[1]}" fill="hold"><p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst>
<p:par><p:cTn id="{c[2]}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" grpId="{grp}" nodeType="{node_type}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
<p:set><p:cBhvr><p:cTn id="{c[3]}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{c[4]}" dur="{dur}"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr></p:animEffect>
</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>"""

    def build(self, click_shapes, dur=520):
        parts, grp = [], 0
        for spid in click_shapes:
            parts.append(self.effect(spid, grp, 0, dur))
            grp += 1
        bld = '<p:bldLst>' + "".join(
            '<p:bldP spid="%s" grpId="%d" build="p"/>' % (sp, i) for i, sp in enumerate(click_shapes)
        ) + '</p:bldLst>' if click_shapes else ''
        r, s2 = self.nxt(), self.nxt()
        return f"""<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>
<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{''.join(parts)}</p:childTnLst></p:cTn>
<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>
</p:childTnLst></p:cTn></p:par></p:tnLst>
{bld}</p:timing>"""


def set_timing(slide, click_shapes, dur=520):
    root = slide._element
    for el in root.findall(q("p:timing")):
        root.remove(el)
    inner = TimingBuilder().build([str(s) for s in click_shapes], dur)
    holder = etree.fromstring(
        '<root xmlns:p="%s" xmlns:a="%s" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">%s</root>'
        % (NS["p"], NS["a"], inner))
    for child in holder:
        root.append(child)
    tr = root.find(q("p:transition"))
    timing = root.find(q("p:timing"))
    if tr is not None and timing is not None:
        root.remove(tr)
        root.remove(timing)
        root.append(tr)
        root.append(timing)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# ---------------------------------------------------------------------- build
prs = Presentation()
prs.slide_width = Emu(int(13.3333 * EMU_IN))
prs.slide_height = Emu(int(7.5 * EMU_IN))
BLANK = prs.slide_layouts[6]


def new(dark=False):
    s = prs.slides.add_slide(BLANK)
    bg(s, INK if dark else PAPER)
    return s


CW3, CW4, CW2 = 3.98, 2.96, 6.0   # larguras de grade

# 1 · capa --------------------------------------------------------------
s = new(dark=True)
glow(s, 9.4, -2.7, 5.4, 5.4, VIOLET, 26)     # halos de canto, semi-transparentes
glow(s, -2.5, 4.5, 5.0, 5.0, LIME, 16)
kicker(s, "PITCH · TCC ETAPA 5 · 19/10/2026", LIME, w=3.6)
t = box(s, 0.5, 1.30, 9.0, 1.05)
put(t, [("CoreMotion", 50, True, WHITE, DISPLAY, 0.95)], space_after=0)
tag = box(s, 0.5, 2.48, 8.6, 1.05)
put(tag, [("O marketplace do corredor: loja verificada, revenda com cotação justa "
           "e comunidade no mesmo login.", 17, True, LIME, BODY, 1.22)], space_after=0)
metas = []
for i, (lab, val) in enumerate([
    ("PRODUTO", "Marketplace B2C + C2C de corrida e endurance"),
    ("MODELO", "Loja verificada, anúncio entre atletas, comunidade"),
    ("STACK", "Next.js 15 · TypeScript · Supabase/Postgres"),
]):
    m = box(s, 0.5 + i * 3.0, 4.0, 2.86, 1.05, fill=WHITE)
    put(m, [(lab, 9, True, SLATE, MONO, 1.0), (val, 11, True, TXT, BODY, 1.15)], space_after=3)
    metas.append(m)
fundo = note(s, "Equipe: 4 integrantes · orientador e banca a confirmar pela coordenação. "
                "Nenhum número de tração é inventado: o que não existe hoje aparece como meta ou como próximo passo.",
             fill=LIME, y=5.45, h=0.75, size=12, bold=True)
notes(s, "Abertura (40s): «A gente não veio mostrar um site de tênis. Veio mostrar o lugar onde o "
         "corredor compra sem medo, vende sem perder dinheiro e continua depois da compra.»")

# 2 · problema ----------------------------------------------------------
s = new()
kicker(s, "O PROBLEMA", CORAL, w=2.0)
title(s, "Comprar tênis de corrida é um ato de fé", size=30)
problemas = grid(s, [
    ("PROCEDÊNCIA INCERTA", ["Nada prova que o par é original, importado ou recondicionado. "
                             "O anúncio diz “como novo” e ninguém verifica."]),
    ("LOJA PEQUENA SEM VITRINE", ["O lojista de bairro disputa espaço em marketplace generalista: "
                                  "sem página própria, sem selo e sem histórico do cliente."]),
    ("REVENDA ÀS CEGAS", ["Quem vende um par de placa de carbono não sabe o preço justo: depende de "
                          "grupo de WhatsApp e de quem aparece primeiro."]),
    ("COMPRAR E TREINAR EM LUGARES SEPARADOS", ["A compra acontece num site, o treino e a dúvida em outro. "
                                                "Ninguém cria raiz, e o lojista nunca vê o cliente."]),
], 2, CW2, 1.62, y0=1.78, gap=0.33, body=12.5)
fecho2 = note(s, "O corredor não quer mais um checkout: quer comprar sem medo e vender sem perder dinheiro.",
              fill=VIOLET_T, line=VIOLET, y=5.62, h=0.85, size=14)
notes(s, "Problema (60s): três dores que resolvemos — procedência, vitrine do lojista pequeno e preço "
         "de revenda. A quarta é a que ninguém resolveu: o corredor compra num lugar e vive o esporte em outro.")

# 3 · solução ------------------------------------------------------------
s = new()
kicker(s, "A SOLUÇÃO", LIME, w=1.9)
title(s, "Um só lugar para comprar, vender e treinar", size=30)
pilares = grid(s, [
    ("VITRINE VERIFICADA", ["Loja com CNPJ, selo, rating e histórico de vendas visíveis na página do produto."]),
    ("B2C + C2C", ["Estoque da loja e revenda de atleta no mesmo catálogo, com condição, tamanho e cor."]),
    ("PEDIDO DE VERDADE", ["Do carrinho ao rastreio: PIX, cartão ou boleto e o ciclo pagar → separar → entregar."]),
    ("COMUNIDADE", ["Post, comentário, treinador com CREF e atleta buscando patrocínio no mesmo login."]),
], 4, CW4, 2.05, y0=1.78, body=11.5)
dif3 = strip(s, "COMO SE DIFERENCIA", [
    "Marketplace generalista não sabe o que é um tênis de corrida; grupo de WhatsApp não sabe se o par é "
    "legítimo. Aqui, condição, procedência, cotação e comunidade estão no mesmo produto."],
    fill=VIOLET_T, line=VIOLET, y=4.15, h=1.15, body=12.5)
note(s, "Proposta de valor: procedência antes do pagamento e preço antes da revenda.",
     fill=CYAN_T, y=5.55, h=0.75, size=14)
notes(s, "Solução (60s): quatro pilares na tela única. Dizer em voz alta que nada aqui é app novo — é o "
         "produto que já existe, com a fundação que ainda falta.")

# 4 · fluxo do comprador --------------------------------------------------
s = new()
kicker(s, "COMO FUNCIONA · COMPRADOR", CYAN, w=3.3)
title(s, "Da vitrine ao rastreio, sem sair do site", size=29)
comp = grid(s, [
    ("01 · EXPLORAR", ["Home com destaques, marcas, categorias e lojas em destaque."]),
    ("02 · FILTRAR", ["Marca, esporte, condição, tamanho, preço e busca no catálogo e na loja."]),
    ("03 · CONFIAR", ["Página da loja com selo de verificação, rating e total de vendas."]),
    ("04 · ESCOLHER", ["Detalhe do produto com tamanho, cor, estoque, vistas e forma de envio."]),
    ("05 · PAGAR", ["Carrinho e checkout com PIX, cartão de crédito ou boleto."]),
    ("06 · ACOMPANHAR", ["Status do pedido: pago, em separação, enviado, entregue — com rastreio."]),
], 3, CW3, 1.85, y0=1.75, body=11.5)
note(s, "Leitura honesta: a navegação e o carrinho já existem; sessão, estoque e pedido duráveis são a "
        "onda 1 e a onda 2 do roadmap.", fill=LIME_T, line=LIME, y=5.95, h=0.75, size=13)
notes(s, "Comprador (60s): percorrer os seis passos como narrativa de uso. Se a banca pedir demo ao vivo, "
         "avisar que o banco responde 500 no ambiente atual e a vitrine vem do catálogo inicial.")

# 5 · fluxo do lojista ----------------------------------------------------
s = new()
kicker(s, "COMO FUNCIONA · LOJISTA", AMBER, w=3.1)
title(s, "Montar a loja leva uma tarde", size=30)
loj = grid(s, [
    ("CRIAR LOJA", ["Nome, descrição, endereço e logo num modal só."]),
    ("PEDIR VERIFICAÇÃO", ["CNPJ, contato e documentos no cadastro; status fica pendente até análise."]),
    ("PUBLICAR ANÚNCIO", ["B2C da loja ou C2C do atleta, com marca, condição, cores, tamanhos e estoque."]),
    ("GERIR ESTOQUE", ["Editar, mudar de ativo a vendido ou suspenso e acompanhar vistas e curtidas."]),
    ("RECEBER PEDIDO", ["Pedido entra no ciclo de pagamento e entrega; rating e vendas acompanham."]),
], 5, 2.38, 2.75, y0=1.75, gap=0.11, body=11.5)
strip(s, "O QUE FALTA PARA O LOJISTA DEPENDER DO SITE", [
    "Verificação aprovada pelo admin e pedido lido no servidor — ondas 1 e 2.",
    "Monetização projetada: comissão por venda B2C/C2C e destaque de vitrine, com taxa e prazo a validar com a banca.",
], fill=VIOLET_T, line=VIOLET, y=4.75, h=1.5, body=12.5)
notes(s, "Lojista (50s): venda a dor do lojista pequeno. Ele entra pela verificação e fica pelo estoque; as "
         "duas peças que faltam estão nomeadas no rodapé.")

# 6 · mecânicas de confiança (dark) --------------------------------------
s = new(dark=True)
kicker(s, "MECÂNICAS DE CONFIANÇA", LIME, w=3.1)
title(s, "Confiança é a funcionalidade", size=30, dark=True, w=12.33)
conf = grid(s, [
    ("SELO DE VERIFICAÇÃO", ["Loja com CNPJ e documentos passa por análise; o selo aparece na vitrine e no produto."]),
    ("CONDIÇÃO DECLARADA", ["Novo, como novo, seminovo, usado excelente ou usado bom: o estado vem no anúncio e no filtro."]),
    ("COTAÇÃO JUSTA", ["SmartScan liga desgaste de entressola e placa ao preço de mercado e sugere um valor."]),
    ("MODERAÇÃO", ["Denúncia em post, bloqueio de usuário e retirada de anúncio sinalizado."]),
    ("REPUTAÇÃO", ["Rating e vendas acumuladas da loja; avaliação do vendedor C2C por quem comprou."]),
    ("CICLO DO PEDIDO", ["pending_payment → paid → preparing → shipped → delivered, com cancelamento registrado."]),
], 3, CW3, 1.95, y0=1.75, body=11.5)
fim6 = box(s, 0.5, 6.05, 12.33, 0.6)
put(fim6, [("Cada item acima tem campo no modelo de dados — não é promessa de slide.",
            15, True, LIGHT, BODY, 1.15)], space_after=0)
notes(s, "Confiança (60s): o coração do pitch. Selo, condição, cotação, moderação, reputação e ciclo do "
         "pedido — cada um existe no modelo de dados (lib/types.ts).")

# 7 · papéis --------------------------------------------------------------
s = new()
kicker(s, "OS PAPÉIS", VIOLET, w=1.9)
title(s, "Quatro papéis hoje, cinco na próxima onda", size=29)
papeis = []
for i, (lab, txt, hot) in enumerate([
    ("VISITOR", "Navega catálogo, lojas, comunidade e treinadores; não compra nem anuncia.", False),
    ("USUÁRIO", "Compra, anuncia em C2C, curte, comenta, avalia e bloqueia quem denuncia.", False),
    ("LOJISTA", "Cria loja, pede verificação, publica anúncio B2C e gerencia estoque e status.", False),
    ("ADMIN", "Aprova verificação de loja, modera conteúdo e gerencia usuários (um clique hoje).", False),
    ("SUPERVISOR", "Previsto na hierarquia do enunciado e ainda ausente no código: entra na onda 1.", True),
]):
    y = 1.75 + i * 0.82
    k = box(s, 0.5, y, 2.6, 0.72, fill=LIME if hot else SLATE_T, line=LIME if hot else HAIR)
    put(k, [(lab, 12, True, TXT, MONO, 1.0)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    b = box(s, 3.2, y, 9.63, 0.72, fill=WHITE, line=HAIR)
    put(b, [(txt, 12.5, False, TXT, BODY, 1.15)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    papeis += [k, b]
note(s, "A role hoje mora no registro do usuário; a separação por vínculo loja↔usuário é decisão em aberto "
        "(D-01) e entra na onda 1, junto com autorização no servidor.",
     fill=CYAN_T, y=5.95, h=0.85, size=12.5, bold=True)
notes(s, "Papéis (45s): quatro existem, o quinto é exigência do enunciado. Se a banca perguntar por que "
         "ainda não está pronto: a decisão D-01 vem antes do código.")

# 8 · ecossistema ---------------------------------------------------------
s = new()
kicker(s, "ECOSSISTEMA", CYAN, w=2.3)
title(s, "A comunidade é o que faz o cliente voltar", size=29)
eco = grid(s, [
    ("COMUNIDADE", ["Categorias treino, equipamento, evento, dúvida e conquista; curtir, comentar, "
                    "denunciar e bloquear; badge no autor."]),
    ("TREINADORES", ["Perfil com CREF, certificação, valor por hora, disponibilidade e rating: serviço ao lado do produto."]),
    ("ATLETAS", ["Conquistas e status de patrocínio (buscando ou patrocinado): ponte natural entre atleta e marca."]),
    ("EDITORIAL", ["Notícia com tempo de leitura e autor; falta ligar a view no menu — conteúdo já modelado."]),
], 2, CW2, 1.62, y0=1.78, gap=0.33, body=12.5)
note(s, "Nada aqui depende de fornecedor externo: é o que separa um marketplace de um catálogo com login.",
     fill=VIOLET_T, line=VIOLET, y=5.62, h=0.8, size=14)
notes(s, "Ecossistema (50s): o que faz o cliente voltar. A view de notícias já está modelada e falta só ligar "
         "no menu — trabalho pequeno, efeito visível.")

# 9 · SmartScan (dark) ----------------------------------------------------
s = new(dark=True)
kicker(s, "INTELIGÊNCIA DE PRODUTO", LIME, w=3.0)
title(s, "SmartScan: do desgaste ao preço justo", size=29, dark=True, w=12.33)
scan = grid(s, [
    ("ENTRADA", ["Modelo, preço praticado, pace do corredor e pisada: o que o atleta já sabe de cabeça."]),
    ("ANÁLISE", ["Vida útil da entressola e estado da placa de carbono, com expectativa em km e risco de lesão."]),
    ("SAÍDA", ["Cotação justa para venda ou troca, na tela de quem está decidindo, não depois."]),
], 3, CW3, 2.15, y0=1.75, body=12)
strip(s, "ONDA 3 · AINDA FORA DA NAVEGAÇÃO", [
    "O componente está pronto na tela, mas o seletor de views ainda não o expõe e ele não consome histórico de "
    "pedidos nem tabela própria. Integrá-lo ao fluxo de venda é o que transforma o recurso em argumento comercial."],
    fill=CORAL_T, y=4.15, h=1.5, body=12.5)
fim9 = box(s, 0.5, 5.9, 12.33, 0.7)
put(fim9, [("Não vendemos IA em produção: vendemos a peça pronta que falta encaixar.",
            15, True, LIME, BODY, 1.15)], space_after=0)
notes(s, "SmartScan (50s): o diferencial. Deixar claro o estado real — componente pronto, fora da navegação, "
         "sem histórico de pedidos. É a peça que vira argumento comercial quando entrar no fluxo.")

# 10 · arquitetura --------------------------------------------------------
s = new()
kicker(s, "ARQUITETURA", CYAN, w=2.4)
title(s, "Feito para virar produto, não maquete", size=29)
stack = grid(s, [
    ("FRONT", ["Next.js 15 (App Router), TypeScript estrito, Tailwind; uma view com modal por função."]),
    ("SERVIDOR", ["app/api + app/actions + services; build standalone pronto para rodar em Node."]),
    ("DADOS", ["Postgres no Supabase com RLS; migração versionada e modelos de loja, produto, pedido e post."]),
    ("ESTADO", ["Store React com persistência local: carrinho, pedido e sessão vivem no cliente."]),
], 4, CW4, 2.3, y0=1.78, body=11.5)
strip(s, "A DECISÃO QUE IMPORTA", [
    "Autorização e preço no servidor, store como cache: assim o Supabase real entra sem reescrever a interface. "
    "É por isso que a fundação vem antes de qualquer função nova."],
    fill=VIOLET_T, line=VIOLET, y=4.35, h=1.15, body=12.5)
note(s, "Baseline da rodada: npm install 995 pacotes · type-check passa · lint 0 erros / 23 avisos · build "
        "passa · GET / 200 · /api/products, /api/stores e /api/users 500.",
     fill=SLATE_T, y=5.72, h=0.85, size=11.5, bold=False, font=MONO)
notes(s, "Arquitetura (45s): responder antes da pergunta — por que não plugar o Supabase agora? Porque a store "
         "é a fonte de verdade; primeiro o servidor, depois o resto.")

# 11 · onde estamos -------------------------------------------------------
s = new()
kicker(s, "ONDE ESTAMOS", AMBER, w=2.4)
title(s, "O que roda, o que falta, o que vem", size=29)
colunas = [
    ("NO AR HOJE", ["· Catálogo com busca, filtros e ordenação", "· Loja com selo, rating e vitrine própria",
                    "· Anúncio B2C e C2C com condição, tamanho e cor", "· Carrinho e checkout com PIX, cartão e boleto",
                    "· Comunidade, treinadores e notícias na interface"], LIME_T, LIME),
    ("EM CONSTRUÇÃO", ["· Sessão no cliente, sem cookie httpOnly", "· Autorização que ainda confia no dado do navegador",
                       "· Ciclo de pedido no estado, sem leitura no servidor", "· Verificação sem aprovação pelo admin",
                       "· RLS sem WITH CHECK nem GRANT restrito"], WHITE, CORAL),
    ("PRÓXIMA ONDA", ["· Supervisor e autorização no servidor", "· PSP real com webhook e estoque transacional",
                       "· Comunidade persistida e avaliação com prova de compra", "· SmartScan dentro do fluxo de venda",
                       "· CI, testes e observabilidade"], WHITE, HAIR),
]
onde = []
for i, (head, lines, fill, line) in enumerate(colunas):
    c = card(s, 0.5 + i * (CW3 + 0.19), 1.72, CW3, 3.95, head, lines, fill=fill, line=line, body=11)
    onde.append(c)
note(s, "A coluna do meio não é detalhe: é a base que faz o resto valer. Por ela abre o roadmap.",
     fill=VIOLET_T, line=VIOLET, y=5.9, h=0.75, size=14)
notes(s, "Onde estamos (60s): o slide de credibilidade. Ler a coluna do meio sem rodeios e seguir para o "
         "roadmap; é aqui que a banca decide se confia no resto.")

# 12 · roadmap (dark) -----------------------------------------------------
s = new(dark=True)
kicker(s, "ROADMAP", LIME, w=1.8)
title(s, "Três ondas, uma ordem", size=30, dark=True, w=12.33)
ondas = [
    ("ONDA 1 · FUNDAÇÃO SEGURA", "≈ 4 semanas", ["· Sessão em cookie httpOnly",
        "· Preço e estoque recalculados no servidor", "· public.users, RLS com WITH CHECK e GRANT",
        "· Rotação da credencial exposta, segredo fora do repo", "· Papel supervisor e matriz de permissões"]),
    ("ONDA 2 · NEGÓCIO REAL", "≈ 6 semanas", ["· Verificação aprovada por admin, com auditoria",
        "· Checkout com PSP real, webhook e idempotência", "· Pedido, estoque e cancelamento no banco",
        "· Comunidade e denúncias persistidas", "· E-mail transacional de confirmação"]),
    ("ONDA 3 · CRESCIMENTO", "≈ 6 semanas", ["· SmartScan no fluxo de venda e de troca",
        "· Avaliações com prova de compra", "· Busca com facetas e sugestões",
        "· CI com type-check, lint e testes", "· Observabilidade, rate limit e mobile"]),
]
road = []
for i, (head, weeks, lines) in enumerate(ondas):
    line = LIME if i == 0 else WHITE
    paras = [(head, 10.5, True, TXT, MONO, 1.1), (weeks, 11, True, SLATE, BODY, 1.1)]
    paras += [(ln, 11, False, TXT, BODY, 1.2) for ln in lines]
    sh = box(s, 0.5 + i * (CW3 + 0.19), 1.72, CW3, 3.95, fill=fill, line=line, radius=0.05)
    put(sh, paras, space_after=5)
    road.append(sh)
fim12 = box(s, 0.5, 5.9, 12.33, 0.7)
put(fim12, [("≈ 16 semanas · fundação segura antes de função nova · cada item com arquivo e linha no diagnóstico.",
             14.5, True, LIGHT, BODY, 1.15)], space_after=0)
notes(s, "Roadmap (70s): três ondas, ~16 semanas. Reforçar a ordem — fundação segura antes de função nova — "
         "e dizer que cada item tem arquivo e linha no documento de pendências.")

# 13 · riscos -------------------------------------------------------------
s = new()
kicker(s, "RISCOS", CORAL, w=1.7)
title(s, "Os riscos que aceitamos enfrentar", size=29)
riscos = []
for i, (lab, txt) in enumerate([
    ("SEGURANÇA", "Credencial exposta no repositório e sessão no navegador → rotação imediata, segredo fora do "
                  "repo e cookie httpOnly abrem a onda 1."),
    ("DADO FALSO", "Preço e estoque chegam do cliente → cálculo no servidor, transação e constraint de estoque."),
    ("PAGAMENTO", "PIX em sandbox, sem webhook → PSP real com estado conciliado, idempotência e reconciliação diária."),
    ("ESCALA", "Sem índice, CI ou testes → pipeline com type-check, lint e build, índice de busca e smoke de API."),
]):
    y = 1.72 + i * 1.13
    r = box(s, 0.5, y, 12.33, 1.0, fill=WHITE, line=HAIR, radius=0.03)
    put(r, [(lab + " — " + txt, 12.5, False, TXT, BODY, 1.2)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    riscos.append(r)
note(s, "Nenhum dos quatro riscos é descoberto pela banca: todos estão descritos no diagnóstico com arquivo e linha.",
     fill=LIME_T, line=LIME, y=6.35, h=0.62, size=13)
notes(s, "Riscos (45s): não esconder nenhum. Fechar lembrando que os quatro já estão no inventário, com evidência.")

# 14 · metricas -----------------------------------------------------------
s = new()
kicker(s, "MÉTRICAS", VIOLET, w=2.0)
title(s, "Como medimos se está funcionando", size=29)
ns14 = box(s, 0.5, 1.72, 12.33, 1.0, fill=LIME, line=LIME)
put(ns14, [("NORTH STAR METRIC", 10, True, INK, MONO, 1.0),
           ("Pedidos concluídos por loja verificada — a única métrica que depende de confiança, conversão "
            "e receita ao mesmo tempo.", 13.5, True, TXT, BODY, 1.15)], space_after=3)
metas14 = grid(s, [
    ("CONVERSÃO", ["Visita → pedido pago. Baseline a medir nas quatro primeiras semanas."]),
    ("VERIFICAÇÃO", ["Meta: menos de 48h entre o pedido do lojista e a aprovação do selo."]),
    ("RETENÇÃO", ["Usuário que volta à comunidade em 30 dias; medir após a onda 2."]),
    ("COBERTURA", ["Lojas com selo e anúncios com condição e tamanho preenchidos."]),
], 4, CW4, 1.65, y0=2.95, body=11.5)
note(s, "Sem baseline inventada: o site ainda não tem tráfego real, então as metas entram em vigor quando a "
        "onda 2 liga o banco. O que não sabemos fica marcado como PENDENTE no documento.",
     fill=AMBER_T, line=AMBER, y=5.15, h=1.05, size=12.5, bold=False)
notes(s, "Métricas (40s): north star + quatro metas. Não inventar baseline; o que não existe hoje fica PENDENTE "
         "no documento e entra em vigor com a onda 2.")

# 15 · pedido (dark) ------------------------------------------------------
s = new(dark=True)
glow(s, 10.4, 4.4, 4.6, 4.6, VIOLET, 28)
glow(s, -2.2, -2.6, 4.6, 4.6, LIME, 14)
kicker(s, "O PEDIDO", LIME, w=1.9)
title(s, "Agora, pedimos três coisas", size=32, dark=True, w=12.33)
ped = grid(s, [
    ("VALIDAR A ONDA 1", ["Sessão, autorização, roles e rotação da credencial antes de qualquer função nova."]),
    ("APROVAR D-01", ["Lojista é papel ou vínculo com a loja? A resposta muda tabela, permissão e verificação."]),
    ("AUTORIZAR DADOS DE TESTE", ["Para medir conversão e retenção precisamos de tráfego de teste e consentimento no cadastro."]),
], 3, CW3, 2.0, y0=1.72, body=12)
fim15 = box(s, 0.5, 4.05, 12.33, 1.5, fill=LIME)
put(fim15, [("CoreMotion não pede uma nota: pede para continuar.", 20, True, INK, DISPLAY, 1.1),
            ("Obrigado — Equipe CoreMotion · TCC Etapa 5 · 19/10/2026", 12, True, INK, BODY, 1.2)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=6)
notes(s, "Fecho (40s): pedir as três coisas uma por uma e parar de falar. A última frase é a que fica: o "
         "produto não pede nota, pede para continuar.")

# ------------------------------------------- transicoes + entradas por clique
TRANSITIONS = ["fade", "morph", "fade", "push", "fade", "wipe", "fade", "push",
               "fade", "push", "fade", "morph", "fade", "push", "fade"]

for idx, sl in enumerate(prs.slides):
    set_transition(sl, TRANSITIONS[idx % len(TRANSITIONS)], dur=650)
    ids = [sh.shape_id for sh in sl.shapes][2:]   # kicker e titulo ficam fixos
    set_timing(sl, click_shapes=ids[:6])

out = sys.argv[1] if len(sys.argv) > 1 else "/home/user/pitch-animado.pptx"
prs.save(out)
print("salvo em %s · %d slides" % (out, len(prs.slides._sldIdLst)))
