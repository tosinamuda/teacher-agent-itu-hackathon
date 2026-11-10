import { ChoiceCount, ConditionMean } from "./types";

/** The five ways a Part 2 comparison could come out, P1's side first. */
export const OUTCOMES = [
  { favoured: "P1", strength: "clearly", label: "P1 clearly better" },
  { favoured: "P1", strength: "slightly", label: "P1 slightly better" },
  { favoured: "neither", strength: null, label: "About the same" },
  { favoured: "P0", strength: "slightly", label: "P0 slightly better" },
  { favoured: "P0", strength: "clearly", label: "P0 clearly better" },
] as const;

/** One condition's scores over every criterion pooled: the mean weighted by each's scores. */
export function overallMeans(means: ConditionMean[]): Map<string, ConditionMean> {
  const pooled = new Map<string, ConditionMean>();
  for (const mean of means) {
    const total = pooled.get(mean.condition);
    if (!total) {
      pooled.set(mean.condition, { ...mean, criterion_id: "all" });
      continue;
    }
    const n = total.n + mean.n;
    pooled.set(mean.condition, {
      ...total,
      mean: (total.mean * total.n + mean.mean * mean.n) / n,
      n,
      score_counts: total.score_counts.map((count, i) => count + (mean.score_counts[i] ?? 0)),
      double_rated: total.double_rated + mean.double_rated,
      both_favourable: total.both_favourable + mean.both_favourable,
    });
  }
  return pooled;
}

/** One criterion's comparisons, as a count per outcome in ``OUTCOMES`` order. */
export function outcomeCounts(counts: ChoiceCount[], criterionId: string): number[] {
  const mine = counts.filter((count) => count.criterion_id === criterionId);
  return OUTCOMES.map(
    (outcome) =>
      mine.find(
        (count) => count.favoured === outcome.favoured && count.strength === outcome.strength
      )?.count ?? 0
  );
}
