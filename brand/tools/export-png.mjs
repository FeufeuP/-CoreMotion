/**
 * Exporta os SVGs de brand/svg para PNG em brand/png.
 *
 * Uso: node brand/tools/export-png.mjs
 * Requer @resvg/resvg-js (devDependency do projeto).
 */
import { Resvg } from '@resvg/resvg-js';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.dirname(HERE);            // brand/
const SRC = path.join(ROOT, 'svg');
const OUT = path.join(ROOT, 'png');

/** [arquivo, larguras em px] */
const JOBS = [
  ['01-logotipo-duotone.svg', [1600]],
  ['02-logotipo-branco.svg', [1600]],
  ['03-logotipo-preto.svg', [1600]],
  ['04-logotipo-com-regua.svg', [1600]],
  ['05-isotipo.svg', [1024, 512, 256, 128]],
  ['06-isotipo-branco.svg', [512]],
  ['07-isotipo-mono.svg', [512]],
  ['08-isotipo-simplificado.svg', [256, 64]],
  ['09-imagotipo-horizontal.svg', [1600]],
  ['10-imagotipo-horizontal-branco.svg', [1600]],
  ['11-imagotipo-vertical.svg', [1000]],
  ['12-imagotipo-vertical-branco.svg', [1000]],
  ['13-isologo.svg', [1200, 600]],
  ['14-isologo-mono.svg', [1200]],
  ['15-icone-app.svg', [1024, 512, 192]],
  ['16-favicon.svg', [512, 180, 32]],
];

const slug = (file) => file.replace(/^\d+-/, '').replace(/\.svg$/, '');

fs.mkdirSync(OUT, { recursive: true });

for (const [file, widths] of JOBS) {
  const svg = fs.readFileSync(path.join(SRC, file), 'utf8');
  for (const width of widths) {
    const png = new Resvg(svg, { fitTo: { mode: 'width', value: width } }).render().asPng();
    const name = slug(file) === 'favicon'
      ? `favicon-${width}.png`
      : `${slug(file)}-${width}.png`;
    fs.writeFileSync(path.join(OUT, name), png);
  }
}

// favicon.ico do Next.js usa app/favicon.ico; gere-o com ImageMagick a partir dos PNGs.
console.log(`${fs.readdirSync(OUT).length} PNGs em ${OUT}`);
