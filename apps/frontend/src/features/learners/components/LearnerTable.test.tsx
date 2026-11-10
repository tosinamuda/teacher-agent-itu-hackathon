// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it } from "vitest";

import type { ClassLearner } from "../types";
import { LearnerTable } from "./LearnerTable";

afterEach(cleanup);

const ADAEZE: ClassLearner = {
  student_id: "ST-1",
  full_name: "Adaeze O.",
  last_test: {
    lesson_title: "Mixed fractions",
    band: "remediate",
    correct: 2,
    out_of: 5,
    taken_at: "2026-11-04T00:00:00Z",
  },
  notes_to_review: 1,
  notes_approved: 0,
};
const KELECHI: ClassLearner = {
  student_id: "ST-2",
  full_name: "Kelechi N.",
  last_test: null,
  notes_to_review: 0,
  notes_approved: 0,
};

function renderTable(learners: ClassLearner[], isLoading = false) {
  return render(
    <MemoryRouter>
      <LearnerTable learners={learners} isLoading={isLoading} />
    </MemoryRouter>,
  );
}

it("opens a learner from the name, with no button on the row", () => {
  renderTable([ADAEZE]);

  expect(
    screen.getByRole("link", { name: "Adaeze O." }).getAttribute("href"),
  ).toBe("/research/teacher/learners/ST-1");
  expect(screen.queryByRole("button")).toBeNull();
});

it("names each column once", () => {
  renderTable([ADAEZE]);

  const headings = screen
    .getAllByRole("columnheader")
    .map((heading) => heading.textContent);

  expect(new Set(headings).size).toBe(headings.length);
});

it("says so when a search leaves nobody", () => {
  renderTable([]);

  expect(screen.getByText(/No learners to show/)).toBeTruthy();
});

it("shows the band in words and the score", () => {
  renderTable([ADAEZE]);

  expect(screen.getByText("Needs more practice")).toBeTruthy();
  expect(screen.getByText("2 of 5")).toBeTruthy();
});

it("says a learner has not answered rather than leaving the cells empty", () => {
  renderTable([KELECHI]);

  expect(screen.getByText("Not answered")).toBeTruthy();
  expect(screen.getByText("—")).toBeTruthy();
});

it("says where a learner's notes stand", () => {
  renderTable([
    ADAEZE,
    {
      ...ADAEZE,
      student_id: "ST-3",
      full_name: "Ibrahim S.",
      notes_to_review: 0,
      notes_approved: 2,
    },
    KELECHI,
  ]);

  expect(screen.getByText("1 to review")).toBeTruthy();
  expect(screen.getByText("All approved")).toBeTruthy();
  expect(screen.getByText("No notes yet")).toBeTruthy();
});
