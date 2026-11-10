import { BAND_LABEL } from "@/features/learners/lib/bands";
import type { ClassBand, ClassLearner } from "@/features/learners/types";

/** What the evidence list is narrowed to: everyone, one band, or those who have not answered. */
export type EvidenceFilter = "all" | ClassBand | "none";

export const FILTERS: { key: EvidenceFilter; label: string }[] = [
  { key: "all", label: "All" },
  { key: "remediate", label: BAND_LABEL.remediate },
  { key: "reinforce", label: BAND_LABEL.reinforce },
  { key: "extend", label: BAND_LABEL.extend },
  { key: "none", label: "Not answered" },
];

const filterKeyOf = (learner: ClassLearner): Exclude<EvidenceFilter, "all"> =>
  learner.last_test ? learner.last_test.band : "none";

export function filterEvidence(learners: ClassLearner[], filter: EvidenceFilter): ClassLearner[] {
  return filter === "all" ? learners : learners.filter((learner) => filterKeyOf(learner) === filter);
}

/** How many learners each filter would show. */
export function evidenceCounts(learners: ClassLearner[]): Record<EvidenceFilter, number> {
  const counts: Record<EvidenceFilter, number> = { all: learners.length, remediate: 0, reinforce: 0, extend: 0, none: 0 };
  for (const learner of learners) counts[filterKeyOf(learner)] += 1;
  return counts;
}
