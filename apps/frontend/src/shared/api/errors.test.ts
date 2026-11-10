import { describe, expect, it } from "vitest";

import { errorDetail } from "./errors";

describe("errorDetail", () => {
  it("reads a text detail", () => {
    expect(errorDetail(new Error('{"detail":"lesson_not_found"}'), "x")).toBe("lesson_not_found");
  });

  it("shows a structured detail as JSON", () => {
    expect(errorDetail(new Error('{"detail":{"plan":["steps: required"]}}'), "x")).toBe(
      '{"plan":["steps: required"]}'
    );
  });

  it("keeps a plain message and falls back when there is none", () => {
    expect(errorDetail(new Error("Request failed: 500"), "x")).toBe("Request failed: 500");
    expect(errorDetail(new Error(""), "Could not import.")).toBe("Could not import.");
  });
});
