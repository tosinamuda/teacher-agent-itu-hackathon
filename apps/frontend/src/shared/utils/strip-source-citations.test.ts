import { describe, expect, it } from "vitest";

import { stripSourceCitations } from "./strip-source-citations";

describe("stripSourceCitations", () => {
  it("drops whole `Sources: …` lines, with and without markdown emphasis", () => {
    const out = stripSourceCitations(
      "The LCM is the smallest shared multiple.\n" +
        "Sources: REF-1, REF-2\n" +
        "_Sources: REF-3_",
    );
    expect(out).toContain("The LCM is the smallest shared multiple.");
    expect(out).not.toContain("Sources");
    expect(out).not.toContain("REF-1");
    expect(out).not.toContain("REF-3");
  });

  it("removes inline citation markers in every bracketing", () => {
    const out = stripSourceCitations(
      "Numbers share multiples (REF-1), as [REF-2], ⟦REF-3⟧ and 【REF-4】 show; see REF-5.",
    );
    for (const ref of ["REF-1", "REF-2", "REF-3", "REF-4", "REF-5"]) {
      expect(out).not.toContain(ref);
    }
    expect(out).not.toContain("⟦");
    expect(out).not.toContain("【");
    // Prose survives with no double spaces or space-before-punctuation.
    expect(out).toContain("Numbers share multiples,");
    expect(out).not.toContain("  ");
    expect(out).not.toContain(" ,");
    expect(out).not.toContain(" ;");
  });

  it("removes contentless `(Source:)` markers in singular, padded and plural forms", () => {
    const out = stripSourceCitations(
      "Water boils at 100 degrees (Source:). The freezing point is 0 (Source: ).\n" +
        "Plants need sunlight (Sources:) to photosynthesise.",
    );
    expect(out).not.toContain("(Source:)");
    expect(out).not.toContain("(Source: )");
    expect(out).not.toContain("(Sources:)");
    expect(out).not.toContain("Source");
    expect(out).toContain("Water boils at 100 degrees.");
    expect(out).toContain("The freezing point is 0.");
    expect(out).toContain("Plants need sunlight to photosynthesise.");
    expect(out).not.toContain("  ");
    expect(out).not.toContain(" .");
  });

  it("removes every parenthesised `(Source: …)` annotation, content or not", () => {
    // Mirrors the backend: editorial meta-commentary and real-looking citations
    // alike are cut so the browser HTML matches the WeasyPrint PDF.
    const out = stripSourceCitations(
      "The mitochondrion is the powerhouse of the cell (Source: Smith 2020, p.4). " +
        "ATP is the energy currency (Sources: Khan Academy).",
    );
    expect(out).not.toContain("Source");
    expect(out).toContain("The mitochondrion is the powerhouse of the cell.");
    expect(out).toContain("ATP is the energy currency.");
  });

  it("removes an editorial `(Source: REF-1 for …)` without leaving a mangled fragment", () => {
    // The editorial annotation is cut whole, so stripping the inner REF-N never
    // leaves a dangling `(Source: for definition; for X)`.
    const out = stripSourceCitations(
      "This is the prime-factor method (Source: REF-1 for definition; REF-2 for the method).",
    );
    expect(out).not.toContain("Source");
    expect(out).not.toContain("REF-");
    expect(out).not.toContain("(");
    expect(out).toContain("This is the prime-factor method.");
  });

  it("is a no-op for prose and markdown structure without citations", () => {
    const raw = "### Worked example\nStep 1: list multiples.\n- two\n- three";
    expect(stripSourceCitations(raw)).toBe(raw);
  });
});
