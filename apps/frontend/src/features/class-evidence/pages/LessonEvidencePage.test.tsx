// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it, vi } from "vitest";

import type { ClassLearner } from "@/features/learners/types";

import { LessonEvidencePage } from "./LessonEvidencePage";

const learners: ClassLearner[] = [
  {
    student_id: "S-1",
    full_name: "Adaeze O.",
    notes_to_review: 0,
    notes_approved: 0,
    last_test: { lesson_title: "Fractions", band: "remediate", correct: 2, out_of: 5, taken_at: "2026-11-04T00:00:00Z" },
  },
  { student_id: "S-2", full_name: "Kelechi N.", last_test: null, notes_to_review: 0, notes_approved: 0 },
];

vi.mock("../hooks/useLessonEvidence", () => ({
  useLessonEvidence: () => ({ learners, isLoading: false, isError: false }),
}));
vi.mock("../components/StudyResultsSection", () => ({ StudyResultsSection: () => null }));
vi.mock("@/features/lesson-home/hooks/useLessonHome", () => ({
  useLessonHome: () => ({ lesson: { title: "Mixed fractions", week: 2 }, rows: { plan: {}, materials: [], learners: [] } }),
}));

afterEach(cleanup);

const open = () =>
  render(
    <MemoryRouter>
      <LessonEvidencePage lessonPeriodId="P-1" />
    </MemoryRouter>,
  );

it("shows each learner's score and band, and who has not answered", () => {
  open();

  expect(screen.getByText("Scored 2 of 5")).toBeTruthy();
  expect(screen.getByText("Needs more practice", { selector: "span.text-sm" })).toBeTruthy();
  expect(screen.getByText("Not answered", { selector: "span.text-sm" })).toBeTruthy();
});

it("opens the learner's result on this lesson from their line", () => {
  open();

  const link = screen.getByRole("link", { name: /Adaeze O\./ });

  expect(link.getAttribute("href")).toBe("/research/teacher/lessons/P-1/evidence/S-1");
});

it("narrows the list to those who have not answered", () => {
  open();

  fireEvent.click(screen.getByRole("button", { name: /Not answered/ }));

  expect(screen.queryByText("Adaeze O.")).toBeNull();
  expect(screen.getByText("Kelechi N.")).toBeTruthy();
});
