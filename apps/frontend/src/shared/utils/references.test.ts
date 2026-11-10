import { describe, expect, it } from "vitest";

import { groupReferencesByChapter, parseReference } from "./references";

describe("parseReference", () => {
  it("reads the label-first form", () => {
    expect(parseReference("Chapter 2: HCF (ch02-b005)")).toEqual({ label: "Chapter 2: HCF", recordId: "ch02-b005" });
  });

  it("reads the id-first form and drops the kind of passage", () => {
    expect(parseReference("ch09-b027: Chapter 9: Using symbols (exposition)")).toEqual({
      label: "Chapter 9: Using symbols",
      recordId: "ch09-b027",
    });
  });

  it("leaves a plain label alone", () => {
    expect(parseReference("New General Mathematics for JSS1")).toEqual({
      label: "New General Mathematics for JSS1",
      recordId: null,
    });
  });
});

it("groups the id-first sources of a chapter into one entry", () => {
  const groups = groupReferencesByChapter([
    "ch09-b027: Chapter 9: Using symbols (exposition)",
    "ch09-b028: Chapter 9: Using symbols (worked_example)",
    "ch09-b030-i01: Exercise 9.6 (exercise_item)",
    "ch09-b030-i03: Exercise 9.6 (exercise_item)",
  ]);

  expect(groups.map((g) => [g.label, g.records.length])).toEqual([
    ["Chapter 9: Using symbols", 2],
    ["Exercise 9.6", 2],
  ]);
});
