// @vitest-environment jsdom
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { StartOver } from "./StartOver";

const state = vi.hoisted(() => ({
  preview: { counts: {}, blocked: [] } as { counts: Record<string, number>; blocked: string[] },
  clear: vi.fn(),
}));

vi.mock("@/features/teaching-workspace/context/TeachingWorkspaceContext", () => ({
  useTeachingWorkspace: () => ({ currentWorkspace: { id: "W-1" } }),
}));
vi.mock("../api/startOver", () => ({
  previewStartOver: async () => state.preview,
  startOver: (...args: unknown[]) => state.clear(...args),
}));

afterEach(() => {
  cleanup();
  state.clear.mockReset();
  state.preview = { counts: {}, blocked: [] };
});

const open = () =>
  render(
    <QueryClientProvider client={new QueryClient()}>
      <StartOver lessonPeriodId="P-1" />
    </QueryClientProvider>,
  );

it("says what would go, and clears the lesson only when asked", async () => {
  state.preview = { counts: { plan_versions: 1, artefacts: 7 }, blocked: [] };
  state.clear.mockResolvedValue({ counts: {}, blocked: [] });
  open();

  fireEvent.click(screen.getByRole("button", { name: "Start this lesson over" }));

  await screen.findByText(/1 plan, 7 materials/);
  expect(state.clear).not.toHaveBeenCalled();

  fireEvent.click(screen.getByRole("button", { name: "Clear this lesson" }));

  await waitFor(() => expect(state.clear).toHaveBeenCalledWith("W-1", "P-1"));
});

it("offers nothing to clear for a lesson with nothing made", async () => {
  open();

  fireEvent.click(screen.getByRole("button", { name: "Start this lesson over" }));

  await screen.findByText(/Nothing was made for this lesson yet/);
  expect(screen.queryByRole("button", { name: "Clear this lesson" })).toBeNull();
});

it("refuses a lesson the study ran on, in plain words", async () => {
  state.preview = { counts: { experiments: 1 }, blocked: ["the study ran on this lesson (experiments)"] };
  open();

  fireEvent.click(screen.getByRole("button", { name: "Start this lesson over" }));

  await screen.findByText("This is one of the study's own lessons, so it cannot be cleared.");
  expect(screen.queryByRole("button", { name: "Clear this lesson" })).toBeNull();
});

it("closes on cancel without clearing anything", async () => {
  state.preview = { counts: { artefacts: 2 }, blocked: [] };
  open();
  fireEvent.click(screen.getByRole("button", { name: "Start this lesson over" }));
  await screen.findByText(/2 materials/);

  fireEvent.click(screen.getByRole("button", { name: "Cancel" }));

  expect(screen.getByRole("button", { name: "Start this lesson over" })).toBeTruthy();
  expect(state.clear).not.toHaveBeenCalled();
});
