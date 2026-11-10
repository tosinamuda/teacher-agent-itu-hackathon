import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { ContrastRow } from "../../lib/experiments";
import { CHART } from "./chartTheme";

/** Adjacent-condition effect sizes (mean difference) — the staged ablation gains. */
export function PairwiseEffectChart({ contrasts }: { contrasts: ContrastRow[] }) {
  const data = contrasts.map((contrast) => ({
    label: `${contrast.to}−${contrast.from}`,
    delta: contrast.mean_diff,
  }));
  if (data.length === 0) {
    return <p className="py-8 text-center text-sm text-[color:var(--muted)]">No adjacent contrasts yet.</p>;
  }
  return (
    <ResponsiveContainer width="100%" height={240}>
      <BarChart data={data} margin={{ top: 8, right: 8, bottom: 4, left: -12 }}>
        <CartesianGrid stroke={CHART.line} vertical={false} />
        <XAxis dataKey="label" stroke={CHART.muted} fontSize={12} />
        <YAxis stroke={CHART.muted} fontSize={12} />
        <Tooltip formatter={(value) => Number(value).toFixed(2)} />
        <ReferenceLine y={0} stroke={CHART.muted} />
        <Bar dataKey="delta" name="Mean difference" radius={[2, 2, 0, 0]}>
          {data.map((entry) => (
            <Cell key={entry.label} fill={entry.delta >= 0 ? CHART.accent : CHART.danger} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
