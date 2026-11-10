// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import { questionsByObjective } from "../examQuestions";
import type { EngineManifest } from "../types";
import { ExamQuestionsView } from "./ExamQuestionsView";

afterEach(cleanup);

const manifest = {
  content_type: "exam-questions",
  plan_version_id: "LPV-1",
  unit: "lesson_objective",
  sections: [
    {
      unit_id: "lop01",
      label: "Count in millions.",
      part: {
        title: "Count in millions",
        questions: [
          {
            question: "What is one million?",
            marks: 2,
            answer: "1,000,000",
            marking_scheme: "2 marks for the numeral.",
          },
          {
            question: "Write four million.",
            marks: 1,
            answer: "4,000,000",
            marking_scheme: "1 mark.",
          },
        ],
      },
    },
    {
      unit_id: "lop02",
      label: "Count in billions.",
      part: { title: "Count in billions", questions: [] },
    },
  ],
} as unknown as EngineManifest;

it("groups the questions by objective, adding up their marks", () => {
  const [first, second] = questionsByObjective(manifest);

  expect(first.totalMarks).toBe(3);
  expect(first.questions.map((q) => q.markingScheme)).toEqual([
    "2 marks for the numeral.",
    "1 mark.",
  ]);
  expect(second.questions).toEqual([]);
});

it("numbers each question and gives its marks, with the answer kept until asked for", () => {
  render(<ExamQuestionsView manifest={manifest} />);

  expect(
    screen.getByRole("heading", { name: "Count in millions." }),
  ).toBeTruthy();
  expect(screen.getByText("2 questions · 3 marks")).toBeTruthy();
  expect(screen.getByText("1.")).toBeTruthy();
  expect(screen.getByText("2 marks")).toBeTruthy();
  expect(screen.getByText("1 mark")).toBeTruthy();
  expect(screen.getAllByText("Answer and marking scheme")).toHaveLength(2);
});

it("moves to the next objective", () => {
  render(<ExamQuestionsView manifest={manifest} />);

  fireEvent.click(screen.getByRole("button", { name: "Next" }));

  expect(
    screen.getByRole("heading", { name: "Count in billions." }),
  ).toBeTruthy();
});
