import type { ClassLearner } from "../types";
import { BAND_ORDER } from "./bands";

/** Where a learner stands in the list: their band, greatest need first, then those with no test. */
const rankOf = (learner: ClassLearner): number =>
  learner.last_test ? BAND_ORDER.indexOf(learner.last_test.band) : BAND_ORDER.length;

export type LearnerOrder = "attention" | "name";

export const ORDER_LABEL: Record<LearnerOrder, string> = {
  attention: "Needs attention first",
  name: "Name",
};

/** A class's learners whose name holds the search, in the order asked for. */
export function arrangeLearners(
  learners: ClassLearner[],
  search: string,
  order: LearnerOrder = "attention",
): ClassLearner[] {
  const wanted = search.trim().toLowerCase();
  const byName = (a: ClassLearner, b: ClassLearner) => a.full_name.localeCompare(b.full_name);
  return learners
    .filter((learner) => learner.full_name.toLowerCase().includes(wanted))
    .sort(order === "name" ? byName : (a, b) => rankOf(a) - rankOf(b) || byName(a, b));
}
