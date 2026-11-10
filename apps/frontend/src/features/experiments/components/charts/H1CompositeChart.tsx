import {
  Bar,
  BarChart,
  CartesianGrid,
  ErrorBar,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { GroupStat } from "../../lib/experiments";
import { CHART } from "./chartTheme";

/** H1 composite quality (mean 1–5, 95% CI error bars) by condition. */
export function H1CompositeChart({ conditions }: { conditions: Record<string, GroupStat> }) {
  const data = Object.entries(conditions).map(([code, stat]) => ({
    code,
    mean: stat.mean ?? 0,
    ci: stat.ci ?? 0,
    n: stat.n,
  }));
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data} margin={{ top: 8, right: 8, bottom: 4, left: -12 }}>
        <CartesianGrid stroke={CHART.line} vertical={false} />
        <XAxis dataKey="code" stroke={CHART.muted} fontSize={12} />
        <YAxis domain={[1, 5]} stroke={CHART.muted} fontSize={12} allowDecimals />
        <Tooltip
          formatter={(value) => Number(value).toFixed(2)}
          labelStyle={{ color: CHART.ink }}
        />
        <Bar dataKey="mean" fill={CHART.accent} radius={[2, 2, 0, 0]} name="Mean (1–5)">
          <ErrorBar dataKey="ci" stroke={CHART.ink} strokeWidth={1} width={4} direction="y" />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
