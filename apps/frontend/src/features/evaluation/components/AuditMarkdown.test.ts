import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { AuditMarkdown } from "./AuditMarkdown";

const render = (text: string): string =>
  renderToStaticMarkup(createElement(AuditMarkdown, { text }));

describe("AuditMarkdown", () => {
  it("typesets block math written with LaTeX-native \\[ … \\] delimiters", () => {
    const html = render("The quotient is \\[ x = \\frac{12}{3} \\] exactly.");
    expect(html).toContain("katex");
    expect(html).not.toContain("\\[");
    expect(html).not.toContain("\\]");
  });

  it("typesets inline math written with \\( … \\) delimiters", () => {
    const html = render("Here \\( a^2 + b^2 \\) is the sum of squares.");
    expect(html).toContain("katex");
    expect(html).not.toContain("\\(");
    expect(html).not.toContain("\\)");
  });

  it("keeps source citations visible — this is the source-grounding surface", () => {
    const html = render("The LCM is the smallest shared multiple (REF-1).");
    expect(html).toContain("REF-1");
  });
});
