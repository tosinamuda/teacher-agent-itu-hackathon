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

import { CHART } from "@/features/experiments/components/charts/chartTheme";

import { AXIS, CONDITION_FILL, inOrder, inkLabel } from "./chartStyle";
import { SCORE_LABELS, favourableRows, spreadRows } from "./proportions";
import { InstrumentCriterion, LessonResults } from "./types";

/** Scores 1 to 3 in greys, 4 in a pale accent, 5 in the accent. */
const SCORE_FILL = ["#6f6862", "#a39c93", "#d6d1c9", "#e3a684", CHART.accent];

const percent = (value: unknown) => `${Number(value).toFixed(1)}%`;

/** Part 1: each criterion's share of scores at 4 or 5, a bar per condition. */
export function FavourableChart({
  results,
  criteria,
}: {
  results: LessonResults;
  criteria: InstrumentCriterion[];
}) {
  const conditions = [...new Set(results.part_1.map((mean) => mean.condition))].sort();
  return (
    <ResponsiveContainer width="100%" height={270}>
      <BarChart
        data={favourableRows(results, criteria)}
        margin={{ top: 8, right: 8, bottom: 4, left: -8 }}
      >
        <CartesianGrid stroke={CHART.line} vertical={false} />
        <XAxis dataKey="criterion" {...AXIS} />
        <YAxis domain={[0, 100]} ticks={[0, 25, 50, 75, 100]} unit="%" {...AXIS} />
        <Tooltip formatter={percent} />
        <Legend
          wrapperStyle={{ fontSize: 12 }}
          formatter={inkLabel}
          itemSorter={inOrder(conditions)}
        />
        {conditions.map((condition) => (
          <Bar
            key={condition}
            dataKey={condition}
            fill={CONDITION_FILL[condition] ?? CHART.info}
            radius={[2, 2, 0, 0]}
          />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}

/** Part 1: how each condition's scores spread over the scale, every criterion pooled. */
export function SpreadChart({ results }: { results: LessonResults }) {
  const rows = spreadRows(results);
  const labels = [...SCORE_LABELS];
  return (
    <ResponsiveContainer width="100%" height={60 + rows.length * 44}>
      <BarChart
        data={rows}
        layout="vertical"
        stackOffset="expand"
        margin={{ top: 4, right: 8, bottom: 4, left: -16 }}
      >
        <XAxis type="number" hide />
        <YAxis type="category" dataKey="condition" {...AXIS} />
        <Tooltip formatter={percent} />
        <Legend wrapperStyle={{ fontSize: 12 }} formatter={inkLabel} itemSorter={inOrder(labels)} />
        {labels.map((label, i) => (
          <Bar key={label} dataKey={label} stackId="spread" fill={SCORE_FILL[i]} barSize={22} />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}
