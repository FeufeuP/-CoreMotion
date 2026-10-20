# CoreMotion — Pitch: o que ficou para depois

Registro do que **não** foi feito nesta rodada, do que foi feito pela metade de propósito e do
que precisa ser conferido por uma pessoa antes da banca. Complementa o
[`CoreMotion-Pitch-Roteiro.md`](CoreMotion-Pitch-Roteiro.md), que cobre o conteúdo falado.

**Última atualização:** 2026-10-19 · branch `arena/b969919e-coremotion`

---

## 1. Adiado por decisão

### 1.1 Logo / identidade da marca

O pedido veio junto com a reestilização do deck e foi explicitamente deixado para depois
(“pensamos nisto depois”). **Nada de logo foi criado nesta rodada** — o que existe é apenas o
sistema visual do deck (tema neo-brutalista com DM Sans + Space Mono), que pode servir de base.

Está travado por quatro respostas que só você tem:

| # | Pergunta | Por que trava |
|---|---|---|
| 1 | O nome continua **CoreMotion**? | Nome define som, sílabas e espaço no lockup |
| 2 | Três palavras que a marca precisa transmitir | Separa “performance técnica” de “comunidade/confiança” |
| 3 | Referências visuais que você gosta (e alguma que odeia) | Evita 3 rodadas de tentativa e erro |
| 4 | Onde ela aparece primeiro (site, Instagram, camiseta, embalagem) | Muda o desenho: ícone pequeno ≠ assinatura horizontal |

Quando isso voltar, o caminho sugerido é: 3 direções conceituais em preto e branco →
1 escolhida → refino com cor, versões (horizontal, empilhada, ícone), arquivos SVG/PNG e
aplicação no deck e no favicon. O logo entra no lugar do marcador quadrado vermelho do
cabeçalho (`chrome()` no PPTX, `.hud__brand i` no deck web).

### 1.2 Capa e encerramento com dados reais

Capa e slide 15 mantêm os campos entre colchetes de propósito, para não inventar nome,
cidade ou contato. Ver seção 2.

---

## 2. Bloqueia a apresentação (5 minutos de edição)

Trocar nos arquivos `.pptx`, `.html` e no roteiro:

| Campo | Onde aparece |
|---|---|
| `[seu nome]` | capa (linha “Apresentado por”) |
| `[cidade]` | capa |
| `[seu@email.com]` | slide 15 |
| `[telefone]` | slide 15 |
| `[site]` | slide 15 |
| `P1`–`P4` + “nome · bio” | slide 13 (time) |
| `R$ 300 mil` | slide 14 — ajustar ao plano real antes de apresentar |

O roteiro já tem um checklist de véspera em `CoreMotion-Pitch-Roteiro.md` (§ “Antes de
apresentar”). Nada disso foi preenchido porque depende de informação que não está no repositório.

---

## 3. Verificar antes de apresentar (não validado aqui)

### 3.1 Deck web em navegador — **não abriu em navegador neste ambiente**

O sandbox não tem Chromium/Playwright funcionando (dependências de sistema ausentes e sem
permissão de instalação). A validação do `CoreMotion-Pitch-Web.html` foi **estrutural**:
`HTMLParser` sem erro de aninhamento, 15 seções, ids únicos, âncoras internas resolvendo,
chaves de CSS balanceadas, 7 fontes embutidas em base64 e `node --check` no JS.

O que ainda precisa de olho humano, cena por cena (15 cenas):

- [ ] Capa: disco, triângulo e chips não sangram para fora da viewport em 1440×900
- [ ] Capa: parallax do mouse não briga com o scroll
- [ ] Cena 06: o fluxo acende nos 4 nós e reinicia sem piscar
- [ ] Cena 08: os 4 estados acendem em sequência e param quando a cena sai de vista
- [ ] Cena 10: matriz não estoura a altura em telas de 720 px
- [ ] Cena 12: cabeçalho fica legível nas duas metades (metade clara / metade escura)
- [ ] Navegação: ←/→/espaço, Home/End, `M` para o índice, `Esc` fecha, `#s7` abre no lugar certo
- [ ] `prefers-reduced-motion`: com a preferência ligada, nada deve sumir
- [ ] Mobile (390 px): colunas empilham, menu vira uma coluna, nada corta

### 3.2 Importação para Google Slides

A cópia “CoreMotion — Pitch (Google Slides)” foi gerada a partir do `.pptx`, mas **não foi
inspecionada slide a slide**. O Google Slides não importa as transições (`cover`/`push`) nem
as animações em cascata — nesse arquivo o deck fica estático. Para apresentar com movimento,
usar o `.pptx` no PowerPoint ou o HTML no navegador.

- [ ] Conferir se nenhuma caixa de texto mudou de tamanho na importação
- [ ] Conferir se as fontes DM Sans / Space Mono aparecem (o Google Slides não tem as duas
      instaladas por padrão)

### 3.3 PPTX no PowerPoint / Keynote

Verificado por render próprio (PIL) e por leitura do XML: 15 slides, 1 transição + 1 `p:timing`
por slide, sombras duras e rotações presentes. **Não** foi aberto no PowerPoint de verdade.

- [ ] Abrir em modo apresentação e conferir a ordem das cascatas
- [ ] Conferir as transições `cover` com direção (`p14:dur`, requer PowerPoint 2010+)
- [ ] Ver se as fontes estão instaladas na máquina da banca (ou usar o PDF como plano B)

---

## 4. Fora de escopo nesta rodada (consciente)

- **Tema escuro completo** no PPTX. O dark do token set só aparece no slide 15 (Obrigado).
  Um deck dark inteiro é outro projeto, não uma variação de cor.
- **Versão em inglês.**
- **Slides de apêndice** (financeiro detalhado, comparativo de concorrentes, currículos).
  O pedido era 15 slides e ele está fechado em 15.
- **Vídeo / demo gravada** do produto. A cena 07 usa wireframes desenhados, não telas reais.
- **Testes de contraste com leitor de tela** além do que o CSS resolve (foco visível e
  `prefers-reduced-motion` já estão no arquivo).

---

## 5. Decisões tomadas que valem registrar

| Decisão | Motivo |
|---|---|
| Tema neo-brutalista (branco/preto, `#FF3333`, `#FFFF00`, `#0066FF`, raio 0, sombra dura) | Substituiu o pastel geométrico a pedido |
| PPTX com 5 cenas full-bleed (agenda, problema, diferencial, pedido, onde estamos) | Quebrar a leitura de “template” |
| Deck web como formato principal de impacto | `.pptx` não sustenta o nível de motion pedido |
| Fontes embutidas em base64 no HTML | Abrir igual sem internet |
| Conteúdo e números preservados | A reestilização não era reescrita do pitch |

---

## 6. Próximo passo recomendado

1. Preencher a seção 2 (10 min) e regerar os artefatos com os scripts da pasta.
2. Rodar o checklist 3.1 no navegador e me dizer a cena + o que quebrou.
3. Responder as quatro perguntas do logo (1.1) para abrir essa frente.
