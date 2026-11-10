import { shortName } from "./chartData";
import { overallMeans } from "./lessonResults";
import { ConditionMean, InstrumentCriterion, LessonResults } from "./types";

/** The five points of the scale, as a chart names them. */
export const SCORE_LABELS = ["Score 1", "Score 2", "Score 3", "Score 4", "Score 5"] as const;

/** A count out of a total, and that as a percentage to one decimal place. */
export type Share = { count: number; of: number; percent: number };

export const shareOf = (count: number, of: number): Share => ({
  count,
  of,
  percent: of ? Math.round((count / of) * 1000) / 10 : 0,
});

/** Scores of 4 or 5, which the study counts as favourable, out of all the scores. */
export const favourable = (mean: ConditionMean): Share =>
  shareOf((mean.score_counts[3] ?? 0) + (mean.score_counts[4] ?? 0), mean.n);

/** Cells both raters scored 4 or 5, out of the cells two raters scored. */
export const bothFavourable = (mean: ConditionMean): Share =>
  shareOf(mean.both_favourable, mean.double_rated);

export type ShareRow = { criterion: string } & Record<string, number | string>;

/** One row per criterion, and one for all criteria, each condition's favourable percentage. */
export function favourableRows(
  results: LessonResults,
  criteria: InstrumentCriterion[],
): ShareRow[] {
  const rows: ShareRow[] = criteria.map((criterion) => {
    const row: ShareRow = { criterion: shortName(criterion) };
    for (const mean of results.part_1.filter((m) => m.criterion_id === criterion.id)) {
      row[mean.condition] = favourable(mean).percent;
    }
    return row;
  });
  const all: ShareRow = { criterion: "All criteria" };
  for (const [condition, mean] of overallMeans(results.part_1)) {
    all[condition] = favourable(mean).percent;
  }
  return [...rows, all];
}

export type SpreadRow = { condition: string; n: number } & Record<string, number | string>;

/** One row per condition: each score's percentage of its scores, every criterion pooled. */
export function spreadRows(results: LessonResults): SpreadRow[] {
  return [...overallMeans(results.part_1).values()]
    .sort((a, b) => a.condition.localeCompare(b.condition))
    .map((mean) => {
      const row: SpreadRow = { condition: mean.condition, n: mean.n };
      SCORE_LABELS.forEach((label, i) => {
        row[label] = shareOf(mean.score_counts[i] ?? 0, mean.n).percent;
      });
      return row;
    });
}
