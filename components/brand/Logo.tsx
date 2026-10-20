'use client';

/**
 * CoreMotion — componentes de marca.
 *
 * Geometria 100% vetorial, gerada por `brand/tools/generate.py`
 * (fonte da verdade: brand/svg/*.svg). Nenhuma dependência de imagem externa.
 *
 * Variantes:
 *  - <CoreMotionMark />        isotipo (C de velocidade)
 *  - <CoreMotionWordmark />    logotipo (só tipografia)
 *  - <CoreMotionLogo />        imagotipo (símbolo + texto, separáveis)
 *  - <CoreMotionSeal />        isologo (emblema circular inseparável)
 */

import {
  MARK_CORE,
  MARK_TRAIL,
  MARK_RIM,
  MARK_SPEC,
  WORD_ALL,
  WORD_CORE,
  WORD_MOTION,
  WORD_WIDTH,
  WORD_CAP,
  WORD_CORE_ADV,
} from './marks.generated';

export type MarkMode = 'gradient' | 'white' | 'ink';

const RED_GRAD_ID = 'cm-red-grad';
const RIM_GRAD_ID = 'cm-rim-grad';
const SPEC_GRAD_ID = 'cm-spec-grad';

function MarkDefs() {
  return (
    <defs>
      <linearGradient id={RED_GRAD_ID} x1="0.08" y1="0" x2="0.82" y2="1">
        <stop offset="0" stopColor="#FF8A4C" />
        <stop offset="0.14" stopColor="#FF4A34" />
        <stop offset="0.42" stopColor="#EF0F1D" />
        <stop offset="0.72" stopColor="#C40814" />
        <stop offset="1" stopColor="#7C0410" />
      </linearGradient>
      <linearGradient id={RIM_GRAD_ID} x1="0.1" y1="0" x2="0.9" y2="1">
        <stop offset="0" stopColor="#FFFFFF" stopOpacity="0.95" />
        <stop offset="0.4" stopColor="#FFD9C2" stopOpacity="0.5" />
        <stop offset="1" stopColor="#FF9C6B" stopOpacity="0" />
      </linearGradient>
      <linearGradient id={SPEC_GRAD_ID} x1="0" y1="0" x2="0.6" y2="1">
        <stop offset="0" stopColor="#FFFFFF" stopOpacity="0.34" />
        <stop offset="1" stopColor="#FFFFFF" stopOpacity="0" />
      </linearGradient>
    </defs>
  );
}

/** Isotipo: o "C" de velocidade. */
export function CoreMotionMark({
  size = 36,
  mode = 'gradient',
  detailed = true,
  className,
  title = 'CoreMotion',
}: {
  size?: number;
  mode?: MarkMode;
  detailed?: boolean;
  className?: string;
  title?: string;
}) {
  const mono = mode === 'white' ? '#F8FAFC' : mode === 'ink' ? '#0B0C10' : null;
  const fill = mono ?? `url(#${RED_GRAD_ID})`;
  return (
    <svg
      viewBox="0 0 512 512"
      width={size}
      height={size}
      className={className}
      role="img"
      aria-label={title}
    >
      {mode === 'gradient' && <MarkDefs />}
      {detailed && <path d={MARK_TRAIL} fill={mono ?? '#FF6A45'} opacity={mono ? 0.9 : 0.95} />}
      <path d={MARK_CORE} fill={fill} />
      {detailed && mode === 'gradient' && (
        <>
          <path d={MARK_RIM} fill={`url(#${RIM_GRAD_ID})`} opacity="0.55" />
          <path d={MARK_SPEC} fill={`url(#${SPEC_GRAD_ID})`} opacity="0.55" />
        </>
      )}
    </svg>
  );
}

/** Logotipo: "CoreMotion" (Core branco · Motion vermelho). */
export function CoreMotionWordmark({
  height = 34,
  twoTone = true,
  color = '#F8FAFC',
  accent = '#E50914',
  className,
  title = 'CoreMotion',
}: {
  height?: number;
  twoTone?: boolean;
  color?: string;
  accent?: string;
  className?: string;
  title?: string;
}) {
  // as curvas são geradas com a linha de base em y = 0 e crescem para cima:
  // o viewBox precisa começar em y negativo, senão o topo das letras é cortado.
  const pad = WORD_CAP * 0.16;          // folga lateral (inclinação de −13°)
  const asc = WORD_CAP * 0.035;
  const desc = WORD_CAP * 0.03;
  const vbW = WORD_WIDTH + pad * 2;
  const vbH = WORD_CAP + asc + desc;
  const scale = height / WORD_CAP;
  const width = vbW * scale;
  return (
    <svg
      viewBox={`${-pad} ${-WORD_CAP - asc} ${vbW} ${vbH}`}
      width={width}
      height={vbH * scale}
      className={className}
      role="img"
      aria-label={title}
    >
      {twoTone ? (
        <>
          <path d={WORD_CORE} fill={color} />
          <path d={WORD_MOTION} fill={accent} transform={`translate(${WORD_CORE_ADV} 0)`} />
        </>
      ) : (
        <path d={WORD_ALL} fill={color} />
      )}
    </svg>
  );
}

/** Imagotipo: símbolo + texto (funcionam juntos, mas são separáveis). */
export function CoreMotionLogo({
  height = 40,
  tagline = true,
  mode = 'gradient',
  color = '#F8FAFC',
  sub = '#94A3B8',
  className,
}: {
  height?: number;
  tagline?: boolean;
  mode?: MarkMode;
  color?: string;
  sub?: string;
  className?: string;
}) {
  const markH = Math.round(height);
  const textH = height * 0.66;
  return (
    <span className={`inline-flex items-center gap-3 ${className ?? ''}`}>
      <CoreMotionMark size={markH} mode={mode} />
      <span className="flex flex-col justify-center leading-none">
        <CoreMotionWordmark height={textH} color={color} />
        {tagline && (
          <span
            className="mt-1 font-semibold uppercase"
            style={{
              color: sub,
              fontSize: Math.max(7, height * 0.19),
              letterSpacing: '0.3em',
            }}
          >
            Hub de Alta Performance
          </span>
        )}
      </span>
    </span>
  );
}
