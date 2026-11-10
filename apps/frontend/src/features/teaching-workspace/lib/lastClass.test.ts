// @vitest-environment jsdom
import { afterEach, expect, it, vi } from "vitest";

import { readLastWorkspace, rememberWorkspace } from "./lastClass";

afterEach(() => {
  window.localStorage.clear();
  vi.restoreAllMocks();
});

it("remembers the class a teacher last opened", () => {
  rememberWorkspace("teacher-1", "W-2");

  expect(readLastWorkspace("teacher-1")).toBe("W-2");
});

it("keeps one class per access code", () => {
  rememberWorkspace("teacher-1", "W-1");
  rememberWorkspace("teacher-2", "W-9");

  expect(readLastWorkspace("teacher-1")).toBe("W-1");
  expect(readLastWorkspace("teacher-2")).toBe("W-9");
});

it("remembers nothing before a teacher has signed in", () => {
  rememberWorkspace(null, "W-1");

  expect(readLastWorkspace(null)).toBeNull();
});

it("opens into the primary class when the browser will not keep one", () => {
  vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
    throw new Error("blocked");
  });
  vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
    throw new Error("blocked");
  });

  expect(() => rememberWorkspace("teacher-1", "W-1")).not.toThrow();
  expect(readLastWorkspace("teacher-1")).toBeNull();
});
