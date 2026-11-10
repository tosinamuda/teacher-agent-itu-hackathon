// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it, vi } from "vitest";

import { MakePlanPage } from "./MakePlanPage";

const state = vi.hoisted(() => ({
  generate: vi.fn(),
  isGenerating: false,
  generateError: null as unknown,
  replace: vi.fn(),
}));

vi.mock("../hooks/usePlanGenerator", () => ({
  usePlanGenerator: () => ({
    generate: state.generate,
    isGenerating: state.isGenerating,
    generateError: state.generateError,
  }),
}));
vi.mock("../hooks/useDraftingProgress", () => ({
  useDraftingProgress: () => ({ lines: [], outline: null }),
}));
vi.mock("@/features/lesson-home/hooks/useLessonHome", () => ({
  useLessonHome: () => ({ lesson: { title: "Quantitative reasoning" } }),
}));
vi.mock("@/features/lesson-home/components/LessonConversations", () => ({
  LessonConversations: () => <p>Conversations</p>,
}));
vi.mock(
  "@/features/teaching-workspace/context/TeachingWorkspaceContext",
  () => ({
    useTeachingWorkspace: () => ({ currentWorkspace: { teacher_id: "T-1" } }),
  }),
);
vi.mock("@/shared/router", async (original) => ({
  ...(await original<typeof import("@/shared/router")>()),
  useRouter: () => ({ replace: state.replace, push: vi.fn() }),
}));

afterEach(() => {
  cleanup();
  state.generate.mockReset();
  state.replace.mockReset();
  state.isGenerating = false;
  state.generateError = null;
});

const open = () =>
  render(
    <MemoryRouter>
      <MakePlanPage lessonPeriodId="P-1" />
    </MemoryRouter>,
  );

it("offers the four ways to make the plan, each under the lesson", () => {
  open();

  expect(screen.getByRole("button", { name: "Generate" })).toBeTruthy();
  const hrefOf = (name: string) =>
    screen.getByRole("link", { name }).getAttribute("href");
  expect(hrefOf("Import")).toBe("/research/teacher/lessons/P-1/plan/import");
  expect(hrefOf("Write")).toBe("/research/teacher/lessons/P-1/plan/write");
  expect(hrefOf("Choose")).toBe("/research/teacher/lessons/P-1/reuse-plan");
});

it("generates the plan for this lesson and opens it when it is written", () => {
  state.generate.mockImplementation((_request, options) =>
    options.onSuccess({ plan_id: "LP-9" }),
  );
  open();

  fireEvent.click(screen.getByRole("button", { name: "Generate" }));

  expect(state.generate).toHaveBeenCalledWith(
    { session_id: "P-1", teacher_id: "T-1" },
    expect.anything(),
  );
  expect(state.replace).toHaveBeenCalledWith(
    "/research/teacher/lesson-plan/LP-9",
  );
});

it("waits for the plan while the agent writes it, in place of the ways", () => {
  state.isGenerating = true;
  open();

  expect(screen.getByText("Writing the plan")).toBeTruthy();
  expect(screen.queryByRole("button", { name: "Generate" })).toBeNull();
});

it("says why the plan was not finished and offers another go", () => {
  state.generateError = new Error("The model timed out.");
  open();

  expect(screen.getByRole("alert").textContent).toContain(
    "The model timed out.",
  );
  fireEvent.click(screen.getByRole("button", { name: "Try again" }));
  expect(state.generate).toHaveBeenCalled();
});
