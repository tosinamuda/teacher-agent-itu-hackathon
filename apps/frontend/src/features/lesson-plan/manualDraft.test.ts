import { describe, expect, it } from "vitest";

import {
  buildManualSessionPlanContent,
  emptyManualPlanDraft,
  emptyObjectiveDraft,
  manualDraftIssues,
  type CurriculumObjectiveOption,
} from "./manualDraft";

const CURRICULUM: CurriculumObjectiveOption[] = [
  {
    curriculum_objective_id: "cur_obj01",
    objective_text: "Read place value",
    objective_order: 1,
  },
];
const byId = new Map(
  CURRICULUM.map((option) => [option.curriculum_objective_id, option]),
);

function conceptDraft() {
  const draft = emptyManualPlanDraft();
  draft.intro.content = "Recap counting.";
  draft.objectives = [
    {
      ...emptyObjectiveDraft(),
      curriculumObjectiveId: "cur_obj01",
      objectiveText: "State the place value of a digit",
      kcType: "concept",
      kcFocus: "place value names",
      explanation: "Each position has a value ten times the one to its right.",
      practice: { question: "Place value of 3 in 35?", answer: "30" },
    },
  ];
  return draft;
}

describe("buildManualSessionPlanContent", () => {
  it("omits server-forced identity (subject/session_id/curriculum_objectives)", () => {
    const content = buildManualSessionPlanContent(conceptDraft(), byId);
    expect(content).not.toHaveProperty("subject");
    expect(content).not.toHaveProperty("session_id");
    expect(content).not.toHaveProperty("curriculum_objectives");
    expect(content).toHaveProperty("lesson_plan_objectives");
    expect(content).toHaveProperty("steps");
  });

  it("a concept core step has an explanation block only", () => {
    const content = buildManualSessionPlanContent(conceptDraft(), byId);
    const steps = content.steps as Array<Record<string, unknown>>;
    const core = steps.find((step) => step.step_kind === "core")!;
    const blocks = core.blocks as Array<Record<string, unknown>>;
    expect(blocks.map((block) => block.type)).toEqual(["explanation"]);
    expect(core.lesson_objective_id).toBe("lop01");
    // Schema-required step fields (the JSON-schema validator enforces these).
    expect(core.instructional_type).toBe("explain_only");
    expect(core.activities).toEqual([]);
  });

  it("every step carries the schema-required activity arrays + instructional_type", () => {
    const content = buildManualSessionPlanContent(conceptDraft(), byId);
    const steps = content.steps as Array<Record<string, unknown>>;
    for (const step of steps) {
      expect(step.activities).toEqual([]);
      expect(step.blocks).toBeDefined();
    }
    expect(
      steps.find((step) => step.step_kind === "evaluation")!.instructional_type,
    ).toBe("check");
  });

  it("a procedure core step has explanation + worked_example + practice", () => {
    const draft = conceptDraft();
    draft.objectives[0].kcType = "procedure";
    draft.objectives[0].workedExample = {
      problem: "Add 23 + 19",
      steps: [{ label: "Step 1", content: "Add ones" }],
      finalAnswer: "42",
    };
    const content = buildManualSessionPlanContent(draft, byId);
    const steps = content.steps as Array<Record<string, unknown>>;
    const core = steps.find((step) => step.step_kind === "core")!;
    const blocks = core.blocks as Array<Record<string, unknown>>;
    expect(blocks.map((block) => block.type)).toEqual([
      "explanation",
      "worked_example",
      "practice",
    ]);
    expect(core.instructional_type).toBe("explain_example_practice");
  });

  it("the evaluation step has one practice per objective, each tagged to its objective", () => {
    const content = buildManualSessionPlanContent(conceptDraft(), byId);
    const steps = content.steps as Array<Record<string, unknown>>;
    const evaluation = steps.find((step) => step.step_kind === "evaluation")!;
    const blocks = evaluation.blocks as Array<Record<string, unknown>>;
    expect(blocks).toHaveLength(1);
    expect(blocks[0].type).toBe("practice");
    expect(blocks[0].lesson_objective_id).toBe("lop01");
  });
});

describe("manualDraftIssues", () => {
  it("is empty for a complete concept draft", () => {
    expect(manualDraftIssues(conceptDraft())).toEqual([]);
  });

  it("flags an unmapped objective and a procedure missing its worked example", () => {
    const draft = conceptDraft();
    draft.objectives[0].curriculumObjectiveId = "";
    draft.objectives[0].kcType = "procedure";
    const issues = manualDraftIssues(draft);
    expect(issues.some((issue) => issue.includes("curriculum objective"))).toBe(
      true,
    );
    expect(issues.some((issue) => issue.includes("worked example"))).toBe(true);
  });
});
