// @vitest-environment jsdom
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it, vi } from "vitest";

import { ReuseLessonNotePage } from "./ReuseLessonNotePage";

const state = vi.hoisted(() => ({
  planVersionId: "LPV-NEW" as string | null,
  reuse: vi.fn(),
  push: vi.fn(),
  notes: [] as unknown[],
}));

vi.mock("../hooks/useLessonHome", () => ({
  useLessonHome: () => ({
    planVersionId: state.planVersionId,
    isLoading: false,
  }),
}));
vi.mock("@/features/content/hooks/useContent", () => ({
  useLessonContent: () => ({ data: state.notes }),
}));
vi.mock("@/features/class-evidence/hooks/useStudyResults", () => ({
  useStudySources: () => ({
    isLoading: false,
    data: [
      { plan_version_id: "V-1", lesson_title: "Algebra", lesson_note_id: "AT-STUDY", note_fits: true },
      { plan_version_id: "V-2", lesson_title: "Shapes", lesson_note_id: "AT-SHAPES", note_fits: false },
      { plan_version_id: "V-3", lesson_title: "Statistics", lesson_note_id: null, note_fits: false },
    ],
  }),
}));
vi.mock("@/features/content/api/reuseNote", () => ({
  reuseLessonNote: (...args: unknown[]) => state.reuse(...args),
}));
vi.mock("@/shared/router", async (original) => ({
  ...(await original<typeof import("@/shared/router")>()),
  useRouter: () => ({ push: state.push }),
}));
vi.mock("@/features/lesson-plan/components/PlanSourcePicker", () => ({
  PlanSourcePicker: ({ onChange }: { onChange: (source: unknown) => void }) => (
    <button
      type="button"
      onClick={() => onChange({ kind: "version", planVersionId: "LPV-SRC" })}
    >
      Pick a lesson
    </button>
  ),
}));

afterEach(() => {
  cleanup();
  state.reuse.mockReset();
  state.push.mockClear();
  state.planVersionId = "LPV-NEW";
  state.notes = [];
});

const open = () =>
  render(
    <QueryClientProvider client={new QueryClient()}>
      <MemoryRouter>
        <ReuseLessonNotePage lessonPeriodId="P-1" />
      </MemoryRouter>
    </QueryClientProvider>,
  );

const note = {
  id: "AT-1",
  type: "lesson-note",
  level: "class",
  version: 1,
  review_status: "approved",
  created_at: "2026-11-01T00:00:00Z",
};

it("asks for the plan to be approved first when it is not", () => {
  state.planVersionId = null;
  open();

  expect(screen.getByText(/Approve this lesson's plan first/)).toBeTruthy();
});

it("lists the lesson note of the chosen lesson, and copies it onto this plan", async () => {
  state.notes = [note, { ...note, id: "AT-2", type: "class-test" }];
  state.reuse.mockResolvedValue({ content_id: "AT-NEW" });
  open();
  fireEvent.click(screen.getByRole("button", { name: "Pick a lesson" }));

  expect(screen.getAllByRole("radio")).toHaveLength(1);
  fireEvent.click(screen.getByRole("radio"));
  fireEvent.click(screen.getByRole("button", { name: "Use this note" }));

  await waitFor(() =>
    expect(state.push).toHaveBeenCalledWith("/research/teacher/content/AT-NEW"),
  );
  expect(state.reuse).toHaveBeenCalledWith("AT-1", "LPV-NEW");
});

it("says when the chosen lesson has no note", () => {
  open();
  fireEvent.click(screen.getByRole("button", { name: "Pick a lesson" }));

  expect(screen.getByText("That lesson has no lesson note yet.")).toBeTruthy();
});

it("copies the evaluation's lesson note, offering only the lessons that have one", async () => {
  state.reuse.mockResolvedValue({ content_id: "AT-COPY" });
  open();

  fireEvent.click(screen.getByRole("button", { name: /The evaluation's lesson note/ }));

  expect(screen.getByText("Algebra")).toBeTruthy();
  expect(screen.queryByText("Statistics")).toBeNull();
  expect(screen.queryByRole("radio", { name: /Shapes/ })).toBeNull();

  fireEvent.click(screen.getByRole("radio", { name: /Algebra/ }));
  fireEvent.click(screen.getByRole("button", { name: "Use this note" }));

  await waitFor(() => expect(state.reuse).toHaveBeenCalledWith("AT-STUDY", "LPV-NEW"));
});
