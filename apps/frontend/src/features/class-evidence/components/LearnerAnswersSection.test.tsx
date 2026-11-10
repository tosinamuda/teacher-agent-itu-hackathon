// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { LearnerAnswersSection } from "./LearnerAnswersSection";

const state = vi.hoisted(() => ({ data: null as unknown }));

vi.mock("../hooks/useStudyResults", () => ({
  useLearnerAnswers: () => ({ data: state.data, isLoading: false, isError: false }),
}));

afterEach(cleanup);

const open = () => render(<LearnerAnswersSection lessonPeriodId="P-1" studentId="S-1" />);

it("shows what the learner answered, what was right, and the mistake", () => {
  state.data = {
    source: "marked_work",
    answers: [
      { objective_text: "Order of operations", question: "6 + 2 x 3", student_answer: "24", correct_answer: "12", correct: false, misconception: "ADD_FIRST" },
      { objective_text: "Coefficients", question: "Coefficient of 5x", student_answer: "5", correct_answer: "5", correct: true, misconception: null },
    ],
  };
  open();

  expect(screen.getByText("6 + 2 x 3")).toBeTruthy();
  expect(screen.getByText("24")).toBeTruthy();
  expect(screen.getByText("Should be: 12")).toBeTruthy();
  expect(screen.getByText("Mistake shown: ADD_FIRST")).toBeTruthy();
  expect(screen.getByText("Right:")).toBeTruthy();
  expect(screen.queryByText(/Only the questions/)).toBeNull();
});

it("says only the missed questions were kept when that is all there is", () => {
  state.data = {
    source: "missed_only",
    answers: [{ objective_text: "O", question: "Q", student_answer: "B. x", correct_answer: "A. y", correct: false, misconception: null }],
  };
  open();

  expect(screen.getByText(/Only the questions this learner got wrong were kept/)).toBeTruthy();
});

it("shows nothing when no answers are kept", () => {
  state.data = { source: "none", answers: [] };
  const { container } = open();

  expect(container.textContent).toBe("");
});
