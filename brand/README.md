# CoreMotion — Identidade Visual

Sistema de marca do **CoreMotion**: um **C estilizado** desenhado como um traço em
velocidade, com rastro de cometa, corte em cinzel e acabamento metálico.

Abra **[`apresentacao.html`](./apresentacao.html)** para ver o manual completo
(autocontido: SVGs e fontes embutidos — funciona offline).
Visão geral rápida: **[`showcase.png`](./showcase.png)**.

---

## 1. Classificação técnica da marca

| Tipo | O que é | Arquivos | Como se aplica aqui |
| --- | --- | --- | --- |
| **Logotipo** | Só texto/tipografia estilizada | `01`–`04` | “CoreMotion” em Montserrat 900, tracking −3%, inclinação −13°, com corte cromático entre *Core* (branco) e *Motion* (vermelho). |
| **Isotipo** | Só o símbolo | `05`–`08` | O “C” de velocidade. Funciona sozinho em ícone, favicon, avatar. |
| **Imagotipo** | Símbolo + texto, separáveis | `09`–`12` | Símbolo ao lado (ou acima) do nome, com distância fixa. Padrão de cabeçalho. |
| **Isologo** | Símbolo + texto inseparáveis | `13`–`14` | Emblema circular: anel de velocidade + tipografia em arco + C no centro. |

Referências de mercado: logotipo → Google, Coca-Cola; isotipo → Apple, Nike;
imagotipo → Adidas, Lacoste; isologo → Burger King, Starbucks.

## 2. Anatomia do símbolo

| Elemento | Função |
| --- | --- |
| Cabeça em cinzel | corte diagonal no topo; a marca entra na curva com intenção |
| Corpo em fita | espessura 1,2 → 42,6 unidades (aceleração e frenagem) |
| Cauda em ponta | o traço morre em bico, como rastro que se dissolve |
| Rastro de cometa | espiral coral que nasce na cauda e se enrola no núcleo |
| Rim light + specular | volume metálico sem sair do vetor |

## 3. Arquivos

```
brand/
├── apresentacao.html          manual visual (autocontido)
├── svg/                       16 vetores — FONTE DA VERDADE
│   ├── 01-logotipo-duotone.svg
│   ├── 02-logotipo-branco.svg
│   ├── 03-logotipo-preto.svg
│   ├── 04-logotipo-com-regua.svg
│   ├── 05-isotipo.svg
│   ├── 06-isotipo-branco.svg
│   ├── 07-isotipo-mono.svg
│   ├── 08-isotipo-simplificado.svg
│   ├── 09-imagotipo-horizontal.svg
│   ├── 10-imagotipo-horizontal-branco.svg
│   ├── 11-imagotipo-vertical.svg
│   ├── 12-imagotipo-vertical-branco.svg
│   ├── 13-isologo.svg
│   ├── 14-isologo-mono.svg
│   ├── 15-icone-app.svg
│   └── 16-favicon.svg
├── png/                       exportações (1×/2×, ícones, favicons)
└── tools/
    ├── generate.py            gera svg/ + marks.generated.ts
    ├── build_board.py         gera apresentacao.html
    ├── export-png.mjs         exporta svg → png
    └── fonts/                 Montserrat 700/800/900 + Barlow Condensed 900 (OFL)
```

No produto, a marca é renderizada por código, sem imagens externas:

- `components/brand/Logo.tsx` → `<CoreMotionMark />`, `<CoreMotionWordmark />`, `<CoreMotionLogo />`
- `components/brand/marks.generated.ts` → geometria gerada (não editar à mão)
- `app/icon.svg` → favicon do Next.js

## 4. Cor

| Token | Hex | Uso |
| --- | --- | --- |
| Vermelho CoreMotion | `#E50914` | cor primária (já usada no produto) |
| Coral de rastro | `#FF6A45` | rastro de cometa e realces |
| Vinho de profundidade | `#7C0410` | fim do gradiente |
| Grafite profundo | `#0B0C10` | fundo principal |
| Grafite de card | `#111319` | superfícies |
| Branco neve | `#F8FAFC` | texto e versão branca |
| Aço | `#94A3B8` | texto secundário, taglines |

Gradiente do símbolo: `#FF8A4C → #FF4A34 → #EF0F1D → #C40814 → #7C0410`.

## 5. Tipografia

- **Montserrat 900** — wordmark e títulos. Tracking −3%, inclinação −13° no logotipo.
- **Montserrat 700** — tagline “HUB DE ALTA PERFORMANCE”, tracking +30%.
- **Barlow Condensed 900** — números e dados de performance. Nunca no logotipo.

Ambas sob SIL Open Font License; os arquivos `.woff2` estão em `tools/fonts/` e os
SVGs já saem com as **curvas convertidas** — não é preciso ter a fonte instalada.

## 6. Regras

**Faça**
- Respiro mínimo = altura da boca do “C” em todos os lados.
- Fundo escuro → isotipo/imagotipo colorido ou branco; fundo claro → versão preta.
- Abaixo de 32 px, use o isotipo simplificado (`08`).
- Grafia oficial: **CoreMotion**.

**Não faça**
- Não esticar, rotacionar ou aplicar perspectiva.
- Não recolora o gradiente fora da paleta.
- Não separe o anel de texto do isologo.
- Não adicione contornos, sombras duras ou efeitos 3D extras.

## 7. Regenerar

```bash
python3 -m pip install fonttools brotli     # dependências do gerador
python3 brand/tools/generate.py             # brand/svg/*.svg + marks.generated.ts
python3 brand/tools/build_board.py          # brand/apresentacao.html
```

Para reexportar PNGs é usado `@resvg/resvg-js` (devDependency do projeto):

```bash
node brand/tools/export-png.mjs      # brand/png/*.png
convert brand/png/favicon-32.png brand/png/favicon-180.png brand/png/favicon-512.png \
  -define icon:auto-resize=64,48,32,16 brand/png/favicon.ico
```
