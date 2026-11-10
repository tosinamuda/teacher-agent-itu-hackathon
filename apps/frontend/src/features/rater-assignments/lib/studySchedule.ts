import type { RatedSet } from "@/features/study-ratings/types";

/** Part 1 as a grid: each note, by condition and draw, with the sets that rated it. */
export type Part1Grid = {
  conditions: string[];
  draws: number[];
  ratedBy: (condition: string, draw: number) => RatedSet[];
};

/** One rater's Part 1 load: how many notes, how many came back short, and the dates written. */
export type RaterLoad = {
  rater: string;
  notes: number;
  short: number;
  dates: string[];
};

const sorted = <T>(values: Iterable<T>): T[] =>
  [...new Set(values)].sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));

const byRater = (a: RatedSet, b: RatedSet) => a.rater_name.localeCompare(b.rater_name);

export function part1Grid(sets: RatedSet[]): Part1Grid {
  const part1 = sets.filter((set) => set.part === 1 && set.condition && set.draw);
  const cells = new Map<string, RatedSet[]>();
  for (const set of part1) {
    const key = `${set.condition}|${set.draw}`;
    cells.set(key, [...(cells.get(key) ?? []), set].sort(byRater));
  }
  return {
    conditions: sorted(part1.map((set) => set.condition as string)),
    draws: sorted(part1.map((set) => set.draw as number)),
    ratedBy: (condition, draw) => cells.get(`${condition}|${draw}`) ?? [],
  };
}

export function raterLoads(sets: RatedSet[]): RaterLoad[] {
  const loads = new Map<string, RatedSet[]>();
  for (const set of sets.filter((each) => each.part === 1)) {
    loads.set(set.rater_name, [...(loads.get(set.rater_name) ?? []), set]);
  }
  return [...loads.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([rater, rated]) => ({
      rater,
      notes: rated.length,
      short: rated.filter((set) => set.state !== "complete").length,
      dates: sorted(rated.flatMap((set) => (set.date_completed ? [set.date_completed] : []))),
    }));
}

/** Each learner's Part 2 sets, in rater order. */
export function part2ByLearner(sets: RatedSet[]): Map<string, RatedSet[]> {
  const learners = new Map<string, RatedSet[]>();
  for (const set of sets) {
    if (set.part !== 2 || !set.learner_id) continue;
    learners.set(set.learner_id, [...(learners.get(set.learner_id) ?? []), set].sort(byRater));
  }
  return learners;
}

/** Which note a Part 2 set showed as Candidate A and which as B, e.g. "A: P1 · B: P0". */
export function candidateOrder(set: RatedSet): string | null {
  if (set.condition === "P1") return "A: P1 · B: P0";
  if (set.condition === "P0") return "A: P0 · B: P1";
  return null;
}
