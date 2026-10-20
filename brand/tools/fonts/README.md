# Fontes embutidas

Estes arquivos são usados **apenas** pelo gerador (`../generate.py`) para converter
o logotipo em curvas. Nenhum site precisa carregá-los em runtime: os SVGs e o
componente React já contêm os paths prontos.

| Arquivo | Família | Uso |
| --- | --- | --- |
| `montserrat-latin-900-normal.woff2` | Montserrat 900 | wordmark (logotipo) |
| `montserrat-latin-800-normal.woff2` | Montserrat 800 | isologo (texto em arco) |
| `montserrat-latin-700-normal.woff2` | Montserrat 700 | tagline “HUB DE ALTA PERFORMANCE” |
| `barlow-condensed-latin-900-normal.woff2` | Barlow Condensed 900 | variante técnica (números/dados) |

Ambas as famílias são distribuídas sob a **SIL Open Font License 1.1**
(ver `LICENSE-Montserrat.txt` e `LICENSE-BarlowCondensed.txt`), o que permite
incorporar as curvas em uma marca sem custo de licenciamento.

Baixadas de `@fontsource/montserrat` e `@fontsource/barlow-condensed` (npm).
