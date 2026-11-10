import { expect, it } from "vitest";

import type { LessonStepStructured } from "@/shared/types/lesson-schema";

import { planSubtitle, timelineOf, totalMinutes } from "./planSummary";

const step = (step_id: string, title: string, duration_minutes?: number) =>
  ({
    step_id,
    title,
    type: "core",
    duration_minutes,
  }) as unknown as LessonStepStructured;

const STEPS = [
  step("s1", "Intro", 5),
  step("s2", "Improper to mixed", 20),
  step("s3", "Evaluation", 25),
];

it("adds up the minutes of the steps", () => {
  expect(totalMinutes(STEPS)).toBe(50);
});

it("gives each step a segment as wide as the step is long", () => {
  expect(
    timelineOf(STEPS).map((segment) => [segment.number, segment.share]),
  ).toEqual([
    [1, 10],
    [2, 40],
    [3, 50],
  ]);
});

it("gives equal segments when no step has a length", () => {
  expect(
    timelineOf([step("a", "A"), step("b", "B")]).map(
      (segment) => segment.share,
    ),
  ).toEqual([50, 50]);
});

it("says what the plan is in one line", () => {
  expect(
    planSubtitle({
      grade: "SS1",
      subject: "Mathematics",
      term: "First Term",
      week: 1,
      steps: STEPS,
    }),
  ).toBe("SS1 · Mathematics · First Term, week 1 · 3 steps · 50 minutes");
  expect(planSubtitle({ steps: [step("a", "A")] })).toBe("1 step");
});
