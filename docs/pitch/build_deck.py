"""CoreMotion — deck de pitch para banca (15 slides, tema pastel geométrico)."""
import sys
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from deck_lib import *   # noqa

TOTAL = 15
prs = new_deck()


def title_block(slide, kicker, title, sub=None, y=0.95, color_kicker=CORAL_D):
    k = txt(slide, 0.9, y, 8.0, 0.25, kicker.upper(), size=9,
            color=color_kicker, bold=True, spc=2.2)
    t = txt(slide, 0.9, y + 0.28, 11.2, 0.75, title, size=31, color=INK,
            bold=True, spc=-0.4, line_spacing=0.95)
    s = None
    if sub:
        s = txt(slide, 0.9, y + 1.02, 8.6, 0.4, sub, size=12.5, color=INK2)
    return [k, t] + ([s] if s else [])


# =====================================================================
# 01 — CAPA
# =====================================================================
s = blank(prs)
bg_shapes = [
    shape(s, "oval", 8.25, -2.05, 7.2, 7.2, fill=LAV),
    shape(s, "oval", 11.55, 4.05, 3.05, 3.05, fill=MINT),
    shape(s, "oval", 7.72, 5.62, 1.05, 1.05, fill=BUTTER),
    shape(s, "oval", 8.62, 0.95, 3.62, 3.62, fill=None, line=CORAL_D, lw=7),
    shape(s, "oval", 9.22, 1.55, 2.42, 2.42, fill=WHITE, shadow=True,
          shadow_alpha=14),
    shape(s, "tri", 7.62, 1.62, 0.52, 0.52, fill=PEACH, rot=14),
]
chk1 = line(s, 9.90, 2.46, 10.18, 2.78, CORAL_D, lw=7)
chk2 = line(s, 10.18, 2.78, 10.72, 2.12, CORAL_D, lw=7)

chip1 = shape(s, "round", 11.02, 1.42, 2.12, 0.44, fill=WHITE, radius=0.5,
              shadow=True)
shape(s, "oval", 11.20, 1.60, 0.09, 0.09, fill=MINT_D)
t = txt(s, 11.40, 1.42, 1.62, 0.44, "LOJAS VERIFICADAS", size=7.2,
        color=INK, bold=True, spc=1.2, anchor="m")

chip2 = shape(s, "round", 8.42, 4.52, 1.62, 0.44, fill=WHITE, radius=0.5,
              shadow=True)
shape(s, "oval", 8.60, 4.70, 0.09, 0.09, fill=LAV_D)
txt(s, 8.80, 4.52, 1.12, 0.44, "CUSTÓDIA", size=7.2, color=INK, bold=True,
    spc=1.2, anchor="m")

chip3 = shape(s, "round", 11.42, 4.62, 0.95, 0.44, fill=WHITE, radius=0.5,
              shadow=True)
txt(s, 11.42, 4.62, 0.95, 0.44, "C2C", size=7.4, color=INK, bold=True,
    spc=1.4, align="c", anchor="m")

kicker = chip(s, 0.9, 1.18, 2.42, 0.36, "PITCH · BANCA 2026", CORAL,
              color=INK, size=8, spc=1.8)
brand = txt(s, 0.9, 1.82, 6.9, 1.15, "CoreMotion", size=64, color=INK,
            bold=True, spc=-1.6, line_spacing=0.9)
rule = shape(s, "round", 0.96, 3.16, 1.55, 0.055, fill=CORAL_D, radius=0.5)
sub = txt(s, 0.9, 3.46, 6.35, 1.35, [
    "O ponto de encontro",
    ("do esporte de alta performance.", {"color": INK, "bold": True}),
], size=22, color=INK2, line_spacing=1.18)
meta = txt(s, 0.9, 5.02, 6.6, 0.3,
           "MARKETPLACE ESPORTIVO  ·  LOJAS VERIFICADAS  ·  CUSTÓDIA",
           size=8.5, color=MUTED, bold=True, spc=1.7)
foot = txt(s, 0.9, 6.42, 6.6, 0.3,
           "Apresentado por [seu nome]  ·  [cidade], 2026", size=9.5,
           color=MUTED)
animate(s, cascade(bg_shapes, start=0, step=90, effect="zoom", dur=700) +
        [(chip1, "drop", 260, 500), (chip2, "left", 380, 500),
         (chip3, "left", 460, 500),
         (kicker, "fade", 120, 420), (brand, "rise", 180, 700),
         (rule, "wipe", 420, 500), (sub, "rise", 500, 650),
         (meta, "fade", 720, 500), (foot, "fade", 820, 500)])
transition(s, "fade")
notes(s, (
    "ABERTURA (30s).\n"
    "• Meu nome é [nome] e o CoreMotion é um marketplace esportivo com lojas "
    "verificadas, venda entre atletas e custódia financeira.\n"
    "• A frase-guia da apresentação: hoje comprar esporte é um ato de fé. "
    "Nosso produto transforma confiança em fluxo.\n"
    "• Prometer 15 minutos e seguir o roteiro da agenda."
))
chrome(s, 1, TOTAL, "Capa")

# =====================================================================
# 02 — AGENDA
# =====================================================================
s = blank(prs)
deco = [
    shape(s, "oval", 10.9, -1.35, 3.4, 3.4, fill=MINT, alpha=55),
    shape(s, "oval", -0.85, 5.85, 2.5, 2.5, fill=CORAL, alpha=45),
]
head = title_block(s, "Agenda", "O caminho",
                   "Quinze minutos, quatro blocos. Sem slide de história da empresa.")

cards = []
AGENDA = [
    ("01", "O problema", "Por que comprar e vender esporte ainda é inseguro.", CORAL),
    ("02", "A solução", "As três camadas que fazem o CoreMotion funcionar.", MINT),
    ("03", "O negócio", "Como a plataforma ganha dinheiro e escala.", LAV),
    ("04", "A entrega", "Onde estamos e o que precisamos de você.", BUTTER),
]
for i, (num, name, desc, col) in enumerate(AGENDA):
    x = 0.9 + i * 2.94
    c = card(s, x, 2.55, 2.68, 3.28, fill=WHITE)
    circ = shape(s, "oval", x + 0.30, 2.85, 0.78, 0.78, fill=col)
    n = txt(s, x + 0.30, 2.85, 0.78, 0.78, num, size=20, color=INK, bold=True,
            align="c", anchor="m")
    nm = txt(s, x + 0.30, 3.86, 2.1, 0.55, name, size=14.5, color=INK,
             bold=True)
    ds = txt(s, x + 0.30, 4.46, 2.1, 1.05, desc, size=10, color=INK2,
             line_spacing=1.25)
    cards += [c, circ, n, nm, ds]

foot = chip(s, 9.05, 6.28, 3.38, 0.4, "PITCH PARA BANCA · COREMOTION 2026",
            WHITE, color=INK2, size=7.6, spc=1.5)
animate(s, cascade(head, 80, 110, "rise", 550) +
        cascade(cards, 380, 55, "rise", 500) +
        [(foot, "fade", 900, 400)])
transition(s, "push")
notes(s, (
    "AGENDA (45s).\n"
    "• Quatro blocos. O primeiro é o mais importante: o problema.\n"
    "• Se o tempo apertar, cortamos o bloco 3 e mantemos problema, solução "
    "e pedido."
))
chrome(s, 2, TOTAL, "Agenda")

# =====================================================================
# 03 — PROBLEMA
# =====================================================================
s = blank(prs)
deco = [
    shape(s, "oval", 11.6, 5.4, 2.6, 2.6, fill=CORAL, alpha=40),
    shape(s, "tri", -0.45, 5.55, 1.5, 1.5, fill=BUTTER, alpha=70, rot=-12),
]
head = title_block(s, "O problema", "Comprar esporte ainda é um ato de fé.")

PROB = [
    ("oval", "Falsificação", "Réplica vendida como original. Não há verificação de loja, de catálogo nem de histórico.", CORAL, MINT_D),
    ("tri", "Dinheiro exposto", "Pix direto para o vendedor: se a peça não chega, o prejuízo inteiro é do atleta.", MINT, CORAL_D),
    ("diamond", "Atleta invisível", "Quem vende usado não tem canal confiável. Quem procura não sabe em quem confiar.", LAV, LAV_D),
]
cards = []
for i, (ic, name, desc, col, ic_col) in enumerate(PROB):
    x = 0.9 + i * 3.83
    c = card(s, x, 2.32, 3.55, 3.28, fill=WHITE)
    circle = shape(s, "oval", x + 0.34, 2.62, 0.92, 0.92, fill=col)
    icon = shape(s, ic, x + 0.55, 2.83, 0.50, 0.50, fill=ic_col)
    nm = txt(s, x + 0.34, 3.76, 2.85, 0.4, name, size=15, color=INK, bold=True)
    ds = txt(s, x + 0.34, 4.21, 2.85, 1.2, desc, size=10.5, color=INK2,
             line_spacing=1.3)
    cards += [c, circle, icon, nm, ds]

band = shape(s, "round", 0.9, 5.95, 11.53, 0.78, fill=INK, radius=0.18,
             shadow=True)
band_tx = txt(s, 1.25, 5.95, 10.9, 0.78,
              "O atleta compra no escuro. A loja vende sem alcance. "
              "O dinheiro fica no meio.", size=13.5, color=WHITE,
              bold=True, anchor="m")
animate(s, cascade(head, 60, 100, "rise", 520) +
        cascade(cards, 300, 60, "rise", 500) +
        [(band, "zoom", 900, 600), (band_tx, "fade", 1000, 500)])
transition(s, "fade")
notes(s, (
    "PROBLEMA (2min).\n"
    "• Conte um caso concreto de compra frustrada (se tiver).\n"
    "• As três dores: falsificação, dinheiro exposto, atleta sem canal.\n"
    "• Fechamento: o problema não é oferta, é confiança."
))
chrome(s, 3, TOTAL, "O problema")

# =====================================================================
# 04 — POR QUE AGORA
# =====================================================================
s = blank(prs)
head = title_block(s, "Por que agora", "Três mudanças abriram essa janela.",
                   "O mercado não precisa de mais um catálogo. Precisa de confiança.")

ROWS = [
    ("O esporte virou consumo de identidade",
     "Equipamento deixou de ser acessório: é pertencimento, performance e status.", CORAL),
    ("O atleta virou mídia e canal",
     "Comunidades e redes criam demanda qualificada todos os dias, de graça.", MINT),
    ("O pagamento amadureceu",
     "Pix, verificação digital e custódia permitem segurar o valor até a entrega.", LAV),
]
rows = []
for i, (nm, ds, col) in enumerate(ROWS):
    y = 2.38 + i * 1.32
    bar = shape(s, "round", 0.9, y, 0.10, 0.95, fill=col, radius=0.5)
    nmt = txt(s, 1.28, y - 0.02, 6.1, 0.38, nm, size=14.5, color=INK, bold=True)
    dst = txt(s, 1.28, y + 0.38, 6.0, 0.62, ds, size=10.5, color=INK2,
              line_spacing=1.3)
    rows += [bar, nmt, dst]

# composição geométrica à direita
visual = []
base_y = 5.72
visual.append(shape(s, "oval", 8.55, 1.62, 3.55, 3.55, fill=None,
                    line=LAV_D, lw=2, line_alpha=45))
visual.append(shape(s, "oval", 9.25, 2.32, 2.15, 2.15, fill=MINT, alpha=85))
visual.append(shape(s, "oval", 9.25, 2.32, 2.15, 2.15, fill=None,
                    line=WHITE, lw=2, line_alpha=60))
for i, (h, col) in enumerate([(1.05, CORAL), (1.55, MINT_D), (2.05, LAV_D),
                              (2.65, BUTTER_D)]):
    visual.append(shape(s, "round", 8.75 + i * 0.82, base_y - h, 0.52, h,
                        fill=col, radius=0.18, alpha=88))
visual.append(shape(s, "rect", 8.62, base_y, 3.55, 0.02, fill=INK, alpha=25))
caption = txt(s, 8.62, 6.02, 3.6, 0.55,
              "Confiança é o gargalo —\ne a maior oportunidade.",
              size=11, color=INK, bold=True, line_spacing=1.2)

animate(s, cascade(head, 60, 100, "rise", 520) +
        [(v, "zoom" if i < 3 else "wipeup", 150 + i * 70, 600)
         for i, v in enumerate(visual)] +
        cascade(rows, 420, 70, "rise", 520) +
        [(caption, "fade", 950, 500)])
transition(s, "wipe")
notes(s, (
    "POR QUE AGORA (1min30).\n"
    "• Três mudanças estruturais — não é tendência passageira.\n"
    "• Se a banca perguntar de dados: diga que o deck evita números de "
    "mercado sem fonte; ofereça o recorte do seu nicho depois."
))
chrome(s, 4, TOTAL, "Por que agora")

# =====================================================================
# 05 — SOLUÇÃO
# =====================================================================
s = blank(prs)
deco = [shape(s, "oval", -1.1, -1.2, 3.3, 3.3, fill=BUTTER, alpha=55)]
head = title_block(s, "A solução", "Uma plataforma, três camadas.",
                   "Cada camada resolve uma das dores — e todas compartilham o mesmo checkout.")

SOL = [
    ("01", "Lojas verificadas",
     "Selo em três camadas: documento, histórico e catálogo. Só loja aprovada vende no CoreMotion.",
     CORAL, "oval", ["documento + CNPJ", "histórico de vendas", "catálogo auditado"]),
    ("02", "Venda entre atletas",
     "C2C com reputação, fotos guiadas e mediação de disputa. O usado também tem garantia.",
     MINT, "tri", ["perfil com reputação", "fotos guiadas", "mediação de disputa"]),
    ("03", "Custódia financeira",
     "O valor fica retido até a entrega confirmada. Depois, o repasse é automático para o vendedor.",
     LAV, "diamond", ["valor retido no Pix", "prazo de conferência", "repasse automático"]),
]
cards = []
for i, (num, name, desc, col, ic, bullets) in enumerate(SOL):
    x = 0.9 + i * 3.83
    c = card(s, x, 2.32, 3.55, 3.86, fill=col)
    icirc = shape(s, "oval", x + 0.34, 2.60, 0.82, 0.82, fill=WHITE, alpha=90)
    ishape = shape(s, ic, x + 0.50, 2.76, 0.50, 0.50, fill=INK, alpha=80)
    numt = txt(s, x + 1.30, 2.78, 1.0, 0.3, num, size=10, color=INK,
               bold=True, spc=2.0, anchor="m")
    nm = txt(s, x + 0.34, 3.58, 2.9, 0.72, name, size=15.5, color=INK,
             bold=True, line_spacing=1.02)
    ds = txt(s, x + 0.34, 4.24, 2.9, 0.75, desc, size=9.2, color=INK2,
             line_spacing=1.24)
    by = 5.02
    for j, b in enumerate(bullets):
        shape(s, "oval", x + 0.36, by + 0.09, 0.06, 0.06, fill=INK, alpha=55)
        bt = txt(s, x + 0.52, by, 2.7, 0.24, b, size=7.9, color=INK, bold=True,
                 spc=0.6)
        cards += [bt]
        by += 0.28
    cards += [c, icirc, ishape, numt, nm, ds]

chips = []
for i, label in enumerate(["UM CATÁLOGO", "UMA REPUTAÇÃO", "UM CAIXA"]):
    chips.append(chip(s, 0.9 + i * 2.22, 6.48, 2.05, 0.36, label, WHITE,
                      color=INK2, size=7.4, spc=1.6))

animate(s, cascade(deco, 0, 0, "zoom", 800) +
        cascade(head, 60, 100, "rise", 520) +
        cascade(cards, 320, 55, "rise", 520) +
        cascade(chips, 900, 80, "fade", 400))
transition(s, "fade")
notes(s, (
    "SOLUÇÃO (2min).\n"
    "• Uma plataforma, uma conta, um checkout.\n"
    "• A ordem importa: verificação cria confiança; C2C cria giro; "
    "custódia protege o dinheiro.\n"
    "• Não venda como 'mais um marketplace'. É infraestrutura de confiança."
))
chrome(s, 5, TOTAL, "A solução")

# =====================================================================
# 06 — COMO FUNCIONA
# =====================================================================
s = blank(prs)
head = title_block(s, "Como funciona", "Do anúncio ao repasse, em quatro passos.")

steps_y = 3.05
conn = line(s, 1.55, steps_y, 11.9, steps_y, LINE, lw=2, dash=True)
STEP = [
    ("1", "Anuncia", "Loja verificada ou atleta publica com fotos guiadas e histórico.", CORAL),
    ("2", "Compra", "Checkout único: Pix ou cartão, com o valor em custódia.", BUTTER),
    ("3", "Recebe", "Envio rastreado e prazo de conferência para o comprador.", MINT),
    ("4", "Libera", "Entrega confirmada, repasse liberado automaticamente.", LAV),
]
steps = []
for i, (num, name, desc, col) in enumerate(STEP):
    x = 1.06 + i * 2.92
    c = shape(s, "oval", x, steps_y - 0.36, 0.72, 0.72, fill=col,
              line=WHITE, lw=3, shadow=True)
    n = txt(s, x, steps_y - 0.36, 0.72, 0.72, num, size=15, color=INK,
            bold=True, align="c", anchor="m")
    nm = txt(s, x - 0.22, steps_y + 0.56, 2.5, 0.35, name, size=13, color=INK,
             bold=True)
    ds = txt(s, x - 0.22, steps_y + 0.97, 2.32, 0.95, desc, size=9.6,
             color=INK2, line_spacing=1.28)
    steps += [c, n, nm, ds]

cust = card(s, 0.9, 5.35, 11.53, 1.35, fill=WHITE)
clabel = txt(s, 1.18, 5.55, 1.4, 0.25, "CUSTÓDIA", size=8, color=CORAL_D,
             bold=True, spc=2.0)
csub = txt(s, 1.18, 5.82, 1.55, 0.65, "o dinheiro não\nanda sozinho", size=8.8,
           color=MUTED, line_spacing=1.15)
flow = []
FLOW = ["Pix aprovado", "Valor retido", "Entrega confirmada", "Repasse liberado"]
for i, label in enumerate(FLOW):
    x = 2.85 + i * 2.42
    c = shape(s, "round", x, 5.66, 2.02, 0.72, fill=[CORAL, BUTTER, MINT, LAV][i],
              radius=0.3, alpha=55)
    t = txt(s, x + 0.1, 5.66, 1.82, 0.72, label, size=8.8, color=INK,
            bold=True, align="c", anchor="m")
    flow += [c, t]
    if i < 3:
        ar = shape(s, "chev", x + 2.06, 5.90, 0.22, 0.24, fill=MUTED)

animate(s, cascade(head, 60, 100, "rise", 520) +
        [(conn, "wipe", 250, 700)] +
        cascade(steps, 380, 55, "rise", 500) +
        [(cust, "zoom", 880, 600), (clabel, "fade", 980, 400),
         (csub, "fade", 1020, 400)] +
        cascade(flow, 1000, 90, "fade", 420))
transition(s, "push")
notes(s, (
    "COMO FUNCIONA (2min).\n"
    "• Passo 4 é o argumento comercial: o vendedor recebe sem correr risco "
    "de calote, o comprador recebe antes de pagar de fato.\n"
    "• Enfatize que a custódia é o que permite vender C2C com segurança."
))
chrome(s, 6, TOTAL, "Como funciona")

# =====================================================================
# 07 — PRODUTO
# =====================================================================
s = blank(prs)
head = title_block(s, "Produto", "O produto por dentro.",
                   "Fluxos desenhados para reduzir dúvida em cada tela.")

# browser
bw, bh = 5.95, 3.85
bx, by = 0.9, 2.25
browser = card(s, bx, by, bw, bh, fill=WHITE)
bar = shape(s, "round", bx, by, bw, 0.38, fill=RGBColor(0xF1, 0xEC, 0xE5), radius=0.28)
bar2 = shape(s, "rect", bx, by + 0.20, bw, 0.18, fill=RGBColor(0xF1, 0xEC, 0xE5))
for i, c in enumerate([CORAL_D, BUTTER_D, MINT_D]):
    shape(s, "oval", bx + 0.20 + i * 0.18, by + 0.14, 0.10, 0.10, fill=c)
# conteúdo
shape(s, "round", bx + 0.26, by + 0.62, 1.25, 0.26, fill=RGBColor(0xEF, 0xEA, 0xE3), radius=0.5)
shape(s, "round", bx + 0.26, by + 1.02, 2.15, 0.30, fill=INK, alpha=8, radius=0.5)
shape(s, "round", bx + 0.26, by + 1.44, 2.55, 0.30, fill=INK, alpha=8, radius=0.5)
for i in range(3):
    shape(s, "round", bx + 0.26, by + 2.02 + i * 0.52, 2.55, 0.40,
          fill=[CORAL, MINT, LAV][i], radius=0.25, alpha=55)
shape(s, "round", bx + 3.02, by + 0.62, 2.65, 2.95, fill=RGBColor(0xF7, 0xF3, 0xEE), radius=0.06)
shape(s, "round", bx + 3.22, by + 0.82, 2.25, 1.55, fill=PEACH, radius=0.08)
shape(s, "tri", bx + 4.02, by + 1.28, 0.65, 0.65, fill=CORAL_D, alpha=70)
shape(s, "round", bx + 3.22, by + 2.52, 1.55, 0.22, fill=INK, alpha=12, radius=0.5)
shape(s, "round", bx + 3.22, by + 2.86, 2.25, 0.44, fill=CORAL_D, radius=0.3)

# phones
phones = []
for i, (label, accent) in enumerate([("Página verificada", MINT_D),
                                     ("Custódia", LAV_D)]):
    px = 7.35 + i * 2.72
    py = 2.10
    ph = card(s, px, py, 2.28, 4.30, fill=WHITE, radius=0.12)
    scr = shape(s, "round", px + 0.12, py + 0.18, 2.04, 3.94,
                fill=RGBColor(0xFA, 0xF6, 0xF0), radius=0.10)
    shape(s, "round", px + 0.86, py + 0.26, 0.56, 0.10, fill=RGBColor(0xE3, 0xDC, 0xD2), radius=0.5)
    shape(s, "round", px + 0.26, py + 0.50, 1.76, 1.14, fill=[PEACH, MINT][i], radius=0.07)
    shape(s, "round", px + 0.26, py + 1.76, 1.20, 0.18, fill=INK, alpha=14, radius=0.5)
    shape(s, "round", px + 0.26, py + 2.02, 1.76, 0.18, fill=INK, alpha=8, radius=0.5)
    shape(s, "round", px + 0.26, py + 2.36, 0.95, 0.34, fill=accent, radius=0.4, alpha=70)
    shape(s, "round", px + 0.26, py + 2.86, 1.76, 0.12, fill=INK, alpha=8, radius=0.5)
    shape(s, "round", px + 0.26, py + 3.10, 1.20, 0.12, fill=INK, alpha=8, radius=0.5)
    shape(s, "round", px + 0.26, py + 3.52, 1.76, 0.42, fill=INK, radius=0.3)
    phones += [ph, scr]
    lbl = txt(s, px, py + 4.42, 2.28, 0.28, label.upper(), size=7.6, color=MUTED,
              bold=True, spc=1.6, align="c")

blbl = txt(s, bx, by + 3.98, bw, 0.28, "CATÁLOGO", size=7.6, color=MUTED,
           bold=True, spc=1.6, align="c")

animate(s, cascade(head, 60, 100, "rise", 520) +
        [(browser, "zoom", 260, 700)] +
        cascade(phones, 420, 120, "rise", 650) +
        [(blbl, "fade", 900, 400)])
transition(s, "fade")
notes(s, (
    "PRODUTO (1min30).\n"
    "• As telas são wireframes: o objetivo é mostrar a lógica, não o visual "
    "final.\n"
    "• Destaque a tela de custódia: status do dinheiro e do envio juntos."
))
chrome(s, 7, TOTAL, "Produto")

# =====================================================================
# 08 — DIFERENCIAL
# =====================================================================
s = blank(prs)
head = title_block(s, "Diferencial", "Confiança não é um selo. É um fluxo.")

# coluna esquerda
lt = txt(s, 0.9, 2.22, 4.9, 0.28, "VERIFICAÇÃO · 3 CAMADAS", size=8.2,
         color=CORAL_D, bold=True, spc=2.0)
VER = [
    ("Documento e CNPJ", "Existência real, sócio responsável e dados bancários."),
    ("Histórico de vendas", "Tempo de operação, volume e taxa de disputa."),
    ("Catálogo auditado", "Marcas, procedência e amostra de produtos."),
]
ver_items = []
for i, (nm, ds) in enumerate(VER):
    y = 2.70 + i * 1.18
    n = shape(s, "oval", 0.9, y, 0.55, 0.55, fill=[CORAL, BUTTER, MINT][i])
    nt = txt(s, 0.9, y, 0.55, 0.55, str(i + 1), size=12, color=INK, bold=True,
             align="c", anchor="m")
    nmt = txt(s, 1.66, y - 0.02, 4.1, 0.32, nm, size=12.5, color=INK, bold=True)
    dst = txt(s, 1.66, y + 0.34, 4.2, 0.55, ds, size=9.8, color=INK2,
              line_spacing=1.25)
    ver_items += [n, nt, nmt, dst]

# coluna direita
panel = card(s, 5.72, 2.12, 3.55, 4.35, fill=INK, radius=0.06)
pt = txt(s, 6.02, 2.38, 3.0, 0.3, "CUSTÓDIA · 4 ESTADOS", size=8.2,
         color=RGBColor(0xFF, 0xC9, 0xC9), bold=True, spc=1.8)
STATES = [("Pago", "valor entra na conta custodial", CORAL_D, "1"),
          ("Retido", "comprador confirma o recebimento", BUTTER_D, "2"),
          ("Em trânsito", "prazo de conferência aberto", SKY, "3"),
          ("Liberado", "repasse automático ao vendedor", MINT_D, "4")]
state_items = []
for i, (nm, ds, col, num) in enumerate(STATES):
    y = 2.86 + i * 0.88
    d = shape(s, "oval", 6.02, y, 0.20, 0.20, fill=col)
    nmt = txt(s, 6.34, y - 0.10, 2.6, 0.28, nm, size=11, color=WHITE, bold=True)
    dst = txt(s, 6.34, y + 0.18, 2.7, 0.30, ds, size=8.0, color=RGBColor(0xC3, 0xB9, 0xB9))
    state_items += [d, nmt, dst]

# card à direita com a tese
thesis = card(s, 9.60, 2.12, 2.83, 4.35, fill=WHITE)
th1 = txt(s, 9.88, 2.42, 2.3, 0.5, "Ninguém faz\nos dois juntos.", size=15,
          color=INK, bold=True, line_spacing=1.05)
th2 = txt(s, 9.88, 3.24, 2.32, 1.05,
          "Marketplaces têm alcance e não verificam. Lojas têm confiança e "
          "não têm tráfego de atleta.", size=9.4, color=INK2, line_spacing=1.3)
pill_items = []
for i, (label, col) in enumerate([("verificação", CORAL), ("reputação", MINT),
                                  ("custódia", LAV)]):
    y = 4.42 + i * 0.44
    pl = shape(s, "round", 9.88, y, 2.10, 0.34, fill=col, radius=0.5,
               alpha=75)
    pt2 = txt(s, 9.98, y, 1.90, 0.34, label, size=7.6, color=INK, bold=True,
              spc=1.2, anchor="m")
    pill_items += [pl, pt2]
th3 = shape(s, "round", 9.88, 5.72, 2.25, 0.44, fill=INK, radius=0.3)
th4 = txt(s, 9.88, 5.72, 2.25, 0.44, "os três juntos", size=8.2,
          color=WHITE, bold=True, align="c", anchor="m", spc=1.0)

animate(s, cascade(head, 60, 100, "rise", 520) +
        [(lt, "fade", 200, 400)] +
        cascade(ver_items, 280, 55, "rise", 480) +
        [(panel, "zoom", 560, 650), (pt, "fade", 700, 400)] +
        cascade(state_items, 760, 60, "fade", 420) +
        [(thesis, "left", 900, 600), (th1, "fade", 1000, 400),
         (th2, "fade", 1080, 400)] +
        cascade(pill_items, 1140, 90, "rise", 450) +
        [(th3, "zoom", 1500, 500), (th4, "fade", 1600, 400)])
transition(s, "fade")
notes(s, (
    "DIFERENCIAL (1min30).\n"
    "• A frase-chave: confiança não é selo, é fluxo de dinheiro e de "
    "informação.\n"
    "• Verificação sem custódia não protege o pagamento; custódia sem "
    "verificação não protege o produto."
))
chrome(s, 8, TOTAL, "Diferencial")

# =====================================================================
# 09 — MODELO DE NEGÓCIO
# =====================================================================
s = blank(prs)
deco = [shape(s, "oval", 12.1, 0.4, 1.9, 1.9, fill=MINT, alpha=45)]
head = title_block(s, "Modelo de negócio", "Como o dinheiro entra.",
                   "Receita no fluxo, não em mensalidade do atleta.")

REV = [
    ("Comissão por venda", "6% a 10% do valor da transação, descontados no repasse ao vendedor.", "RECEITA PRINCIPAL", CORAL),
    ("Destaque de loja", "Assinatura mensal para vitrine, selo e prioridade na busca.", "RECORRENTE", MINT),
    ("Serviços esportivos", "Fotografia, laudo de autenticidade e eventos com parceiros.", "EXPANSÃO", LAV),
]
cards = []
METRICS = ["6–10%", "R$ 99/mês", "20%"]
for i, (nm, ds, tag, col) in enumerate(REV):
    x = 0.9 + i * 3.83
    c = card(s, x, 2.32, 3.55, 2.78, fill=WHITE)
    top = shape(s, "round", x, 2.32, 3.55, 0.16, fill=col, radius=0.3)
    nmt = txt(s, x + 0.32, 2.60, 2.9, 0.34, nm, size=13.2, color=INK, bold=True)
    dst = txt(s, x + 0.32, 3.00, 2.88, 0.78, ds, size=9.4, color=INK2,
              line_spacing=1.26)
    shape(s, "rect", x + 0.32, 3.92, 2.55, 0.008, fill=LINE)
    mv = txt(s, x + 0.32, 4.04, 1.75, 0.45, METRICS[i], size=20, color=INK,
             bold=True, spc=-0.4)
    tg = chip(s, x + 0.32, 4.52, 1.75, 0.30, tag, col, color=INK, size=6.6,
              spc=1.2)
    cards += [c, top, nmt, dst, mv, tg]

unit = card(s, 0.9, 5.40, 11.53, 1.30, fill=INK)
ulabel = txt(s, 1.22, 5.58, 2.0, 0.25, "EXEMPLO ILUSTRATIVO", size=7.6,
             color=RGBColor(0xFF, 0xC9, 0xC9), bold=True, spc=1.8)
STATS = [("R$ 480", "ticket médio"), ("8%", "take rate"),
         ("R$ 38", "receita / pedido"), ("R$ 60", "CAC alvo")]
stat_items = []
for i, (v, l) in enumerate(STATS):
    x = 3.35 + i * 2.42
    vt = txt(s, x, 5.62, 2.0, 0.42, v, size=19, color=WHITE, bold=True)
    lt2 = txt(s, x, 6.06, 2.0, 0.25, l, size=8.4, color=RGBColor(0xC3, 0xB9, 0xB9),
              spc=1.2)
    stat_items += [vt, lt2]

animate(s, cascade(deco, 0, 0, "zoom", 700) +
        cascade(head, 60, 100, "rise", 520) +
        cascade(cards, 300, 55, "rise", 500) +
        [(unit, "zoom", 820, 600), (ulabel, "fade", 920, 400)] +
        cascade(stat_items, 980, 80, "fade", 420))
transition(s, "push")
notes(s, (
    "MODELO (1min30).\n"
    "• Receita principal é comissão; assinatura de loja e serviços são "
    "alavancas.\n"
    "• Os números do rodapé são exemplo — troque pelos seus antes da banca.\n"
    "• Se perguntarem de margem: custo dominante é pagamento + suporte de "
    "disputa."
))
chrome(s, 9, TOTAL, "Modelo de negócio")

# =====================================================================
# 10 — POSICIONAMENTO
# =====================================================================
s = blank(prs)
head = title_block(s, "Posicionamento", "Onde ninguém está.")

mx, my, mw, mh = 1.05, 2.28, 7.65, 4.35
quads = [
    (mx, my, mw / 2, mh / 2, RGBColor(0xF6, 0xEF, 0xF1)),
    (mx + mw / 2, my, mw / 2, mh / 2, RGBColor(0xEC, 0xF6, 0xF0)),
    (mx, my + mh / 2, mw / 2, mh / 2, RGBColor(0xF2, 0xF0, 0xF8)),
    (mx + mw / 2, my + mh / 2, mw / 2, mh / 2, RGBColor(0xFB, 0xF3, 0xE4)),
]
mats = []
for x, y, w, h, c in quads:
    mats.append(shape(s, "rect", x, y, w, h, fill=c))
mats.append(shape(s, "rect", mx + mw / 2 - 0.006, my, 0.012, mh, fill=INK, alpha=18))
mats.append(shape(s, "rect", mx, my + mh / 2 - 0.006, mw, 0.012, fill=INK, alpha=18))
mats.append(shape(s, "rect", mx, my + mh, mw, 0.02, fill=INK, alpha=40))
mats.append(shape(s, "rect", mx, my, 0.02, mh, fill=INK, alpha=40))

axis_x = txt(s, mx, my + mh + 0.12, mw - 0.25, 0.25, "ALCANCE E TRÁFEGO",
             size=7.4, color=MUTED, bold=True, spc=1.8, align="r")
arrow_x = shape(s, "tri", mx + mw - 0.16, my + mh + 0.17, 0.11, 0.11,
                fill=MUTED, rot=90)
axis_y = txt(s, mx, my - 0.30, 3.0, 0.25, "CONFIANÇA", size=7.4, color=MUTED,
             bold=True, spc=1.8)
arrow_y = shape(s, "tri", mx + 0.94, my - 0.27, 0.11, 0.11, fill=MUTED)

# concorrentes
comp = []
comp.append((shape(s, "oval", 3.05, 4.95, 0.34, 0.34, fill=MUTED, alpha=70),
             txt(s, 3.45, 4.92, 2.4, 0.3, "classificados", size=8.6, color=MUTED)))
comp.append((shape(s, "oval", 1.55, 2.85, 0.34, 0.34, fill=MUTED, alpha=70),
             txt(s, 1.95, 2.82, 2.4, 0.3, "lojas próprias", size=8.6, color=MUTED)))
comp.append((shape(s, "oval", 5.55, 4.25, 0.34, 0.34, fill=MUTED, alpha=70),
             txt(s, 5.95, 4.22, 2.6, 0.3, "marketplaces genéricos", size=8.6, color=MUTED)))

star = shape(s, "oval", 7.30, 2.72, 0.30, 0.30, fill=CORAL_D)
ring1 = shape(s, "oval", 7.02, 2.44, 0.86, 0.86, fill=None, line=CORAL_D, lw=1.5, line_alpha=45)
ring2 = shape(s, "oval", 6.72, 2.14, 1.46, 1.46, fill=None, line=CORAL_D, lw=1.2, line_alpha=25)
lbl = txt(s, 6.55, 1.72, 2.4, 0.3, "CoreMotion", size=11.5, color=INK, bold=True)

# lateral
side = []
SIDE = ["Marketplaces genéricos têm alcance, mas não verificam quem vende.",
        "Lojas próprias têm confiança, mas não têm tráfego de atleta.",
        "CoreMotion junta os dois — e ainda segura o dinheiro."]
for i, t in enumerate(SIDE):
    y = 2.42 + i * 1.28
    dot = shape(s, "oval", 9.35, y + 0.10, 0.12, 0.12, fill=[MUTED, MUTED, CORAL_D][i])
    tx = txt(s, 9.62, y, 2.92, 1.0, t, size=10.2, color=INK if i == 2 else INK2,
             bold=(i == 2), line_spacing=1.28)
    side += [dot, tx]

animate(s, cascade(head, 60, 100, "rise", 520) +
        [(m, "fade", 200 + i * 40, 500) for i, m in enumerate(mats)] +
        [(axis_x, "fade", 420, 400), (axis_y, "fade", 420, 400),
         (arrow_x, "fade", 460, 400), (arrow_y, "fade", 460, 400)] +
        [(c[0], "zoom", 520 + i * 90, 450) for i, c in enumerate(comp)] +
        [(c[1], "fade", 560 + i * 90, 400) for i, c in enumerate(comp)] +
        [(ring2, "zoom", 900, 700), (ring1, "zoom", 960, 600),
         (star, "zoom", 1020, 500), (lbl, "fade", 1100, 400)] +
        cascade(side, 1160, 90, "left", 520))
transition(s, "fade")
notes(s, (
    "POSICIONAMENTO (1min).\n"
    "• O eixo vertical é confiança; o horizontal é alcance.\n"
    "• O quadrante superior direito está vazio — é onde o CoreMotion quer "
    "estar.\n"
    "• Não citar concorrentes por nome."
))
chrome(s, 10, TOTAL, "Posicionamento")

# =====================================================================
# 11 — ROADMAP
# =====================================================================
s = blank(prs)
head = title_block(s, "Roadmap", "Do MVP à escala.",
                   "Quatro fases, cada uma com uma pergunta a responder.")

base_y = 6.15
PH = [
    ("AGORA", "Fase 1", "MVP: catálogo, verificação manual e custódia.", 2.05, CORAL),
    ("PRÓXIMO", "Fase 2", "Checkout completo, reputação e painel da loja.", 2.62, BUTTER),
    ("DEPOIS", "Fase 3", "App do atleta, disputas e logística parceira.", 3.12, MINT),
    ("ESCALA", "Fase 4", "Expansão regional e serviços esportivos.", 3.60, LAV),
]
bars = []
for i, (tag, phase, desc, h, col) in enumerate(PH):
    x = 0.9 + i * 2.94
    b = shape(s, "round", x, base_y - h, 2.2, h, fill=col, radius=0.07, shadow=True)
    tg = txt(s, x + 0.22, base_y - h + 0.24, 1.75, 0.25, tag, size=7.8,
             color=INK, bold=True, spc=2.0)
    ph = txt(s, x + 0.22, base_y - h + 0.56, 1.75, 0.26, phase, size=9.5,
             color=INK2, bold=True)
    ds = txt(s, x + 0.22, base_y - h + 0.88, 1.78, 0.75, desc, size=8.6,
             color=INK2, line_spacing=1.25)
    bars += [b, tg, ph, ds]

base = shape(s, "rect", 0.9, base_y, 11.5, 0.02, fill=INK, alpha=35)

animate(s, cascade(head, 60, 100, "rise", 520) +
        [(base, "wipe", 250, 700)] +
        [(b, "wipeup", 380 + i * 130, 750) for i, b in enumerate(bars[::4])] +
        [(b, "fade", 700 + i * 60, 400) for i, b in enumerate(bars) if b not in bars[::4]])
transition(s, "wipe")
notes(s, (
    "ROADMAP (1min).\n"
    "• Cada fase responde uma pergunta: dá para vender? dá para confiar? "
    "dá para escalar?\n"
    "• A banca quer saber o que você faz nos próximos 90 dias: foque na "
    "Fase 1."
))
chrome(s, 11, TOTAL, "Roadmap")

# =====================================================================
# 12 — ONDE ESTAMOS
# =====================================================================
s = blank(prs)
deco = [shape(s, "oval", -0.9, 5.6, 2.4, 2.4, fill=LAV, alpha=40)]
head = title_block(s, "Onde estamos", "O que já existe, de verdade.")

STAT = [
    ("Produto", "Fluxos de catálogo, loja e checkout desenhados; identidade visual e telas definidas.", CORAL, "oval"),
    ("Técnica", "Next.js 15 + TypeScript + Supabase. Build e type-check passando no repositório.", MINT, "hex"),
    ("Operação", "Quatro frentes independentes, com contratos de integração escritos.", LAV, "diamond"),
]
cards = []
for i, (nm, ds, col, ic) in enumerate(STAT):
    x = 0.9 + i * 3.83
    c = card(s, x, 2.35, 3.55, 2.45, fill=WHITE)
    icirc = shape(s, "oval", x + 0.30, 2.62, 0.66, 0.66, fill=col)
    ish = shape(s, ic, x + 0.45, 2.77, 0.36, 0.36, fill=INK, alpha=75)
    nmt = txt(s, x + 1.10, 2.72, 2.2, 0.35, nm, size=14, color=INK, bold=True)
    dst = txt(s, x + 0.30, 3.52, 2.95, 1.1, ds, size=10, color=INK2, line_spacing=1.28)
    cards += [c, icirc, ish, nmt, dst]

band = shape(s, "round", 0.9, 5.18, 11.53, 1.35, fill=INK, radius=0.14)
bt = txt(s, 1.25, 5.38, 10.85, 0.95,
         "Ainda sem tração medida. O que existe é base técnica, produto "
         "desenhado e plano de execução — e é exatamente isso que queremos "
         "validar com você.", size=12.5, color=WHITE, line_spacing=1.3)

animate(s, cascade(deco, 0, 0, "zoom", 700) +
        cascade(head, 60, 100, "rise", 520) +
        cascade(cards, 300, 60, "rise", 500) +
        [(band, "zoom", 850, 600), (bt, "fade", 950, 500)])
transition(s, "fade")
notes(s, (
    "ONDE ESTAMOS (1min).\n"
    "• Transparência total: sem métricas de tração ainda.\n"
    "• O ativo atual é a base técnica e o desenho de produto — isso reduz "
    "risco de execução.\n"
    "• Se a banca valorizar time, emende o próximo slide."
))
chrome(s, 12, TOTAL, "Onde estamos")

# =====================================================================
# 13 — TIME / FRENTES
# =====================================================================
s = blank(prs)
head = title_block(s, "Quem executa", "Quatro frentes, uma entrega.",
                   "Cada frente responde pelo próprio estado, sem esperar liberação.")

TEAM = [
    ("Identidade & acesso", "Sessão, papéis, permissões e painel administrativo.", CORAL),
    ("Catálogo & negócio", "Lojas, produtos, checkout e regras de comissão.", MINT),
    ("Documento & diagramas", "Requisitos, arquitetura e material de apresentação.", BUTTER),
    ("Verificação & entrega", "Ambiente de testes, QA e critérios de aceite.", LAV),
]
cards = []
for i, (nm, ds, col) in enumerate(TEAM):
    x = 0.9 + i * 2.94
    c = card(s, x, 2.38, 2.68, 3.15, fill=WHITE)
    av = shape(s, "oval", x + 0.30, 2.66, 0.92, 0.92, fill=col)
    ini = txt(s, x + 0.30, 2.66, 0.92, 0.92, ["P1", "P2", "P3", "P4"][i],
              size=16, color=INK, bold=True, align="c", anchor="m")
    nmt = txt(s, x + 0.30, 3.70, 2.15, 0.62, nm, size=12.5, color=INK,
              bold=True, line_spacing=1.05)
    dst = txt(s, x + 0.30, 4.34, 2.12, 0.95, ds, size=9.4, color=INK2,
              line_spacing=1.25)
    cards += [c, av, ini, nmt, dst]

note = txt(s, 0.9, 5.86, 11.5, 0.3,
           "Nomes e mini-bios entram na versão final deste slide.",
           size=9.2, color=MUTED, italic=True)

animate(s, cascade(head, 60, 100, "rise", 520) +
        cascade(cards, 300, 60, "rise", 500) +
        [(note, "fade", 980, 400)])
transition(s, "push")
notes(s, (
    "TIME (45s).\n"
    "• Não é 'somos quatro amigos': são quatro responsabilidades com "
    "entregáveis.\n"
    "• Cite rapidamente o que cada um já entregou."
))
chrome(s, 13, TOTAL, "Quem executa")

# =====================================================================
# 14 — O PEDIDO
# =====================================================================
s = blank(prs)
deco = [
    shape(s, "oval", 11.9, -1.0, 2.7, 2.7, fill=CORAL, alpha=45),
    shape(s, "oval", -1.0, 5.9, 2.2, 2.2, fill=MINT, alpha=50),
]
head = title_block(s, "O pedido", "O que precisamos para os próximos 90 dias.")

ASK = [
    ("Piloto com 5 lojas", "Acesso a lojas esportivas para validar verificação e custódia com vendas reais.", "REDE", CORAL),
    ("R$ 300 mil", "Produto, operação e marketing do piloto. Ajuste o valor ao seu plano.", "INVESTIMENTO", BUTTER),
    ("Dois conselheiros", "Marketplace e operação de pagamentos, com uma conversa por mês.", "MENTORIA", LAV),
]
cards = []
for i, (nm, ds, tag, col) in enumerate(ASK):
    x = 0.9 + i * 3.83
    c = card(s, x, 2.42, 3.55, 2.85, fill=WHITE)
    banda = shape(s, "round", x, 2.42, 3.55, 0.14, fill=col, radius=0.3)
    tg = txt(s, x + 0.32, 2.72, 2.9, 0.25, tag, size=7.4, color=MUTED, bold=True, spc=2.0)
    nmt = txt(s, x + 0.32, 3.00, 2.9, 0.5, nm, size=17, color=INK, bold=True)
    dst = txt(s, x + 0.32, 3.62, 2.9, 1.35, ds, size=9.8, color=INK2, line_spacing=1.3)
    cards += [c, banda, tg, nmt, dst]

goal = shape(s, "round", 0.9, 5.62, 11.53, 0.92, fill=INK, radius=0.2)
gt = txt(s, 1.25, 5.62, 10.9, 0.92,
         "META DO PILOTO   ·   5 lojas   ·   300 pedidos   ·   100% com custódia   ·   90 dias",
         size=12, color=WHITE, bold=True, spc=0.8, anchor="m")

animate(s, cascade(deco, 0, 0, "zoom", 700) +
        cascade(head, 60, 100, "rise", 520) +
        cascade(cards, 300, 60, "rise", 500) +
        [(goal, "zoom", 900, 600), (gt, "fade", 1000, 500)])
transition(s, "fade")
notes(s, (
    "O PEDIDO (1min30).\n"
    "• Seja direto: 5 lojas, investimento e dois conselheiros.\n"
    "• Ajuste R$ 300 mil ao seu plano antes de apresentar.\n"
    "• Se a banca não puder investir, peça a conexão com uma loja — o pedido "
    "tem três portas de entrada."
))
chrome(s, 14, TOTAL, "O pedido")

# =====================================================================
# 15 — OBRIGADO
# =====================================================================
s = blank(prs)
s.background.fill.solid()
s.background.fill.fore_color.rgb = INK
geo = [
    shape(s, "oval", 8.9, -1.9, 6.2, 6.2, fill=CORAL, alpha=55),
    shape(s, "oval", 10.55, 2.7, 3.6, 3.6, fill=MINT, alpha=58),
    shape(s, "oval", 7.95, 4.55, 2.6, 2.6, fill=None, line=BUTTER, lw=2,
          line_alpha=80),
    shape(s, "tri", 11.35, 5.35, 1.15, 1.15, fill=BUTTER, alpha=85, rot=18),
    shape(s, "oval", 9.6, 0.45, 0.28, 0.28, fill=WHITE, alpha=70),
    shape(s, "oval", 12.35, 2.1, 0.16, 0.16, fill=WHITE, alpha=50),
]
kick = txt(s, 0.9, 1.42, 6.0, 0.28, "COREMOTION · 2026", size=9, color=BUTTER,
           bold=True, spc=2.6)
big = txt(s, 0.9, 1.92, 7.6, 1.3, "Obrigado.", size=76, color=WHITE, bold=True,
          spc=-1.8)
sub2 = txt(s, 0.9, 3.30, 6.4, 1.15,
           "Vamos construir o ponto de encontro\ndo esporte de alta performance?",
           size=20, color=RGBColor(0xE8, 0xE2, 0xDC), line_spacing=1.22)
crule = shape(s, "round", 0.96, 4.72, 1.4, 0.05, fill=CORAL_D, radius=0.5)
contact = txt(s, 0.9, 4.98, 6.6, 0.9,
              "[seu@email.com]   ·   [telefone]   ·   [site]", size=12,
              color=RGBColor(0xC9, 0xC2, 0xBA), bold=True, spc=0.6)
end = txt(s, 0.9, 6.55, 7.0, 0.3,
          "Obrigado pela leitura. Perguntas, agora.", size=9.5,
          color=RGBColor(0x9A, 0x94, 0x8E))

animate(s, cascade(geo, 0, 100, "zoom", 900) +
        [(kick, "fade", 100, 500), (big, "rise", 180, 750),
         (sub2, "rise", 420, 650), (crule, "wipe", 620, 500),
         (contact, "fade", 780, 500), (end, "fade", 900, 500)])
transition(s, "fade")
notes(s, (
    "FECHAMENTO (30s).\n"
    "• Pare de falar depois do 'obrigado'. Deixe a banca perguntar.\n"
    "• Tenha à mão: custo de aquisição, plano de 90 dias e a lista de lojas "
    "que já disseram sim."
))
chrome(s, 15, TOTAL, "Obrigado", accent=CORAL, dark=True)

prs.core_properties.title = "CoreMotion — Pitch para banca"
prs.core_properties.author = "CoreMotion"
prs.core_properties.subject = "Marketplace esportivo de alta performance"
prs.core_properties.language = "pt-BR"

out = sys.argv[1] if len(sys.argv) > 1 else "../CoreMotion-Pitch-Banca.pptx"
prs.save(out)
print("salvo:", out, "| slides:", len(prs.slides.__iter__.__self__._sldIdLst))
