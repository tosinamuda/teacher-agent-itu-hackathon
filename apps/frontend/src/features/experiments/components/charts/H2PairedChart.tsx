import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { H2Pair } from "../../lib/experiments";
import { CHART, SERIES } from "./chartTheme";

/** H2 paired P0->P1 scores, one line per focal learner — the personalisation lift. */
export function H2PairedChart({ pairs }: { pairs: H2Pair[] }) {
  const usable = pairs.filter((pair) => pair.p0 !== null && pair.p1 !== null);
  if (usable.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-[color:var(--muted)]">
        No paired P0/P1 ratings yet.
      </p>
    );
  }
  const stages: Record<string, string | number>[] = [
    { stage: "P0 base" },
    { stage: "P1 personalised" },
  ];
  usable.forEach((pair, index) => {
    const key = `Learner ${index + 1}`;
    stages[0][key] = pair.p0 ?? 0;
    stages[1][key] = pair.p1 ?? 0;
  });

  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={stages} margin={{ top: 8, right: 12, bottom: 4, left: -12 }}>
        <CartesianGrid stroke={CHART.line} vertical={false} />
        <XAxis dataKey="stage" stroke={CHART.muted} fontSize={12} />
        <YAxis domain={[1, 5]} stroke={CHART.muted} fontSize={12} />
        <Tooltip formatter={(value) => Number(value).toFixed(2)} />
        <Legend wrapperStyle={{ fontSize: 11 }} />
        {usable.map((_pair, index) => (
          <Line
            key={index}
            dataKey={`Learner ${index + 1}`}
            stroke={SERIES[index % SERIES.length]}
            strokeWidth={2}
            dot={{ r: 3 }}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
