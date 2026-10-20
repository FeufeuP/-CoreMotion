# CoreMotion — Pitch: o que ficou para depois

Registro do que **não** foi feito nesta rodada, do que foi feito pela metade de propósito e do
que precisa ser conferido por uma pessoa antes da banca. Complementa o
[`CoreMotion-Pitch-Roteiro.md`](CoreMotion-Pitch-Roteiro.md), que cobre o conteúdo falado.

**Última atualização:** 2026-10-20 · branch `arena/c1445c41-coremotion`

---

## 1. Adiado por decisão

### 1.1 Logo / identidade da marca

O pedido veio junto com a reestilização do deck e foi explicitamente deixado para depois
(“pensamos nisto depois”). O que existe hoje é um **lockup provisório no deck web**: o quadrado
vermelho com o monograma **CM** (a mesma marca já usada no header do site, `components/Sidebar.tsx`)
ao lado da assinatura **CoreMotion.** em DM Sans. Serve para apresentar, mas não é a logo final.

Está travado por quatro respostas que só você tem:

| # | Pergunta | Por que trava |
|---|---|---|
| 1 | O nome continua **CoreMotion**? | Nome define som, sílabas e espaço no lockup |
| 2 | Três palavras que a marca precisa transmitir | Separa “performance técnica” de “comunidade/confiança” |
| 3 | Referências visuais que você gosta (e alguma que odeia) | Evita 3 rodadas de tentativa e erro |
| 4 | Onde ela aparece primeiro (site, Instagram, camiseta, embalagem) | Muda o desenho: ícone pequeno ≠ assinatura horizontal |

**Trocar o lockup provisório** é mexer em `web/src/00_cover.html` (bloco `.s0__lockup`) e nos
tamanhos em `web/src/scenes0.css` — o resto da cena não depende dele.

Quando isso voltar, o caminho sugerido é: 3 direções conceituais em preto e branco →
1 escolhida → refino com cor, versões (horizontal, empilhada, ícone), arquivos SVG/PNG e
aplicação no deck e no favicon. O logo entra no lugar do marcador quadrado vermelho do
cabeçalho (`chrome()` no PPTX, `.hud__brand i` no deck web).

### 1.2 Capa e encerramento com dados reais

A capa já está limpa (a faixa “Apresentado por…” foi removida a pedido). O slide 16 usa os
contatos informados: **alfeuvlp@gmail.com** e **41 9 9893-8283** (também no gerador do PPTX).
O site não foi informado e saiu da lista — quando existir, entra ao lado do telefone.

### 1.3 Animação de reveal da logo

O slide `00` já tem uma animação de aparição completa (cortina vermelha → monograma → brilho →
assinatura por clip-path → fio → frase), documentada no `README.md`. **A animação “especificada
depois” ainda não chegou**; quando chegar, troca-se só o bloco `@keyframes s0*` e os
`animation-delay` em `web/src/scenes0.css`.

- [ ] Definir o comportamento desejado (ex.: traço desenhado, letras caindo, glitch, contador)
- [ ] Definir se roda **toda vez** que a cena entra ou **só na abertura** do deck (hoje roda
      toda vez que o slide volta ao centro)

### 1.4 Interface de edição e HUD PowerPoint

Antes da apresentação, o arquivo único mostra uma interface completa inspirada no PowerPoint:
barra do aplicativo, nome/estado do arquivo, abas/faixa de opções, miniaturas navegáveis,
canvas de slide, notas e barra inferior. Os comandos de edição são somente visuais.

Ao apresentar, a interface recolhe e aparece o HUD inferior do modo de apresentação. Funcionam
apenas iniciar/sair da tela cheia e navegação; os ícones/ferramentas de edição permanecem visuais.

- [x] Botões Apresentar, miniaturas, F5/Shift+F5, setas, clique, roda, swipe, Home/End e Esc
- [x] Tela cheia real e retorno à interface de edição testados no Chromium
- [x] Arquivo HTML autocontido com fontes, JS, CSS e slides, sem dependências externas
- [ ] Testar o botão de tela cheia no navegador/projetor da banca (o navegador pode bloquear fullscreen em iframe)

### 1.5 Formato PowerPoint 16:9, tema escuro e enquadramento (feito)

HTML, PPTX e PDF agora têm **16 páginas em 16:9** e fundo escuro uniforme. O deck web tem
palco fixo, uma cena por vez e controles ancorados ao canvas; o PPTX foi reconstruído com
capa igual em conceito e superfícies escuras. A página 16 é o fechamento com os contatos reais.

- [x] Palco 16:9 com ajuste proporcional à área, sem rolagem e sem cortar a composição
- [x] Auditoria de limites: textos das 16 cenas cabem em edição (1440×810) e apresentação (1280×720)
- [x] Rebuild do PPTX: 16 slides, 13,333×7,5 pol, backgrounds escuros e abertura de marca
- [x] PDF estático reconstruído em 16 páginas
- [ ] Conferir a abertura e as fontes no PowerPoint/Keynote da banca
- [ ] Confirmar no projetor 16:9 que HUD e botões estão dentro da área útil

### 1.6 Decoração 3D

No HTML, itens esportivos coloridos ficam atrás do conteúdo e flutuam em direções diagonais
aleatórias dentro do slide, com ciclos de 8–17 s. O último slide permanece sem decoração.
No PPTX os grafismos são estáticos: as animações 3D aleatórias são próprias do navegador.

- [x] Mais contraste e movimento verificável no Chromium
- [ ] Conferir a cadência dos itens 3D no projetor da banca

---

## 2. Bloqueia a apresentação (5 minutos de edição)

Trocar nos arquivos `.pptx`, `.html` e no roteiro:

| Campo | Onde aparece |
|---|---|
| `P1`–`P4` + “nome · bio” | slide 14 (time) |
| `R$ 300 mil` | slide 15 — ajustar ao plano real antes de apresentar |

O roteiro já tem um checklist de véspera em `CoreMotion-Pitch-Roteiro.md` (§ “Antes de
apresentar”). Nada disso foi preenchido porque depende de informação que não está no repositório.

---

## 3. Verificar antes de apresentar (não validado aqui)

### 3.1 Deck web em navegador

O Chromium foi executado no sandbox e os 16 slides foram capturados. Canvas 16:9, fundos
escuros, texto dentro dos limites, movimentos 3D e HUD/atalhos foram verificados; console limpo.

O que ainda precisa de olho humano, cena por cena (16 cenas) — o que já foi medido aqui está
marcado:

- [x] Canvas 16:9 em janela 16:10: barras pretas e HUD/controles ancorados ao slide
- [x] Fundo escuro uniforme nas 16 cenas, sem superfícies de tela branca
- [x] Cena 06: texto e fluxo cabem no canvas 16:9 em 1280×720 e 1920×1080
- [x] Cena 08: estados animados continuam quando o slide está ativo e pausam fora dele
- [x] Cena 10: matriz permanece dentro do canvas em 1280×720
- [x] Cena 12: as duas metades preservam contraste no tema escuro
- [x] Abertura (`#s0`): reveal e tagline legíveis no canvas 16:9
- [x] Abertura: reveal reaparece ao reentrar no slide sem sumir o conteúdo
- [x] Decoração 3D: peças atrás do texto em todas as cenas, **nenhuma** na cena 15 (Obrigado)
- [x] Decoração 3D: cada peça com uma cor da paleta, sorteada por cena (medido no Chromium)
- [x] Canvas 16:9: proporção confirmada em 1920×1080, 1600×900, 1440×810, 1366×768 e 1280×720
- [x] HUD: marca, seção e contador legíveis no tema escuro
- [x] Decoração 3D: nada passa por cima de texto (verificado em captura nas cenas 06, 12 e 14)
- [x] Cena 06: o destaque amarelo fecha o texto dentro do cartão em 1280×720 e 1920×1080
- [x] Apresentação: F5/Shift+F5, Esc, clique, teclado, roda, swipe, ir para slide e menu ⋯ (testado no Chromium)
- [x] Navegação: setas, clique, roda, teclado numérico + Enter, hash e tela cheia testados
- [x] `prefers-reduced-motion`: movimentos decorativos e transições são desativados
- [ ] Mobile em retrato: conferir legibilidade da interface compacta

### 3.2 Importação para Google Slides

A cópia “CoreMotion — Pitch (Google Slides)” foi gerada a partir do `.pptx`, mas **não foi
inspecionada slide a slide**. O Google Slides não importa as transições (`cover`/`push`) nem
as animações em cascata — nesse arquivo o deck fica estático. Para apresentar com movimento,
usar o `.pptx` no PowerPoint ou o HTML no navegador.

- [ ] Conferir se nenhuma caixa de texto mudou de tamanho na importação
- [ ] Conferir se as fontes DM Sans / Space Mono aparecem (o Google Slides não tem as duas
      instaladas por padrão)

### 3.3 PPTX no PowerPoint / Keynote

Verificado por render próprio (PIL) e leitura do XML: 16 slides, tamanho 13,333×7,5 pol, tema
escuro, 1 transição + 1 `p:timing` por slide, sombras duras e rotações. **Não** foi aberto no
PowerPoint de verdade.

- [ ] Abrir em modo apresentação e conferir a ordem das cascatas
- [ ] Conferir as transições `cover` com direção (`p14:dur`, requer PowerPoint 2010+)
- [ ] Ver se as fontes estão instaladas na máquina da banca (ou usar o PDF como plano B)

---

## 4. Fora de escopo nesta rodada (consciente)

- **Versão em inglês.**
- **Slides de apêndice** (financeiro detalhado, comparativo de concorrentes, currículos).
  A versão atual tem 16 slides, com abertura alinhada ao deck web.
- **Vídeo / demo gravada** do produto. A cena 07 usa wireframes desenhados, não telas reais.
- **Testes de contraste com leitor de tela** além do que o CSS resolve (foco visível e
  `prefers-reduced-motion` já estão no arquivo).

---

## 5. Decisões tomadas que valem registrar

| Decisão | Motivo |
|---|---|
| Tema neo-brutalista escuro (`#090A0D`, acentos `#FF3333`, `#FFFF00`, `#0066FF`, raio 0, sombra dura) | Aplicado nos 16 slides a pedido |
| PPTX com 5 cenas full-bleed (agenda, problema, diferencial, pedido, onde estamos) | Quebrar a leitura de “template” |
| HTML como formato de motion; PPTX/PDF mantidos em 16:9 | Cada formato usa a ferramenta adequada |
| Fontes embutidas em base64 no HTML | Abrir igual sem internet |
| Conteúdo e números preservados | A reestilização não era reescrita do pitch |

---

## 6. Próximo passo recomendado

1. Preencher a seção 2 (10 min) e regerar os artefatos com os scripts da pasta.
2. Rodar o checklist 3.1 no navegador e me dizer a cena + o que quebrou.
3. Responder as quatro perguntas do logo (1.1) para abrir essa frente.
