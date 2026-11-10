// @vitest-environment jsdom
import { act, cleanup, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";

import { useProgressLines } from "./useProgressLines";

const api = vi.hoisted(() => ({ apiFetch: vi.fn() }));
vi.mock("@/shared/api/client", () => api);

const line = (id: number) => ({ id, kind: "tool", data: { tool: "add_part" } });

beforeEach(() => api.apiFetch.mockReset());
afterEach(cleanup);

it("shows nothing of the run before while the next one starts, and keeps a stopped run's lines", async () => {
  api.apiFetch.mockResolvedValueOnce({ lines: [line(1), line(2)], next: 2 });
  const hook = renderHook(
    ({ running, keep }) =>
      useProgressLines("/progress", { a: "1" }, running, keep),
    { initialProps: { running: true, keep: false } },
  );
  await act(async () => undefined);
  expect(hook.result.current.map((l) => l.id)).toEqual([1, 2]);

  hook.rerender({ running: false, keep: true });
  await act(async () => undefined);
  expect(hook.result.current.map((l) => l.id)).toEqual([1, 2]);

  api.apiFetch.mockReturnValueOnce(new Promise(() => undefined));
  hook.rerender({ running: true, keep: false });
  expect(hook.result.current).toEqual([]);
});
