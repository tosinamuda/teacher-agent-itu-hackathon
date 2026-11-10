import katex from "katex";
import { describe, expect, it } from "vitest";

import { asKatex } from "./katexDialect";

const renders = (tex: string) => () =>
  katex.renderToString(tex, { displayMode: true, throwOnError: true, strict: "ignore" });

describe("asKatex", () => {
  it("draws MathJax's long division with the bar and bracket KaTeX has", () => {
    const tex = "\\require{enclose}\\begin{array}{r} 4\\newline 7 \\enclose{longdiv}{30}\\newline \\underline{-28} \\newline 2 \\end{array}";

    expect(asKatex(tex)).toBe(
      "\\begin{array}{r} 4\\\\ 7 \\overline{\\smash{)}\\,30}\\\\ \\underline{-28} \\\\ 2 \\end{array}",
    );
    expect(renders(asKatex(tex))).not.toThrow();
  });

  it("keeps a circled sign's colour", () => {
    const tex = '7\\,\\enclose{circle}[mathcolor="red"]{-}(-10)';

    expect(asKatex(tex)).toBe("7\\,\\textcolor{red}{\\text{\\textcircled{$-$}}}(-10)");
    expect(renders(asKatex(tex))).not.toThrow();
  });

  it("keeps the body of a notation KaTeX cannot draw", () => {
    expect(asKatex("\\enclose{actuarial}{x+1}")).toBe("{x+1}");
  });

  it("restores commands whose escapes a decode ate", () => {
    expect(asKatex("\begin{align}\x07ngle A &= 50^{\\circ}\\end{align}")).toBe(
      "\\begin{align}\\angle A &= 50^{\\circ}\\end{align}",
    );
    expect(asKatex("4 \times 5 = 20 \text{ cm}")).toBe("4 \\times 5 = 20 \\text{ cm}");
    expect(asKatex("x \neq y")).toBe("x \\neq y");
  });

  it("leaves a real line break before a variable a line break", () => {
    expect(asKatex("a\nu = 5\nx")).toBe("a\nu = 5\nx");
  });

  it("restores a newline command whose escape became a space", () => {
    expect(asKatex("\\begin{array}{r | r} 2 & 180  ewline \\hline & 90 \\end{array}")).toBe(
      "\\begin{array}{r | r} 2 & 180  \\\\ \\hline & 90 \\end{array}",
    );
  });

  it("halves an escape written twice where it names a command", () => {
    expect(asKatex("\\\\begin{array}{r} 1 \\\\ 2 \\end{array}")).toBe(
      "\\begin{array}{r} 1 \\\\ 2 \\end{array}",
    );
    expect(asKatex("a \\\\ b")).toBe("a \\\\ b");
  });

  it("gives a column count the column letters KaTeX wants", () => {
    expect(asKatex("\\begin{array}{2} a & b \\end{array}")).toBe("\\begin{array}{ll} a & b \\end{array}");
  });

  it("ends each row an \\hline follows, and only once", () => {
    const tex = "\\begin{array}{|c|c|} \\hline a & b \\hline c & d \\\\ \\hline \\hline e & f \\ \\end{array}";

    expect(asKatex(tex)).toBe(
      "\\begin{array}{|c|c|} \\hline a & b \\\\ \\hline c & d \\\\ \\hline \\hline e & f \\\\ \\end{array}",
    );
    expect(renders(asKatex(tex))).not.toThrow();
  });

  it("changes nothing KaTeX reads already", () => {
    const tex = "\\frac{30}{7} = 4\\frac{2}{7} \\quad \\text{and} \\quad \\sqrt[3]{8} = 2";

    expect(asKatex(tex)).toBe(tex);
  });
});
