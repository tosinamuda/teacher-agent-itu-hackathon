import { expect, it } from "vitest";

import type { HomeRow } from "./lessonHome";
import { lessonSidebarGroups } from "./lessonSidebar";

const HOME = "/research/teacher/lessons/P-1";
const row = (key: string, over: Partial<HomeRow> = {}): HomeRow => ({
  key,
  title: key,
  status: "complete",
  ...over,
});
const rows = {
  plan: row("Plan", { href: "/research/teacher/lesson-plan/LP-1" }),
  materials: [
    row("Lesson note", { href: "/research/teacher/content/C-1" }),
    row("Slides", { status: "notStarted", create: { type: "slides" } }),
  ],
  learners: [row("Class evidence", { status: "locked" })],
};

it("lists the overview and the plan, the materials and the learners' lines in that order", () => {
  const groups = lessonSidebarGroups(HOME, rows, HOME);

  expect(groups.map((group) => group.items.map((item) => item.label))).toEqual([
    ["Overview", "Plan"],
    ["Lesson note", "Slides"],
    ["Class evidence"],
  ]);
  expect(groups[1].heading).toBe("Materials");
});

it("keeps a locked line in the list, dimmed and not a link", () => {
  const evidence = lessonSidebarGroups(HOME, rows, HOME)[2].items[0];

  expect(evidence).toEqual({ label: "Class evidence", disabled: true });
});

it("selects the material whose page is open, and the plan on any plan page", () => {
  const onMaterial = lessonSidebarGroups(
    HOME,
    rows,
    "/research/teacher/content/C-1",
  );
  expect(onMaterial[1].items[0].active).toBe(true);
  expect(onMaterial[0].items[1].active).toBe(false);

  const onPlan = lessonSidebarGroups(
    HOME,
    rows,
    "/research/teacher/lesson-plan/LP-1",
  );
  expect(onPlan[0].items[1].active).toBe(true);
  expect(onPlan[0].items[0].active).toBe(false);
});

it("selects the overview on the lesson's own page, and a way back to it from anywhere", () => {
  const onHome = lessonSidebarGroups(HOME, rows, HOME)[0].items[0];
  expect(onHome).toEqual({ label: "Overview", href: HOME, active: true });

  const onMaterial = lessonSidebarGroups(
    HOME,
    rows,
    "/research/teacher/content/C-1",
  )[0].items[0];
  expect(onMaterial).toMatchObject({ href: HOME, active: false });
});

it("sends a material not made yet to the lesson, and never selects it", () => {
  const slides = lessonSidebarGroups(HOME, rows, HOME)[1].items[1];

  expect(slides).toMatchObject({ label: "Slides", href: HOME, active: false });
});

it("marks the materials the agent is writing", () => {
  const groups = lessonSidebarGroups(HOME, rows, HOME, new Set(["Slides"]));

  expect(groups[1].items.map((item) => item.working)).toEqual([false, true]);
});
