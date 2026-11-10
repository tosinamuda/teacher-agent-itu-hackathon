import { describe, expect, it } from "vitest";

import { tidyMathMarkdown } from "./mathMarkdown";

describe("tidyMathMarkdown", () => {
  it("drops the backslash left before the naira sign and before an amount", () => {
    expect(tidyMathMarkdown("Write it as $\\₦P$, so \\15 naira less is $\\₦(P-15)$.")).toBe(
      "Write it as $₦P$, so 15 naira less is $₦(P-15)$.",
    );
  });

  it("keeps the backslashes of a line break, even before a digit", () => {
    expect(tidyMathMarkdown("$a \\\\1 b$")).toBe("$a \\\\1 b$");
  });

  it("rewrites the LaTeX delimiters, but not a spaced line break", () => {
    expect(tidyMathMarkdown("So \\(x\\) and \\[y \\\\[4pt] z\\].")).toBe("So $x$ and $$y \\\\[4pt] z$$.");
  });

  it("puts a display's fences on lines of their own, so its first line is kept", () => {
    expect(tidyMathMarkdown("$$\\begin{array}{r | r}\n 2 & 12\n \\end{array}$$")).toBe(
      "$$\n\\begin{array}{r | r}\n2 & 12\n\\end{array}\n$$",
    );
  });

  it("sets a display written on one line as a display", () => {
    expect(tidyMathMarkdown("  $$12=2 \\times 2 \\times 3$$")).toBe("  $$\n  12=2 \\times 2 \\times 3\n  $$");
  });

  it("leaves maths inside a sentence inline", () => {
    expect(tidyMathMarkdown("Area is $$x$$ square units.")).toBe("Area is $$x$$ square units.");
  });

  it("drops the MathJax extension a display loaded, and the empty pairs it leaves", () => {
    const nested =
      "            $$\n\\require{enclose}\n\n$$\n\\begin{array}{r}\n4\\newline\n\\end{array}\n$$\n\n$$\n\n            Whole number: 4";

    expect(tidyMathMarkdown(nested)).toBe(
      "            \n\n$$\n\\begin{array}{r}\n4\\newline\n\\end{array}\n$$\n\n\n\n            Whole number: 4",
    );
  });

  it("indents a display's maths and close as its open, to keep it in its list item", () => {
    expect(tidyMathMarkdown("2. $x$\n\n            $$\n\\therefore x\n$$\n\n            Next")).toBe(
      "2. $x$\n\n            $$\n            \\therefore x\n            $$\n\n            Next",
    );
  });

  it("keeps two displays that follow one another", () => {
    expect(tidyMathMarkdown("$$\na\n$$\n$$\nb\n$$")).toBe("$$\na\n$$\n$$\nb\n$$");
  });

  it("displays an environment standing in prose, and none inside maths", () => {
    expect(tidyMathMarkdown("Rows: \\begin{cases} a \\end{cases} and $\\begin{matrix} b \\end{matrix}$")).toBe(
      "Rows: \n$$\n\\begin{cases} a \\end{cases}\n$$\n and $\\begin{matrix} b \\end{matrix}$",
    );
  });
});
