// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it, vi } from "vitest";

import { LessonLearnerEvidencePage } from "./LessonLearnerEvidencePage";

const state = vi.hoisted(() => ({ results: null as unknown }));

vi.mock("@/features/lesson-home/hooks/useLessonHome", () => ({
  useLessonHome: () => ({ lesson: { title: "Coefficients", week: 9 } }),
}));
vi.mock("@/features/learners/hooks/useLearnerResults", () => ({
  useLearnerResults: () => ({ data: state.results, isLoading: false, isError: false }),
}));

vi.mock("../hooks/useStudyResults", () => ({
  useLearnerAnswers: () => ({ data: { source: "none", answers: [] }, isLoading: false, isError: false }),
}));

afterEach(cleanup);

const open = () =>
  render(
    <MemoryRouter>
      <LessonLearnerEvidencePage lessonPeriodId="P-1" studentId="S-1" />
    </MemoryRouter>,
  );

it("shows the learner's score, each objective and their note for this lesson only", () => {
  state.results = {
    student_id: "S-1",
    full_name: "Student Two",
    tests: [
      { lesson_period_id: "P-1", lesson_title: "Coefficients", band: "remediate", correct: 1, out_of: 4, taken_at: "", entered_by: "Teacher One · marks of student-01" },
      { lesson_period_id: "P-2", lesson_title: "Other", band: "extend", correct: 4, out_of: 4, taken_at: "" },
    ],
    objectives: [
      { lesson_period_id: "P-1", lesson_title: "Coefficients", objective_text: "Order of operations", band: "remediate", correct: 0, out_of: 2 },
      { lesson_period_id: "P-2", lesson_title: "Other", objective_text: "Something else", band: "extend", correct: 2, out_of: 2 },
    ],
    lessons: [
      { lesson_period_id: "P-1", lesson_title: "Coefficients", correct: 1, out_of: 4, band: "remediate", revision_note: "to_review", revision_note_id: "AT-9" },
    ],
  };
  open();

  expect(screen.getByRole("heading", { name: "Student Two" })).toBeTruthy();
  expect(screen.getByText("Scored 1 of 4")).toBeTruthy();
  expect(screen.getByText("Entered on their behalf: Teacher One · marks of student-01")).toBeTruthy();
  expect(screen.getByText("Order of operations")).toBeTruthy();
  expect(screen.queryByText("Something else")).toBeNull();
  expect(screen.getByText("Waiting for your review")).toBeTruthy();
  expect(screen.getByRole("link", { name: "Open note" }).getAttribute("href")).toBe("/research/teacher/pack-reviews/AT-9");
});

it("says so when the learner has no result on the lesson", () => {
  state.results = { student_id: "S-1", full_name: "Student Two", tests: [], objectives: [], lessons: [] };
  open();

  expect(screen.getByText("This learner has no result on this lesson yet.")).toBeTruthy();
});

it("leads back to the class evidence and to all of the learner's results", () => {
  state.results = { student_id: "S-1", full_name: "Student Two", tests: [], objectives: [], lessons: [] };
  open();

  expect(screen.getByRole("link", { name: /Class evidence/ }).getAttribute("href")).toBe("/research/teacher/lessons/P-1/evidence");
  expect(screen.getByRole("link", { name: /All of Student Two/ }).getAttribute("href")).toBe("/research/teacher/learners/S-1");
});
