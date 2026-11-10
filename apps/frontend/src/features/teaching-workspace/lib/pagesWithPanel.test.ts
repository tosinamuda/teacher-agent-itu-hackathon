import { expect, it } from "vitest";

import { hasPanel } from "./pagesWithPanel";

it("fills the frame for the class landing and a lesson's home", () => {
  expect(hasPanel("/research/teacher/lessons")).toBe(true);
  expect(hasPanel("/research/teacher/lessons/abc")).toBe(true);
});

it("pads the forms that reuse a plan or a note", () => {
  expect(hasPanel("/research/teacher/lessons/abc/evidence")).toBe(true);
  expect(hasPanel("/research/teacher/lessons/abc/evidence/S-1")).toBe(true);
  expect(hasPanel("/research/teacher/lessons/abc/plan/new")).toBe(true);
  expect(hasPanel("/research/teacher/lessons/abc/plan/import")).toBe(false);
  expect(hasPanel("/research/teacher/lessons/abc/plan/write")).toBe(false);
  expect(hasPanel("/research/teacher/lessons/abc/reuse-plan")).toBe(false);
  expect(hasPanel("/research/teacher/lessons/abc/reuse-note")).toBe(false);
});

it("fills the frame for an opened plan, not for the generator or manual entry", () => {
  expect(hasPanel("/research/teacher/lesson-plan/LP-1")).toBe(true);
  expect(hasPanel("/research/teacher/lesson-plan/new")).toBe(false);
  expect(hasPanel("/research/teacher/lesson-plan/manual")).toBe(false);
});

it("fills the frame for a material", () => {
  expect(hasPanel("/research/teacher/content/C-1")).toBe(true);
  expect(hasPanel("/research/teacher/pack-reviews/A-1")).toBe(true);
  expect(hasPanel("/research/teacher/pack-reviews")).toBe(true);
});

it("fills the frame for the class's learners and one learner, not for the form to add one", () => {
  expect(hasPanel("/research/teacher/learners")).toBe(true);
  expect(hasPanel("/research/teacher/learners/ST-1")).toBe(true);
  expect(hasPanel("/research/teacher/learners/new")).toBe(false);
});

it("pads the pages that have no panel yet", () => {
  expect(hasPanel("/research/teacher/lesson-plan")).toBe(false);
});
