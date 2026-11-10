import { ExperimentSummary } from "../lib/experiments";

/** Lifecycle state of a single lesson-preparation step. */
export type LessonPrepStatus = "done" | "current" | "upcoming" | "auto";

/** A lesson's per-student revision notes: students who have one, and those awaiting review. */
export type StudentNoteProgress = { made: number; awaiting: number };

/** One step in the teacher's lesson-preparation workflow (read-only view). */
export type LessonPrepStep = {
  title: string;
  detail: string;
  status: LessonPrepStatus;
  /** Where the teacher acts on this step, when it's the current actionable one. */
  href?: string;
};

/**
 * Derive the teacher's lesson-preparation checklist for one lesson from its
 * readiness flags. Read-only: the research conditions (C0–C3) run in the
 * background and never surface here — the teacher only sees "prepare the lesson
 * material" steps. Some steps are still automatic today (marked `auto`); those
 * are candidates to become explicit manual actions later.
 */
export function buildLessonPrepSteps(
  experiment: ExperimentSummary,
  studentNotes: StudentNoteProgress = { made: 0, awaiting: 0 },
  assessment: { ready: boolean; sent: boolean } = { ready: false, sent: false },
): LessonPrepStep[] {
  const readiness = experiment.readiness;
  const planAuthored = Boolean(experiment.plan_version_id);
  const planApproved = Boolean(experiment.baseline_approved_by);
  const lessonNoteId = readiness.lesson_note_artefact_id;
  const lessonNoteApproved = Boolean(readiness.lesson_note_approved);
  const noteReady = Boolean(readiness.base_pack_ready);
  const noteApproved = Boolean(readiness.base_pack_approved);
  const someSubmitted = Boolean(readiness.learner_evidence_ready);
  const { made, awaiting } = studentNotes;
  const studentNotesStarted = made > 0 || awaiting > 0 || someSubmitted;
  // Whether the class revision note's background build has been kicked off.
  const noteBuildStarted = experiment.h1_summary.execution_count > 0;

  const planReviewHref = `/research/teacher/experiment-plans/${experiment.experiment_id}/plan`;
  const noteReviewHref = readiness.base_pack_artefact_id
    ? `/research/teacher/pack-reviews/${readiness.base_pack_artefact_id}`
    : undefined;

  return [
    {
      title: "Set up the lesson plan",
      detail: "Author the plan for this lesson.",
      status: planAuthored ? "done" : "current",
    },
    {
      title: "Review & accept the lesson plan",
      detail: "Read the draft through, refine it, and accept it when you're satisfied.",
      status: planApproved ? "done" : planAuthored ? "current" : "upcoming",
      href: planAuthored && !planApproved ? planReviewHref : undefined,
    },
    {
      title: "Create the lesson note",
      detail: "Generate the note for each step of your accepted plan: what you teach in it.",
      status: lessonNoteId ? "done" : planApproved ? "current" : "upcoming",
    },
    {
      title: "Review & accept the lesson note",
      detail: "Read it through, refine it, and accept it. The class revision note is built from it.",
      status: lessonNoteApproved ? "done" : lessonNoteId ? "current" : "upcoming",
      href:
        lessonNoteId && !lessonNoteApproved
          ? `/research/teacher/content/${lessonNoteId}`
          : undefined,
    },
    {
      title: "Create the class revision note",
      detail: "Generate the revision note for your class from your accepted plan and lesson note.",
      status: noteReady
        ? "done"
        : !planApproved || !lessonNoteApproved
          ? "upcoming"
          : noteBuildStarted
            ? "auto"
            : "current",
    },
    {
      title: "Review & accept the revision note",
      detail: "Read it through, compare it with your plan, refine if you'd like, and accept it.",
      status: noteApproved ? "done" : noteReady ? "current" : "upcoming",
      href: noteReady && !noteApproved ? noteReviewHref : undefined,
    },
    {
      title: "Create the assessment",
      detail: "Generate a short assessment for your students from your accepted plan.",
      status: assessment.ready ? "done" : planApproved ? "current" : "upcoming",
    },
    {
      title: "Send the assessment to students",
      detail: "Release the assessment so your students can take it.",
      status: assessment.sent ? "done" : assessment.ready ? "current" : "upcoming",
    },
    {
      title: "Students take the assessment",
      detail: "Students answer it — their results shape each one's personalised revision note.",
      // A student's note is made from that student's answers, so once notes exist the students
      // have taken it.
      status:
        made > 0 || awaiting > 0 ? "done" : someSubmitted || assessment.sent ? "current" : "upcoming",
    },
    {
      title: "Create each student's draft revision note",
      detail:
        "A personalised draft is created for each student once the class revision note is accepted and they have submitted the assessment.",
      status: made > 0 ? "done" : studentNotesStarted ? "auto" : "upcoming",
    },
    {
      title: "Review, revise & accept each student's note",
      detail:
        awaiting > 0
          ? `${awaiting} awaiting you — read each one, ask for revisions if needed, and accept it before the student sees it.`
          : "Read each student's note, ask for revisions if needed, and accept it before they can see it.",
      status: awaiting > 0 ? "current" : made > 0 ? "done" : "upcoming",
      href: awaiting > 0 ? "/research/teacher/pack-reviews" : undefined,
    },
  ];
}

/** Compact summary of a lesson's prep progress, for the lessons list. */
export type LessonPrepSummary = {
  doneCount: number;
  total: number;
  current?: LessonPrepStep;
};

/**
 * Reduce a lesson's steps to a one-line summary: how many are done and which
 * step the teacher is on now (the first `current`, else the first `auto`).
 */
export function summariseLessonPrep(steps: LessonPrepStep[]): LessonPrepSummary {
  const doneCount = steps.filter((step) => step.status === "done").length;
  const current =
    steps.find((step) => step.status === "current") ??
    steps.find((step) => step.status === "auto");
  return { doneCount, total: steps.length, current };
}
