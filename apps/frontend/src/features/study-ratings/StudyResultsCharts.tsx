import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { CHART } from "@/features/experiments/components/charts/chartTheme";

import { AXIS, CONDITION_FILL, OUTCOME_FILL, inOrder, inkLabel } from "./chartStyle";
import { ObjectiveSeries, conditionRows, part1Rows, part2Rows } from "./chartData";
import { OUTCOMES } from "./lessonResults";
import { InstrumentCriterion, LessonResults } from "./types";

/** Part 1: each criterion's mean score out of 5, a bar per condition. */
export function Part1Chart({
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
        data={part1Rows(results, criteria)}
        margin={{ top: 8, right: 8, bottom: 4, left: -16 }}
      >
        <CartesianGrid stroke={CHART.line} vertical={false} />
        <XAxis dataKey="criterion" {...AXIS} />
        <YAxis domain={[1, 5]} ticks={[1, 2, 3, 4, 5]} {...AXIS} />
        <Tooltip formatter={(value) => Number(value).toFixed(2)} />
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

/** Part 2: for each criterion, how the comparisons split from P1 clearly better to P0. */
export function Part2Chart({
  results,
  criteria,
}: {
  results: LessonResults;
  criteria: InstrumentCriterion[];
}) {
  const rows = part2Rows(results, criteria);
  const labels = OUTCOMES.map((outcome) => outcome.label);
  return (
    <ResponsiveContainer width="100%" height={60 + rows.length * 44}>
      <BarChart
        data={rows}
        layout="vertical"
        stackOffset="expand"
        margin={{ top: 4, right: 8, bottom: 4, left: 8 }}
      >
        <XAxis type="number" hide />
        <YAxis type="category" dataKey="criterion" width={140} {...AXIS} />
        <Tooltip formatter={(value) => `${value}%`} />
        <Legend wrapperStyle={{ fontSize: 12 }} formatter={inkLabel} itemSorter={inOrder(labels)} />
        {labels.map((label, index) => (
          <Bar
            key={label}
            dataKey={label}
            stackId="split"
            fill={OUTCOME_FILL[index]}
            barSize={22}
          />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}

/**
 * Every lesson objective followed across the conditions, a thin line each, with the mean over
 * objectives drawn bold: each objective is one data point per condition.
 */
export function ObjectiveLinesChart({ series }: { series: ObjectiveSeries[] }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={conditionRows(series)} margin={{ top: 8, right: 16, bottom: 4, left: -16 }}>
        <CartesianGrid stroke={CHART.line} vertical={false} />
        <XAxis dataKey="condition" {...AXIS} />
        <YAxis domain={[1, 5]} ticks={[1, 2, 3, 4, 5]} {...AXIS} />
        <Legend wrapperStyle={{ fontSize: 12 }} formatter={inkLabel} />
        {series.map((each, index) => (
          <Line
            key={each.key}
            dataKey={each.key}
            name="Each objective"
            legendType={index === 0 ? "line" : "none"}
            stroke="#c9c3ba"
            strokeWidth={1.25}
            dot={{ r: 2, fill: "#c9c3ba", strokeWidth: 0 }}
            connectNulls
            isAnimationActive={false}
          />
        ))}
        <Line
          dataKey="mean"
          name="Mean over objectives"
          stroke={CHART.accent}
          strokeWidth={3}
          dot={{ r: 4, fill: CHART.accent, strokeWidth: 0 }}
          isAnimationActive={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
