// @vitest-environment jsdom
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, waitFor } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { NewLearnerPage } from "./NewStudentPage";

// The context hands its consumers the same workspace object on every render.
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
    path.startsWith("/school/subject-offerings")
      ? {
          fields_of_study: {},
          trade_subjects: [],
          core_compulsory_subjects: [],
        }
      : [],
  ),
}));

afterEach(cleanup);

it("opens with the workspace's grade and makes the code from the name", async () => {
  const { container } = render(
    <QueryClientProvider client={new QueryClient()}>
      <NewLearnerPage />
    </QueryClientProvider>,
  );
  const field = (name: string) =>
    container.querySelector<HTMLInputElement>(`[name="${name}"]`)!;

  await waitFor(() => expect(field("grade").value).toBe("JSS1"));

  fireEvent.change(field("full_name"), { target: { value: "Ada Obi" } });
  await waitFor(() => expect(field("code").value).toBe("ada-obi"));
});
