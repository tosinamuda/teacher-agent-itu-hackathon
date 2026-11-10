// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { ReasonAction } from "./ReasonAction";

afterEach(cleanup);

it("asks why before it acts, and sends the reason trimmed", () => {
  const onSubmit = vi.fn();
  render(<ReasonAction verb="Reject" isPending={false} onSubmit={onSubmit} />);

  fireEvent.click(screen.getByRole("button", { name: "Reject" }));
  fireEvent.change(screen.getByLabelText(/Why\?/), {
    target: { value: "  Too long.  " },
  });
  fireEvent.click(screen.getByRole("button", { name: "Reject" }));

  expect(onSubmit).toHaveBeenCalledWith("Too long.");
});

it("does not act on a reason too short to say anything", () => {
  render(<ReasonAction verb="Reject" isPending={false} onSubmit={vi.fn()} />);

  fireEvent.click(screen.getByRole("button", { name: "Reject" }));
  fireEvent.change(screen.getByLabelText(/Why\?/), { target: { value: "No" } });

  expect(
    (screen.getByRole("button", { name: "Reject" }) as HTMLButtonElement)
      .disabled,
  ).toBe(true);
});

it("says what the action changes, and why it failed", () => {
  render(
    <ReasonAction
      verb="Withdraw approval"
      note="Nothing already made changes."
      error="Not allowed."
      isPending={false}
      onSubmit={vi.fn()}
    />,
  );

  fireEvent.click(screen.getByRole("button", { name: "Withdraw approval" }));

  expect(screen.getByText("Nothing already made changes.")).toBeTruthy();
  expect(screen.getByText("Not allowed.")).toBeTruthy();
});

it("lets the teacher change their mind", () => {
  render(<ReasonAction verb="Reject" isPending={false} onSubmit={vi.fn()} />);

  fireEvent.click(screen.getByRole("button", { name: "Reject" }));
  fireEvent.click(screen.getByRole("button", { name: "Cancel" }));

  expect(screen.queryByLabelText(/Why\?/)).toBeNull();
});
