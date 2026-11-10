import { OUTCOMES, outcomeCounts, overallMeans } from "./lessonResults";
import { InstrumentCriterion, LessonResults, ObjectiveMean } from "./types";

/** Short names for the instrument's criteria, for a chart's axis; the full name is the fallback. */
const SHORT: Record<string, string> = {
  curriculum_objective_alignment: "Objective",
  lesson_context_alignment: "Taught lesson",
  instructional_quality: "Correct & useful",
  learner_evidence_alignment: "Learner evidence",
  adaptive_calibration: "Support & challenge",
  instructional_integrity: "Correct & focused",
};

export const shortName = (criterion: InstrumentCriterion) => SHORT[criterion.id] ?? criterion.name;

export type Part1Row = { criterion: string } & Record<string, number | string>;

/** One row per criterion, and one for all criteria, each condition's mean as a column. */
export function part1Rows(results: LessonResults, criteria: InstrumentCriterion[]): Part1Row[] {
  const rows: Part1Row[] = criteria.map((criterion) => {
    const row: Part1Row = { criterion: shortName(criterion) };
    for (const mean of results.part_1.filter((m) => m.criterion_id === criterion.id)) {
      row[mean.condition] = Number(mean.mean.toFixed(2));
    }
    return row;
  });
  const all: Part1Row = { criterion: "All criteria" };
  for (const [condition, mean] of overallMeans(results.part_1)) {
    all[condition] = Number(mean.mean.toFixed(2));
  }
  return [...rows, all];
}

export type Part2Row = { criterion: string; total: number } & Record<string, number | string>;

/** One row per criterion, each outcome's share of its comparisons, in percent. */
export function part2Rows(results: LessonResults, criteria: InstrumentCriterion[]): Part2Row[] {
  return criteria.map((criterion) => {
    const counts = outcomeCounts(results.part_2, criterion.id);
    const total = counts.reduce((sum, count) => sum + count, 0);
    const row: Part2Row = { criterion: shortName(criterion), total };
    OUTCOMES.forEach((outcome, index) => {
      row[outcome.label] = total ? Math.round((counts[index] / total) * 1000) / 10 : 0;
    });
    return row;
  });
}

/** One objective of one lesson, followed across the conditions. */
export type ObjectiveSeries = {
  key: string;
  lesson: string;
  text: string;
  means: Record<string, number>;
};

/** Each objective's means by condition, in lesson order. */
export function objectiveSeries(objectives: ObjectiveMean[]): ObjectiveSeries[] {
  const series = new Map<string, ObjectiveSeries>();
  for (const point of objectives) {
    const key = `${point.lesson} · ${point.objective_id}`;
    const entry = series.get(key) ?? {
      key,
      lesson: point.lesson,
      text: point.objective_text || point.objective_id,
      means: {},
    };
    entry.means[point.condition] = Number(point.mean.toFixed(2));
    series.set(key, entry);
  }
  return [...series.values()].sort((a, b) => a.key.localeCompare(b.key));
}

export type ConditionRow = { condition: string; mean: number } & Record<string, number | string>;

/** One row per condition: every objective's mean as a column, and the mean over objectives. */
export function conditionRows(series: ObjectiveSeries[]): ConditionRow[] {
  const conditions = [...new Set(series.flatMap((each) => Object.keys(each.means)))].sort();
  return conditions.map((condition) => {
    const values = series.flatMap((each) =>
      each.means[condition] === undefined ? [] : [each.means[condition]],
    );
    const row: ConditionRow = {
      condition,
      mean: Number((values.reduce((sum, value) => sum + value, 0) / values.length).toFixed(2)),
    };
    for (const each of series) {
      if (each.means[condition] !== undefined) row[each.key] = each.means[condition];
    }
    return row;
  });
}
