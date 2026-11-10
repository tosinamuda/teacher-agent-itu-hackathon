import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { CHART, H1_DIMENSION_LABELS, SERIES, labelFor } from "./chartTheme";

type DimensionMeans = Record<string, Record<string, number | null>>;

/** H1 per-dimension means by condition (grouped bars) — shows which dimensions improve. */
export function H1DimensionChart({ dimensions }: { dimensions: DimensionMeans }) {
  const dimensionIds = Object.keys(dimensions);
  const codes = Array.from(
    new Set(dimensionIds.flatMap((id) => Object.keys(dimensions[id])))
  );
  const data = codes.map((code) => {
    const row: Record<string, string | number> = { code };
    dimensionIds.forEach((id) => {
      row[id] = dimensions[id][code] ?? 0;
    });
    return row;
  });

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data} margin={{ top: 8, right: 8, bottom: 4, left: -12 }}>
        <CartesianGrid stroke={CHART.line} vertical={false} />
        <XAxis dataKey="code" stroke={CHART.muted} fontSize={12} />
        <YAxis domain={[1, 5]} stroke={CHART.muted} fontSize={12} />
        <Tooltip formatter={(value) => Number(value).toFixed(2)} />
        <Legend wrapperStyle={{ fontSize: 11 }} />
        {dimensionIds.map((id, index) => (
          <Bar
            key={id}
            dataKey={id}
            name={labelFor(H1_DIMENSION_LABELS, id)}
            fill={SERIES[index % SERIES.length]}
            radius={[2, 2, 0, 0]}
          />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}
