// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { PanelResizer } from "./PanelResizer";
import { DEFAULT_PANEL_WIDTH } from "./panelWidth";

afterEach(cleanup);

const open = (width = 400) => {
  const onChange = vi.fn();
  render(<PanelResizer width={width} onChange={onChange} />);
  return { onChange, bar: screen.getByRole("separator") };
};

it("makes the panel wider with the left arrow and narrower with the right", () => {
  const { onChange, bar } = open(400);

  fireEvent.keyDown(bar, { key: "ArrowLeft" });
  fireEvent.keyDown(bar, { key: "ArrowRight" });

  expect(onChange).toHaveBeenNthCalledWith(1, 424);
  expect(onChange).toHaveBeenNthCalledWith(2, 376);
});

it("goes back to the default width on a double click", () => {
  const { onChange, bar } = open(500);

  fireEvent.doubleClick(bar);

  expect(onChange).toHaveBeenCalledWith(DEFAULT_PANEL_WIDTH);
});

it("says its width to a screen reader", () => {
  const { bar } = open(420);

  expect(bar.getAttribute("aria-valuenow")).toBe("420");
});
