import { expect, it } from "vitest";

import type { TermClassSubject } from "@/features/curriculum/hooks/useSchemeOfWork";
import type { TeachingWorkspace } from "@/features/teaching-workspace/types";

import type { LessonReview } from "@/features/teaching-workspace/api/lessonReviews";

import {
  lessonCountText,
  lessonToStart,
  longestWaiting,
  sinceText,
  termsOf,
  waitingText,
  weekRows,
} from "./weeks";

const scheme = {
  weeks: [
    {
      id: "W2",
      week_number: 2,
      title: "Mixed numbers",
      lesson_periods: [
        { id: "P2", period_number: 2, title: null, subtopic_title: null },
        {
          id: "P1",
          period_number: 1,
          title: null,
          subtopic_title: "Mixed fractions",
        },
      ],
    },
    { id: "W1", week_number: 1, title: "Fractions", lesson_periods: [] },
  ],
} as unknown as TermClassSubject;

it("lists the weeks in order, each with its lessons in order", () => {
  const rows = weekRows(scheme);

  expect(rows.map((row) => row.number)).toEqual([1, 2]);
  expect(rows[1].lessons.map((lesson) => lesson.title)).toEqual([
    "Mixed fractions",
    "Lesson 2",
  ]);
});

it("counts lessons in the singular and the plural", () => {
  expect(lessonCountText(1)).toBe("1 lesson");
  expect(lessonCountText(3)).toBe("3 lessons");
  expect(lessonCountText(0)).toBe("0 lessons");
});

it("finds the other terms of the same class and subject", () => {
  const ws = (
    id: string,
    class_id: string,
    subject_code: string,
    term: string,
  ) => ({ id, class_id, subject_code, term }) as unknown as TeachingWorkspace;
  const first = ws("a", "C1", "MTH", "First Term");
  const all = [
    first,
    ws("b", "C1", "MTH", "Second Term"),
    ws("c", "C2", "MTH", "First Term"),
    ws("d", "C1", "ENG", "First Term"),
  ];

  expect(termsOf(all, first).map((w) => w.id)).toEqual(["a", "b"]);
  expect(termsOf(all, null)).toEqual([]);
});

const review = (
  lesson: string,
  plans: number,
  materials: number,
  notes: number,
): LessonReview => ({
  lesson_period_id: lesson,
  plans_to_approve: plans,
  materials_to_review: materials,
  notes_to_review: notes,
  oldest_kind: "slide-deck",
  waiting_since: "2026-11-02T09:00:00Z",
});

it("says what waits in a lesson, and nothing when nothing does", () => {
  expect(waitingText(review("P1", 1, 0, 0))).toBe("Plan to approve");
  expect(waitingText(review("P1", 0, 1, 3))).toBe(
    "1 material to review · 3 notes to review",
  );
  expect(waitingText(review("P1", 0, 0, 0))).toBeNull();
  expect(waitingText(undefined)).toBeNull();
});

it("adds up what waits across the lessons of a week", () => {
  const rows = weekRows(scheme, [review("P1", 1, 0, 2), review("P2", 0, 1, 0)]);

  expect(rows[1].waiting).toBe(4);
  expect(rows[0].waiting).toBe(0);
  expect(rows[1].lessons.map((lesson) => lesson.waiting)).toEqual([
    "Plan to approve · 2 notes to review",
    "1 material to review",
  ]);
});

it("starts with the first lesson that has no plan, this week's before the others", () => {
  const rows = weekRows({
    ...scheme,
    current_week_number: 2,
  } as TermClassSubject);
  const noPlan = new Set(["P1", "P2"]);

  expect(lessonToStart(rows, noPlan, [])).toEqual({
    id: "P1",
    title: "Mixed fractions",
    weekNumber: 2,
  });
  expect(lessonToStart(rows, noPlan, [review("P1", 1, 0, 0)])).toEqual({
    id: "P2",
    title: "Lesson 2",
    weekNumber: 2,
  });
  expect(lessonToStart(rows, new Set(), [])).toBeNull();
});

it("names the lesson that has waited longest and what to do about it", () => {
  const rows = weekRows(scheme);
  const newer = {
    ...review("P2", 0, 1, 0),
    waiting_since: "2026-11-05T09:00:00Z",
    oldest_kind: "lesson-note",
  };
  const older = review("P1", 0, 1, 0);

  expect(
    longestWaiting(rows, [newer, older], new Date("2026-11-04T12:00:00Z")),
  ).toEqual({
    id: "P1",
    title: "Mixed fractions",
    weekNumber: 2,
    since: "Monday",
    action: "Review slides",
  });
  expect(longestWaiting(rows, [], new Date())).toBeNull();
});

it("says a day of the week for a wait of under a week, and the date for longer", () => {
  expect(
    sinceText("2026-11-02T09:00:00Z", new Date("2026-11-04T12:00:00Z")),
  ).toBe("Monday");
  expect(
    sinceText("2026-10-02T09:00:00Z", new Date("2026-11-04T12:00:00Z")),
  ).toBe("2 Oct");
});
