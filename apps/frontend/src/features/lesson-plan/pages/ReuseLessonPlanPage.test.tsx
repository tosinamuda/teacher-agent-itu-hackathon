// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it, vi } from "vitest";

import { ReuseLessonPlanPage } from "./ReuseLessonPlanPage";

const state = vi.hoisted(() => ({
  mutate: vi.fn(),
  data: undefined as unknown,
  push: vi.fn(),
}));

vi.mock("../components/ThisLesson", () => ({
  ThisLesson: () => <p>For this lesson: Mixed fractions</p>,
}));
vi.mock("../hooks/useReuseLessonPlan", () => ({
  useReuseLessonPlan: () => ({
    mutate: state.mutate,
    reset: vi.fn(),
    data: state.data,
    isPending: false,
    isError: false,
  }),
}));
vi.mock("@/shared/router", async (original) => ({
  ...(await original<typeof import("@/shared/router")>()),
  useRouter: () => ({ push: state.push }),
}));
vi.mock("../components/PlanSourcePicker", () => ({
  PlanSourcePicker: ({ onChange }: { onChange: (source: unknown) => void }) => (
    <button
      type="button"
      onClick={() => onChange({ kind: "version", planVersionId: "LPV-SRC" })}
    >
      Pick a plan
    </button>
  ),
}));

afterEach(() => {
  cleanup();
  state.mutate.mockClear();
  state.push.mockClear();
  state.data = undefined;
});

const open = () =>
  render(
    <MemoryRouter>
      <ReuseLessonPlanPage lessonPeriodId="P-1" />
    </MemoryRouter>,
  );

it("cannot use a plan before one is chosen", () => {
  open();

  expect(
    (screen.getByRole("button", { name: "Use this plan" }) as HTMLButtonElement)
      .disabled,
  ).toBe(true);
});

it("uses the chosen plan on this lesson, and opens the saved draft", () => {
  open();
  fireEvent.click(screen.getByRole("button", { name: "Pick a plan" }));

  fireEvent.click(screen.getByRole("button", { name: "Use this plan" }));

  const [variables, options] = state.mutate.mock.calls[0];
  expect(variables).toEqual({
    source: { kind: "version", planVersionId: "LPV-SRC" },
    choices: {},
  });
  options.onSuccess({
    status: "reused",
    plan: { plan_id: "LP-9", version_id: "LPV-9" },
  });
  expect(state.push).toHaveBeenCalledWith("/research/teacher/lesson-plan/LP-9");
});

it("names the lesson the plan is for", () => {
  open();

  expect(screen.getByText("For this lesson: Mixed fractions")).toBeTruthy();
});
