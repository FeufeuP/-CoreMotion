"""Monta brand/apresentacao.html — manual de marca autocontido (SVGs + fontes embutidos)."""
import base64, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                 # brand/
SVG = os.path.join(ROOT, 'svg')
FONTS = os.path.join(HERE, 'fonts')

def read(name):
    with open(os.path.join(SVG, name)) as f:
        s = f.read()
    # remove xml declaration if any
    return s

def b64(font):
    with open(os.path.join(FONTS, font), 'rb') as f:
        return base64.b64encode(f.read()).decode()

def art(name, cls='', style=''):
    return f'<div class="art {cls}" style="{style}">{read(name)}</div>'

def img(name, alt='', cls='', style=''):
    return f'<img class="{cls}" style="{style}" alt="{alt}" src="data:image/svg+xml;base64,{base64.b64encode(read(name).encode()).decode()}"/>'

M900 = b64('montserrat-latin-900-normal.woff2')
M700 = b64('montserrat-latin-700-normal.woff2')

FILES = [
    ('01-logotipo-duotone.svg', 'Logotipo duotone', 'Core branco, Motion vermelho: aceleração cromática. Versão principal.'),
    ('02-logotipo-branco.svg', 'Logotipo branco', 'Uma cor, para fundos escuros e imagens.'),
    ('03-logotipo-preto.svg', 'Logotipo preto', 'Uma cor, para fundos claros e impressos.'),
    ('04-logotipo-com-regua.svg', 'Logotipo + régua', 'Régua de velocidade sob o nome: leitura de movimento.'),
    ('05-isotipo.svg', 'Isotipo', 'O C de velocidade com rastro de cometa, rim light e brilho.'),
    ('06-isotipo-branco.svg', 'Isotipo branco', 'Aplicação em uma cor sobre fundo escuro.'),
    ('07-isotipo-mono.svg', 'Isotipo monocromático', 'Preto sobre branco: fax, bordado, gravação.'),
    ('08-isotipo-simplificado.svg', 'Isotipo simplificado', 'Sem rastro nem brilhos: 16–32 px, favicon, UI.'),
    ('09-imagotipo-horizontal.svg', 'Imagotipo horizontal', 'Símbolo + nome. Padrão para cabeçalhos.'),
    ('10-imagotipo-horizontal-branco.svg', 'Imagotipo horizontal branco', 'Versão de uma cor para fundos escuros.'),
    ('11-imagotipo-vertical.svg', 'Imagotipo vertical', 'Para espaços estreitos e formatos quadrados.'),
    ('12-imagotipo-vertical-branco.svg', 'Imagotipo vertical branco', 'Versão de uma cor.'),
    ('13-isologo.svg', 'Isologo', 'Emblema circular: anel de velocidade + tipografia em arco.'),
    ('14-isologo-mono.svg', 'Isologo monocromático', 'Para selos, patches e materiais de baixa tinta.'),
    ('15-icone-app.svg', 'Ícone de app', 'App icon com cantos arredondados e halo interno.'),
    ('16-favicon.svg', 'Favicon', 'Versão quadrada, sem cantos arredondados.'),
]

def card(f, i):
    name, title, desc = f
    return f'''
    <figure class="card">
      <div class="card-art">{img(name, title)}</div>
      <figcaption>
        <span class="num">{i:02d}</span>
        <strong>{title}</strong>
        <p>{desc}</p>
        <code>brand/svg/{name}</code>
      </figcaption>
    </figure>'''

CLASSES = [
    ('Logotipo', 'texto', 'Representação feita exclusivamente por texto ou tipografia estilizada — o nome escrito de forma única.',
     'Google, Coca-Cola, Disney', '01–04', 'CoreMotion em Montserrat 900 inclinada, com corte cromático entre “Core” e “Motion”.'),
    ('Isotipo', 'símbolo', 'Apenas o símbolo, ícone ou desenho, sem nenhuma palavra.',
     'Apple, Nike, Twitter', '05–08', 'O “C” de velocidade. Funciona sozinho no app, no favicon e em qualquer avatar.'),
    ('Imagotipo', 'símbolo + texto', 'Junção de símbolo e texto que funcionam juntos — mas podem ser separados e continuam reconhecíveis.',
     'Adidas, Lacoste, McDonald’s', '09–12', 'Símbolo e nome lado a lado (ou empilhados), com distância fixa entre eles.'),
    ('Isologo', 'bloco único', 'União inseparável de texto e símbolo num único bloco visual: separar destrói a identidade.',
     'Burger King, Starbucks, Harley-Davidson', '13–14', 'O emblema circular: o anel de velocidade, o arco de texto e o C formam uma peça só.'),
]

COLORS = [
    ('#E50914', 'Vermelho CoreMotion', 'Cor primária — velocidade, intensidade, performance.'),
    ('#FF6A45', 'Coral de rastro', 'Rastro de cometa e realces. Só sobre fundo escuro.'),
    ('#7C0410', 'Vinho de profundidade', 'Fim do gradiente: dá volume ao C.'),
    ('#0B0C10', 'Grafite profundo', 'Fundo principal do produto.'),
    ('#111319', 'Grafite de card', 'Superfícies e painéis.'),
    ('#F8FAFC', 'Branco neve', 'Texto principal e versão branca da marca.'),
    ('#94A3B8', 'Aço', 'Texto secundário, taglines, linhas finas.'),
]

THUMB = ['04-logotipo-com-regua.svg', '05-isotipo.svg',
         '09-imagotipo-horizontal.svg', '13-isologo.svg']

def html():
    logos = '\n'.join(card(f, i + 1) for i, f in enumerate(FILES))
    classes = ''
    for i, (title, kind, definition, ex, files, note) in enumerate(CLASSES):
        classes += f'''
        <article class="class-card">
          <header>
            <span class="kicker">{kind}</span>
            <h3>{title}</h3>
          </header>
          <div class="thumb">{img(THUMB[i], title)}</div>
          <p class="def">{definition}</p>
          <p class="ex"><b>Exemplos:</b> {ex}</p>
          <p class="note">{note}</p>
          <footer>arquivos {files}</footer>
        </article>'''

    swatches = ''.join(
        f'''<div class="swatch"><div class="chip" style="background:{hexv}"></div>
        <div><strong>{name}</strong><code>{hexv}</code><p>{desc}</p></div></div>'''
        for hexv, name, desc in COLORS)

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>CoreMotion — Manual de Marca</title>
<style>
@font-face {{ font-family:'MontserratX'; src:url(data:font/woff2;base64,{M900}) format('woff2'); font-weight:900; font-style:normal; }}
@font-face {{ font-family:'MontserratX'; src:url(data:font/woff2;base64,{M700}) format('woff2'); font-weight:700; font-style:normal; }}
:root {{
  --ink:#0B0C10; --ink2:#111319; --ink3:#181B24; --red:#E50914; --coral:#FF6A45;
  --snow:#F8FAFC; --steel:#94A3B8; --line:rgba(255,255,255,.09); --muted:#64748B;
}}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{
  margin:0; background:var(--ink); color:var(--snow);
  font-family:'MontserratX', 'Helvetica Neue', Arial, sans-serif; font-weight:700;
  -webkit-font-smoothing:antialiased;
  background-image:radial-gradient(circle at 50% -10%, #1a1116 0%, var(--ink) 55%);
  background-attachment:fixed;
}}
.wrap {{ max-width:1180px; margin:0 auto; padding:0 28px; }}
section {{ padding:88px 0; border-top:1px solid var(--line); }}
h1,h2,h3,h4 {{ margin:0; letter-spacing:-.02em; }}
h1 {{ font-size:clamp(38px,6vw,74px); font-weight:900; line-height:.98; }}
h2 {{ font-size:clamp(24px,3.2vw,38px); font-weight:900; }}
h3 {{ font-size:22px; font-weight:900; }}
p {{ font-weight:700; color:var(--steel); line-height:1.65; font-size:15px; margin:10px 0 0; }}
code {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:11.5px; color:var(--muted); letter-spacing:0; }}
.art svg, .art img {{ max-width:100%; height:auto; display:block; }}
.kicker {{ font-size:11px; letter-spacing:.34em; text-transform:uppercase; color:var(--red); font-weight:700; }}
.sec-head {{ display:flex; align-items:baseline; gap:18px; margin-bottom:44px; flex-wrap:wrap; }}
.sec-head .idx {{ font-size:13px; color:var(--muted); letter-spacing:.2em; }}
.sec-head p {{ max-width:520px; margin:0 0 0 auto; font-size:13.5px; }}

/* HERO */
.hero {{ padding:56px 0 30px; border:0; }}
.hero-top {{ display:flex; justify-content:space-between; align-items:center; gap:20px; flex-wrap:wrap; }}
.nav {{ display:flex; gap:18px; font-size:12px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); }}
.nav a {{ color:inherit; text-decoration:none; }}
.nav a:hover {{ color:var(--snow); }}
.hero-stage {{
  margin-top:64px; border-radius:28px; overflow:hidden;
  border:1px solid var(--line);
  background:
    radial-gradient(circle at 78% 18%, rgba(229,9,20,.20), transparent 46%),
    radial-gradient(circle at 12% 88%, rgba(255,106,69,.10), transparent 50%),
    linear-gradient(160deg,#14161d,#0B0C10 70%);
  padding:56px;
  position:relative;
}}
.hero-stage .art svg {{ width:min(100%,560px); height:auto; display:block; margin:0 auto; }}
.hero-meta {{ display:flex; gap:12px; flex-wrap:wrap; margin-top:26px; }}
.pill {{ border:1px solid var(--line); border-radius:999px; padding:7px 14px; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--steel); }}
.pill.red {{ border-color:rgba(229,9,20,.45); color:#FF8E84; background:rgba(229,9,20,.09); }}

/* IDEA */
.two {{ display:grid; grid-template-columns:1.05fr .95fr; gap:56px; align-items:center; }}
.mark-big {{ background:linear-gradient(150deg,#15181f,#0c0e13); border:1px solid var(--line); border-radius:26px; padding:36px; }}
.mark-big .art svg {{ width:100%; height:auto; display:block; }}
ul.anatomy {{ list-style:none; padding:0; margin:26px 0 0; }}
ul.anatomy li {{ display:grid; grid-template-columns:30px 1fr; gap:14px; padding:16px 0; border-top:1px solid var(--line); }}
ul.anatomy b {{ display:block; font-size:14px; color:var(--snow); }}
ul.anatomy span {{ font-size:13px; color:var(--steel); font-weight:700; }}
ul.anatomy i {{ font-style:normal; font-size:11px; color:var(--red); letter-spacing:.16em; }}

/* CLASSIFICATION */
.class-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:20px; }}
.class-card {{ background:var(--ink2); border:1px solid var(--line); border-radius:20px; padding:26px; transition:.25s; }}
.class-card:hover {{ border-color:rgba(229,9,20,.42); transform:translateY(-2px); }}
.class-card header {{ display:flex; flex-direction:column; gap:6px; }}
.class-card .def {{ color:#cbd5e1; font-size:14px; }}
.class-card .ex, .class-card .note {{ font-size:12.5px; }}
.class-card .note {{ color:#a9b4c4; border-left:2px solid var(--red); padding-left:12px; }}
.thumb {{ height:132px; display:flex; align-items:center; justify-content:center;
  margin:16px 0 4px; border-radius:12px; padding:14px;
  background:radial-gradient(circle at 50% 45%, #1b1f29, #0d0f14 72%); border:1px solid var(--line); }}
.thumb img {{ max-width:100%; max-height:100%; object-fit:contain; }}
.class-card footer {{ margin-top:16px; font-size:10.5px; letter-spacing:.2em; text-transform:uppercase; color:var(--muted); }}

/* FILES */
.files {{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }}
.card {{ margin:0; background:var(--ink2); border:1px solid var(--line); border-radius:18px; overflow:hidden; display:flex; flex-direction:column; }}
.card-art {{ aspect-ratio:4/3; display:flex; align-items:center; justify-content:center; padding:20px;
  background:radial-gradient(circle at 50% 40%, #1b1f29, #0e1015 70%); }}
.card-art img {{ max-width:100%; max-height:100%; object-fit:contain; }}
.card figcaption {{ padding:16px 18px 18px; border-top:1px solid var(--line); }}
.card figcaption strong {{ display:block; font-size:13.5px; color:var(--snow); }}
.card figcaption p {{ font-size:12px; margin:6px 0 8px; }}
.num {{ font-size:10px; color:var(--red); letter-spacing:.2em; }}

/* COLOR */
.swatches {{ display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }}
.swatch {{ display:grid; grid-template-columns:84px 1fr; gap:18px; align-items:center; background:var(--ink2);
  border:1px solid var(--line); border-radius:16px; padding:14px; }}
.chip {{ width:84px; height:64px; border-radius:10px; border:1px solid rgba(255,255,255,.14); }}
.swatch strong {{ font-size:13.5px; }}
.swatch code {{ display:block; color:var(--red); font-size:12px; margin:2px 0 4px; }}
.swatch p {{ font-size:11.5px; margin:0; }}

/* TYPE */
.type-row {{ display:grid; grid-template-columns:1fr 1fr; gap:22px; }}
.type-box {{ background:var(--ink2); border:1px solid var(--line); border-radius:18px; padding:26px; }}
.type-box .sample {{ font-weight:900; font-size:44px; letter-spacing:-.03em; }}
.type-box .sample2 {{ font-weight:700; font-size:13px; letter-spacing:.32em; text-transform:uppercase; color:var(--steel); }}
.type-box hr {{ border:0; border-top:1px solid var(--line); margin:18px 0; }}

/* APPLY */
.apply {{ display:grid; grid-template-columns:1.15fr .85fr; gap:20px; }}
.mock {{ background:var(--ink2); border:1px solid var(--line); border-radius:18px; padding:22px; }}
.mock-label {{ font-size:10.5px; letter-spacing:.24em; text-transform:uppercase; color:var(--muted); margin-bottom:14px; }}
.appbar {{ display:flex; align-items:center; gap:12px; background:#0e1015; border:1px solid var(--line);
  border-radius:14px; padding:14px 16px; }}
.appbar .brand {{ display:flex; align-items:center; gap:10px; }}
.appbar .brand img {{ width:34px; height:34px; }}
.appbar .brand .word img {{ height:13px; display:block; }}
.appbar .brand .tag {{ font-size:8px; letter-spacing:.3em; color:var(--steel); text-transform:uppercase; margin-top:4px; }}
.badge-pro {{ margin-left:6px; font-size:8px; letter-spacing:.14em; padding:3px 7px; border-radius:5px;
  color:#FF8E84; background:rgba(229,9,20,.14); border:1px solid rgba(229,9,20,.32); }}
.avatar {{ width:120px; height:120px; border-radius:32px; display:flex; align-items:center; justify-content:center;
  background:radial-gradient(circle at 50% 35%, #241016, #0c0e13 72%); border:1px solid var(--line); }}
.avatar img {{ width:78%; height:78%; }}
.avatar.round {{ border-radius:50%; }}
.iconrow {{ display:flex; gap:14px; align-items:flex-end; }}
.iconrow img.sq {{ width:96px; height:96px; border-radius:22px; }}
.iconrow img.rd {{ width:56px; height:56px; border-radius:50%; }}
.iconrow img.sm {{ width:24px; height:24px; }}

/* RULES */
.rules {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; }}
.rule {{ border-radius:18px; padding:22px; border:1px solid var(--line); background:var(--ink2); }}
.rule h4 {{ font-size:12px; letter-spacing:.22em; text-transform:uppercase; margin-bottom:14px; }}
.rule.ok h4 {{ color:#34D399; }}
.rule.no h4 {{ color:#F87171; }}
.rule ul {{ margin:0; padding-left:18px; }}
.rule li {{ font-size:13px; color:#c3ccd9; line-height:1.9; font-weight:700; }}

footer.end {{ padding:44px 0 70px; color:var(--muted); font-size:12px; display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap; }}
@media (max-width:900px) {{
  .two, .class-grid, .files, .swatches, .type-row, .apply, .rules {{ grid-template-columns:1fr; }}
  section {{ padding:60px 0; }}
  .hero-stage {{ padding:28px; }}
}}
@media print {{
  body {{ background:#fff; color:#0B0C10; }}
  section {{ page-break-inside:avoid; }}
}}
</style>
</head>
<body>

<div class="wrap hero">
  <div class="hero-top">
    <div class="art" style="width:300px">{read('09-imagotipo-horizontal.svg')}</div>
    <nav class="nav">
      <a href="#ideia">A ideia</a><a href="#classificacao">Classificação</a>
      <a href="#variacoes">Variações</a><a href="#cores">Cores</a><a href="#aplicacoes">Aplicações</a>
    </nav>
  </div>

  <div class="hero-stage" style="margin-top:44px">
    <div class="art">{read('13-isologo.svg')}</div>
    <div class="hero-meta">
      <span class="pill red">Manual de marca · v1.0</span>
      <span class="pill">Isotipo · Logotipo · Imagotipo · Isologo</span>
      <span class="pill">Vetor · SVG + PNG</span>
    </div>
  </div>
</div>

<section id="ideia">
  <div class="wrap">
    <div class="sec-head"><span class="idx">01</span><h2>O “C” de velocidade</h2>
      <p>Um único gesto: a letra C desenhada como um traço em movimento. Quanto mais perto do fim do traço, mais fino — como uma pincelada que acelerou.</p></div>
    <div class="two">
      <div class="mark-big">
        <div class="art">{read('05-isotipo.svg')}</div>
      </div>
      <div>
        <ul class="anatomy">
          <li><i>A</i><div><b>Cabeça em cinzel</b><span>Corte diagonal no topo: a marca “entra” na curva em vez de começar num traço mole.</span></div></li>
          <li><i>B</i><div><b>Corpo em fita</b><span>Espessura variável (1,2 → 42,6 unidades) que sugere aceleração e frenagem.</span></div></li>
          <li><i>C</i><div><b>Cauda em ponta</b><span>O traço morre em bico, na diagonal, como um rastro que se dissolve.</span></div></li>
          <li><i>D</i><div><b>Rastro de cometa</b><span>Espiral coral que nasce na cauda e se enrola no núcleo, criando profundidade.</span></div></li>
          <li><i>E</i><div><b>Luz de borda e brilho</b><span>Rim light e varredura especular dão volume metálico sem perder o vetor.</span></div></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section id="classificacao">
  <div class="wrap">
    <div class="sec-head"><span class="idx">02</span><h2>Classificação técnica</h2>
      <p>A mesma marca em quatro arranjos. Cada um resolve um problema diferente de aplicação — e todos são reconhecíveis isoladamente, exceto o isologo, que é um bloco único.</p></div>
    <div class="class-grid">{classes}</div>
  </div>
</section>

<section id="variacoes">
  <div class="wrap">
    <div class="sec-head"><span class="idx">03</span><h2>As 16 variações</h2>
      <p>Versões cromáticas, monocromáticas, reduzidas e de aplicação. Todos os arquivos são vetoriais, com curvas convertidas (sem dependência de fonte instalada).</p></div>
    <div class="files">{logos}</div>
  </div>
</section>

<section id="cores">
  <div class="wrap">
    <div class="sec-head"><span class="idx">04</span><h2>Cor e tipografia</h2>
      <p>O vermelho já existia no produto (--accent-red). A identidade o organiza em gradiente, com o coral como única cor de apoio.</p></div>
    <div class="swatches">{swatches}</div>
    <div class="type-row" style="margin-top:26px">
      <div class="type-box">
        <div class="kicker">Primária · display</div>
        <div class="sample" style="margin-top:14px">Montserrat 900</div>
        <p>Caixa alta e baixa, tracking −3%, inclinação −13° no wordmark. Peso 900 para títulos.</p>
        <hr/>
        <div class="sample2">Hub de alta performance · 700</div>
      </div>
      <div class="type-box">
        <div class="kicker">Apoio · técnica</div>
        <div class="sample" style="margin-top:14px">Barlow Condensed</div>
        <p>Reservada para números, dados de performance e dashboards. Nunca no logotipo.</p>
        <hr/>
        <div class="sample2">Velocidade média · 4:12/km</div>
      </div>
    </div>
  </div>
</section>

<section id="aplicacoes">
  <div class="wrap">
    <div class="sec-head"><span class="idx">05</span><h2>Aplicações</h2>
      <p>O imagotipo vive no cabeçalho; o isotipo resolve ícone, avatar e favicon; o isologo assina materiais e conquistas.</p></div>
    <div class="apply">
      <div class="mock">
        <div class="mock-label">Cabeçalho do produto</div>
        <div class="appbar">
          <div class="brand">
            <img src="data:image/svg+xml;base64,{base64.b64encode(read('05-isotipo.svg').encode()).decode()}" alt=""/>
            <div>
              <div class="word"><img src="data:image/svg+xml;base64,{base64.b64encode(read('02-logotipo-branco.svg').encode()).decode()}" alt=""/><span class="badge-pro">PRO</span></div>
              <div class="tag">Hub de alta performance</div>
            </div>
          </div>
        </div>
        <div class="mock-label" style="margin-top:22px">Ícone de app e favicon</div>
        <div class="iconrow">
          <img class="sq" src="data:image/svg+xml;base64,{base64.b64encode(read('15-icone-app.svg').encode()).decode()}" alt=""/>
          <img class="rd" src="data:image/svg+xml;base64,{base64.b64encode(read('05-isotipo.svg').encode()).decode()}" alt=""/>
          <img class="sm" src="data:image/svg+xml;base64,{base64.b64encode(read('08-isotipo-simplificado.svg').encode()).decode()}" alt=""/>
        </div>
      </div>
      <div class="mock">
        <div class="mock-label">Avatar / perfil</div>
        <div style="display:flex;gap:16px">
          <div class="avatar"><img src="data:image/svg+xml;base64,{base64.b64encode(read('05-isotipo.svg').encode()).decode()}" alt=""/></div>
          <div class="avatar round"><img src="data:image/svg+xml;base64,{base64.b64encode(read('05-isotipo.svg').encode()).decode()}" alt=""/></div>
        </div>
        <div class="mock-label" style="margin-top:24px">Escala mínima</div>
        <div style="display:flex;gap:24px;align-items:center;padding:6px 0">
          <img style="width:24px" src="data:image/svg+xml;base64,{base64.b64encode(read('08-isotipo-simplificado.svg').encode()).decode()}" alt=""/>
          <img style="width:16px" src="data:image/svg+xml;base64,{base64.b64encode(read('08-isotipo-simplificado.svg').encode()).decode()}" alt=""/>
          <img style="width:12px" src="data:image/svg+xml;base64,{base64.b64encode(read('08-isotipo-simplificado.svg').encode()).decode()}" alt=""/>
        </div>
        <p style="font-size:12px">Abaixo de 32 px, use sempre o isotipo simplificado — o rastro e o brilho desaparecem.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><span class="idx">06</span><h2>Regras de uso</h2>
      <p>Poucas regras, sempre as mesmas — é o que mantém a marca imediatamente reconhecível.</p></div>
    <div class="rules">
      <div class="rule ok">
        <h4>Faça</h4>
        <ul>
          <li>Use a área de respiro equivalente à altura da boca do “C”.</li>
          <li>Prefira o isotipo sobre fundos escuros; versão branca em fotografia.</li>
          <li>Mantenha a inclinação de −13° do wordmark.</li>
          <li>Em fundos claros, use a versão preta ou o vermelho puro.</li>
          <li>Abaixo de 32 px, troque pelo isotipo simplificado.</li>
        </ul>
      </div>
      <div class="rule no">
        <h4>Não faça</h4>
        <ul>
          <li>Não estique, rotate ou aplique perspectiva na marca.</li>
          <li>Não recolora o gradiente fora da paleta.</li>
          <li>Não separe o anel de texto do isologo: ele é um bloco único.</li>
          <li>Não adicione sombras duras, contornos ou efeitos 3D extras.</li>
          <li>Não escreva “CoreMotiom”: a grafia oficial é <b>CoreMotion</b>.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><span class="idx">07</span><h2>Arquivos e regeneração</h2>
      <p>Os SVGs são a fonte da verdade. Os PNGs são exportações; o código React do site consome a mesma geometria.</p></div>
    <div class="two" style="align-items:start">
      <div>
        <ul class="anatomy">
          <li><i>SVG</i><div><b>brand/svg/*.svg</b><span>16 arquivos vetoriais, curvas convertidas em paths.</span></div></li>
          <li><i>PNG</i><div><b>brand/png/*.png</b><span>Exportações em 1×, 2× e tamanhos de ícone.</span></div></li>
          <li><i>APP</i><div><b>components/brand/Logo.tsx</b><span>Componentes React usados no cabeçalho e no rodapé.</span></div></li>
          <li><i>ICO</i><div><b>app/icon.svg</b><span>Favicon do Next.js.</span></div></li>
        </ul>
      </div>
      <div class="type-box">
        <div class="kicker">Pipeline</div>
        <p style="margin-bottom:14px">A geometria do C e a tipografia do wordmark são geradas por código — o mesmo script escreve os SVGs e as constantes usadas pelo React.</p>
        <code style="display:block;line-height:1.9;white-space:pre-wrap">python3 brand/tools/generate.py
# → brand/svg/*.svg
# → components/brand/marks.generated.ts</code>
        <p style="font-size:12px;margin-top:14px">Fontes: Montserrat e Barlow Condensed (SIL Open Font License), embutidas em <code>brand/tools/fonts</code>.</p>
      </div>
    </div>
  </div>
</section>

<footer class="end wrap">
  <span>CoreMotion · Manual de Marca v1.0</span>
  <span>Hub de Alta Performance</span>
</footer>

</body>
</html>'''

if __name__ == '__main__':
    out = os.path.join(ROOT, 'apresentacao.html')
    with open(out, 'w') as f:
        f.write(html())
    print('escrito', out, round(os.path.getsize(out) / 1024), 'KB')
