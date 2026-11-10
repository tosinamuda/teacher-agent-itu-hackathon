import { expect, it } from "vitest";

import type { ClassBand, ClassLearner } from "@/features/learners/types";

import { evidenceCounts, filterEvidence } from "./evidence";

const learner = (name: string, band?: ClassBand): ClassLearner => ({
  student_id: name,
  full_name: name,
  notes_to_review: 0,
  notes_approved: 0,
  last_test: band
    ? { lesson_title: "Fractions", band, correct: 2, out_of: 5, taken_at: "2026-11-04T00:00:00Z" }
    : null,
});
const CLASS = [learner("Adaeze", "remediate"), learner("Funmi", "remediate"), learner("Ibrahim", "reinforce"), learner("Kelechi")];

it("counts each band, and those who have not answered", () => {
  expect(evidenceCounts(CLASS)).toEqual({ all: 4, remediate: 2, reinforce: 1, extend: 0, none: 1 });
});

it("narrows the list to a band, or to those who have not answered", () => {
  expect(filterEvidence(CLASS, "remediate").map((l) => l.full_name)).toEqual(["Adaeze", "Funmi"]);
  expect(filterEvidence(CLASS, "none").map((l) => l.full_name)).toEqual(["Kelechi"]);
  expect(filterEvidence(CLASS, "all")).toHaveLength(4);
});
