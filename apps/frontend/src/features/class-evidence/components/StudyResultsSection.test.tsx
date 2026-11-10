// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { StudyResultsSection } from "./StudyResultsSection";

const state = vi.hoisted(() => ({
  results: {
    data: { imported: false, learners: [] as unknown[] },
    isLoading: false,
  },
  mutate: vi.fn(),
  error: null as Error | null,
}));

vi.mock("../hooks/useStudyResults", () => ({
  useStudyResults: () => state.results,
  useStudySources: () => ({
    data: [
      { plan_version_id: "V-1", lesson_title: "Mixed fractions", learners: 12, fits: true },
      { plan_version_id: "V-2", lesson_title: "Decimals", learners: 1, fits: true },
      { plan_version_id: "V-3", lesson_title: "Geometry", learners: 5, fits: false },
    ],
    isLoading: false,
    isError: false,
  }),
  useStandIns: () => ({ mutate: vi.fn(), isPending: false, isError: false, isSuccess: false }),
  useImportStudyResults: () => ({
    mutate: state.mutate,
    isPending: false,
    isError: state.error !== null,
    error: state.error,
  }),
}));

afterEach(() => {
  cleanup();
  state.mutate.mockReset();
  state.error = null;
  state.results = { data: { imported: false, learners: [] }, isLoading: false };
});

it("imports the chosen evaluation lesson", () => {
  render(<StudyResultsSection lessonPeriodId="P-1" planApproved classLearners={[]} lesson={{ title: "Algebra", week: 9 }} />);

  expect(screen.getByText("Algebra")).toBeTruthy();
  fireEvent.change(screen.getByLabelText("Take the marks from"), {
    target: { value: "V-2" },
  });
  fireEvent.click(screen.getByRole("button", { name: "Import class results" }));

  expect(state.mutate).toHaveBeenCalledWith("V-2");
  expect(screen.getByText("Decimals · 1 learner")).toBeTruthy();
  expect(screen.queryByRole("option", { name: /Geometry/ })).toBeNull();
});

it("offers nothing until the plan is approved", () => {
  const { container } = render(
    <StudyResultsSection lessonPeriodId="P-1" planApproved={false} classLearners={[]} />,
  );

  expect(container.textContent).toBe("");
});

it("says why an import was refused", () => {
  state.error = new Error('{"detail":"the_plan_lacks_the_objectives:O-1"}');
  render(<StudyResultsSection lessonPeriodId="P-1" planApproved classLearners={[]} />);

  expect(screen.getByRole("alert").textContent).toContain(
    "does not cover the objectives",
  );
});

it("lists each imported learner with their band and misconceptions", () => {
  state.results = {
    isLoading: false,
    data: {
      imported: true,
      learners: [
        {
          student_id: "S-1",
          full_name: "Adaeze O.",
          teacher_total: "1/4",
          band: "remediate",
          correct: 1,
          out_of: 4,
          objectives: [
            { misconceptions: ["M1", "M2"] },
            { misconceptions: ["M1"] },
          ],
        },
      ],
    },
  };
  render(<StudyResultsSection lessonPeriodId="P-1" planApproved classLearners={[]} />);

  expect(screen.getByText("Needs more practice")).toBeTruthy();
  expect(
    screen.getByText(/Marked 1 of 4 · teacher's total 1\/4 · M1, M2/),
  ).toBeTruthy();
  expect(
    screen.queryByRole("button", { name: "Import class results" }),
  ).toBeNull();
});

it("offers the learners who have not answered a study learner's marks each", () => {
  state.results = {
    isLoading: false,
    data: {
      imported: true,
      learners: [
        { student_id: "a", full_name: "student-01", teacher_total: "1/4", band: "remediate", correct: 1, out_of: 4, objectives: [] },
        { student_id: "b", full_name: "student-07", teacher_total: "4/4", band: "extend", correct: 4, out_of: 4, objectives: [] },
      ],
    },
  };
  render(
    <StudyResultsSection
      lessonPeriodId="P-1"
      planApproved
      classLearners={[{ student_id: "S1", full_name: "Student One", answered: false }]}
    />,
  );

  expect(screen.getByLabelText("Learner 1")).toBeTruthy();
  expect(screen.getByRole("button", { name: "Make their notes" })).toBeTruthy();
  expect((screen.getByLabelText("Study learner 1") as HTMLSelectElement).value).toBe("b");
});

it("keeps the imported marks collapsed, with how many learners they cover", () => {
  state.results = {
    isLoading: false,
    data: {
      imported: true,
      learners: [
        { student_id: "a", full_name: "student-01", teacher_total: "1/4", band: "remediate", correct: 1, out_of: 4, objectives: [] },
      ],
    },
  };
  const { container } = render(<StudyResultsSection lessonPeriodId="P-1" planApproved classLearners={[]} />);

  expect((container.querySelector("details") as HTMLDetailsElement).open).toBe(false);
  expect(screen.getByText("Imported from the evaluation · 1 learner")).toBeTruthy();
});
