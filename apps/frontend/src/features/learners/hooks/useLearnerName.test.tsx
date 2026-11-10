// @vitest-environment jsdom
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import type { ReactNode } from "react";
import { expect, it, vi } from "vitest";

import { useLearnerName } from "./useLearnerName";

vi.mock("@/features/teaching-workspace/context/TeachingWorkspaceContext", () => ({
  useTeachingWorkspace: () => ({ currentWorkspace: { id: "W-1" } }),
}));
vi.mock("@/shared/api/client", () => ({
  apiFetch: async () => ({ learners: [{ student_id: "S-1", full_name: "Adebayo Oluwaseun" }] }),
}));

const wrapper = ({ children }: { children: ReactNode }) => (
  <QueryClientProvider client={new QueryClient()}>{children}</QueryClientProvider>
);

it("names a learner of the open class", async () => {
  const { result } = renderHook(() => useLearnerName("S-1"), { wrapper });

  await waitFor(() => expect(result.current).toBe("Adebayo Oluwaseun"));
});

it("has no name for a learner who is not in the open class", async () => {
  const { result } = renderHook(() => useLearnerName("S-9"), { wrapper });

  await new Promise((resolve) => setTimeout(resolve, 50));
  expect(result.current).toBeNull();
});
