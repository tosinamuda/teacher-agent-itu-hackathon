import { ComparativeJudgement } from "./types";

type Rated = { rater: string; criterion_id: string };

/** The raters in a set of rows, in name order, each once. */
export function ratersOf<T extends Rated>(rows: T[]): string[] {
  return [...new Set(rows.map((row) => row.rater))].sort();
}

/** One rater's row on one criterion, if they gave one. */
export function cellOf<T extends Rated>(rows: T[], rater: string, criterionId: string): T | undefined {
  return rows.find((row) => row.rater === rater && row.criterion_id === criterionId);
}

/** A judgement in terms of the notes, not the letters: "P1, slightly", "P0, clearly" or "Same". */
export function judgementLabel(judgement: ComparativeJudgement): string {
  const favoured = judgement.favoured_condition;
  if (!favoured || favoured === "neither") return "Same";
  const strength = /clearly/i.test(judgement.choice) ? "clearly" : "slightly";
  return `${favoured}, ${strength}`;
}
