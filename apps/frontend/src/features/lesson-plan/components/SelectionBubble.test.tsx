// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { SelectionBubble } from "./SelectionBubble";

afterEach(cleanup);

const rect = { left: 40, bottom: 100 } as DOMRect;

const open = (props: Partial<Parameters<typeof SelectionBubble>[0]> = {}) => {
  const handlers = {
    onAsk: vi.fn(),
    onEdit: vi.fn(),
    onDismiss: vi.fn(),
    ...props,
  };
  render(<SelectionBubble rect={rect} {...handlers} />);
  return handlers;
};

it("asks what should change, and sends it from the same place", () => {
  const { onAsk } = open();

  fireEvent.click(
    screen.getByRole("button", { name: "Ask the agent about this" }),
  );
  const box = screen.getByLabelText("What should change?");
  fireEvent.change(box, { target: { value: "Add a word problem." } });
  fireEvent.click(screen.getByRole("button", { name: "Send" }));

  expect(onAsk).toHaveBeenCalledWith("Add a word problem.");
});

it("sends with Enter, and sends nothing while the request is empty", () => {
  const { onAsk } = open();
  fireEvent.click(
    screen.getByRole("button", { name: "Ask the agent about this" }),
  );
  const box = screen.getByLabelText("What should change?");

  fireEvent.keyDown(box, { key: "Enter" });
  expect(onAsk).not.toHaveBeenCalled();

  fireEvent.change(box, { target: { value: "Shorten it." } });
  fireEvent.keyDown(box, { key: "Enter" });
  expect(onAsk).toHaveBeenCalledWith("Shorten it.");
});

it("offers to edit when the plan can be edited, and not otherwise", () => {
  const { onEdit } = open();
  fireEvent.click(screen.getByRole("button", { name: "Edit this by hand" }));
  expect(onEdit).toHaveBeenCalledTimes(1);

  cleanup();
  open({ onEdit: undefined });
  expect(
    screen.queryByRole("button", { name: "Edit this by hand" }),
  ).toBeNull();
});

it("goes away when the teacher clicks elsewhere or presses Escape, but not when they use it", () => {
  const { onDismiss } = open();

  fireEvent.mouseDown(
    screen.getByRole("button", { name: "Ask the agent about this" }),
  );
  expect(onDismiss).not.toHaveBeenCalled();

  fireEvent.mouseDown(document.body);
  fireEvent.keyDown(document, { key: "Escape" });
  expect(onDismiss).toHaveBeenCalledTimes(2);
});

it("sits just below the selected words", () => {
  open();

  const style = screen.getByRole("toolbar").getAttribute("style") ?? "";
  expect(style).toContain("left: 40px");
  expect(style).toContain("top: 108px");
});
