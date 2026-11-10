// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it, vi } from "vitest";

import { LessonConversations } from "./LessonConversations";

const row = (key: string, title: string, over: object = {}) => ({
  key,
  title,
  status: "complete",
  ...over,
});
const state = vi.hoisted(() => ({ rows: null as unknown }));

vi.mock("../hooks/useLessonHome", () => ({
  useLessonHome: () => ({ rows: state.rows }),
}));

afterEach(cleanup);

it("lists the plan's conversation and each made material's, and leaves out what is not made", () => {
  state.rows = {
    plan: row("plan", "Lesson plan", {
      href: "/research/teacher/lesson-plan/LP-1",
    }),
    materials: [
      row("lesson-note", "Lesson note", {
        href: "/research/teacher/content/C-1",
      }),
      row("revision-note", "Revision note", {
        status: "needsYou",
        action: { label: "Review", href: "/research/teacher/content/C-3" },
      }),
      row("slide-deck", "Slides", {
        status: "notStarted",
        create: { type: "slide-deck" },
      }),
      row("class-test", "Class test", {
        status: "locked",
        href: "/research/teacher/content/C-2",
      }),
    ],
    learners: [],
  };
  render(
    <MemoryRouter>
      <LessonConversations lessonPeriodId="P-1" />
    </MemoryRouter>,
  );

  expect(
    screen
      .getAllByRole("link")
      .map((link) => [link.textContent, link.getAttribute("href")]),
  ).toEqual([
    ["Lesson planOpen chat", "/research/teacher/lesson-plan/LP-1"],
    ["Lesson noteOpen chat", "/research/teacher/content/C-1"],
    ["Revision noteOpen chat", "/research/teacher/content/C-3"],
  ]);
});

it("lists no conversation for a plan that has not been started", () => {
  state.rows = {
    plan: row("plan", "Lesson plan", {
      status: "notStarted",
      action: {
        label: "Create plan",
        href: "/research/teacher/lesson-plan/new?session_id=S",
      },
    }),
    materials: [],
    learners: [],
  };
  const { container } = render(
    <MemoryRouter>
      <LessonConversations lessonPeriodId="P-1" />
    </MemoryRouter>,
  );

  expect(container.textContent).toBe("");
});
