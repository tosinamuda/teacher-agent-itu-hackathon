import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { PlanStepCard } from "./PlanStepCard";

describe("a plan step's activities", () => {
  const html = renderToStaticMarkup(
    createElement(PlanStepCard, {
      index: 0,
      step: {
        step_id: "s1",
        type: "core",
        title: "Meaning of fraction",
        activities: [
          { who: "teacher", what: "Shows a **fraction chart**." },
          { who: "student", what: "Shade \\(\\frac{3}{5}\\) of the bar." },
        ],
      },
    }),
  );

  it("draws markdown emphasis, not the asterisks", () => {
    expect(html).toContain("<strong>fraction chart</strong>");
    expect(html).not.toContain("**");
  });

  it("draws maths as KaTeX", () => {
    expect(html).toContain('class="katex"');
    expect(html).not.toContain("\\(");
  });
});
