import { describe, expect, it } from "vitest";

import { figureId, splitFigures } from "./figures";

// Shared with the backend's test (apps/backend/tests/test_figures.py): both must name this
// drawing by the same id, or the browser would ask for a figure the server does not hold.
const DRAWING = "\\begin{tikzpicture}\n  \\draw (0,0) -- (1,1);\n\\end{tikzpicture}";
const DRAWING_ID = "b428001695a60547dffb293ba008d6c97d5f0c15d47993429e87da33d8b08ce6";

describe("figureId", () => {
  it("names a drawing as the server does, however it is padded", async () => {
    expect(await figureId(DRAWING)).toBe(DRAWING_ID);
    expect(await figureId(`  ${DRAWING}\n`)).toBe(DRAWING_ID);
  });
});

describe("splitFigures", () => {
  it("lifts each drawing, and its centring, out of the text around it", () => {
    const note = `Two lines meet.\n\n\\begin{center}\n${DRAWING}\n\\end{center}\n\nSo.`;

    expect(splitFigures(note)).toEqual([
      { kind: "text", text: "Two lines meet.\n\n" },
      { kind: "figure", source: DRAWING },
      { kind: "text", text: "\n\nSo." },
    ]);
    expect(splitFigures("No drawing.")).toEqual([{ kind: "text", text: "No drawing." }]);
  });
});
