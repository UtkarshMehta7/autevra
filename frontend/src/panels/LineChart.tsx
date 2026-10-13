import { niceExtent, ticks } from "../state/engineering";

export interface Series {
  label: string;
  values: number[];
  color: string;
  dashed?: boolean;
}

interface Props {
  title: string;
  unit: string;
  t: number[];
  series: Series[];
  /** Horizontal reference lines, e.g. travel limits. */
  limits?: { value: number; label: string }[];
  baselineT?: number[];
  height?: number;
}

const W = 420, PAD = { l: 44, r: 8, t: 18, b: 22 };

/** Plain SVG line chart of solver output; every point drawn is a computed sample. */
export function LineChart({ title, unit, t, series, limits = [], baselineT, height = 150 }: Props) {
  const all = series.flatMap((s) => s.values);
  const [lo, hi] = niceExtent(all, limits.map((l) => l.value));
  const tMax = Math.max(t[t.length - 1] ?? 1, baselineT?.[baselineT.length - 1] ?? 0);
  const x = (v: number) => PAD.l + (v / tMax) * (W - PAD.l - PAD.r);
  const y = (v: number) => PAD.t + (1 - (v - lo) / (hi - lo)) * (height - PAD.t - PAD.b);
  const path = (ts: number[], vs: number[]) =>
    vs.map((v, i) => `${i ? "L" : "M"}${x(ts[i]).toFixed(1)},${y(v).toFixed(1)}`).join("");

  return (
    <svg className="chart" viewBox={`0 0 ${W} ${height}`} role="img" aria-label={title}>
      <text x={PAD.l} y={12} className="chart-title">{title} ({unit})</text>
      {ticks([lo, hi]).map((v) => (
        <g key={v}>
          <line x1={PAD.l} x2={W - PAD.r} y1={y(v)} y2={y(v)} className="grid" />
          <text x={PAD.l - 4} y={y(v) + 3} className="tick" textAnchor="end">{v}</text>
        </g>
      ))}
      {ticks([0, tMax]).map((v) => (
        <text key={v} x={x(v)} y={height - 6} className="tick" textAnchor="middle">{v} s</text>
      ))}
      {limits.map((l) => (
        <g key={l.label}>
          <line x1={PAD.l} x2={W - PAD.r} y1={y(l.value)} y2={y(l.value)} className="limit" />
          <text x={W - PAD.r} y={y(l.value) - 3} className="tick limit-label" textAnchor="end">
            {l.label}
          </text>
        </g>
      ))}
      {series.map((s) => (
        <path key={s.label} d={path(s.dashed && baselineT ? baselineT : t, s.values)}
          stroke={s.color} fill="none" strokeWidth={s.dashed ? 1 : 1.5}
          strokeDasharray={s.dashed ? "4 3" : undefined} />
      ))}
      <g className="legend">
        {series.map((s, i) => (
          <text key={s.label} x={W - PAD.r - (series.length - 1 - i) * 92} y={12}
            textAnchor="end" fill={s.color}>{s.label}</text>
        ))}
      </g>
    </svg>
  );
}
