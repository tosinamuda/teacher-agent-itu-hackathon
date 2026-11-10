import { describe, expect, it } from "vitest";

import { fieldTitle, fieldsOf, kindOf, partsFor } from "./engineParts";
import { PartField, Spec } from "./types";

const PARTS: PartField[] = [
  { name: "title", description: "A heading", type: "text", required: true },
  {
    name: "worked_examples",
    description: "Examples",
    type: "items",
    required: true,
    fields: [
      {
        name: "problem",
        description: "The problem",
        type: "markdown",
        required: true,
      },
    ],
  },
];

describe("engine content fields", () => {
  it("reads a field name as words", () => {
    expect(fieldTitle("worked_examples")).toBe("Worked examples");
  });

  it("draws the spec's fields in the spec's order", () => {
    expect(fieldsOf({ worked_examples: [], title: "T" }, PARTS)).toBe(PARTS);
  });

  it("draws the part's own keys while the spec loads", () => {
    expect(
      fieldsOf({ title: "T", tips: ["a"] }, null).map((f) => [f.name, f.type]),
    ).toEqual([
      ["title", "markdown"],
      ["tips", "list"],
    ]);
  });

  it("draws the lesson's section from the lesson's own schema", () => {
    const lesson: PartField[] = [
      { name: "intro", description: "d", type: "group", required: true },
    ];
    const spec = { parts: PARTS, lesson_parts: lesson } as Spec;
    const section = { unit_id: "lesson", label: "L", part: {} };
    expect(partsFor({ ...section, unit: "lesson" }, spec)).toBe(lesson);
    expect(
      partsFor(
        { ...section, unit_id: "c1", unit: "curriculum_objective" },
        spec,
      ),
    ).toBe(PARTS);
    expect(partsFor(section, null)).toBeNull();
  });

  it("finds the kind an item of a mixed list is", () => {
    const kinds = [
      { name: "explanation", description: "d", fields: [] },
      { name: "practice", description: "d", fields: [] },
    ];
    expect(kindOf({ kind: "practice" }, kinds)?.name).toBe("practice");
    expect(kindOf({ kind: "table" }, kinds)).toBeUndefined();
  });
});
