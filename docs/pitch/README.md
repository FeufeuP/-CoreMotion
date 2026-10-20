# CoreMotion — Pitch

Material de apresentação para a banca: 15 slides, tema neo-brutalista (branco/preto,
`#FF3333` / `#FFFF00` / `#0066FF` / `#00CC00` / `#CC00CC`, cantos retos, sombra dura),
DM Sans + Space Mono.

## Entregáveis

| Arquivo | O que é |
|---|---|
| `CoreMotion-Pitch-Banca.pptx` | deck editável, animações em cascata e transições |
| `CoreMotion-Pitch-Banca.pdf` | backup fiel, 15 páginas a 200 DPI |
| `CoreMotion-Pitch-Web.html` | deck web cinemático, arquivo único com fontes embutidas |
| `CoreMotion-Pitch-Previa.png` | grade de contato 3×5 com os 15 slides |
| `CoreMotion-Pitch-Roteiro.md` | fala, tempo e checklist de véspera |
| `PENDENCIAS.md` | o que ficou para depois e o que precisa ser conferido |

## Movimento e transições

O deck foi tunado para transmitir **velocidade e esporte** sem perder o tema
neo-brutalista:

- **Transição `morph` (mesclagem) em todos os slides** — p159 (PowerPoint
  2016+): os objetos de cada slide **se transformam nos do próximo**, de forma
  fluida. Os pares casam por nome (`CM!!…`): kicker e manchete (`CM!!kick`/
  `CM!!head`) deslizam entre os títulos, o chrome (ponto, marca, contador, fio)
  permanece vivo e, no fechamento, a faixa preta "meta 90 dias" do slide 14
  **toma a tela inteira** e vira o fundo do "Obrigado". Versões antigas caem em
  fade. (Também dá para trocar por `flash`, `vortex`, `conveyor` etc. — o motor
  já suporta.)
- **Efeitos de entrada** — além de `fade/rise/zoom/wipe`, o motor tem
  `whip` (entra esticado, como rastro), `speed`/`boost` (chega freando com
  ultrapassagem), `spin` (assenta girando) e `race` (trajeto de corrida — a
  bolinha vermelha do slide 6 corre o fluxo de pedido até o repasse).
- **Kit esportivo** (`brutal_lib.py`) — `speed_streaks` (rastros de
  movimento), `chevrons` (>>> de ritmo), `checkered` (bandeira de largada:
  capa, chegada do roadmap, fechamento), `speedometer` (velocímetro na capa,
  no take rate e no "obrigado") e `ghost` (palavras gigantes em 6% —
  VELOCIDADE, GO, ATRITO, 90 DIAS…).
- **Equipe no fechamento** — dorsais do grupo (Alfeu N1, André N2, Bruno N3,
  Marcus N18, Mattheus N22) nas cores da identidade.
- **Morph pairing** — shapes com nomes `CM!!…` casam entre slides para o morph
  mover de verdade.

Animações ficam no XML nativo de timing (`p:timing`), então abrem em qualquer
PowerPoint 2010+; transições p14/p159 exigem PowerPoint 2010/2016+ e degradam
graciosamente em alternativas padrão.

## Como regerar

```bash
cd docs/pitch

# PPTX (requer python-pptx + lxml)
python build_brutal.py CoreMotion-Pitch-Banca.pptx

# PNGs por slide (requer Pillow + fontes DM Sans/Space Mono instaladas)
python render.py CoreMotion-Pitch-Banca.pptx ../out 200

# Deck web (concatena web/src/* em um HTML autocontido)
python web/build_web.py
```

O PDF e a prévia saem dos PNGs gerados por `render.py`:

```python
from PIL import Image
import glob
ims = [Image.open(f) for f in sorted(glob.glob("out/slide-*.png"))]
ims[0].save("CoreMotion-Pitch-Banca.pdf", save_all=True,
            append_images=ims[1:], resolution=200.0)
```

`render.py` lê DM Sans e Space Mono em `/tmp/fonts` e, sem elas, cai para Arimo em `/tmp/arimo`
(métricas próximas de Arial) — nesse caso a prévia não bate com o PowerPoint.

## Estrutura do deck web

`web/src/` guarda as partes soltas — `base.css` (tokens e motion), `scenes1..4.css`,
`ui.css` (índice e transições), `01_hero.html` … `05_team.html` (as 15 cenas), `app.js`
(navegação, parallax, loops de custódia) e `fonts.css` (base64). Edite a parte e rode
`python web/build_web.py`.

Atalhos: `←`/`→`/espaço` navegam, `Home`/`End` vão aos extremos, `M` abre o índice,
`Esc` fecha. `#s7` no final da URL abre direto na cena.

## Histórico

`build_deck.py` + `deck_lib.py` geram a versão pastel anterior. Ficaram no repositório como
histórico; não são usados pelo deck atual.
