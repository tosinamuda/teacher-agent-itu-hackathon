// @vitest-environment jsdom
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { LearnerProfile } from "../types";
import { LearnerDetailPage } from "./StudentDetailPage";

const LEARNER: LearnerProfile = {
  student_id: "ST-7",
  code: "stu-7",
  full_name: "Ada Obi",
  grade: "JSS1",
  track: "General",
  time_budget_minutes: 30,
};
const WORKSPACE = { currentWorkspace: { grade_level: "JSS1" } };
const ROUTER = { replace: vi.fn(), push: vi.fn() };

vi.mock(
  "@/features/teaching-workspace/context/TeachingWorkspaceContext",
  () => ({
    useTeachingWorkspace: () => WORKSPACE,
  }),
);
vi.mock("@/shared/router", () => ({ useRouter: () => ROUTER }));
vi.mock("@/shared/api/client", () => ({
  apiFetch: vi.fn(async (path: string) =>
    path.startsWith("/learners/")
      ? LEARNER
      : path.startsWith("/school/subject-offerings")
        ? {
            fields_of_study: {},
            trade_subjects: [],
            core_compulsory_subjects: [],
          }
        : [],
  ),
}));

afterEach(cleanup);

it("edits the loaded learner, and a cancelled edit reopens with the saved values", async () => {
  const { container } = render(
    <QueryClientProvider client={new QueryClient()}>
      <LearnerDetailPage learnerId="stu-7" />
    </QueryClientProvider>,
  );
  const field = (name: string) =>
    container.querySelector<HTMLInputElement>(`[name="${name}"]`)!;
  const edit = async () =>
    fireEvent.click(await screen.findByRole("button", { name: /edit/i }));

  await edit();
  expect([
    field("full_name").value,
    field("time_budget_minutes").value,
  ]).toEqual(["Ada Obi", "30"]);

  fireEvent.change(field("full_name"), { target: { value: "Someone Else" } });
  fireEvent.click(screen.getByRole("button", { name: "Cancel" }));
  await edit();

  await waitFor(() => expect(field("full_name").value).toBe("Ada Obi"));
});
