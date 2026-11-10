// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import { Drawer } from "./Drawer";

afterEach(cleanup);

it("is drawn into the page body, outside a card that carries a transform", () => {
  render(
    <div data-testid="card" style={{ transform: "translateY(0)" }}>
      <Drawer open onClose={() => undefined} title="Chat">
        <p>inside</p>
      </Drawer>
    </div>,
  );

  const panel = screen.getByText("inside");

  expect(screen.getByTestId("card").contains(panel)).toBe(false);
  expect(document.body.contains(panel)).toBe(true);
});
