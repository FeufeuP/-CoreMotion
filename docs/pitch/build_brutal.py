"""CoreMotion — deck de pitch no tema neo-brutalista (tokens do TweakCN).

Branco puro, preto, primary #FF3333, secondary #FFFF00, accent #0066FF,
cantos retos, sombras duras de 4px e DM Sans + Space Mono.
"""
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from brutal_lib import *          # noqa
from deck_lib import animate, transition

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)


def blank(dark=False):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = D_BG if dark else BG
    return s


def card(s, x, y, w, h, fill=WHITE, lw=2.2, shadow_px=6):
    return box(s, x, y, w, h, fill=fill, border=INK, lw=lw,
               shadow=True, shadow_px=shadow_px)


# =====================================================================
# 01 — CAPA
# =====================================================================
s = blank()
art = []
art.append(box(s, 8.45, 1.10, 4.35, 4.35, fill=PRIMARY, border=INK, lw=3,
               kind="oval", shadow=True, shadow_px=9))
# check preto
art.append(box(s, 10.05, 3.02, 0.16, 0.62, fill=WHITE, border=None,
               shadow=False, rot=-45))
art.append(box(s, 10.40, 2.60, 0.16, 1.12, fill=WHITE, border=None,
               shadow=False, rot=45))
art.append(box(s, 11.62, 4.72, 1.28, 1.28, fill=ACCENT, border=INK, lw=2.5,
               rot=12, shadow=True, shadow_px=7))
art.append(box(s, 7.62, 4.72, 1.18, 1.02, fill=SECONDARY, border=INK, lw=2.5,
               kind="tri", shadow=True, shadow_px=7))
art.append(box(s, 9.28, 6.18, 0.52, 0.52, fill=GREEN, border=INK, lw=2.2,
               shadow=True, shadow_px=5))
art.append(box(s, 12.28, 1.02, 0.86, 0.86, fill=MAGENTA, border=INK, lw=2.2,
               kind="star", shadow=True, shadow_px=5))

chip1 = sticker(s, 10.22, 1.34, 2.30, 0.38, "LOJAS VERIFICADAS", WHITE,
                color=INK, size=7.4, spc=1.4, dot=GREEN)
chip2 = sticker(s, 7.55, 3.46, 1.62, 0.38, "CUSTÓDIA", ACCENT, color=WHITE,
                size=7.4, spc=1.4)
chip3 = sticker(s, 11.58, 4.18, 0.85, 0.38, "C2C", SECONDARY, color=INK,
                size=7.4, spc=1.4)

kick = sticker(s, 0.78, 1.62, 2.55, 0.40, "PITCH · BANCA 2026", SECONDARY,
               color=INK, size=7.6, spc=1.6, shadow_px=6)
brand = text(s, 0.78, 2.14, 7.0, 1.25, "CoreMotion", size=80, color=INK,
             bold=True, spc=-2.6, line=0.9)
under = box(s, 0.84, 3.34, 1.85, 0.11, fill=PRIMARY, border=None, shadow=False)
lead = text(s, 0.78, 3.66, 6.7, 1.30,
            ["O ponto de encontro", ("do esporte de alta performance.", {"bold": True})],
            size=21, color=INK, line=1.22, spc=-0.4)
meta = mono(s, 0.78, 5.14, 6.7, 0.22,
            "MARKETPLACE · LOJAS VERIFICADAS · CUSTÓDIA", size=8, color=INK_SOFT,
            spc=1.8)
foot = box(s, 0.78, 6.30, 6.55, 0.50, fill=INK, border=INK, lw=2,
           shadow=True, shadow_px=6)
foot_t = mono(s, 0.98, 6.30, 6.2, 0.50, "APRESENTADO POR [SEU NOME] · [CIDADE], 2026",
              size=7.6, color=WHITE, spc=1.2, anchor="m")

animate(s, cascade(art, 0, 90, "zoom", 650) +
        [(chip1, "drop", 260, 480), (chip2, "left", 340, 480),
         (chip3, "left", 420, 480), (kick, "fade", 120, 400),
         (brand, "rise", 180, 680), (under, "wipe", 420, 450),
         (lead, "rise", 480, 600), (meta, "fade", 700, 420),
         (foot, "rise", 800, 500), (foot_t, "fade", 900, 450)])
transition(s, "fade")
notes(s, (
    "ABERTURA (30s).\n"
    "• Meu nome é [nome] e o CoreMotion é um marketplace esportivo com lojas "
    "verificadas, venda entre atletas e custódia financeira.\n"
    "• A frase-guia: comprar esporte hoje é um ato de fé; o produto transforma "
    "confiança em fluxo.\n"
    "• Prometer 15 minutos e seguir a agenda."
))
chrome(s, 1, "Capa")

# =====================================================================
# 02 — AGENDA
# =====================================================================
s = blank()
head = title_block(s, "AGENDA", "O caminho",
                   "Quinze minutos, quatro blocos. Sem slide de história da empresa.")
AGENDA = [
    ("01", "O problema", "Por que comprar e vender esporte ainda é inseguro.", PRIMARY),
    ("02", "A solução", "As três camadas que fazem o CoreMotion funcionar.", SECONDARY),
    ("03", "O negócio", "Como a plataforma ganha dinheiro e escala.", ACCENT),
    ("04", "A entrega", "Onde estamos e o que precisamos de você.", GREEN),
]
ag = []
for i, (num, nm, ds, col) in enumerate(AGENDA):
    x = 0.78 + i * 3.00
    c = card(s, x, 2.80, 2.78, 3.32)
    sq = box(s, x + 0.28, 3.08, 0.82, 0.82, fill=col, border=INK, lw=2.2,
             shadow=True, shadow_px=4)
    n = mono(s, x + 0.28, 3.08, 0.82, 0.82, num, size=22, color=INK, spc=0.5,
             align="c", anchor="m")
    t = text(s, x + 0.28, 4.16, 2.25, 0.62, nm, size=17.5, color=INK,
             bold=True, spc=-0.4, line=1.02)
    d = text(s, x + 0.28, 4.86, 2.22, 0.95, ds, size=10.5, color=INK_SOFT,
             line=1.35)
    ar = box(s, x + 2.20, 5.72, 0.24, 0.24, fill=INK, border=None,
             kind="tri", rot=90, shadow=False)
    ag += [c, sq, n, t, d, ar]

tag = sticker(s, 9.35, 6.42, 3.18, 0.36, "PITCH PARA BANCA · COREMOTION 2026",
              SECONDARY, color=INK, size=6.8, spc=1.2, shadow_px=5)
animate(s, cascade(head, 60, 100, "rise", 520) +
        cascade(ag, 340, 55, "rise", 480) + [(tag, "fade", 980, 400)])
transition(s, "push")
notes(s, (
    "AGENDA (45s).\n"
    "• Quatro blocos. O primeiro é o mais importante: o problema.\n"
    "• Se o tempo apertar, cortamos o bloco 3 e mantemos problema, solução e pedido."
))
chrome(s, 2, "Agenda")

# =====================================================================
# 03 — PROBLEMA
# =====================================================================
s = blank()
head = title_block(s, "O PROBLEMA", "Comprar esporte ainda é um ato de fé.")
PROB = [
    ("Falsificação", "Réplica vendida como original. Sem verificação de loja, de catálogo ou de histórico.", PRIMARY, "oval"),
    ("Dinheiro exposto", "Pix direto para o vendedor: se a peça não chega, o prejuízo inteiro é do atleta.", SECONDARY, "tri"),
    ("Atleta invisível", "Quem vende usado não tem canal confiável. Quem procura não sabe em quem confiar.", ACCENT, "diamond"),
]
pb = []
for i, (nm, ds, col, icon) in enumerate(PROB):
    x = 0.78 + i * 4.02
    c = card(s, x, 2.72, 3.72, 3.28)
    bar = box(s, x, 2.72, 3.72, 0.18, fill=col, border=INK, lw=2.2,
              shadow=False)
    isq = box(s, x + 0.30, 3.14, 0.98, 0.98, fill=col, border=INK, lw=2.2,
              shadow=True, shadow_px=4)
    ivl = {"oval": 0.42, "tri": 0.50, "diamond": 0.44}[icon]
    ic = box(s, x + 0.30 + (0.98 - ivl) / 2, 3.14 + (0.98 - ivl) / 2, ivl, ivl,
             fill=INK, border=None, kind=icon, shadow=False)
    t = text(s, x + 0.30, 4.38, 3.05, 0.42, nm, size=18, color=INK, bold=True,
             spc=-0.4)
    d = text(s, x + 0.30, 4.90, 3.05, 0.95, ds, size=10.5, color=INK_SOFT,
             line=1.35)
    pb += [c, bar, isq, ic, t, d]

band = box(s, 0.78, 6.24, 11.77, 0.56, fill=INK, border=INK, lw=2,
           shadow=True, shadow_px=6)
bt = mono(s, 1.02, 6.24, 11.2, 0.56,
          "O atleta compra no escuro. A loja vende sem alcance. O dinheiro fica no meio.",
          size=9.5, color=WHITE, spc=0.6, anchor="m")

animate(s, cascade(head, 60, 100, "rise", 520) +
        cascade(pb, 300, 55, "rise", 500) +
        [(band, "zoom", 900, 550), (bt, "fade", 1000, 450)])
transition(s, "fade")
notes(s, (
    "PROBLEMA (2min).\n"
    "• Conte um caso concreto de compra frustrada, se tiver.\n"
    "• As três dores: falsificação, dinheiro exposto, atleta sem canal.\n"
    "• Fechamento: o problema não é oferta, é confiança."
))
chrome(s, 3, "O problema")

# =====================================================================
# 04 — POR QUE AGORA
# =====================================================================
s = blank()
head = title_block(s, "POR QUE AGORA", "Três mudanças abriram essa janela.",
                   "O mercado não precisa de mais um catálogo. Precisa de confiança.")
ROWS = [
    ("01", "O esporte virou consumo de identidade",
     "Equipamento deixou de ser acessório: é pertencimento, performance e status.", PRIMARY),
    ("02", "O atleta virou mídia e canal",
     "Comunidades e redes criam demanda qualificada todos os dias, de graça.", ACCENT),
    ("03", "O pagamento amadureceu",
     "Pix, verificação digital e custódia permitem segurar o valor até a entrega.", GREEN),
]
rw = []
for i, (num, nm, ds, col) in enumerate(ROWS):
    y = 2.72 + i * 1.24
    n = box(s, 0.78, y, 0.60, 0.60, fill=col, border=INK, lw=2.0,
            shadow=True, shadow_px=4)
    nt = mono(s, 0.78, y, 0.60, 0.60, num, size=10.5, color=INK, spc=0.6,
              align="c", anchor="m")
    t = text(s, 1.58, y - 0.02, 5.5, 0.34, nm, size=15.5, color=INK, bold=True,
             spc=-0.3)
    d = text(s, 1.58, y + 0.36, 5.45, 0.55, ds, size=10.5, color=INK_SOFT,
             line=1.3)
    rw += [n, nt, t, d]

# gráfico de barras
chart = []
base_y = 5.86
chart.append(box(s, 7.35, base_y, 5.15, 0.04, fill=INK, border=None,
                 shadow=False))
BARS = [(1.05, PRIMARY), (1.62, SECONDARY), (2.18, ACCENT), (2.78, GREEN)]
for i, (h, col) in enumerate(BARS):
    chart.append(box(s, 7.62 + i * 1.18, base_y - h, 0.92, h, fill=col,
                     border=INK, lw=2.2, shadow=True, shadow_px=6))
cap = sticker(s, 7.35, 6.18, 3.95, 0.38, "CONFIANÇA É O GARGALO", SECONDARY,
              color=INK, size=7.6, spc=1.4, shadow_px=5)

animate(s, cascade(head, 60, 100, "rise", 520) +
        cascade(rw, 300, 60, "rise", 480) +
        [(chart[0], "wipe", 620, 600)] +
        [(b, "wipeup", 720 + i * 90, 620) for i, b in enumerate(chart[1:])] +
        [(cap, "zoom", 1150, 450)])
transition(s, "wipe")
notes(s, (
    "POR QUE AGORA (1min30).\n"
    "• Três mudanças estruturais — não é tendência passageira.\n"
    "• Se perguntarem de dados: o deck evita número de mercado sem fonte; "
    "ofereça o recorte do seu nicho."
))
chrome(s, 4, "Por que agora")

# =====================================================================
# 05 — SOLUÇÃO
# =====================================================================
s = blank()
head = title_block(s, "A SOLUÇÃO", "Uma plataforma, três camadas.",
                   "Cada camada resolve uma das dores — e todas compartilham o mesmo checkout.")
SOL = [
    ("01", "Lojas verificadas",
     "Selo em três camadas: documento, histórico e catálogo. Só loja aprovada vende.",
     PRIMARY, WHITE, "oval", ["documento + CNPJ", "histórico de vendas", "catálogo auditado"]),
    ("02", "Venda entre atletas",
     "C2C com reputação, fotos guiadas e mediação de disputa. O usado tem garantia.",
     SECONDARY, INK, "tri", ["perfil com reputação", "fotos guiadas", "mediação de disputa"]),
    ("03", "Custódia financeira",
     "O valor fica retido até a entrega confirmada. Depois, o repasse é automático.",
     ACCENT, WHITE, "diamond", ["valor retido no Pix", "prazo de conferência", "repasse automático"]),
]
sl = []
for i, (num, nm, ds, col, fg, icon, bullets) in enumerate(SOL):
    x = 0.78 + i * 4.02
    c = box(s, x, 2.66, 3.72, 3.52, fill=col, border=INK, lw=2.6,
            shadow=True, shadow_px=8)
    bd = box(s, x + 0.30, 2.96, 0.86, 0.86, fill=WHITE, border=INK, lw=2.2,
             shadow=True, shadow_px=4)
    ivl = {"oval": 0.36, "tri": 0.44, "diamond": 0.40}[icon]
    ic = box(s, x + 0.30 + (0.86 - ivl) / 2, 2.96 + (0.86 - ivl) / 2, ivl, ivl,
             fill=INK, border=None, kind=icon, shadow=False)
    nt = mono(s, x + 1.30, 3.02, 1.0, 0.25, num, size=9.5, color=fg, spc=2.0)
    t = text(s, x + 0.30, 4.04, 3.05, 0.78, nm, size=19, color=fg, bold=True,
             spc=-0.6, line=1.0)
    d = text(s, x + 0.30, 4.90, 3.02, 0.75, ds, size=10, color=fg, line=1.32)
    sl += [c, bd, ic, nt, t, d]
    for j, b in enumerate(bullets):
        by = 5.62 + j * 0.16
        dot = box(s, x + 0.31, by + 0.055, 0.07, 0.07, fill=fg, border=None,
                  shadow=False)
        bl = mono(s, x + 0.47, by, 2.9, 0.18, b, size=6.6, color=fg, spc=0.8)
        sl += [dot, bl]

chips = []
for i, (label, col, fg) in enumerate([("UM CATÁLOGO", WHITE, INK),
                                     ("UMA REPUTAÇÃO", WHITE, INK),
                                     ("UM CAIXA", WHITE, INK)]):
    chips.append(sticker(s, 0.78 + i * 2.34, 6.40, 2.20, 0.36, label, col,
                         color=fg, size=7.0, spc=1.4, shadow_px=5))

animate(s, cascade(head, 60, 100, "rise", 520) +
        cascade(sl, 300, 45, "rise", 500) +
        cascade(chips, 1050, 80, "fade", 400))
transition(s, "fade")
notes(s, (
    "SOLUÇÃO (2min).\n"
    "• Uma plataforma, uma conta, um checkout.\n"
    "• A ordem importa: verificação cria confiança; C2C cria giro; custódia "
    "protege o dinheiro.\n"
    "• Não venda como 'mais um marketplace'. É infraestrutura de confiança."
))
chrome(s, 5, "A solução")

# =====================================================================
# 06 — COMO FUNCIONA
# =====================================================================
s = blank()
head = title_block(s, "COMO FUNCIONA", "Do anúncio ao repasse, em quatro passos.")
STEP = [
    ("1", "Anuncia", "Loja verificada ou atleta publica com fotos guiadas e histórico.", PRIMARY),
    ("2", "Compra", "Checkout único: Pix ou cartão, com o valor em custódia.", SECONDARY),
    ("3", "Recebe", "Envio rastreado e prazo de conferência para o comprador.", GREEN),
    ("4", "Libera", "Entrega confirmada, repasse liberado automaticamente.", ACCENT),
]
dline = box(s, 1.10, 2.86, 10.95, 0.02, fill=INK, border=None, shadow=False,
            dash=True)
st = []
for i, (num, nm, ds, col) in enumerate(STEP):
    x = 0.78 + i * 2.98
    c = box(s, x, 2.55, 0.64, 0.64, fill=col, border=INK, lw=2.4,
            kind="oval", shadow=True, shadow_px=4)
    n = mono(s, x, 2.55, 0.64, 0.64, num, size=13, color=INK, spc=0.4,
             align="c", anchor="m")
    t = text(s, x - 0.06, 3.40, 2.55, 0.34, nm, size=15, color=INK, bold=True,
             spc=-0.3)
    d = text(s, x - 0.06, 3.80, 2.48, 0.90, ds, size=10.3, color=INK_SOFT,
             line=1.32)
    st += [c, n, t, d]

cust = card(s, 0.78, 5.02, 11.77, 1.45)
cl = mono(s, 1.04, 5.22, 1.55, 0.22, "CUSTÓDIA", size=8, color=PRIMARY, spc=2.0)
cs = text(s, 1.04, 5.50, 1.45, 0.70, "o dinheiro não\nanda sozinho", size=9,
          color=INK_SOFT, line=1.25)
FLOW = [("Pix aprovado", PRIMARY, WHITE), ("Valor retido", SECONDARY, INK),
        ("Entrega confirmada", GREEN, INK), ("Repasse liberado", ACCENT, WHITE)]
fl = []
for i, (label, col, fg) in enumerate(FLOW):
    x = 2.62 + i * 2.44
    fb = box(s, x, 5.28, 2.02, 0.88, fill=col, border=INK, lw=2.2,
             shadow=True, shadow_px=4)
    ft = text(s, x, 5.28, 2.02, 0.88, label, size=9.5, color=fg, bold=True,
              align="c", anchor="m", line=1.1)
    fl += [fb, ft]
    if i < 3:
        fl.append(box(s, x + 2.10, 5.71, 0.24, 0.24, fill=INK, border=None,
                      kind="tri", rot=90, shadow=False))

animate(s, cascade(head, 60, 100, "rise", 520) +
        [(dline, "wipe", 260, 650)] +
        cascade(st, 380, 60, "rise", 480) +
        [(cust, "zoom", 900, 600)] +
        [(cl, "fade", 1000, 400), (cs, "fade", 1040, 400)] +
        cascade(fl, 1080, 60, "fade", 380))
transition(s, "push")
notes(s, (
    "COMO FUNCIONA (2min).\n"
    "• Passo 4 é o argumento comercial: o vendedor recebe sem risco de calote e "
    "o comprador recebe antes de o dinheiro sair de fato.\n"
    "• A custódia é o que permite vender C2C com segurança."
))
chrome(s, 6, "Como funciona")

# =====================================================================
# 07 — PRODUTO
# =====================================================================
s = blank()
head = title_block(s, "PRODUTO", "O produto por dentro.",
                   "Fluxos desenhados para reduzir dúvida em cada tela.")
# browser
bw, bh = 6.05, 3.62
bx, by = 0.78, 2.78
br = card(s, bx, by, bw, bh)
bbar = box(s, bx + 0.02, by + 0.02, bw - 0.04, 0.34, fill=MUTED, border=INK,
           lw=1.6, shadow=False)
dots = []
for i, c in enumerate([PRIMARY, SECONDARY, GREEN]):
    dots.append(box(s, bx + 0.20 + i * 0.20, by + 0.14, 0.11, 0.11, fill=c,
                    border=INK, lw=1.2, kind="oval", shadow=False))
ui = []
ui.append(box(s, bx + 0.28, by + 0.62, 1.25, 0.26, fill=SECONDARY, border=INK,
              lw=1.4, shadow=False))
for i in range(3):
    ui.append(box(s, bx + 0.28, by + 0.98 + i * 0.28, 1.95, 0.18, fill=MUTED,
                  border=INK, lw=1.2, shadow=False))
for i, col in enumerate([PRIMARY, SECONDARY, ACCENT]):
    ui.append(box(s, bx + 0.28, by + 2.00 + i * 0.40, 2.35, 0.32, fill=col,
                  border=INK, lw=1.6, shadow=True, shadow_px=3))
ui.append(box(s, bx + 2.95, by + 0.60, 2.82, 2.72, fill=MUTED, border=INK,
              lw=1.6, shadow=False))
ui.append(box(s, bx + 3.12, by + 0.78, 2.48, 1.46, fill=PRIMARY, border=INK,
              lw=1.6, shadow=False))
ui.append(box(s, bx + 3.12, by + 2.36, 1.22, 0.20, fill=WHITE, border=INK,
              lw=1.2, shadow=False))
ui.append(box(s, bx + 3.12, by + 2.70, 2.48, 0.36, fill=INK, border=INK,
              lw=1.4, shadow=True, shadow_px=3))

# phones
ph = []
for i, (label, col) in enumerate([("PÁGINA VERIFICADA", GREEN), ("CUSTÓDIA", ACCENT)]):
    px = 7.20 + i * 2.62
    py = 2.72
    ph.append(card(s, px, py, 2.28, 3.86))
    scr = box(s, px + 0.10, py + 0.16, 2.08, 3.54, fill=MUTED, border=INK,
              lw=1.6, shadow=False)
    ph.append(scr)
    ph.append(box(s, px + 0.80, py + 0.26, 0.68, 0.09, fill=INK, border=None,
                  shadow=False))
    ph.append(box(s, px + 0.24, py + 0.48, 1.80, 1.02, fill=col, border=INK,
                  lw=1.6, shadow=True, shadow_px=3))
    ph.append(box(s, px + 0.24, py + 1.62, 1.10, 0.16, fill=WHITE, border=INK,
                  lw=1.2, shadow=False))
    ph.append(box(s, px + 0.24, py + 1.88, 1.80, 0.15, fill=WHITE, border=INK,
                  lw=1.2, shadow=False))
    ph.append(box(s, px + 0.24, py + 2.18, 0.90, 0.28, fill=SECONDARY, border=INK,
                  lw=1.4, shadow=False))
    ph.append(box(s, px + 0.24, py + 2.62, 1.80, 0.13, fill=WHITE, border=INK,
                  lw=1.2, shadow=False))
    ph.append(box(s, px + 0.24, py + 2.88, 1.20, 0.13, fill=WHITE, border=INK,
                  lw=1.2, shadow=False))
    ph.append(box(s, px + 0.24, py + 3.22, 1.80, 0.36, fill=INK, border=INK,
                  lw=1.4, shadow=True, shadow_px=3))
    ph.append(mono(s, px, py + 3.96, 2.28, 0.22, label, size=6.8, color=INK_SOFT,
                   spc=1.2, align="c"))

bl = mono(s, bx, by + 3.72, bw, 0.22, "CATÁLOGO", size=6.8, color=INK_SOFT,
          spc=1.2, align="c")

animate(s, cascade(head, 60, 100, "rise", 520) +
        [(br, "zoom", 260, 650)] +
        [(x, "fade", 420 + i * 25, 380) for i, x in enumerate([bbar] + dots + ui)] +
        cascade(ph, 640, 30, "rise", 450) +
        [(bl, "fade", 1150, 350)])
transition(s, "fade")
notes(s, (
    "PRODUTO (1min30).\n"
    "• As telas são wireframes: o objetivo é mostrar a lógica, não o visual final.\n"
    "• Destaque a tela de custódia: status do dinheiro e do envio juntos."
))
chrome(s, 7, "Produto")

# =====================================================================
# 08 — DIFERENCIAL
# =====================================================================
s = blank()
head = title_block(s, "DIFERENCIAL", "Confiança não é um selo. É um fluxo.")
left = [mono(s, 0.78, 2.70, 4.3, 0.22, "VERIFICAÇÃO · 3 CAMADAS", size=7.6,
             color=PRIMARY, spc=1.8)]
VER = [("1", "Documento e CNPJ", "Existência real, sócio responsável e dados bancários.", PRIMARY),
       ("2", "Histórico de vendas", "Tempo de operação, volume e taxa de disputa.", SECONDARY),
       ("3", "Catálogo auditado", "Marcas, procedência e amostra de produtos.", GREEN)]
for i, (num, nm, ds, col) in enumerate(VER):
    y = 3.10 + i * 1.10
    n = box(s, 0.78, y, 0.54, 0.54, fill=col, border=INK, lw=2.0,
            shadow=True, shadow_px=4)
    nt = mono(s, 0.78, y, 0.54, 0.54, num, size=10, color=INK, align="c",
              anchor="m")
    t = text(s, 1.50, y - 0.03, 3.6, 0.30, nm, size=13.5, color=INK, bold=True)
    d = text(s, 1.50, y + 0.33, 3.62, 0.55, ds, size=9.6, color=INK_SOFT,
             line=1.28)
    left += [n, nt, t, d]

panel = box(s, 5.30, 2.56, 3.55, 4.06, fill=INK, border=INK, lw=2.6,
            shadow=True, shadow_px=8)
pt = mono(s, 5.58, 2.78, 3.0, 0.22, "CUSTÓDIA · 4 ESTADOS", size=7.4,
          color=SECONDARY, spc=1.6)
STATES = [("Pago", "valor entra na conta custodial", PRIMARY),
          ("Retido", "comprador confirma o recebimento", SECONDARY),
          ("Em trânsito", "prazo de conferência aberto", ACCENT),
          ("Liberado", "repasse automático ao vendedor", GREEN)]
stt = [panel, pt]
for i, (nm, ds, col) in enumerate(STATES):
    y = 3.20 + i * 0.82
    stt.append(box(s, 5.58, y, 0.18, 0.18, fill=col, border=WHITE, lw=1.4,
                   kind="oval", shadow=False))
    stt.append(text(s, 5.88, y - 0.08, 2.75, 0.28, nm, size=11.5, color=WHITE,
                    bold=True))
    stt.append(text(s, 5.88, y + 0.20, 2.72, 0.26, ds, size=8.2, color=D_MUTED,
                    line=1.2))

thesis = card(s, 9.05, 2.56, 3.50, 4.06)
th1 = text(s, 9.33, 2.82, 3.0, 0.72, "Ninguém faz\nos dois juntos.", size=20,
           color=INK, bold=True, spc=-0.8, line=1.02)
th2 = text(s, 9.33, 3.72, 2.95, 1.05,
           "Marketplaces têm alcance e não verificam. Lojas têm confiança e não "
           "têm tráfego de atleta.", size=9.2, color=INK_SOFT, line=1.32)
pills = []
for i, (label, col, fg) in enumerate([("VERIFICAÇÃO", PRIMARY, WHITE),
                                     ("REPUTAÇÃO", GREEN, INK),
                                     ("CUSTÓDIA", ACCENT, WHITE)]):
    y = 4.88 + i * 0.42
    pills.append(box(s, 9.33, y, 2.05, 0.32, fill=col, border=INK, lw=1.8,
                     shadow=True, shadow_px=3))
    pills.append(mono(s, 9.33, y, 2.05, 0.32, label, size=6.6, color=fg,
                      spc=1.2, align="c", anchor="m"))
cta = box(s, 9.33, 6.14, 2.95, 0.34, fill=INK, border=INK, lw=1.8,
          shadow=False)
ct = mono(s, 9.33, 6.14, 2.95, 0.34, "OS TRÊS JUNTOS", size=6.8, color=WHITE,
          spc=1.4, align="c", anchor="m")

animate(s, cascade(head, 60, 100, "rise", 520) +
        cascade(left, 260, 50, "rise", 460) +
        [(panel, "zoom", 560, 600), (pt, "fade", 680, 400)] +
        cascade(stt[2:], 720, 55, "fade", 400) +
        [(thesis, "left", 900, 550), (th1, "fade", 1000, 400),
         (th2, "fade", 1060, 400)] +
        cascade(pills, 1120, 60, "rise", 420) +
        [(cta, "zoom", 1360, 420), (ct, "fade", 1440, 380)])
transition(s, "wipe")
notes(s, (
    "DIFERENCIAL (1min30).\n"
    "• A frase-chave: confiança não é selo, é fluxo de dinheiro e de informação.\n"
    "• Verificação sem custódia não protege o pagamento; custódia sem "
    "verificação não protege o produto."
))
chrome(s, 8, "Diferencial")

# =====================================================================
# 09 — MODELO DE NEGÓCIO
# =====================================================================
s = blank()
head = title_block(s, "MODELO DE NEGÓCIO", "Como o dinheiro entra.",
                   "Receita no fluxo, não em mensalidade do atleta.")
REV = [("Comissão por venda", "6% a 10% do valor da transação, descontados no repasse.",
        "6–10%", "RECEITA PRINCIPAL", PRIMARY, WHITE),
       ("Destaque de loja", "Assinatura mensal para vitrine, selo e prioridade na busca.",
        "R$ 99", "RECORRENTE", SECONDARY, INK),
       ("Serviços esportivos", "Fotografia, laudo de autenticidade e eventos com parceiros.",
        "20%", "EXPANSÃO", ACCENT, WHITE)]
rv = []
for i, (nm, ds, metric, tag, col, fg) in enumerate(REV):
    x = 0.78 + i * 4.02
    c = card(s, x, 2.64, 3.72, 2.72)
    bar = box(s, x, 2.64, 3.72, 0.16, fill=col, border=INK, lw=2.2,
              shadow=False)
    t = text(s, x + 0.28, 2.94, 3.05, 0.34, nm, size=15.5, color=INK, bold=True,
             spc=-0.4)
    d = text(s, x + 0.28, 3.36, 3.05, 0.72, ds, size=9.8, color=INK_SOFT,
             line=1.32)
    rule(s, x + 0.28, 4.10, 2.85, 0.012)
    m = mono(s, x + 0.28, 4.24, 1.9, 0.45, metric, size=24, color=INK, spc=0,
             bold=True)
    tg = box(s, x + 0.28, 4.80, 1.72, 0.28, fill=col, border=INK, lw=1.6,
             shadow=True, shadow_px=3)
    tt = mono(s, x + 0.28, 4.80, 1.72, 0.28, tag, size=5.9, color=fg, spc=1.0,
              align="c", anchor="m")
    rv += [c, bar, t, d, m, tg, tt]

stats = box(s, 0.78, 5.60, 11.77, 1.18, fill=INK, border=INK, lw=2.4,
            shadow=True, shadow_px=7)
sl = [stats, mono(s, 1.04, 5.80, 1.7, 0.20, "EXEMPLO ILUSTRATIVO", size=6.4,
                  color=SECONDARY, spc=1.2)]
STATS = [("R$ 480", "ticket médio", WHITE), ("8%", "take rate", SECONDARY),
         ("R$ 38", "receita / pedido", GREEN), ("R$ 60", "CAC alvo", D_MUTED)]
for i, (v, l, col) in enumerate(STATS):
    x = 3.10 + i * 2.38
    sl.append(text(s, x, 5.82, 2.05, 0.42, v, size=21, color=col, bold=True,
                   spc=-0.5))
    sl.append(mono(s, x, 6.28, 2.05, 0.2, l, size=6.2, color=D_MUTED, spc=1.0))

animate(s, cascade(head, 60, 100, "rise", 520) +
        cascade(rv, 300, 50, "rise", 480) +
        [(stats, "zoom", 850, 600)] + cascade(sl[1:], 950, 50, "fade", 380))
transition(s, "fade")
notes(s, (
    "MODELO (1min30).\n"
    "• Receita principal é comissão; assinatura de loja e serviços são alavancas.\n"
    "• Os números do rodapé são exemplo — troque pelos seus antes da banca.\n"
    "• Se perguntarem de margem: custo dominante é pagamento + suporte de disputa."
))
chrome(s, 9, "Modelo de negócio")

# =====================================================================
# 10 — POSICIONAMENTO
# =====================================================================
s = blank()
head = title_block(s, "POSICIONAMENTO", "Onde ninguém está.")
mx, my, mw, mh = 0.78, 2.34, 7.35, 3.86
quads = [(mx, my, mw / 2, mh / 2, WHITE),
         (mx + mw / 2, my, mw / 2, mh / 2, RGBColor(0xF0, 0xF0, 0xF0)),
         (mx, my + mh / 2, mw / 2, mh / 2, RGBColor(0xF0, 0xF0, 0xF0)),
         (mx + mw / 2, my + mh / 2, mw / 2, mh / 2, WHITE)]
mt = []
for x, y, w, h, col in quads:
    mt.append(box(s, x, y, w, h, fill=col, border=None, shadow=False))
frame = box(s, mx, my, mw, mh, fill=None, border=INK, lw=2.6, shadow=True,
            shadow_px=8)
mt.append(frame)
mt.append(box(s, mx + mw / 2 - 0.01, my, 0.02, mh, fill=INK, border=None,
              shadow=False))
mt.append(box(s, mx, my + mh / 2 - 0.01, mw, 0.02, fill=INK, border=None,
              shadow=False))
# acentos de canto
mt.append(box(s, mx + mw / 2, my, 0.55, 0.10, fill=SECONDARY, border=INK,
              lw=1.4, shadow=False))
mt.append(box(s, mx + mw - 0.10, my + mh / 2 - 0.55, 0.10, 0.55, fill=ACCENT,
              border=INK, lw=1.4, shadow=False))

axis_x = mono(s, mx + mw - 2.85, my + mh + 0.14, 2.55, 0.2, "ALCANCE E TRÁFEGO",
              size=6.8, color=INK_SOFT, spc=1.2, align="r")
arrow_x = box(s, mx + mw - 0.22, my + mh + 0.18, 0.22, 0.22, fill=INK,
              border=None, kind="tri", rot=90, shadow=False)
axis_y = mono(s, mx + 0.24, my - 0.26, 3.0, 0.2, "CONFIANÇA", size=6.8,
              color=INK_SOFT, spc=1.2)
arrow_y = box(s, mx + 0.04, my - 0.30, 0.20, 0.20, fill=INK, border=None,
              kind="tri", shadow=False)

COMP = [("lojas próprias", 0.22, 0.30), ("classificados", 0.32, 0.80),
        ("marketplaces genéricos", 0.58, 0.55)]
comp = []
for label, fx, fy in COMP:
    cx = mx + mw * fx
    cy = my + mh * fy
    dot = box(s, cx - 0.11, cy - 0.11, 0.22, 0.22, fill=WHITE, border=INK,
              lw=2.0, kind="oval", shadow=True, shadow_px=3)
    lb = text(s, cx + 0.18, cy - 0.13, 2.4, 0.26, label, size=8.5,
              color=INK_SOFT)
    comp.append((dot, lb))

tx, ty = mx + mw * 0.82, my + mh * 0.26
target = [box(s, tx - 0.29, ty - 0.29, 0.58, 0.58, fill=SECONDARY, border=INK,
              lw=2.0, kind="star", shadow=True, shadow_px=4),
          box(s, tx - 0.11, ty - 0.11, 0.22, 0.22, fill=PRIMARY, border=INK,
              lw=1.6, kind="oval", shadow=False)]
tlabel = sticker(s, tx - 0.82, ty - 0.76, 1.64, 0.32, "COREMOTION", PRIMARY,
                 color=WHITE, size=6.6, spc=1.2, shadow_px=4)

SIDE = ["Marketplaces genéricos têm alcance, mas não verificam quem vende.",
        "Lojas próprias têm confiança, mas não têm tráfego de atleta.",
        "CoreMotion junta os dois — e ainda segura o dinheiro."]
sd = []
for i, t in enumerate(SIDE):
    y = 2.60 + i * 1.34
    col = PRIMARY if i == 2 else WHITE
    sd.append(box(s, 8.55, y + 0.06, 0.18, 0.18, fill=col, border=INK, lw=1.6,
                  shadow=False))
    sd.append(text(s, 8.92, y, 3.55, 1.05, t,
                   size=10.5, color=INK if i == 2 else INK_SOFT,
                   bold=(i == 2), line=1.35))

animate(s, cascade(head, 60, 100, "rise", 520) +
        [(m, "fade", 200 + i * 40, 480) for i, m in enumerate(mt)] +
        [(axis_x, "fade", 460, 380), (axis_y, "fade", 460, 380),
         (arrow_x, "fade", 480, 360), (arrow_y, "fade", 480, 360)] +
        [(c[0], "zoom", 520 + i * 90, 420) for i, c in enumerate(comp)] +
        [(c[1], "fade", 560 + i * 90, 380) for i, c in enumerate(comp)] +
        [(tlabel, "drop", 900, 450), (target[0], "zoom", 960, 500),
         (target[1], "fade", 1050, 350)] +
        cascade(sd, 1120, 80, "left", 480))
transition(s, "fade")
notes(s, (
    "POSICIONAMENTO (1min).\n"
    "• O eixo vertical é confiança; o horizontal é alcance.\n"
    "• O quadrante superior direito está vazio — é onde o CoreMotion quer estar.\n"
    "• Não citar concorrentes por nome."
))
chrome(s, 10, "Posicionamento")

# =====================================================================
# 11 — ROADMAP
# =====================================================================
s = blank()
head = title_block(s, "ROADMAP", "Do MVP à escala.",
                   "Quatro fases, cada uma com uma pergunta a responder.")
base_y = 6.14
road = [box(s, 0.78, base_y, 11.77, 0.05, fill=INK, border=None, shadow=False)]
PH = [("AGORA", "Fase 1", "MVP: catálogo, verificação manual e custódia.", 2.05, PRIMARY, WHITE),
      ("PRÓXIMO", "Fase 2", "Checkout completo, reputação e painel da loja.", 2.58, SECONDARY, INK),
      ("DEPOIS", "Fase 3", "App do atleta, disputas e logística parceira.", 3.10, GREEN, INK),
      ("ESCALA", "Fase 4", "Expansão regional e serviços esportivos.", 3.62, ACCENT, WHITE)]
for i, (tag, phase, desc, h, col, fg) in enumerate(PH):
    x = 0.78 + i * 2.96
    bar = box(s, x, base_y - h, 2.20, h, fill=col, border=INK, lw=2.4,
              shadow=True, shadow_px=7)
    tg = mono(s, x + 0.20, base_y - h + 0.20, 1.75, 0.20, tag, size=6.8,
              color=fg, spc=1.6)
    ph = text(s, x + 0.20, base_y - h + 0.50, 1.80, 0.28, phase, size=11.5,
              color=fg, bold=True)
    ds = text(s, x + 0.20, base_y - h + 0.86, 1.78, 0.80, desc, size=8.4,
              color=fg, line=1.3)
    road += [bar, tg, ph, ds]

anim = cascade(head, 60, 100, "rise", 520) + [(road[0], "wipe", 260, 650)]
bars = road[1::4]
for i, b in enumerate(bars):
    anim.append((b, "wipeup", 380 + i * 120, 700))
rest = [sh for sh in road[1:] if sh not in bars]
anim += [(sh, "fade", 800 + i * 30, 380) for i, sh in enumerate(rest)]
animate(s, anim)
transition(s, "push")
notes(s, (
    "ROADMAP (1min).\n"
    "• Cada fase responde uma pergunta: dá para vender? dá para confiar? dá para escalar?\n"
    "• A banca quer saber o que você faz nos próximos 90 dias: foque na Fase 1."
))
chrome(s, 11, "Roadmap")

# =====================================================================
# 12 — ONDE ESTAMOS
# =====================================================================
s = blank()
head = title_block(s, "ONDE ESTAMOS", "O que já existe, de verdade.")
STAT = [("Produto", "Fluxos de catálogo, loja e checkout desenhados; identidade visual e telas definidas.", PRIMARY, "oval"),
        ("Técnica", "Next.js 15 + TypeScript + Supabase. Build e type-check passando no repositório.", SECONDARY, "hex"),
        ("Operação", "Quatro frentes independentes, com contratos de integração escritos.", ACCENT, "diamond")]
where = []
for i, (nm, ds, col, icon) in enumerate(STAT):
    x = 0.78 + i * 4.02
    c = card(s, x, 2.66, 3.72, 2.60)
    isq = box(s, x + 0.28, 2.94, 0.80, 0.80, fill=col, border=INK, lw=2.2,
              shadow=True, shadow_px=4)
    ivl = {"oval": 0.36, "hex": 0.44, "diamond": 0.40}[icon]
    ic = box(s, x + 0.28 + (0.80 - ivl) / 2, 2.94 + (0.80 - ivl) / 2, ivl, ivl,
             fill=INK, border=None, kind=icon, shadow=False)
    t = text(s, x + 1.24, 3.16, 2.2, 0.36, nm, size=17, color=INK, bold=True,
             spc=-0.4)
    d = text(s, x + 0.28, 4.00, 3.10, 1.05, ds, size=10.2, color=INK_SOFT,
             line=1.35)
    where += [c, isq, ic, t, d]

band = box(s, 0.78, 5.52, 11.77, 1.18, fill=INK, border=INK, lw=2.4,
           shadow=True, shadow_px=7)
bT = text(s, 1.06, 5.70, 11.2, 0.85,
          "Ainda sem tração medida. O que existe é base técnica, produto desenhado "
          "e plano de execução — e é exatamente isso que queremos validar com você.",
          size=12.5, color=WHITE, bold=True, line=1.35)

animate(s, cascade(head, 60, 100, "rise", 520) +
        cascade(where, 300, 55, "rise", 500) +
        [(band, "zoom", 900, 600), (bT, "fade", 1000, 450)])
transition(s, "fade")
notes(s, (
    "ONDE ESTAMOS (1min).\n"
    "• Transparência total: sem métricas de tração ainda.\n"
    "• O ativo atual é a base técnica e o desenho de produto — reduz risco de execução."
))
chrome(s, 12, "Onde estamos")

# =====================================================================
# 13 — TIME
# =====================================================================
s = blank()
head = title_block(s, "QUEM EXECUTA", "Quatro frentes, uma entrega.",
                   "Cada frente responde pelo próprio estado, sem esperar liberação.")
TEAM = [("P1", "Identidade & acesso", "Sessão, papéis, permissões e painel administrativo.", PRIMARY),
        ("P2", "Catálogo & negócio", "Lojas, produtos, checkout e regras de comissão.", SECONDARY),
        ("P3", "Documento & diagramas", "Requisitos, arquitetura e material de apresentação.", GREEN),
        ("P4", "Verificação & entrega", "Ambiente de testes, QA e critérios de aceite.", ACCENT)]
tm = []
for i, (ini, nm, ds, col) in enumerate(TEAM):
    x = 0.78 + i * 3.00
    c = card(s, x, 2.66, 2.78, 3.02)
    av = box(s, x + 0.28, 2.94, 0.82, 0.82, fill=col, border=INK, lw=2.2,
             shadow=True, shadow_px=4)
    it = mono(s, x + 0.28, 2.94, 0.82, 0.82, ini, size=19, color=INK,
              spc=0.5, align="c", anchor="m")
    t = text(s, x + 0.28, 4.02, 2.30, 0.62, nm, size=14, color=INK, bold=True,
             spc=-0.3, line=1.05)
    d = text(s, x + 0.28, 4.76, 2.25, 0.75, ds, size=9.4, color=INK_SOFT,
             line=1.32)
    tm += [c, av, it, t, d]

note = text(s, 0.78, 5.96, 8.0, 0.22,
            "Nomes e mini-bios entram na versão final deste slide.",
            size=9, color=INK_SOFT, italic=True)

animate(s, cascade(head, 60, 100, "rise", 520) +
        cascade(tm, 300, 55, "rise", 500) + [(note, "fade", 1000, 380)])
transition(s, "push")
notes(s, (
    "TIME (45s).\n"
    "• Não é 'somos quatro amigos': são quatro responsabilidades com entregáveis.\n"
    "• Cite rapidamente o que cada um já entregou."
))
chrome(s, 13, "Quem executa")

# =====================================================================
# 14 — O PEDIDO
# =====================================================================
s = blank()
head = title_block(s, "O PEDIDO", "O que precisamos para os próximos 90 dias.")
ASK = [("Piloto com 5 lojas", "Acesso a lojas esportivas para validar verificação e custódia com vendas reais.", "REDE", PRIMARY, WHITE),
       ("R$ 300 mil", "Produto, operação e marketing do piloto. Ajuste o valor ao seu plano.", "INVESTIMENTO", SECONDARY, INK),
       ("Dois conselheiros", "Marketplace e operação de pagamentos, com uma conversa por mês.", "MENTORIA", ACCENT, WHITE)]
ak = []
for i, (nm, ds, tag, col, fg) in enumerate(ASK):
    x = 0.78 + i * 4.02
    c = card(s, x, 2.66, 3.72, 2.86)
    bar = box(s, x, 2.66, 3.72, 0.16, fill=col, border=INK, lw=2.2,
              shadow=False)
    tg = mono(s, x + 0.28, 2.96, 2.9, 0.2, tag, size=6.6, color=INK_SOFT, spc=1.8)
    t = text(s, x + 0.28, 3.26, 3.10, 0.72, nm, size=23, color=INK, bold=True,
             spc=-0.9, line=1.0)
    d = text(s, x + 0.28, 4.12, 3.05, 1.10, ds, size=10.2, color=INK_SOFT,
             line=1.35)
    ak += [c, bar, tg, t, d]

goal = box(s, 0.78, 5.82, 11.77, 0.62, fill=INK, border=INK, lw=2.4,
           shadow=True, shadow_px=6)
gt = mono(s, 1.04, 5.82, 11.2, 0.62,
          "META DO PILOTO · 5 LOJAS · 300 PEDIDOS · 100% COM CUSTÓDIA · 90 DIAS",
          size=8.6, color=WHITE, spc=0.8, anchor="m")

animate(s, cascade(head, 60, 100, "rise", 520) +
        cascade(ak, 300, 55, "rise", 500) +
        [(goal, "zoom", 920, 600), (gt, "fade", 1020, 450)])
transition(s, "fade")
notes(s, (
    "O PEDIDO (1min30).\n"
    "• Seja direto: 5 lojas, investimento e dois conselheiros.\n"
    "• Ajuste R$ 300 mil ao seu plano antes de apresentar.\n"
    "• Se a banca não puder investir, peça conexão com uma loja."
))
chrome(s, 14, "O pedido")

# =====================================================================
# 15 — OBRIGADO (dark)
# =====================================================================
s = blank(dark=True)
dark_shapes = [
    box(s, 9.05, 1.05, 3.45, 3.45, fill=D_PRIMARY, border=WHITE, lw=2.5,
        kind="oval", shadow=False),
    box(s, 7.85, 4.95, 1.35, 1.35, fill=D_ACCENT, border=WHITE, lw=2.2, rot=-10,
        shadow=False),
    box(s, 11.55, 4.55, 0.95, 0.95, fill=D_SECOND, border=None, kind="star",
        shadow=False),
    box(s, 10.35, 6.05, 0.62, 0.62, fill=GREEN, border=WHITE, lw=2.0,
        shadow=False),
    box(s, 7.55, 1.10, 0.70, 0.70, fill=MAGENTA, border=None, kind="star4",
        shadow=False),
]
kick = mono(s, 0.78, 1.42, 6.5, 0.24, "COREMOTION · 2026", size=8.5,
            color=D_SECOND, spc=2.6)
big = text(s, 0.78, 1.90, 8.0, 1.45, "Obrigado.", size=92, color=WHITE,
           bold=True, spc=-3.2, line=0.9)
sub = text(s, 0.78, 3.42, 6.6, 1.05,
           "Vamos construir o ponto de encontro\ndo esporte de alta performance?",
           size=19, color=D_MUTED, line=1.3)
rule2 = box(s, 0.84, 4.66, 1.55, 0.10, fill=D_PRIMARY, border=None,
            shadow=False)
contact = mono(s, 0.78, 4.98, 7.0, 0.28, "[seu@email.com] · [telefone] · [site]",
               size=8.6, color=WHITE, spc=0.8)
bye = text(s, 0.78, 6.30, 7.0, 0.22, "Obrigado pela leitura. Perguntas, agora.",
           size=9.5, color=RGBColor(0x9A, 0x9A, 0x9A))

animate(s, cascade(dark_shapes, 0, 90, "zoom", 700) +
        [(kick, "fade", 120, 450), (big, "rise", 200, 700),
         (sub, "rise", 420, 600), (rule2, "wipe", 600, 450),
         (contact, "fade", 720, 450), (bye, "fade", 860, 400)])
transition(s, "fade")
notes(s, (
    "FECHAMENTO (30s).\n"
    "• Pare de falar depois do 'obrigado'. Deixe a banca perguntar.\n"
    "• Tenha à mão: custo de aquisição, plano de 90 dias e a lista de lojas "
    "que já disseram sim."
))
chrome(s, 15, "Obrigado", dark=True, accent=D_PRIMARY)

# ------------------------------------------------------------------ metadados
prs.core_properties.title = "CoreMotion — Pitch para banca"
prs.core_properties.author = "CoreMotion"
prs.core_properties.subject = "Marketplace esportivo de alta performance"
prs.core_properties.language = "pt-BR"

out = sys.argv[1] if len(sys.argv) > 1 else "CoreMotion-Pitch-Banca.pptx"
prs.save(out)
print("salvo:", out)
