import { apiFetch } from "@/shared/api/client";

/** Discrete self-report scale for survey signals (legacy 3-bucket). */
export type SignalLevel = "low" | "medium" | "high";

/** Canonical 1-5 survey answer (learner-model spec: values in {1..5}). */
export type SurveyScale = 1 | 2 | 3 | 4 | 5;

/** One MCQ item served to the student (stem + options only — no answer/tags). */
export type ExitAssessmentItem = {
  item_id: string;
  stem: string;
  options: Record<string, string>;
  difficulty?: string | null;
};

/** A lesson objective with its MCQ items. */
export type ExitAssessmentObjective = {
  lesson_objective_id: string;
  objective_text: string | null;
  items: ExitAssessmentItem[];
};

/** The lesson's per-objective MCQ assessment. */
export type ExitAssessmentQuestions = {
  plan_version_id: string;
  subject?: string | null;
  topic?: string | null;
  subtopic?: string | null;
  objectives: ExitAssessmentObjective[];
};

/** One MCQ answer: the option key the student selected. */
export type ExitAssessmentAnswer = {
  item_id: string;
  selected_option: string;
};

/** Per-objective post-class survey: Confidence + Difficulty, 1-5. */
export type ExitAssessmentObjectiveSurvey = {
  lesson_objective_id: string;
  confidence?: SurveyScale | null;
  perceived_difficulty?: SurveyScale | null;
};

/** Session-level survey: Interest + Affect, asked once for the whole session. */
export type ExitAssessmentSessionSurvey = {
  interest?: SurveyScale | null;
  affect?: SurveyScale | null;
};

/** Body for submitting MCQ answers (graded server-side). */
export type ExitAssessmentSubmitRequest = {
  student_id: string;
  plan_version_id: string;
  answers: ExitAssessmentAnswer[];
  survey: ExitAssessmentObjectiveSurvey[];
  session_survey?: ExitAssessmentSessionSurvey | null;
  /** Two-step flow: true defers pack generation until the survey is attached. */
  survey_pending?: boolean;
};

/** Body for attaching the post-class survey to a graded diagnostic (step 2). */
export type ExitAssessmentSurveyAttachRequest = {
  survey: ExitAssessmentObjectiveSurvey[];
  session_survey?: ExitAssessmentSessionSurvey | null;
};

/** Response from submitting an exit assessment. */
export type ExitAssessmentSubmitResponse = {
  diagnostic_id: string;
  student_id: string;
  plan_version_id: string;
};

/** A lesson-plan version summary, used for lesson selection. */
export type LessonVersionSummary = {
  plan_id: string;
  version_id: string;
  session_id: string;
  subject: string;
  track: string;
  grade: string;
  term?: string | null;
  week?: number | null;
  topic?: string | null;
  subtopic?: string | null;
  status?: string | null;
};

const EXIT = "/assessments/exit-assessment";

/** One exit-assessment a student has submitted (per-lesson status signal). */
export type ExitAssessmentSubmissionRow = {
  diagnostic_id: string;
  student_id: string;
  plan_version_id: string;
  created_at?: string | null;
  /** The answers are in and the survey is still to come. */
  survey_pending?: boolean;
};

/** The exit-assessments a student has submitted (which lessons are done). */
export const listSubmissions = (studentId: string) =>
  apiFetch<ExitAssessmentSubmissionRow[]>(
    `${EXIT}/submissions?student_id=${encodeURIComponent(studentId)}`
  );

/** Status-only view of a learner's packs (pending vs approved), no manifest content. */
export type ReviewPackStatusRow = {
  plan_version_id: string;
  review_status: string;
};

/** A learner's pack statuses across lessons — distinguishes generating vs awaiting review. */
export const listPackStatuses = (studentId: string) =>
  apiFetch<ReviewPackStatusRow[]>(
    `/artefacts/post-class-review-packs/statuses?learner_id=${encodeURIComponent(studentId)}`
  );

/** Per-lesson assessment state: created + whether the teacher has released it. */
export type AssessmentStatusRow = {
  plan_version_id: string;
  has_assessment: boolean;
  released: boolean;
};

/** Which of the given lessons have an assessment that's been released to students. */
export const listAssessmentStatus = (planVersionIds: string[]) => {
  if (planVersionIds.length === 0) return Promise.resolve<AssessmentStatusRow[]>([]);
  const params = new URLSearchParams();
  for (const id of planVersionIds) params.append("plan_version_ids", id);
  return apiFetch<AssessmentStatusRow[]>(`${EXIT}/status?${params.toString()}`);
};

/** The lessons taught to the signed-in student's own class (lesson selection). */
export const listMyClassLessons = () =>
  apiFetch<LessonVersionSummary[]>("/artefacts/lesson-plans/for-my-class");

/** Fetch the lesson's per-objective MCQ items (no answers). */
export const getExitAssessmentQuestions = (planVersionId: string) =>
  apiFetch<ExitAssessmentQuestions>(`${EXIT}/${encodeURIComponent(planVersionId)}/questions`);

/** Submit selected options; the server grades them into the diagnostic. */
export const submitExitAssessment = (body: ExitAssessmentSubmitRequest) =>
  apiFetch<ExitAssessmentSubmitResponse>(EXIT, {
    method: "POST",
    body: JSON.stringify(body),
  });

/** Attach the post-class survey to the graded diagnostic (triggers pack gen). */
export const attachExitAssessmentSurvey = (
  diagnosticId: string,
  body: ExitAssessmentSurveyAttachRequest
) =>
  apiFetch<ExitAssessmentSubmitResponse>(
    `${EXIT}/${encodeURIComponent(diagnosticId)}/survey`,
    { method: "POST", body: JSON.stringify(body) }
  );
