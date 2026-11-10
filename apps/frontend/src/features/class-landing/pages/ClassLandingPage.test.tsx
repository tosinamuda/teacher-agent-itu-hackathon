// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it, vi } from "vitest";

import { ClassLandingPage } from "./ClassLandingPage";

const state = vi.hoisted(() => ({
  setWorkspace: vi.fn(),
  lessons: { lessons: [{}, {}], todo: [{ lesson_period_id: "P1" }, {}] } as {
    lessons: unknown[];
    todo: unknown[];
  },
  reviews: [] as unknown[],
  dates: {} as { current_week_number?: number; starts_on?: string },
}));

const FIRST = {
  id: "W1",
  term: "First Term",
  class_id: "C1",
  subject_code: "MTH",
  class_name: "JSS1",
  subject_name: "Mathematics",
  term_class_subject_id: "T1",
};
const SECOND = {
  ...FIRST,
  id: "W2",
  term: "Second Term",
  term_class_subject_id: "T2",
};

vi.mock(
  "@/features/teaching-workspace/context/TeachingWorkspaceContext",
  () => ({
    useTeachingWorkspace: () => ({
      workspaces: [FIRST, SECOND],
      currentWorkspace: FIRST,
      setWorkspace: state.setWorkspace,
    }),
  }),
);
vi.mock("@/features/curriculum/hooks/useSchemeOfWork", () => ({
  useSchemeOfWork: () => ({
    isLoading: false,
    isError: false,
    data: {
      current_week_number: state.dates.current_week_number,
      weeks: [
        {
          id: "K1",
          week_number: 1,
          starts_on: state.dates.starts_on,
          title: "Fractions",
          lesson_periods: [
            {
              id: "P1",
              period_number: 1,
              title: null,
              subtopic_title: "Meaning of fraction",
            },
          ],
        },
        {
          id: "K2",
          week_number: 2,
          title: "Mixed numbers",
          lesson_periods: [],
        },
      ],
    },
  }),
}));
vi.mock("@/features/teaching-workspace/hooks/useLessonReviews", () => ({
  useLessonReviews: () => ({ reviews: state.reviews }),
}));
vi.mock("@/features/teaching-workspace/hooks/useWorkspaceLessons", () => ({
  useWorkspaceLessons: () => state.lessons,
}));
vi.mock("@/features/pack-review/hooks/usePendingPacks", () => ({
  usePendingPacks: () => ({ packs: [] }),
}));

afterEach(() => {
  cleanup();
  state.setWorkspace.mockClear();
  state.dates = {};
  state.reviews = [];
});

const open = () =>
  render(
    <MemoryRouter>
      <ClassLandingPage />
    </MemoryRouter>,
  );

it("lists the weeks with how many lessons each has", () => {
  open();

  expect(screen.getByText("Wk 1")).toBeTruthy();
  expect(screen.getByText("1 lesson")).toBeTruthy();
  expect(screen.getByText("0 lessons")).toBeTruthy();
});

it("opens a week to its lessons, each lesson one link to its page", () => {
  open();

  fireEvent.click(screen.getByRole("button", { name: /Fractions/ }));

  expect(
    screen
      .getByRole("link", { name: /Meaning of fraction/ })
      .getAttribute("href"),
  ).toBe("/research/teacher/lessons/P1");
});

it("tells a class with nothing planned to open a week and then a lesson", () => {
  open();

  expect(
    screen.getByText("Open a week, then open a lesson to start planning."),
  ).toBeTruthy();
});

it("says nothing of planning once a lesson has a plan", () => {
  state.lessons = { lessons: [{}, {}], todo: [{}] };
  open();

  expect(screen.queryByText(/start planning/)).toBeNull();
  state.lessons = { lessons: [{}, {}], todo: [{}, {}] };
});

it("switches to another term of the same class", () => {
  open();

  fireEvent.change(screen.getByLabelText("Term"), { target: { value: "W2" } });

  expect(state.setWorkspace).toHaveBeenCalledWith(SECOND);
});

it("shows the week the term is in, open, with the day it starts", () => {
  state.dates = { current_week_number: 2, starts_on: "2026-09-14" };
  open();

  expect(screen.getByText("This week")).toBeTruthy();
  expect(screen.getByText("14 Sep")).toBeTruthy();
  expect(
    screen
      .getByRole("button", { name: /Mixed numbers/ })
      .getAttribute("aria-expanded"),
  ).toBe("true");
});

it("opens the current week from the button, whatever was open", () => {
  state.dates = { current_week_number: 2 };
  open();
  fireEvent.click(screen.getByRole("button", { name: /Fractions/ }));
  Element.prototype.scrollIntoView = vi.fn();

  fireEvent.click(screen.getByRole("button", { name: "Go to this week" }));

  expect(
    screen
      .getByRole("button", { name: /Mixed numbers/ })
      .getAttribute("aria-expanded"),
  ).toBe("true");
  expect(
    screen
      .getByRole("button", { name: /Fractions/ })
      .getAttribute("aria-expanded"),
  ).toBe("false");
});

it("offers no jump to this week when the term has no dates", () => {
  open();

  expect(screen.queryByRole("button", { name: "Go to this week" })).toBeNull();
  expect(screen.queryByText("This week")).toBeNull();
});

it("marks a week with what waits in its lessons and says it on the lesson", () => {
  state.reviews = [
    {
      lesson_period_id: "P1",
      plans_to_approve: 0,
      materials_to_review: 0,
      notes_to_review: 3,
      oldest_kind: "lesson-note",
      waiting_since: new Date().toISOString(),
    },
  ];
  open();

  expect(screen.getByRole("img", { name: "3 waiting" })).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: /Fractions/ }));
  expect(screen.getByText("3 notes to review")).toBeTruthy();
});

it("offers the first lesson with no plan as where to start", () => {
  state.lessons = { lessons: [{}, {}], todo: [{ lesson_period_id: "P1" }] };
  open();

  expect(screen.getByText("Meaning of fraction")).toBeTruthy();
  expect(
    screen.getByRole("link", { name: "Start planning" }).getAttribute("href"),
  ).toBe("/research/teacher/lessons/P1");
});

it("puts what has waited longest on a card, with the button that reviews it", () => {
  state.reviews = [
    {
      lesson_period_id: "P1",
      plans_to_approve: 0,
      materials_to_review: 1,
      notes_to_review: 0,
      oldest_kind: "slide-deck",
      waiting_since: new Date().toISOString(),
    },
  ];
  open();

  expect(
    screen.getByRole("link", { name: "Review slides" }).getAttribute("href"),
  ).toBe("/research/teacher/lessons/P1");
  expect(screen.queryByRole("link", { name: "Start planning" })).toBeNull();
});

it("says which week of the term it is", () => {
  state.dates = { current_week_number: 2 };
  open();

  expect(screen.getByText("Week 2 of 2")).toBeTruthy();
});
