// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { ResearchManagerGate } from "./ResearchManagerGate";

const auth = vi.hoisted(() => ({ role: "anonymous" }));

vi.mock("@/shared/hooks/useAuthMe", () => ({
  useAuthMe: () => ({
    data: { role: auth.role },
    isLoading: false,
    isFetching: false,
    isError: false,
    error: null,
    refetch: vi.fn(),
  }),
  useRefreshAuthMe: () => vi.fn(),
}));
vi.mock("@/shared/lib/auth", () => ({ setAuthCode: vi.fn() }));

afterEach(cleanup);

it("does not keep a signed-in code in the box after sign-out", () => {
  const gate = () => (
    <ResearchManagerGate>
      <p>workspace</p>
    </ResearchManagerGate>
  );
  const { rerender } = render(gate());
  fireEvent.change(screen.getByLabelText("Access code"), { target: { value: "uncle-tosin" } });

  auth.role = "research_manager";
  rerender(gate());
  expect(screen.getByText("workspace")).toBeTruthy();
  auth.role = "anonymous";
  rerender(gate());

  expect((screen.getByLabelText("Access code") as HTMLInputElement).value).toBe("");
});
