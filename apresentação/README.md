# CoreMotion — Pitch

Material de apresentação para a banca: **16 slides em 16:9**, tema escuro neo-brutalista,
acentos `#FF3333` / `#FFFF00` / `#0066FF` / `#00CC00` / `#CC00CC`, cantos retos,
sombra dura, DM Sans + Space Mono.

O HTML, o PowerPoint e o PDF agora têm 16 páginas, a abertura de marca e tema escuro.
O arquivo único HTML contém a interface PowerPoint-like completa, controles, slides, fontes,
CSS e JavaScript; os itens esportivos 3D flutuam nele. O PPTX conserva formas e transições nativas.

## Entregáveis

| Arquivo | O que é |
|---|---|
| `CoreMotion-Pitch-Banca.pptx` | deck editável, animações em cascata e transições |
| `CoreMotion-Pitch-Banca.pdf` | backup estático, 16 páginas em 16:9 |
| `CoreMotion-Pitch.html` | arquivo HTML autônomo (CSS, JS, fontes e 16 slides embutidos; ~291 KB) |
| `CoreMotion-Pitch-Previa.png` | grade de contato 4×4 com os 16 slides |
| `CoreMotion-Pitch-Roteiro.md` | fala, tempo e checklist de véspera |
| `PENDENCIAS.md` | o que ficou para depois e o que precisa ser conferido |

## Interface e apresentação

Antes da tela cheia, o HTML mostra a interface completa inspirada no PowerPoint: barra de título
com nome/estado do arquivo, pesquisa e ações; abas e faixa de opções; miniaturas dos 16 slides à
esquerda; canvas central 16:9; área de anotações e barra inferior de status/zoom. Os botões de
edição são visuais; as miniaturas navegam entre slides. O canvas fica reduzido proporcionalmente
para caber na área de edição, sem cortar o slide.

Use **▶ Apresentar** (barra superior para o slide atual, ou “Do início” na faixa) — ou `F5` para
começar do slide 1, `Shift+F5` para começar do slide atual. Em tela cheia, a interface de edição
some e aparece o **HUD do modo de apresentação** no canto inferior esquerdo:

```
  ‹  ›   |   ✎  ▦  ⌕  CC   |   ⋯
```

- **Funciona:** ← → (barra e teclado), passar slides por clique, `←→↑↓`/`Espaço`/`Enter`/
  `PageUp`/`PageDown`/`Backspace`/`N`/`P`, roda do mouse (um slide por gesto), swipe,
  `Home`/`End`, ir para o slide digitando o número + `Enter`, menu `⋯` com **Encerrar
  apresentação** e `Esc`.
- Caneta/apontador, ver todos, zoom, legendas, pesquisa, comentários e comandos da faixa são
  somente representações visuais; não executam ferramentas de edição.
- A barra aparece com o mouse e some depois de 2,8 s parado; o cursor some depois de 2,2 s,
  como no PowerPoint.

## Formato: slides PowerPoint 16:9, não site

A apresentação web é um **palco fixo 16:9** (`#deck`) com uma cena visível por vez,
letterbox preto quando a janela não é 16:9 e transição curta de slide — sem rolagem
livre nem cartões de página. O canvas e os controles ficam ancorados na área 16:9.
A navegação é pelo HUD/teclado, clique, roda ou swipe; `Home`/`End` vão ao início/fim.

O PowerPoint e o PDF também foram reconstruídos com 16 slides, incluindo a nova abertura.
Teste Chromium: 16 slides, 16:9 em 1920×1080, 1440×810, 1366×768 e 1280×720; auditoria
por slide confirmou que nenhum elemento textual ultrapassa a página, tanto no canvas de edição
quanto em tela cheia a 1280×720.

## HUD (o chrome do PPTX)

O cabeçalho é o mesmo `chrome()` do `brutal_lib.py`, reproduzido em CSS:
quadrado de accent + **COREMOTION** em Space Mono caixa-alta com tracking,
**SEÇÃO · 01/16** alinhado à direita e o fio inferior de ponta a ponta — que
aqui também mostra o progresso em vermelho. Em fundo vermelho/azul o quadrado
mantém contraste no fundo escuro. A seção, o número atual e o total são atualizados
a cada navegação e permanecem no slide também no modo de edição.

## Abertura de marca (`#s0`)

O deck web abre numa cena só de marca: monograma **CM** + assinatura **CoreMotion.** centralizados,
fio vermelho e a frase de efeito **“Entre em movimento.”** — o equivalente ao *Just do it*.

O reveal é montado em camadas independentes, todas disparadas quando a cena entra em cena
(`.s0.on`), em `scenes0.css`:

| camada | o que faz | quando |
|---|---|---|
| `.s0__wipe` | painel vermelho que sobe e descobre o slide | 0,20 s |
| `.s0__mark` | monograma entra com escala + rotação | 0,62 s |
| `s0Shine` | brilho atravessa o monograma | 1,25 s |
| `.s0__word` | assinatura é revelada por clip-path da esquerda | 0,82 s |
| `.s0__rule` | fio cresce do centro | 1,12 s |
| `.s0__slogan` | frase sobe por trás da máscara `.line` | 1,22 s |
| `.s0__sub` | linha de apoio aparece | 1,45 s |

Trocar a animação é mexer só nos `@keyframes s0*` e nos `animation-delay` desse bloco —
o HTML (`00_cover.html`) e a estrutura da cena não mudam.

## Decoração 3D (todos os slides, menos o último)

Cada cena recebe uma camada `.fx3d` com peças soltas de esporte — tênis, camisa, boné,
garrafa, mochila, medalha, relógio, faixa, óculos, halter, bola e raquete. Elas ficam **atrás
do conteúdo**, atravessam a cena devagar de um lado para o outro e giram em perspectiva 3D.

- **Cor por peça, sortida da paleta:** cada item recebe **uma** cor (`--fx`, inline) sorteada
  entre as cores que existem em cada fundo — `PALETTES` em `app.js`. Nunca é a cor do fundo:
  em todos os fundos escuros entram vermelho/azul/verde/magenta/amarelo/branco, sem preto
  invisível; fundos de destaque também preservam contraste.
  A variedade é garantida por sorteio sem repetição (sacola embaralhada de cores).
- **Relevo 3D:** cada símbolo é a face + 5 cópias deslocadas, todas na mesma cor — o efeito de
  bloco extrudado, sem gradiente. Como as peças atravessam a borda do slide, a camada tem uma
  máscara suave nas bordas para não virar faixa de cor.
- **Posições, tamanho, direção, velocidade e eixo de giro são sorteados** por um PRNG com
  semente fixa por cena (`mulberry32` em `app.js`): o arranjo é reproduzível e cada slide tem
  trajetórias diagonais diferentes. As peças flutuam em ciclos de 8–17 s dentro do canvas.
- **Sem repetição dentro da mesma cena** e, no máximo, 7 peças (4 no celular, 5 na capa).
- Opacidade reforçada (`--fxo` 45%–68%, ajustada por cena): visível sobre o fundo escuro sem
  passar à frente do texto.
- Pausam fora da tela (economia de bateria) e somem na impressão/`prefers-reduced-motion`.

Desligar numa cena: `data-fx="off"` na `<section>` (é o que o último slide usa). Na capa de
marca, `data-fx="soft"` deixa as peças menores e mais discretas.

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
cd apresentação

# PPTX (requer python-pptx + lxml)
python build_brutal.py CoreMotion-Pitch-Banca.pptx

# PNGs por slide (requer Pillow + fontes DM Sans/Space Mono instaladas)
python render.py CoreMotion-Pitch-Banca.pptx out 200

# Deck web (concatena web/src/* em um HTML autocontido)
python web/build_web.py
```

O PDF e a prévia são imagens estáticas derivadas dos PNGs gerados por `render.py`:

```python
from PIL import Image
import glob
ims = [Image.open(f) for f in sorted(glob.glob("out/slide-*.png"))]
ims[0].save("CoreMotion-Pitch-Banca.pdf", save_all=True,
            append_images=ims[1:], resolution=200.0)
```

`render.py` lê DM Sans e Space Mono em `/tmp/fonts` e, sem elas, cai para Arimo em `/tmp/arimo`
(métricas próximas de Arial) — nesse caso a prévia não bate com o PowerPoint.

## Arquivo único e código-fonte

Para apresentar ou compartilhar, basta abrir `CoreMotion-Pitch.html`: é um arquivo compacto (~291 KB) e
independente, sem chamadas externas e sem exigir pasta de assets. Ele incorpora a interface,
CSS, JavaScript, fontes e slides. Os fontes editáveis continuam aqui na pasta `web/src/` para
manutenção. Gere o HTML com `python web/build_web.py`.

`web/src/` guarda as partes soltas — `base.css` (tokens, motion, HUD e fio),
`scenes0..4.css`, `slide.css` (canvas 16:9 e tema escuro), `fx.css` (decoração 3D),
`present.css` (botão Apresentar e HUD),
`ui.css` (índice e transições), `00_cover.html` (abertura de marca),
`01_hero.html` … `05_team.html` (as demais 15 cenas), `app.js` (navegação, parallax, sprite
3D, loops de custódia) e `fonts.css` (base64). Edite a parte e rode `python web/build_web.py`.

Atalhos: `←`/`→`/espaço` navegam, `Home`/`End` vão aos extremos, `M` abre o índice,
`Esc` fecha. `#s7` no final da URL abre direto na cena.

## Histórico

`build_deck.py` + `deck_lib.py` geram a versão pastel anterior. Ficaram no repositório como
histórico; não são usados pelo deck atual.
