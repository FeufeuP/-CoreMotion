"""Gera a versao animada (transicoes + animacoes por clique/paragrafo) do deck
de pendencias do CoreMotion - Etapa 5, em PPTX.

Uso:  python tools/make_deck_pptx.py <saida.pptx>

Transicoes e animacoes sao escritas como XML PresentationML cru (p:transition /
p:timing), porque python-pptx nao expoe esses recursos - exatamente como o
Google Slides API tambem nao expoe.
"""
from __future__ import annotations

import copy
import re
import sys

from lxml import etree
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
VIOLET = RGBColor(0x6C, 0x4C, 0xF1)
VIOLET_T = RGBColor(0xEC, 0xE8, 0xFF)
CYAN = RGBColor(0x14, 0xC8, 0xDC)
AMBER = RGBColor(0xFF, 0xB0, 0x20)
CORAL = RGBColor(0xFF, 0x3B, 0x5C)
CORAL_T = RGBColor(0xFF, 0xEC, 0xEF)
SLATE = RGBColor(0x4A, 0x54, 0x68)
SLATE_T = RGBColor(0xEA, 0xED, 0xF2)
TXT = INK


def q(tag: str) -> str:
    pre, local = tag.split(":")
    return "{%s}%s" % (NS[pre], local)


# ----------------------------------------------------------------- primitives
def bg(slide, color: RGBColor) -> None:
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def box(slide, x, y, w, h, fill=None, line=None, radius=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius is not None else MSO_SHAPE.RECTANGLE,
        Emu(int(x * EMU_IN)), Emu(int(y * EMU_IN)), Emu(int(w * EMU_IN)), Emu(int(h * EMU_IN)),
    )
    if radius is not None:
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


def put(shape, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space_after=4):
    tf = shape.text_frame
    tf.margin_left = Emu(int(0.16 * EMU_IN))
    tf.margin_right = Emu(int(0.14 * EMU_IN))
    tf.margin_top = Emu(int(0.10 * EMU_IN))
    tf.margin_bottom = Emu(int(0.08 * EMU_IN))
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


DISPLAY = "Arial Black"
BODY = "Arial"
MONO = "Consolas"


def kicker(slide, text, color, x=0.5, y=0.38, w=2.6, on_dark=False):
    chip = box(slide, x, y, w, 0.28, fill=color)
    put(chip, [(text, 10, True, INK if not on_dark else INK, MONO, 1.0)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    return chip


def title(slide, text, size=25, x=0.5, y=0.74, w=12.33, on_dark=False, plate=False):
    if on_dark:
        plate_shape = box(slide, x, y - 0.12, w, 0.72, fill=WHITE)
        put(plate_shape, [(text, size, True, TXT, DISPLAY, 1.0)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
        return plate_shape
    t = box(slide, x, y, w, 0.7)
    put(t, [(text, size, True, TXT, DISPLAY, 1.0)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    return t


def panel(slide, x, y, w, h, lines, fill=WHITE, line=HAIR, size=11.5, head=None,
          head_color=None, spc=1.18, align=PP_ALIGN.LEFT):
    shape = box(slide, x, y, w, h, fill=fill, line=line, radius=0.045)
    paras = []
    if head:
        paras.append((head, size + 1.5, True, head_color or TXT, BODY, 1.1))
    for ln in lines:
        paras.append((ln, size, False, TXT, BODY, spc))
    put(shape, paras, align=align, space_after=5)
    return shape


def mono_panel(slide, x, y, w, h, lines, fill=SLATE_T, line=HAIR, size=10.5, head=None):
    shape = box(slide, x, y, w, h, fill=fill, line=line, radius=0.045)
    paras = []
    if head:
        paras.append((head, size + 1, True, TXT, MONO, 1.1))
    for ln in lines:
        paras.append((ln, size, False, TXT, MONO, 1.24))
    put(shape, paras, space_after=3)
    return shape


# ------------------------------------------------------------------- XML magic
def set_transition(slide, kind="fade", dur=650, advance=False):
    """kind: fade | push | morph | wipe | none"""
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
    if advance:
        tr.set("advTm", "8000")
    # transition must precede timing
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
        cid1, cid2, cid3, cid4, cid5 = self.nxt(), self.nxt(), self.nxt(), self.nxt(), self.nxt()
        return f"""<p:par><p:cTn id="{cid1}" fill="hold"><p:stCondLst><p:cond delay="{'0' if slide_level else 'indefinite'}"/></p:stCondLst><p:childTnLst>
<p:par><p:cTn id="{cid2}" fill="hold"><p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst>
<p:par><p:cTn id="{cid3}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" grpId="{grp}" nodeType="{node_type}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
<p:set><p:cBhvr><p:cTn id="{cid4}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{cid5}" dur="{dur}"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr></p:animEffect>
</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>"""

    def build(self, click_shapes, auto_shapes, dur=520):
        """click_shapes: lista de spids que entram a cada clique (com build por paragrafo)
        auto_shapes: spids que entram sozinhos, em sequencia, apos a transicao"""
        groups = []
        grp = 0
        for spid in auto_shapes:
            groups.append(self.effect(spid, grp, 200 + grp * 320, dur, slide_level=True))
            grp += 1
        par_clicks = []
        for spid in click_shapes:
            par_clicks.append(self.effect(spid, grp, 0, dur))
            grp += 1
        inner = "".join(groups) + "".join(par_clicks)
        bld = (
            '<p:bldLst>'
            + "".join('<p:bldP spid="%s" grpId="%d" build="p"/>' % (sp, i + len(auto_shapes))
                      for i, sp in enumerate(click_shapes))
            + '</p:bldLst>'
            if click_shapes else ''
        )
        cid_root, cid_seq = self.nxt(), self.nxt()
        timing = f"""<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>
<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{inner}</p:childTnLst></p:cTn>
<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>
</p:childTnLst></p:cTn></p:par></p:tnLst>
{bld}</p:timing>"""
        return timing


def set_timing(slide, click_shapes, auto_shapes=(), dur=520):
    """Escreve p:timing (entradas por clique, com build por paragrafo) na slide XML."""
    root = slide._element
    for el in root.findall(q("p:timing")):
        root.remove(el)
    inner = TimingBuilder().build([str(s) for s in click_shapes], [str(s) for s in auto_shapes], dur)
    holder = etree.fromstring(
        '<root xmlns:p="%s" xmlns:a="%s" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">%s</root>'
        % (NS["p"], NS["a"], inner)
    )
    for child in holder:
        root.append(child)
    # ordem do schema: cSld, clrMapOvr, transition, timing
    tr = root.find(q("p:transition"))
    timing = root.find(q("p:timing"))
    if tr is not None and timing is not None:
        root.remove(tr)
        root.remove(timing)
        root.append(tr)
        root.append(timing)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# --------------------------------------------------------------------- content
prs = Presentation()
prs.slide_width = Emu(int(13.3333 * EMU_IN))
prs.slide_height = Emu(int(7.5 * EMU_IN))
BLANK = prs.slide_layouts[6]


def slide_new(dark=False):
    s = prs.slides.add_slide(BLANK)
    bg(s, INK if dark else PAPER)
    return s


def spids(shapes):
    return [sh.shape_id for sh in shapes]


# 1 - capa
s = slide_new(dark=True)
box(s, -1.6, -1.8, 6.0, 6.0, fill=VIOLET)
box(s, 9.4, 4.2, 5.4, 5.4, fill=LIME)
kicker(s, "RELATORIO DE PENDENCIAS · ETAPA 5", LIME)
t = title(s, "O que ainda falta no CoreMotion", size=42, y=1.5)
t.text_frame.paragraphs[0].runs[0].font.color.rgb = WHITE
sub = box(s, 0.5, 2.5, 8.2, 1.0)
put(sub, [("Inventario completo da rodada de documentacao: 76 lacunas catalogadas, com prova em arquivo e linha.",
           16, False, SLATE_T, BODY, 1.25)], space_after=0)
meta = []
for i, (label, val, col) in enumerate([
    ("REPOSITORIO", "FeufeuP/-CoreMotion", WHITE),
    ("COMMIT", "b0827ec · main", WHITE),
    ("DATA", "19/10/2026", WHITE),
]):
    m = box(s, 0.5 + i * 3.1, 4.1, 2.9, 0.72, fill=col)
    put(m, [(label, 9, True, SLATE, MONO, 1.0), (val, 12, True, TXT, BODY, 1.05)], space_after=2)
    meta.append(m)
side = box(s, 9.9, 4.1, 2.93, 1.9, fill=LIME)
put(side, [("76", 40, True, TXT, DISPLAY, 0.95), ("lacunas catalogadas", 11, True, TXT, BODY, 1.1)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
notes(s, "Abrir o deck pelo contrato de confianca: nada aqui e chute. Tudo que esta escrito foi lido no repositorio em 19/10/2026. 40s.")

# 2 - legenda
s = slide_new()
kicker(s, "COMO LER ESTA LISTA", CYAN, w=2.7)
title(s, "Cinco estados, nenhuma suposicao", size=30)
legend = [
    ("FALTA", "O entregavel nao existe no repositorio", SLATE_T, HAIR),
    ("PARCIAL", "Existe, mas nao cobre o contrato inteiro", LIME, LIME),
    ("PENDENTE", "Depende de decisao ou dado da equipe", SLATE_T, HAIR),
    ("BLOQUEADO", "Nao comeca antes de um contrato ser aprovado", AMBER, AMBER),
    ("NAO VERIFICADO", "Pode ate existir, mas nao ha prova em execucao", WHITE, HAIR),
]
chips = []
for i, (name, desc, fill, line) in enumerate(legend):
    c = box(s, 0.5, 1.75 + i * 0.86, 7.4, 0.74, fill=fill, line=line, radius=0.09)
    put(c, [(name, 13, True, TXT, MONO, 1.0), (desc, 11, False, SLATE, BODY, 1.1)], space_after=2)
    chips.append(c)
rule = box(s, 8.15, 1.75, 4.68, 4.1, fill=INK, radius=0.05)
put(rule, [("REGRA DE HONESTIDADE", 12, True, LIME, MONO, 1.1),
           ("Nada e declarado concluido sem evidencia.", 13, True, WHITE, BODY, 1.2),
           ("O que nao foi testado em execucao recebe NAO VERIFICADO em vez de suposicao favoravel.", 11.5, False, SLATE_T, BODY, 1.28),
           ("6 checks estao fora da contagem de 76 por isso.", 11.5, False, SLATE_T, BODY, 1.28)], space_after=8)
notes(s, "Explicar a diferenca entre FALTA e NAO VERIFICADO: a segunda protege o TCC de afirmar o que nao foi provado. 35s.")

# 3 - veredito
s = slide_new()
kicker(s, "VEREDITO DA RODADA", VIOLET, w=2.4)
title(s, "O projeto documenta, mas nao entrega", size=32)
v = box(s, 0.5, 1.7, 12.33, 1.55, fill=LIME, line=LIME, radius=0.06)
put(v, [("Compila, sobe - e nada esta provado. A superficie do app existe; autenticacao, autorizacao, pagamento e persistencia sao fachada, enquanto segredo real, documentacao de execucao e TCC ainda nao sairam do papel.",
         15, True, TXT, DISPLAY, 1.16)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
kpis = []
for i, (num, label, fill) in enumerate([
    ("0 / 7", "entregaveis da etapa fechados", WHITE),
    ("13", "lacunas de identidade e acesso", WHITE),
    ("2", "bloqueadores dependente de decisao", SLATE_T),
    ("1", "P0: credencial exposta no codigo", CORAL_T),
]):
    c = box(s, 0.5 + i * 3.14, 3.5, 2.94, 1.35, fill=fill, line=HAIR, radius=0.07)
    put(c, [(num, 30, True, TXT, DISPLAY, 0.95), (label, 10.5, False, SLATE, BODY, 1.15)], space_after=4)
    kpis.append(c)
foot = box(s, 0.5, 5.1, 12.33, 1.2, fill=WHITE, line=HAIR, radius=0.06)
put(foot, [("Provas da rodada: npm install 995 pacotes · type-check PASS · lint 0 erros (23 avisos) · build PASS · GET / 200 · /api/products 500 · /api/stores e /api/users 500.",
            12, False, TXT, MONO, 1.22),
           ("Nada disso prova negocio: o banco devolve 500 e a home cai no mock.", 11.5, True, TXT, BODY, 1.2)], space_after=5)
notes(s, "Fechar o veredito e ja emendar: o build passar nao significa o produto funcionar. 50s.")

# 4 - entregaveis
s = slide_new()
kicker(s, "OS 7 ENTREGAVEIS EXIGIDOS", CORAL, w=2.9)
title(s, "Seis faltam, um so existe", size=30)
a = panel(s, 0.5, 1.65, 6.0, 4.3, [
    "① DOCUMENTO FINAL DE EXECUCAO - FALTA (nao existe; virou guia)",
    "② PLANO DE TESTES - FALTA (so um paragrafo no guia)",
    "③ PLANO DE IMPLEMENTACAO - FALTA (rascunho por pessoa)",
    "④ RELATORIO DE EXECUCAO - PARCIAL (roda de 19/10 sem testes)",
    "⑤ DAILY REPORT - PARCIAL (1 dia em 4)",
], head="ENTREGAVEIS FORMAIS (docs/etapa-5)", size=12, head_color=VIOLET, spc=1.3)
b = panel(s, 6.83, 1.65, 6.0, 4.3, [
    "① CODE REVIEW - PARCIAL: 3 relatorios, sem decisao registrada",
    "② IMPLEMENTACAO - PARCIAL: nada corrigido em app/, components/, lib/, services/",
    "③ REPOSITORIO - PARCIAL: sem README, sem CI, sem testes automatizados",
    "④ DEMO PUBLICADA - PENDENTE: sem link; o guia diz para nao subir",
    "⑤ TCC - FALTA: 0 capturas, 0 figuras, 0 tabelas, secoes 1 a 6 vazias",
    "⑥ DIAGRAMAS - PARCIAL: casos de uso e fluxograma; falta o de atividades",
    "⑦ APRESENTACAO - FALTA: comecou nesta rodada",
], head="ARTEFATOS TECNICOS", size=12, head_color=CORAL, spc=1.22, fill=CORAL_T, line=CORAL_T)
strip = box(s, 0.5, 6.1, 12.33, 0.62, fill=WHITE, line=HAIR, radius=0.1)
put(strip, [("P0 antes de qualquer item de acabamento: credencial do banco exposta no codigo, empacotada no build e publica no GitHub (valor redigido neste deck).",
             12, True, TXT, BODY, 1.1)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
notes(s, "Ler as duas colunas em sequencia, uma linha por clique. Fechar com o P0: e o unico item que cresce a cada push. 1min.")

# 5 - frentes
s = slide_new()
kicker(s, "AS 4 FRENTES", AMBER, w=2.2)
title(s, "Onde a rodada parou em cada frente", size=30)
cols = [
    ("PESSOA 1 · BACKEND", "FALTA", VIOLET, [
        "14 lacunas registradas (B-02 a B-15)",
        "B0 a B4 sem linha de negocio",
        "Zero arquivos de backend criados",
    ]),
    ("PESSOA 2 · FRONTEND", "FALTA", CYAN, [
        "11 lacunas registradas (F-01 a F-11)",
        "Um arquivo unico no lugar do fluxo",
        "Zero telas capturadas",
    ]),
    ("PESSOA 3 · DOCUMENTOS", "FALTA", AMBER, [
        "16 itens pendentes ou faltando",
        "Cap. 1 a 6 do TCC vazios",
        "Falta diagrama de atividades",
    ]),
    ("PESSOA 4 · QUALIDADE", "FALTA", CORAL, [
        "Nenhum teste escrito",
        "Plano e relatorio so no guia",
        "README e links ausentes",
    ]),
]
cards = []
for i, (head, state, color, lines) in enumerate(cols):
    x = 0.5 + i * 3.14
    bar = box(s, x, 1.62, 2.94, 0.14, fill=color)
    c = panel(s, x, 1.76, 2.94, 3.6, lines, size=11.5, head=head, head_color=TXT, spc=1.26)
    st = box(s, x, 5.5, 2.94, 0.5, fill=color, radius=0.1)
    put(st, [(state, 12, True, TXT, MONO, 1.0)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    cards += [bar, c, st]
foot = box(s, 0.5, 6.22, 12.33, 0.5, fill=SLATE_T, radius=0.1)
put(foot, [("As quatro pastas de frente (pessoa-1 a pessoa-4) contem apenas README: nenhum plano, execucao ou review individual foi escrito.",
            11, True, SLATE, BODY, 1.1)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
notes(s, "Enfatizar a simetria: nenhuma frente tem motivo para acreditar que esta mais avancada que as outras. 45s.")

# 6 - P0
s = slide_new(dark=True)
kicker(s, "P0 · ANTES DE QUALQUER CODIGO", LIME, w=3.3)
title(s, "A credencial que vale mais que todo o resto", size=30, on_dark=True)
cards6 = []
for i, (head, text, fill) in enumerate([
    ("O QUE ESTA EXPOSTO", "Senha do banco, URL do projeto Supabase e anon key - hardcoded em lib/db.ts, lib/supabase.ts e services/supabaseClient.ts.", WHITE),
    ("ONDE CHEGOU", "No bundle de producao dentro de .next: 2x no JS do navegador e 3x no server chunk - alem do historico do Git.", WHITE),
    ("COMO VIRA ESCRITA", "resolveDatabaseUrl() usa o padrao embutido quando DATABASE_URL nao existe: a infra passa a depender da credencial vazada.", CORAL_T),
    ("POR QUE NAO BASTA APAGAR", "Remover o arquivo nao muda o historico; o valor segue vivo no Supabase enquanto nao for rotacionado.", WHITE),
]):
    x = 0.5 + i * 3.14
    c = box(s, x, 1.85, 2.94, 2.2, fill=fill, radius=0.06)
    put(c, [(head, 10.5, True, TXT, MONO, 1.1), (text, 11, False, TXT, BODY, 1.24)], space_after=6)
    cards6.append(c)
seq = panel(s, 0.5, 4.3, 6.0, 1.85, [
    "1 · rotacionar a senha no Supabase (acao humana)",
    "2 · DATABASE_URL via variavel de ambiente",
    "3 · remover o default de lib/db.ts e os hardcodes",
    "4 · revogar anon key se houver politicas permissivas",
    "5 · reescrever historia + BFG, com a equipe",
    "6 · reavaliar exposicao do e-mail do Mestre Admin",
], head="ORDEM QUE A EQUIPE PRECISA EXECUTAR (acesso humano, nao o Arena)", size=10.5, fill=WHITE, line=WHITE, head_color=TXT, spc=1.12)
why = panel(s, 6.83, 4.3, 6.0, 1.85, [
    "Quem tem a senha conecta direto no Postgres, fora do Auth e do RLS: le e escreve users, profiles, stores, products, orders e community_posts.",
    "Risco agravado por politicas permissivas: GRANT ALL to anon e INSERT sem checagem de dono.",
], head="CONSEQUENCIA", size=11, fill=LIME, line=LIME, head_color=TXT, spc=1.2)
notes(s, "Este e o unico slide que pede acao imediata fora do escopo do TCC. Nomear quem roda a credencial e registrar data e hora. 1min.")

# 7 - cadeia de auth
s = slide_new()
kicker(s, "FRENTE 1 · IDENTIDADE E ACESSO", VIOLET, w=3.1)
title(s, "Login que entra em qualquer conta", size=31)
steps = [
    "Usuario envia e-mail e senha ao login",
    "signInWithPassword falha: so console.warn, sem retornar erro",
    "Codigo associa usr_<timestamp> fabricado ao e-mail ja cadastrado",
    "Papel vem de user_metadata; Mestre Admin por lista de e-mails",
    "Sync grava ou reativa a linha em public.users e devolve success: true",
    "O resto da aplicacao trusts role / userId / seller_id vindos do cliente",
]
chain = box(s, 0.5, 1.65, 7.1, 4.15, fill=WHITE, line=HAIR, radius=0.05)
put(chain, [("%d · %s" % (i + 1, txt), 13, i in (0, 4, 5), TXT if i in (0, 4, 5) else SLATE, BODY, 1.16)
            for i, txt in enumerate(steps)], space_after=10)
chain.text_frame.margin_left = Emu(int(0.24 * EMU_IN))
chain.text_frame.margin_top = Emu(int(0.18 * EMU_IN))
notes7 = [
    ("PROVA", "services/auth.ts:88-134 - catch com console.warn e continuacao; usr_<timestamp> no codigo de producao.", SLATE_T, HAIR),
    ("IMPACTO", "Quem conhecer o prefixo de um e-mail cadastrado passa a ver painel de vendedor e, no Mestre Admin, dados de outras lojas.", CORAL_T, CORAL_T),
    ("CONTRATO ALVO", "401 para credencial invalida e 403 para papel insuficiente; session.ts + cookies httpOnly; API sem papel no corpo.", VIOLET_T, VIOLET_T),
]
cards7 = []
for i, (head, text, fill, line) in enumerate(notes7):
    c = panel(s, 7.85, 1.65 + i * 1.42, 4.98, 1.28, [text], head=head, size=10.5, fill=fill, line=line,
              head_color=TXT, spc=1.18)
    cards7.append(c)
foot = box(s, 0.5, 6.0, 12.33, 0.7, fill=LIME, radius=0.09)
put(foot, [("Sem o lote B1 (helper de sessao + rotas protegidas + revogacao), os lotes B2 e B3 ficam sem base: auth, papéis e RLS dependem dele.",
            12, True, TXT, BODY, 1.1)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
notes(s, "Percorrer os 6 passos uma linha por vez. Deixar claro que o problema e de arquitetura, nao de digitacao. 1min05.")

# 8 - hierarquia
s = slide_new()
kicker(s, "FRENTE 2 · NEGOCIO", CYAN, w=2.5)
title(s, "A escada de acesso existe so no contrato", size=30)
req = panel(s, 0.5, 1.7, 6.0, 3.5, [
    "Visitante   ler loja, produto e comunidade; pedir credenciamento",
    "Usuario     perfil, pedidos, anuncios, denunciar e bloquear",
    "Vendedor    CRUD de loja e de anuncio, status de pedido",
    "Supervisor  lojas, produtos e pedidos do seu escopo - sem financeiro",
    "Admin       usuarios, aprovacao, roles, segredos e plataforma",
], head="HIERARQUIA EXIGIDA PELO TEMA", size=12, head_color=VIOLET, spc=1.42)
real = panel(s, 6.83, 1.7, 6.0, 3.5, [
    "4 papeis no codigo: visitor | user | seller | admin",
    "supervisor: zero ocorrencias em qualquer arquivo",
    "atleta: default de cadastro - papel que nao e da hierarquia",
    "'Lojista' existe so como vinculo stores.owner_id, nunca como papel",
    "Botoes administrativos de fachada: aparecem e fazem nada",
], head="O QUE O CODIGO TEM HOJE", size=12, head_color=CORAL, spc=1.42, fill=WHITE)
alert = box(s, 0.5, 5.4, 12.33, 0.62, fill=CORAL, radius=0.09)
put(alert, [("D-01 nao tem resposta da equipe - entao types.ts, migração e RLS continuam sem base para comecar.",
             12, True, TXT, BODY, 1.1)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
foot = box(s, 0.5, 6.2, 12.33, 0.5, fill=WHITE, line=HAIR, radius=0.1)
put(foot, [("Matriz-alvo com 26 capacidades ja escrita em docs/etapa-5/contratos/matriz-permissoes.md - e a base do lote B2.",
            11, True, SLATE, BODY, 1.1)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
notes(s, "Este slide justifica por que a frente 1 esta parada: falta decisao de negocio, nao codigo. 50s.")

# 9 - banco
s = slide_new()
kicker(s, "FRENTE 1 · BANCO, RLS E DADOS", LIME, w=3.0)
title(s, "O banco pergunta por uma tabela que nao existe", size=29)
items = [
    ("TABELAS", "users, products, stores, orders, community_posts. A unica migracao cria profiles - e nunca cria public.users.", CORAL_T),
    ("MIGRACOES", "1 arquivo em supabase/migrations; os 9 scripts avulsos em scripts/ nao criam as tabelas que as APIs leem.", WHITE),
    ("UPDATE", "profiles_update_policy aceita edicao de qualquer linha para is_admin(), sem WITH CHECK: admin pode escrever como outro usuario.", WHITE),
    ("INSERT", "Permite qualquer autenticado inserir profiles, sem checagem de auth.uid() = id.", WHITE),
    ("GRANTS", "GRANT ALL to anon e authenticated: qualquer pessoa sem login atinge as tabelas.", CORAL_T),
    ("RLS REAL", "Nao verificado: sem acesso ao banco do projeto, nao da para provar que as politicas estao ativas na base remota.", SLATE_T),
]
cards9 = []
for i, (head, text, fill) in enumerate(items):
    x = 0.5 + (i % 3) * 4.19
    y = 1.68 + (i // 3) * 2.0
    c = panel(s, x, y, 3.97, 1.86, [text], head=head, size=10.5, fill=fill,
              line=HAIR if fill == WHITE else fill, head_color=TXT, spc=1.2)
    cards9.append(c)
foot = box(s, 0.5, 5.85, 12.33, 0.85, fill=VIOLET_T, line=VIOLET_T, radius=0.06)
put(foot, [("Enquanto a API consultar public.users, o 500 de /api/products nao e detalhe de infraestrutura: e prova de que a camada de dados do tema nunca foi entregue.",
            12, True, TXT, BODY, 1.18),
           ("Correcao com escopo fechado: uma migracao incremental com users + RLS + WITH CHECK, testada em ambiente proprio.", 11, False, SLATE, BODY, 1.18)], space_after=4)
notes(s, "Aqui o discurso e curto: schema, migracao e RLS sao um trabalho so, e nenhum dos tres esta pronto. 55s.")

# 10 - fachada
s = slide_new()
kicker(s, "NEGOCIO COMO FACHADA", CORAL, w=2.6)
title(s, "A loja abre, mas nada fica no caixa", size=30)
blocks = [
    ("CATALOGO", [
        "GET /api/products existe e faz SQL - mas o 500 aciona o fallback INITIAL_PRODUCTS",
        "POST /api/products grava no Supabase sem conferir papel, preco ou dono",
        "Server Actions confiam no userId vindo do cliente: um POST pode virar admin",
        "Resultado: a vitrine nunca aparece vazia, mas nao reflete o banco",
    ], WHITE),
    ("CHECKOUT", [
        "PIX gerado com Math.random(): copia a chave da loja e marca paid (orderService.ts:7-20)",
        "QR e imagem do api.qrserver.com com texto arbitrario; modal diz custodia segura",
        "Aprovado no sandbox grava payment_status completed direto no estado do navegador",
        "Ordens nunca passam por app/api/orders nem por Server Action - nem viram pedido de verdade",
    ], WHITE),
    ("VERIFICACAO", [
        "Solicitar verificacao chama requestVerification e escreve rejected - sem Admin, motivo ou prazo",
        "A interface continua mostrando pending: o usuario le algo que o codigo ja negou",
        "Aprovacao de loja nao existe em nenhum endpoint",
    ], CORAL_T),
    ("COMUNIDADE", [
        "Postar e denunciar escrevem so no estado local; ao recarregar, o conteudo desaparece",
        "Bloquear so esconde em quem bloqueou - nao impede nova denuncia no backend",
        "CRUD e moderacao comunitaria: simplesmente nao ha",
    ], CORAL_T),
]
cards10 = []
for i, (head, lines, fill) in enumerate(blocks):
    x = 0.5 + (i % 2) * 6.33
    y = 1.68 + (i // 2) * 2.15
    c = panel(s, x, y, 6.0, 2.0, lines, head=head, size=10.5, fill=fill,
              line=HAIR if fill == WHITE else fill, head_color=CORAL, spc=1.16)
    cards10.append(c)
foot = box(s, 0.5, 6.0, 12.33, 0.72, fill=INK, radius=0.06)
put(foot, [("Corrigir a aparencia da interface e o passo mais atrasado aqui: primeiro o contrato, depois os endpoints, depois a tela. O contrato de catalogo nem foi escrito ainda.",
            11.5, True, WHITE, BODY, 1.16),
           ("Bloco exige o contrato aprovado para que a interface pare de mentir sobre o que aconteceu.", 10.5, False, SLATE_T, BODY, 1.12)], space_after=4)
notes(s, "Nao prometer 'so falta mexer na aparencia': o negocio depende do contrato de catalogo, que ainda nao existe. 55s.")

# 11 - frontend
s = slide_new()
kicker(s, "FRONTEND, UX E ACESSIBILIDADE", AMBER, w=3.0)
title(s, "Uma tela faz o papel do aplicativo inteiro", size=29)
big = panel(s, 0.5, 1.68, 7.2, 4.15, [
    "① Menu que nao leva a lugar nenhum: 'Meu perfil' abre 'Paginas proximas' e a newsletter do rodape nao faz nada",
    "② Um app de uma tela so: app/page.tsx alterna as 26 visoes por switch em activeView; o login e um modal - nada tem URL, historico ou deep link",
    "③ Identidade no navegador: supabase-auth.ts esta morto (0 importadores) e o 'Mestre Admin' entra com um clique no painel",
    "④ Admin para quem quiser: Sidebar expoe o seletor 'Modo' a qualquer visitante e o atalho de Acesso Rapido a Admin",
], head="AS QUATRO RAIZES DO PROBLEMA", size=11.5, head_color=AMBER, spc=1.3)
side11 = []
for i, (head, text, fill) in enumerate([
    ("ESTADOS", "Sem vazio, carregando, erro e negado: a tela cheia de dados e o fallback INITIAL_* quando a API falha. loading e error coexistem no store sem render.", WHITE),
    ("UX MORRENDO", "SmartScanView.tsx (356 linhas) sem importador; components/ui/* sem uso; subpastas que so reexportam; GEMINI_API_KEY no .env.example sem uso real.", WHITE),
    ("QUALIDADE VISUAL", "Zero capturas, nenhum teste de teclado, foco/Escape confirmado; responsivo e a11y sem medicao - NAO VERIFICADO nao e reprovado.", SLATE_T),
]):
    c = panel(s, 7.95, 1.68 + i * 1.42, 4.88, 1.3, [text], head=head, size=10, fill=fill,
              line=HAIR if fill == WHITE else fill, head_color=TXT, spc=1.16)
    side11.append(c)
foot = box(s, 0.5, 6.0, 12.33, 0.72, fill=SLATE_T, radius=0.06)
put(foot, [("Ordem de recuperacao: rota e URL reais → estados de loading/vazio/erro/acesso negado → remover demo, Modo e o seletor de perfil → so entao o design system do guia.",
            11.5, True, TXT, BODY, 1.16), ("Os quatro itens do guia (grafias, acentos, termos e nomes das entidades) continuam sem verificacao de nenhum tipo.",
                                           10.5, False, SLATE, BODY, 1.12)], space_after=4)
notes(s, "Puxar o seletor 'Modo' porque qualquer visitante consegue entrar como Admin sem senha. 50s.")

# 12 - contagem
s = slide_new(dark=True)
kicker(s, "QUANTO FALTA", LIME, w=2.0)
title(s, "76 lacunas catalogadas, 0 concluidas", size=30, on_dark=True)
bars = mono_panel(s, 0.5, 1.75, 7.2, 4.1, [
    "Frente 1 · identidade e acesso   13 █████████████",
    "Frente 4 · testes e entrega      11 ███████████",
    "Contratos e decisoes             11 ███████████",
    "Frente 2 · negocio e catalogo    10 ██████████",
    "Frente 3 · TCC e diagramas        10 ██████████",
    "Dados academicos                  10 ██████████",
    "Higiene de repositorio              8 ████████",
    "Bloqueadores P0                     3 ███",
    "",
    "FALTA 46 · PARCIAL 6 · PENDENTE 22 · BLOQUEADO 2",
    "+6 verificacoes NAO VERIFICADO (fora da contagem)",
], fill=WHITE, line=WHITE, size=11.5)
why = panel(s, 7.95, 1.75, 4.88, 4.1, [
    "A contagem e por leitura do repositorio, nao por impressao: cada item aponta arquivo e linha (ou a ausencia do arquivo).",
    "O bloco mais cheio e o de identidade - porque dele dependem negocio, comunidade, checkout e entrega.",
    "Nenhum item esta marcado como concluido; o que passou em teste virou PARCIAL, nunca FEITO.",
], head="COMO LER", size=11.5, fill=LIME, line=LIME, head_color=TXT, spc=1.24)
notes(s, "Numero-chave para a banca: 76 lacunas, 62 com dono e prazo possivel. A lista integral esta no repositorio. 45s.")

# 13 - decisoes e dados
s = slide_new()
kicker(s, "O QUE SO A EQUIPE RESPONDE", CYAN, w=3.0)
title(s, "Onze decisoes travadas, dez dados ausentes", size=28)
dec = panel(s, 0.5, 1.68, 6.0, 4.3, [
    "D-01  Lojista e papel de acesso ou vinculo com a loja?",
    "D-02  Supervisor e Admin podem criar loja?",
    "D-03  Quem aprova a verificacao de loja?",
    "D-04  Supervisor pode banir conta?",
    "D-05  Supervisor ve a lista de usuarios - e quais campos?",
    "D-06  Supervisor ve ou edita pedidos?",
    "D-07  Admin ve financeiro por loja ou agregado?",
    "D-08  Quem administra segredos de integracao?",
    "D-09  Como isolar o modo demo: flag, rota ou remover?",
    "D-10  Admin pode se rebaixar ou se excluir?",
    "D-11  Publicar contrato-catalogo.md antes de codar",
], head="DECISOES DA MATRIZ (rascunho, sem ata)", size=11, head_color=VIOLET, spc=1.2)
dat = panel(s, 6.83, 1.68, 6.0, 4.3, [
    "A-01  Grafia oficial: CoreMotion, CoreMotiom ou Core Motiom?",
    "A-02  Nomes completos dos quatro integrantes",
    "A-03  Instituicao, curso, cidade e periodo reais",
    "A-04  Orientador e coorientador",
    "A-05  Banca, data de defesa e conceito (nao fabricar)",
    "A-06  Prazo, duracao da defesa e formato dos links",
    "A-07  'Apenas no github.com': codigo, demo ou ambos?",
    "A-08  Autorizacao para rotacionar, limpar historico e publicar",
    "A-09  Segundo PDF de requisitos, se existir",
    "A-10  Consentimento para usar imagens reais da equipe",
    "Folha de aprovacao fica em branco ate a banca existir.",
], head="DADOS QUE NINGUEM PODE PRESUMIR", size=11, head_color=CORAL, spc=1.24, fill=VIOLET_T, line=VIOLET_T)
foot = box(s, 0.5, 6.15, 12.33, 0.6, fill=INK, radius=0.09)
put(foot, [("Nada aqui trava as outras frentes: registre PENDENTE, siga pelo contrato publicado e volte na decisao quando a equipe bater o martelo.",
            11.5, True, WHITE, BODY, 1.1)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
notes(s, "Pedir explicitamente 15 minutos de reuniao para D-01 e a grafia oficial: sao as duas que seguram mais trabalho. 50s.")

# 14 - ordem de execucao
s = slide_new()
kicker(s, "ORDEM DE EXECUCAO", VIOLET, w=2.4)
title(s, "Sete passos - e nada de corrigir antes da lista", size=29)
steps14 = [
    "1 · Rotacionar a credencial no Supabase  →  acao humana, sem isso nada se resolve",
    "2 · Helper de sessao e autorizacao em todas as rotas  →  lote B1",
    "3 · Papeis, migracao incremental e RLS  →  B2 e B3, depois de D-01 a D-10",
    "4 · Remover demo, localStorage e o fallback INITIAL_*  →  F0 e F2",
    "5 · Verificacao de loja, checkout e estados de UI  →  F1 e F3",
    "6 · Ambiente de teste, plano, execucao, relatorio e README  →  frente 4",
    "7 · TCC, diagramas, Daily, slides e links  →  frente 3 e fechamento",
]
big = box(s, 0.5, 1.68, 7.6, 4.3, fill=WHITE, line=HAIR, radius=0.05)
put(big, [(txt, 13.5, i in (0, 1, 6), TXT, BODY, 1.14) for i, txt in enumerate(steps14)], space_after=13)
big.text_frame.margin_left = Emu(int(0.22 * EMU_IN))
big.text_frame.margin_top = Emu(int(0.18 * EMU_IN))
rules = [
    ("ANTES DO PUSH", "Nenhum commit novo enquanto a senha antiga valer; nenhum arquivo de codigo tocado nesta rodada.", CORAL_T),
    ("DURANTE A RODADA", "Cada frente roda lint, type-check e build e registra comando, resultado e limitacao na propria pasta.", LIME),
    ("ANTES DA DEFESA", "README reproduzido em ambiente limpo, links abertos em janela anonima e TCC conferido contra o modelo.", WHITE),
]
cards14 = []
for i, (head, text, fill) in enumerate(rules):
    c = panel(s, 8.35, 1.68 + i * 1.47, 4.48, 1.36, [text], head=head, size=10.5, fill=fill,
              line=HAIR if fill == WHITE else fill, head_color=TXT, spc=1.16)
    cards14.append(c)
foot = box(s, 0.5, 6.15, 12.33, 0.6, fill=SLATE_T, radius=0.09)
put(foot, [("Cada item da lista tem dono, criterio de aceite e evidencia em docs/etapa-5/PENDENCIAS-E-LACUNAS.md.",
            11.5, True, TXT, BODY, 1.1)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
notes(s, "Fechar com a sequencia: seguranca primeiro, contrato depois, interface por ultimo. 1min.")

# 15 - animacoes
s = slide_new()
kicker(s, "ANIMACOES E TRANSICOES", CORAL, w=2.7)
title(s, "O movimento que a API nao escreve - e como obte-lo", size=27)
lim = panel(s, 0.5, 1.68, 5.4, 4.2, [
    "Formas, cores, opacidade, transformacoes, texto, tabelas, video, z-order e fundo: tudo isso o Google Slides API grava - e foi assim que este deck nasceu.",
    "Transicao de slide e animacao de objeto nao tem request correspondente na API v1 (nem no Apps Script).",
    "Por isso nada foi inventado nem simulado: as animacoes deste PPTX foram gravadas direto no XML da apresentacao.",
], head="O QUE A API EXPOE", size=11, head_color=CORAL, spc=1.24)
rec = panel(s, 6.1, 1.68, 6.73, 4.2, [
    "1 · Este arquivo: transicoes por slide (Fade, Push, Morph) e entrada por paragrafo a cada clique - definidas no XML.",
    "2 · No Google Slides: Transicoes → Esmaecer 0,6s → Aplicar a todos os slides (2 min, manual).",
    "3 · Efeito Morph no Slides: duplicar slide, mover as mesmas formas e escolher Dinamico.",
    "4 · Animacao por bloco: menu Animacao → Por objeto → Esmaecer 0,4s.",
    "5 · Atencao: importar PPTX para o Slides costuma descartar animacoes; apresente no PowerPoint Online para preserva-las.",
], head="COMO DAR MOVIMENTO", size=11, head_color=VIOLET, spc=1.2, fill=LIME, line=LIME)
foot = box(s, 0.5, 6.15, 12.33, 0.6, fill=WHITE, line=HAIR, radius=0.09)
put(foot, [("Regra do guia que continua valendo: movimento e estetica, nao evidencia. Nenhum slide deste deck afirma que algo esta concluido.",
            11.5, True, TXT, BODY, 1.1)], anchor=MSO_ANCHOR.MIDDLE, space_after=0)
notes(s, "Explicar o motivo tecnico do pedido (a API nao expoe transicoes) e mostrar o efeito ao vivo, clicando. 45s.")

# 16 - encerramento
s = slide_new(dark=True)
box(s, -1.8, 2.2, 5.2, 5.2, fill=LIME)
kicker(s, "PROXIMO LOTE", LIME, w=2.2)
title(s, "Documentado, nada corrigido - e assim que comeca", size=29, on_dark=True)
fin = [
    ("1 · QUEM TEM ACESSO AO SUPABASE", "Rotacionar a senha do banco, revisar logs desde 16/10, mover DATABASE_URL para variavel de ambiente e confirmar para a equipe.", AMBER),
    ("2 · QUEM ASSINA O TCC", "Registrar D-01 a D-11 em ata, decidir a grafia oficial e fornecer nomes, instituicao, periodo e orientador.", WHITE),
    ("3 · O QUE O ARENA PODE FAZER JA", "Executar o lote B1 (sessao e autorizacao) e abrir os capitulos do TCC com PENDENTE onde faltar dado.", LIME),
]
cards16 = []
for i, (head, text, fill) in enumerate(fin):
    c = box(s, 0.5 + i * 4.19, 2.0, 3.97, 1.95, fill=fill, radius=0.06)
    put(c, [(head, 10.5, True, TXT, MONO, 1.12), (text, 11.5, False, TXT, BODY, 1.26)], space_after=7)
    cards16.append(c)
close = box(s, 0.5, 4.35, 12.33, 1.15, fill=VIOLET_T, radius=0.06)
put(close, [("Retrato do projeto em 19/10/2026 · commit b0827ec · 76 lacunas com arquivo e linha em docs/etapa-5/PENDENCIAS-E-LACUNAS.md",
             13, True, TXT, BODY, 1.16),
            ("Nada neste deck foi corrigido no codigo: e o ponto de partida para a equipe decidir - e so depois tocar em app/, components/, lib/, services/ ou supabase/.",
             11.5, False, SLATE, BODY, 1.2)], anchor=MSO_ANCHOR.MIDDLE, space_after=6)
foot = box(s, 0.5, 5.75, 12.33, 0.9)
put(foot, [("COREMOTIOM · ETAPA 5", 13, True, LIME, MONO, 1.0),
           ("Obrigatoriedade do TCC: autenticacao e autorizacao por perfis · CRUD de lojas e produtos · checkout · comunidade moderada.",
            11.5, False, SLATE_T, BODY, 1.16),
           ("Obrigado.", 16, True, WHITE, DISPLAY, 1.0)], space_after=4)
notes(s, "Encerrar com a decisao que libera o resto: rotacionar a credencial e bater D-01. 30s.")



# ------------------------------------------------------- portugues: acentuacao
# O conteudo e escrito em ASCII no corpo do script; este passe devolve os acentos.
ACCENT = {
    "nao": "não", "ha": "há", "ja": "já", "ate": "até", "tres": "três", "alem": "além",
    "usuario": "usuário", "usuarios": "usuários", "possivel": "possível", "possiveis": "possíveis",
    "sao": "são", "so": "só", "le": "lê", "la": "lá", "mes": "mês",
    "ultima": "última", "ultimo": "último", "ultimas": "últimas", "ultimos": "últimos",
    "unica": "única", "unico": "único", "unicos": "únicos", "saida": "saída", "saidas": "saídas",
    "publica": "pública", "publico": "público", "rapida": "rápida", "rapido": "rápido",
    "proxima": "próxima", "proximo": "próximo", "proximas": "próximas", "proximos": "próximos",
    "pagina": "página", "paginas": "páginas", "codigo": "código", "historico": "histórico",
    "historia": "história", "numero": "número", "criterio": "critério", "criterios": "critérios",
    "periodo": "período", "video": "vídeo", "videos": "vídeos", "grafico": "gráfico",
    "graficos": "gráficos", "politica": "política", "politicas": "políticas",
    "anonima": "anônima", "anonimo": "anônimo", "dinamico": "dinâmico",
    "automatica": "automática", "automatico": "automático", "papel": "papel", "papeis": "papéis",
    "anuncio": "anúncio", "anuncios": "anúncios", "custodia": "custódia",
    "denuncia": "denúncia", "denuncias": "denúncias", "preco": "preço", "precos": "preços",
    "propria": "própria", "proprio": "próprio", "proprias": "próprias", "proprios": "próprios",
    "conteudo": "conteúdo", "conteudos": "conteúdos", "ocorrencia": "ocorrência",
    "ocorrencias": "ocorrências", "vinculo": "vínculo", "vinculos": "vínculos",
    "duracao": "duração", "instituicao": "instituição", "reuniao": "reunião",
    "participacao": "participação", "estao": "estão", "suposicao": "suposição",
    "documentacao": "documentação", "implementacao": "implementação",
    "entregavel": "entregável", "entregaveis": "entregáveis", "relatorio": "relatório",
    "relatorios": "relatórios", "repositorio": "repositório", "inventario": "inventário",
    "limitacao": "limitação", "evidencia": "evidência", "evidencias": "evidências",
    "recuperacao": "recuperação", "integracao": "integração", "correcao": "correção",
    "entao": "então", "secoes": "seções", "secao": "seção", "comeca": "começa",
    "comecar": "começar", "comecam": "começam", "padrao": "padrão", "producao": "produção",
    "moderacao": "moderação", "arbitrario": "arbitrário", "arbitraria": "arbitrária",
    "paragrafo": "parágrafo", "paragrafos": "parágrafos", "botoes": "botões", "botao": "botão",
    "funcao": "função", "funcoes": "funções", "expoe": "expõe", "concluido": "concluído",
    "concluida": "concluída", "concluidos": "concluídos", "concluidas": "concluídas",
    "capitulo": "capítulo", "capitulos": "capítulos", "academico": "acadêmico",
    "academica": "acadêmica", "academicos": "acadêmicos", "definicao": "definição",
    "orientacao": "orientação", "organizacao": "organização", "organisacao": "organização",
    "tambem": "também", "ninguem": "ninguém", "sairam": "saíram", "dificil": "difícil",
    "aparencia": "aparência", "diferenca": "diferença", "referencia": "referência",
    "experiencia": "experiência", "metodo": "método", "metodos": "métodos", "nucleo": "núcleo",
    "modulo": "módulo", "modulos": "módulos", "area": "área", "areas": "áreas", "serie": "série",
    "especifico": "específico", "especificos": "específicos", "versao": "versão",
    "versoes": "versões", "medicao": "medição", "impressao": "impressão",
    "transformacao": "transformação", "transformacoes": "transformações",
    "exposicao": "exposição", "consequencia": "consequência", "ausencia": "ausência",
    "seguranca": "segurança", "superficie": "superfície", "edicao": "edição", "acao": "ação",
    "acoes": "ações", "aplicacao": "aplicação", "apresentacao": "apresentação",
    "autenticacao": "autenticação", "autorizacao": "autorização", "verificacao": "verificação",
    "verificacoes": "verificações", "aprovacao": "aprovação", "execucao": "execução",
    "execucoes": "execuções", "sessao": "sessão", "sessoes": "sessões", "decisao": "decisão",
    "decisoes": "decisões", "migracao": "migração", "migracoes": "migrações",
    "animacao": "animação", "animacoes": "animações", "transicao": "transição",
    "transicoes": "transições", "negocio": "negócio", "negocios": "negócios",
    "catalogo": "catálogo", "catalogos": "catálogos", "pendencia": "pendência",
    "pendencias": "pendências", "favoravel": "favorável", "favoraveis": "favoráveis",
    "tecnico": "técnico", "tecnico1": "técnica", "tecnicos": "técnicos", "tecnica": "técnica",
    "sequencia": "sequência", "confianca": "confiança", "rodape": "rodapé", "raiz": "raiz",
    "raizes": "raízes", "visao": "visão", "visoes": "visões", "invalida": "inválida",
    "invalido": "inválido", "continuacao": "continuação", "revogacao": "revogação",
    "comunitario": "comunitário", "comunitaria": "comunitária", "estetica": "estética",
    "atencao": "atenção", "avancado": "avançado", "avancada": "avançada", "avancados": "avançados",
    "regra": "regra", "grifo": "grifo", "proposito": "propósito", "artigo": "artigo",
    "rotulo": "rótulo", "sitio": "sítio", "publicacao": "publicação", "licitacao": "licitação",
    "declaracao": "declaração", "explicacao": "explicação", "distribuicao": "distribuição",
    "instrucao": "instrução", "obrigacao": "obrigação", "posicao": "posição",
    "comissao": "comissão", "discussao": "discussão", "profissao": "profissão",
    "excecao": "exceção", "licao": "lição", "licoes": "lições", "senso": "senso",
    "digitacao": "digitação", "capacidade": "capacidade", "capacidades": "capacidades",
    "resposta": "resposta", "desempenho": "desempenho", "empenho": "empenho",
    "comportamento": "comportamento", "armazenamento": "armazenamento",
}

# Correcoes finas: casos em que a troca cega de token sairia errada.
PHRASES = [
    ("não da para provar", "não dá para provar"),
    ("Nada e declarado", "Nada é declarado"),
    ("movimento e estética", "movimento é estética"),
    ("A contagem e por leitura", "A contagem é por leitura"),
    ("mais cheio e o de identidade", "mais cheio é o de identidade"),
    ("não e detalhe de infraestrutura: e prova de que", "não é detalhe de infraestrutura: é prova de que"),
    ("interface e o passo mais atrasado", "interface é o passo mais atrasado"),
    ("e o ponto de partida para a equipe", "é o ponto de partida para a equipe"),
    ("e assim que comeca", "é assim que começa"),
    ("papel que nao e da hierarquia", "papel que não é da hierarquia"),
    ("Lojista e papel de acesso", "Lojista é papel de acesso"),
    ("o login e um modal", "o login é um modal"),
    ("nao e reprovado", "não é reprovado"),
    ("problema e de arquitetura", "problema é de arquitetura"),
    ("discurso e curto", "discurso é curto"),
    ("e o unico item", "é o único item"),
    ("esta ausente", "está ausente"),
    ("esta provado", "está provado"),
    ("esta escrito", "está escrito"),
    ("esta atendido", "está atendido"),
    ("esta concluído", "está concluído"),
    ("esta mais", "está mais"),
    ("esta no repositorio", "está no repositório"),
    ("esta parada", "está parada"),
    ("esta pronto", "está pronto"),
    ("contem apenas README", "contêm apenas README"),
    ("aplicacao trusts role", "aplicação confia em role"),
    ("estao hardcoded em", "estão fixados no código em"),
    ("hardcoded em lib/db.ts", "fixados no código em lib/db.ts"),
    ("como obte-lo", "como obtê-lo"),
    ("para preserva-las", "para preservá-las"),
    ("COMO VIRA ESCRITA", "COMO O PADRÃO VIRA REGRA"),
    ("esta morto", "está morto"),
    ("esta marcado", "está marcado"),
    ("esta no repositório", "está no repositório"),
    ("O QUE ESTA EXPOSTO", "O QUE ESTÁ EXPOSTO"),
    (" - ", " — "),
]


def accentuate(text: str) -> str:
    def sub(m):
        w = m.group(0)
        rep = ACCENT.get(w.lower())
        if not rep:
            return w
        if w.isupper():
            return rep.upper()
        if w[:1].isupper():
            rep = rep[:1].upper() + rep[1:]
        return rep
    text = re.sub(r"\b[A-Za-z]+\b", sub, text)
    for src, dst in PHRASES:
        text = text.replace(src, dst)
    return text


def _apply_accents(prs):
    for sl in prs.slides:
        for sh in sl.shapes:
            if not sh.has_text_frame:
                continue
            for para in sh.text_frame.paragraphs:
                for run in para.runs:
                    run.text = accentuate(run.text)
        if sl.has_notes_slide:
            for para in sl.notes_slide.notes_text_frame.paragraphs:
                for run in para.runs:
                    run.text = accentuate(run.text)


# ------------------------------------------------- transicoes + animacoes (XML)
TRANSITIONS = ["fade", "morph", "fade", "push", "fade", "wipe", "fade", "push", "fade", "push",
               "fade", "morph", "fade", "push", "fade", "fade"]

# spids que entram a cada clique (painéis de conteúdo); título/kicker ficam fixos
def collect(slide):
    """ids dos shapes que devem entrar com animacao (pula kicker e titulo)."""
    ids = [sh.shape_id for sh in slide.shapes]
    return ids[2:] if len(ids) > 3 else ids


for idx, sl in enumerate(prs.slides):
    set_transition(sl, TRANSITIONS[idx % len(TRANSITIONS)], dur=650)
    ids = collect(sl)
    set_timing(sl, click_shapes=ids[:6])

_apply_accents(prs)
out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/deck.pptx"
prs.save(out)
print("salvo em %s · %d slides" % (out, len(prs.slides._sldIdLst)))
