// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it, vi } from "vitest";

import { SidebarNav } from "./SidebarNav";

afterEach(cleanup);

function renderNav(groups: Parameters<typeof SidebarNav>[0]["groups"]) {
  return render(
    <MemoryRouter>
      <SidebarNav label="Class" groups={groups} />
    </MemoryRouter>,
  );
}

it("marks the selected page and nothing else", () => {
  renderNav([
    {
      items: [
        { label: "Lessons", href: "/lessons", active: true },
        { label: "Learners", href: "/learners" },
      ],
    },
  ]);

  expect(
    screen.getByRole("link", { name: "Lessons" }).getAttribute("aria-current"),
  ).toBe("page");
  expect(
    screen.getByRole("link", { name: "Learners" }).getAttribute("aria-current"),
  ).toBeNull();
});

it("shows a disabled item in the list without making it a link", () => {
  renderNav([
    { items: [{ label: "Slides", href: "/slides", disabled: true }] },
  ]);

  expect(screen.queryByRole("link", { name: "Slides" })).toBeNull();
  expect(screen.getByText("Slides").getAttribute("aria-disabled")).toBe("true");
});

it("runs the action of an item that switches class", () => {
  const onSelect = vi.fn();
  renderNav([
    {
      heading: "Other classes",
      items: [{ label: "JSS 2B · Mathematics", onSelect }],
    },
  ]);

  fireEvent.click(screen.getByRole("button", { name: "JSS 2B · Mathematics" }));

  expect(onSelect).toHaveBeenCalledOnce();
});

it("lists several rows that open the same page, each once", () => {
  renderNav([
    {
      items: [
        { label: "Slides", href: "/lesson" },
        { label: "Exam questions", href: "/lesson" },
      ],
    },
  ]);

  expect(screen.getAllByRole("link").map((link) => link.textContent)).toEqual([
    "Slides",
    "Exam questions",
  ]);
});
