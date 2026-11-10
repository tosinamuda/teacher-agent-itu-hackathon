import { expect, it } from "vitest";

import type { ClassBand, ClassLearner } from "../types";
import { arrangeLearners } from "./arrangeLearners";

const learner = (full_name: string, band?: ClassBand): ClassLearner => ({
  student_id: full_name,
  full_name,
  last_test: band
    ? { lesson_title: "Fractions", band, correct: 2, out_of: 5, taken_at: "2026-11-04T00:00:00Z" }
    : null,
  notes_to_review: 0,
  notes_approved: 0,
});
const names = (learners: ClassLearner[]) => learners.map((l) => l.full_name);

it("puts the learners who need the most help first, then those with no test", () => {
  const arranged = arrangeLearners(
    [
      learner("Kelechi N."),
      learner("Chinedu E.", "extend"),
      learner("Ibrahim S.", "reinforce"),
      learner("Adaeze O.", "remediate"),
    ],
    "",
  );

  expect(names(arranged)).toEqual(["Adaeze O.", "Ibrahim S.", "Chinedu E.", "Kelechi N."]);
});

it("orders learners in the same band by name", () => {
  const arranged = arrangeLearners(
    [learner("Funmilayo A.", "remediate"), learner("Adaeze O.", "remediate")],
    "",
  );

  expect(names(arranged)).toEqual(["Adaeze O.", "Funmilayo A."]);
});

it("keeps the learners whose name holds the search, ignoring case and spaces around it", () => {
  const arranged = arrangeLearners([learner("Adaeze O."), learner("Chinedu E.")], "  CHIN ");

  expect(names(arranged)).toEqual(["Chinedu E."]);
});

it("orders by name when asked", () => {
  const arranged = arrangeLearners(
    [learner("Kelechi N."), learner("Chinedu E.", "extend"), learner("Adaeze O.", "remediate")],
    "",
    "name",
  );

  expect(names(arranged)).toEqual(["Adaeze O.", "Chinedu E.", "Kelechi N."]);
});
