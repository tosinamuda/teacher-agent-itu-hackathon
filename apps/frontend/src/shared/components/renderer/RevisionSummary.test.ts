import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { RevisionSummary } from "./RevisionSummary";

describe("RevisionSummary", () => {
  const html = renderToStaticMarkup(
    createElement(RevisionSummary, {
      text: 'Swapped the pizza in "intro01" for a bar shaded to \\(\\frac{3}{5}\\).',
    }),
  );

  it("draws the maths", () => {
    expect(html).toContain('class="katex"');
    expect(html).not.toContain("\\(");
  });

  it("shows no internal id", () => {
    expect(html).not.toContain("intro01");
  });
});

describe("RevisionSummary with blocks", () => {
  const message = [
    "The draft is now clean.",
    "",
    "## What was done this round",
    "",
    "- Slide 2 was restored to the note's wording.",
    "- Slide 5 was restored to the note's wording.",
  ].join("\n");
  const html = renderToStaticMarkup(
    createElement(RevisionSummary, { text: message, blocks: true }),
  );

  it("draws a heading as a heading, not as hash signs in the sentence", () => {
    expect(html).toContain("<h2>");
    expect(html).not.toContain("##");
  });

  it("keeps a list as a list", () => {
    expect(html).toContain("<li>");
  });
});
