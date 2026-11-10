// @vitest-environment jsdom
import { act, renderHook } from "@testing-library/react";
import { beforeEach, expect, it } from "vitest";

import {
  DEFAULT_PANEL_WIDTH,
  MAX_PANEL_WIDTH,
  MIN_PANEL_WIDTH,
  clampPanelWidth,
  usePanelWidth,
} from "./panelWidth";

beforeEach(() => window.localStorage.clear());

it("keeps the width between the narrowest and widest a panel can be", () => {
  expect(clampPanelWidth(10)).toBe(MIN_PANEL_WIDTH);
  expect(clampPanelWidth(5000)).toBe(MAX_PANEL_WIDTH);
  expect(clampPanelWidth(400.4)).toBe(400);
});

it("starts at the default and remembers a change", () => {
  const first = renderHook(() => usePanelWidth());
  expect(first.result.current[0]).toBe(DEFAULT_PANEL_WIDTH);

  act(() => first.result.current[1](480));
  expect(first.result.current[0]).toBe(480);

  const later = renderHook(() => usePanelWidth());
  expect(later.result.current[0]).toBe(480);
});

it("ignores a remembered width that is not a number", () => {
  window.localStorage.setItem("right-panel-width", "wide");

  const { result } = renderHook(() => usePanelWidth());

  expect(result.current[0]).toBe(DEFAULT_PANEL_WIDTH);
});
