import { expect, it } from "vitest";

import type { LearnerResults } from "@/features/learners/types";

import { resultsForLesson } from "./lessonLearnerResult";

const RESULTS = {
  student_id: "S-1",
  full_name: "Student One",
  tests: [
    { lesson_period_id: "aaaa1111", lesson_title: "A", band: "extend", correct: 3, out_of: 4, taken_at: "" },
    { lesson_period_id: "bbbb2222", lesson_title: "B", band: "remediate", correct: 1, out_of: 4, taken_at: "" },
  ],
  objectives: [
    { lesson_period_id: "bbbb2222", lesson_title: "B", objective_text: "Add", band: "remediate", correct: 0, out_of: 2 },
    { lesson_period_id: "aaaa1111", lesson_title: "A", objective_text: "Take", band: "extend", correct: 2, out_of: 2 },
  ],
  lessons: [{ lesson_period_id: "aaaa1111", lesson_title: "A", correct: 3, out_of: 4, band: "extend", revision_note: "to_review", revision_note_id: "AT-1" }],
} as unknown as LearnerResults;

it("picks out one lesson's test, objectives and note", () => {
  const found = resultsForLesson(RESULTS, "aaaa1111");

  expect(found.test?.correct).toBe(3);
  expect(found.objectives.map((o) => o.objective_text)).toEqual(["Take"]);
  expect(found.lesson?.revision_note_id).toBe("AT-1");
});

it("finds the lesson whether or not its id has hyphens", () => {
  expect(resultsForLesson(RESULTS, "aaaa-1111").test?.lesson_title).toBe("A");
});

it("has nothing for a lesson the learner has no result in", () => {
  expect(resultsForLesson(RESULTS, "cccc3333")).toEqual({ test: null, objectives: [], lesson: null });
});
