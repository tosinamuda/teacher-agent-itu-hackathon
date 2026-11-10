// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { Pager } from "./Pager";

afterEach(cleanup);

describe("Pager", () => {
  it("moves one part at a time and stops at the ends", () => {
    render(
      <Pager count={3} label="Step">
        {(i) => <p>part {i}</p>}
      </Pager>,
    );
    expect(screen.getByText("Step 1 of 3")).toBeTruthy();
    expect((screen.getByText("Previous") as HTMLButtonElement).disabled).toBe(
      true,
    );
    fireEvent.click(screen.getByText("Next"));
    fireEvent.click(screen.getByText("Next"));
    expect(screen.getByText("part 2")).toBeTruthy();
    expect((screen.getByText("Next") as HTMLButtonElement).disabled).toBe(true);
  });

  it("reports the move when the page keeps the index", () => {
    const onIndexChange = vi.fn();
    render(
      <Pager count={2} index={0} onIndexChange={onIndexChange}>
        {(i) => <p>part {i}</p>}
      </Pager>,
    );
    fireEvent.click(screen.getByText("Next"));
    expect(onIndexChange).toHaveBeenCalledWith(1);
  });

  it("shows no controls for a single part", () => {
    render(<Pager count={1}>{() => <p>only</p>}</Pager>);
    expect(screen.queryByText("Next")).toBeNull();
  });
});
