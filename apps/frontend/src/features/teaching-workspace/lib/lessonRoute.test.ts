import { expect, it } from "vitest";

import { lessonRouteOf } from "./lessonRoute";

it("reads a lesson's own page", () => {
  expect(lessonRouteOf("/research/teacher/lessons/P-1")).toEqual({
    kind: "lesson",
    lessonPeriodId: "P-1",
  });
});

it("reads the pages of a lesson's plan, material and evidence", () => {
  expect(lessonRouteOf("/research/teacher/lesson-plan/LP-1")).toEqual({
    kind: "plan",
    planId: "LP-1",
  });
  expect(lessonRouteOf("/research/teacher/pack-reviews/A-1")).toEqual({
    kind: "pack",
    artefactId: "A-1",
  });
  expect(lessonRouteOf("/research/teacher/pack-reviews")).toBeNull();
  expect(lessonRouteOf("/research/teacher/content/C-1")).toEqual({
    kind: "content",
    contentId: "C-1",
  });
  expect(lessonRouteOf("/research/teacher/diagnostics/LPV-1")).toEqual({
    kind: "diagnostic",
    planVersionId: "LPV-1",
  });
});

it("reads nothing from a page that is about no lesson yet", () => {
  expect(lessonRouteOf("/research/teacher/lesson-plan")).toBeNull();
  expect(lessonRouteOf("/research/teacher/lesson-plan/new")).toBeNull();
  expect(lessonRouteOf("/research/teacher/lesson-plan/manual")).toBeNull();
  expect(lessonRouteOf("/research/teacher/learners/ST-1")).toBeNull();
});
