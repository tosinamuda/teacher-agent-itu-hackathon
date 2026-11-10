import { describe, expect, it } from "vitest";

import { comparedObjectives, lessonObjectives, sectionsFor } from "./objectives";

const plan = {
  lesson_plan_objectives: [
    { lesson_objective_id: "lo-2", objective_text: "interpret tables", objective_order: 2 },
    {
      lesson_objective_id: "lo-1",
      objective_text: "explain statistics",
      objective_order: 1,
      curriculum_objective_text: "List purposes of statistics",
    },
  ],
  steps: [
    { step_id: "s0", type: "intro", step_kind: "intro" as const, title: "Intro" },
    { step_id: "s1", type: "core", step_role: "core" as const, lesson_objective_id: "lo-1", title: "Purposes" },
    { step_id: "s2", type: "core", step_role: "core" as const, lesson_objective_id: "lo-2", title: "Tables" },
    {
      step_id: "s3",
      type: "evaluation",
      step_role: "evaluation" as const,
      title: "Evaluation",
      blocks: [
        { id: "q1", type: "practice" as const, question: "Define statistic", answer: "", lesson_objective_id: "lo-1" },
        { id: "q2", type: "practice" as const, question: "Tabulate", answer: "", lesson_objective_id: "lo-2" },
      ],
    },
  ],
};

describe("lessonObjectives", () => {
  it("takes each objective in order with the steps that teach it and its questions", () => {
    const [first, second] = lessonObjectives(plan);

    expect(first.id).toBe("lo-1");
    expect(first.curriculumTarget).toBe("List purposes of statistics");
    expect(first.steps.map((step) => step.step_id)).toEqual(["s1"]);
    expect(first.questions.map((question) => question.question)).toEqual(["Define statistic"]);
    expect(second.steps.map((step) => step.step_id)).toEqual(["s2"]);
  });
});

describe("sectionsFor", () => {
  it("takes the note's sections for one objective", () => {
    const manifest = {
      artefact_id: "AT-1",
      steps: [
        { step_id: "a", lesson_objective_id: "lo-1", blocks: [] },
        { step_id: "b", lesson_objective_id: "lo-2", blocks: [] },
      ],
    };
    expect(sectionsFor(manifest, "lo-2").map((step) => step.step_id)).toEqual(["b"]);
  });
});

describe("comparedObjectives", () => {
  it("is the objectives the learner has marked class work for", () => {
    const classwork = {
      questions: [
        { n: 1, lesson_objective_id: "lo-1", text: "q", answer: null, answer_source: null },
        { n: 2, lesson_objective_id: "lo-2", text: "q", answer: null, answer_source: null },
      ],
      script: {
        teacher_total: "1/2",
        capture_complete: true,
        answers: [
          { n: 1, mark: "correct", uncertain: false, working: "", misconception_code: null, misconception_why: null },
          { n: 2, mark: "unmarked", uncertain: false, working: "", misconception_code: null, misconception_why: null },
        ],
      },
    };
    expect([...comparedObjectives(lessonObjectives(plan), classwork)]).toEqual(["lo-1"]);
    expect(comparedObjectives(lessonObjectives(plan), undefined).size).toBe(0);
  });
});
