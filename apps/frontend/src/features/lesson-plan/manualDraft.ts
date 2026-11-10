/**
 * The teacher-facing draft for hand-entering a lesson plan (FD-01), and the pure
 * function that assembles it into the `session_plan` *content* the backend's
 * `POST /artefacts/lesson-plans/manual` expects.
 *
 * Lesson identity + the curriculum-objective list are added server-side from the
 * lesson's session context, so this content carries only what the teacher enters.
 * The block structure honours the `SessionPlan` validators: a concept core step
 * needs only an explanation; a procedure/representation core step also needs a
 * worked example and a practice; the evaluation step is practice-only.
 */

export type KcType = "concept" | "procedure" | "representation";

export type WorkedExampleStepDraft = { label: string; content: string };

export type ObjectiveDraft = {
  /** From the lesson's curriculum-objective picker (server-validated). */
  curriculumObjectiveId: string;
  objectiveText: string;
  kcType: KcType;
  kcFocus: string;
  explanation: string;
  /** Captured only when kcType !== "concept". */
  workedExample: {
    problem: string;
    steps: WorkedExampleStepDraft[];
    finalAnswer: string;
  };
  /** One check-for-understanding item, used in the evaluation step (and the core
   *  step for procedure/representation objectives). */
  practice: { question: string; answer: string };
};

export type ManualPlanDraft = {
  intro: { title: string; content: string };
  objectives: ObjectiveDraft[];
  evaluationSummary: string;
  misconceptions: string[];
  instructionalMaterials: string[];
  entryBehaviour: string[];
  references: string[];
};

export type CurriculumObjectiveOption = {
  curriculum_objective_id: string;
  objective_text: string;
  objective_order: number;
};

export function emptyObjectiveDraft(): ObjectiveDraft {
  return {
    curriculumObjectiveId: "",
    objectiveText: "",
    kcType: "concept",
    kcFocus: "",
    explanation: "",
    workedExample: {
      problem: "",
      steps: [{ label: "Step 1", content: "" }],
      finalAnswer: "",
    },
    practice: { question: "", answer: "" },
  };
}

export function emptyManualPlanDraft(): ManualPlanDraft {
  return {
    intro: { title: "Introduction", content: "" },
    objectives: [emptyObjectiveDraft()],
    evaluationSummary: "Check understanding of each objective.",
    misconceptions: [],
    instructionalMaterials: [],
    entryBehaviour: [],
    references: [],
  };
}

type Block = Record<string, unknown>;

function coreBlocks(objective: ObjectiveDraft, index: number): Block[] {
  const blocks: Block[] = [
    {
      id: `blk-exp-${index}`,
      type: "explanation",
      content: objective.explanation,
    },
  ];
  if (objective.kcType !== "concept") {
    blocks.push({
      id: `blk-we-${index}`,
      type: "worked_example",
      problem: objective.workedExample.problem,
      steps: objective.workedExample.steps,
      final_answer: objective.workedExample.finalAnswer,
    });
    blocks.push({
      id: `blk-pr-core-${index}`,
      type: "practice",
      question: objective.practice.question,
      answer: objective.practice.answer,
      lesson_objective_id: lessonObjectiveId(index),
    });
  }
  return blocks;
}

export function lessonObjectiveId(index: number): string {
  return `lop${String(index).padStart(2, "0")}`;
}

/** The instructional_type the schema requires for a core step, derived from its
 *  blocks: concept = explanation only; procedure/representation also carry a
 *  worked example, so they are explain_example_practice. */
function coreInstructionalType(kcType: KcType): string {
  return kcType === "concept" ? "explain_only" : "explain_example_practice";
}

/** Assemble the draft into the SessionPlan-content payload the backend validates. */
export function buildManualSessionPlanContent(
  draft: ManualPlanDraft,
  curriculumById: Map<string, CurriculumObjectiveOption>,
): Record<string, unknown> {
  const lessonObjectives = draft.objectives.map((objective, position) => {
    const order = position + 1;
    const curriculum = curriculumById.get(objective.curriculumObjectiveId);
    return {
      lesson_objective_id: lessonObjectiveId(order),
      objective_text: objective.objectiveText,
      objective_order: order,
      curriculum_objective_id: objective.curriculumObjectiveId,
      curriculum_objective_text:
        curriculum?.objective_text ?? objective.objectiveText,
      kc_type: objective.kcType,
      kc_focus: objective.kcFocus,
    };
  });

  const coreSteps = draft.objectives.map((objective, position) => {
    const order = position + 1;
    return {
      step_id: `step-core-${order}`,
      step_kind: "core",
      kc_type: objective.kcType,
      instructional_type: coreInstructionalType(objective.kcType),
      lesson_objective_id: lessonObjectiveId(order),
      title: objective.objectiveText || `Objective ${order}`,
      content:
        objective.explanation ||
        objective.objectiveText ||
        `Objective ${order}`,
      estimated_minutes: 10,
      blocks: coreBlocks(objective, order),
      activities: [],
    };
  });

  const evaluationBlocks = draft.objectives.map((objective, position) => {
    const order = position + 1;
    return {
      id: `blk-eval-pr-${order}`,
      type: "practice",
      question: objective.practice.question,
      answer: objective.practice.answer,
      lesson_objective_id: lessonObjectiveId(order),
    };
  });

  const steps = [
    {
      step_id: "step-intro",
      step_kind: "intro",
      title: draft.intro.title,
      content: draft.intro.content,
      estimated_minutes: 5,
      blocks: [],
      activities: [],
    },
    ...coreSteps,
    {
      step_id: "step-evaluation",
      step_kind: "evaluation",
      instructional_type: "check",
      title: "Evaluation",
      content: draft.evaluationSummary,
      estimated_minutes: 10,
      blocks: evaluationBlocks,
      activities: [],
    },
  ];

  return {
    lesson_plan_objectives: lessonObjectives,
    steps,
    misconceptions: draft.misconceptions,
    instructional_materials: draft.instructionalMaterials,
    entry_behaviour: draft.entryBehaviour,
    references: draft.references,
  };
}

/** Teacher-facing problems with the draft (empty = ready to submit). */
export function manualDraftIssues(draft: ManualPlanDraft): string[] {
  const issues: string[] = [];
  if (!draft.intro.content.trim()) issues.push("Introduction needs a summary.");
  if (draft.objectives.length === 0) issues.push("Add at least one objective.");
  draft.objectives.forEach((objective, position) => {
    const order = position + 1;
    const label = `Objective ${order}`;
    if (!objective.curriculumObjectiveId)
      issues.push(`${label}: map it to a curriculum objective.`);
    if (!objective.objectiveText.trim())
      issues.push(`${label}: enter the objective text.`);
    if (!objective.kcFocus.trim())
      issues.push(`${label}: enter what it focuses on.`);
    if (!objective.explanation.trim())
      issues.push(`${label}: enter an explanation.`);
    if (
      !objective.practice.question.trim() ||
      !objective.practice.answer.trim()
    ) {
      issues.push(`${label}: enter a practice question and answer.`);
    }
    if (objective.kcType !== "concept") {
      if (
        !objective.workedExample.problem.trim() ||
        !objective.workedExample.finalAnswer.trim()
      ) {
        issues.push(
          `${label}: a ${objective.kcType} objective needs a worked example.`,
        );
      }
    }
  });
  return issues;
}
