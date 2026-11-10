import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { ClassTestText } from "@/shared/components/renderer/ClassTestText";

import { withFractionsAsMath } from "./fractionMarkup";

describe("withFractionsAsMath", () => {
  it("marks a slashed fraction", () => {
    expect(withFractionsAsMath("Calculate 2/3 + 3/8.")).toBe(
      "Calculate \\(\\frac{2}{3}\\) + \\(\\frac{3}{8}\\).",
    );
  });

  it("marks the fraction of a mixed number", () => {
    expect(withFractionsAsMath("1 1/12")).toBe("1 \\(\\frac{1}{12}\\)");
  });

  it("marks a fraction written in superscript and subscript digits", () => {
    expect(withFractionsAsMath("Which is ⁸⁄₅?")).toBe("Which is \\(\\frac{8}{5}\\)?");
    expect(withFractionsAsMath("¹²/₂₀")).toBe("\\(\\frac{12}{20}\\)");
  });

  it("marks a fraction written with the fraction slash", () => {
    expect(withFractionsAsMath("8⁄5")).toBe("\\(\\frac{8}{5}\\)");
  });

  it("marks a vulgar fraction", () => {
    expect(withFractionsAsMath("⅗ of the class")).toBe("\\(\\frac{3}{5}\\) of the class");
  });

  it("leaves delimited maths as written", () => {
    const text = "Equivalent to \\(\\frac{3}{5}\\) or $6/10$ with denominator 20?";
    expect(withFractionsAsMath(text)).toBe(text);
  });

  it("leaves what is not a fraction", () => {
    for (const text of ["27/09/2026", "2.5/10", "km/h", "3/4x"]) {
      expect(withFractionsAsMath(text)).toBe(text);
    }
  });

  it("marks the fraction beside a missing numerator, and leaves the gap", () => {
    expect(withFractionsAsMath("?/8 = 3/4")).toBe("?/8 = \\(\\frac{3}{4}\\)");
  });
});

describe("ClassTestText", () => {
  it("stacks a fraction with KaTeX", () => {
    const html = renderToStaticMarkup(createElement(ClassTestText, { text: "⁸⁄₅" }));
    expect(html).toContain('class="mfrac"');
    expect(html).not.toContain("katex-error");
  });
});
