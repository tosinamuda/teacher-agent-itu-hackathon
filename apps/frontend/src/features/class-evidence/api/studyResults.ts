import { apiFetch } from "@/shared/api/client";
import type { ClassBand } from "@/features/learners/types";

/** A lesson of the evaluation whose marked classwork can be brought onto another lesson. */
export type StudySource = {
  plan_version_id: string;
  lesson_title: string;
  learners: number;
  /** Whether this lesson's approved plan has every objective the marks were written against. */
  fits: boolean;
  /** The evaluation lesson's approved lesson note, when it has one. */
  lesson_note_id: string | null;
  /** Whether that note has a section for every step of this lesson's plan. */
  note_fits: boolean;
};

export type StudyObjectiveResult = {
  lesson_objective_id: string;
  objective_text: string;
  band: ClassBand;
  correct: number;
  out_of: number;
  misconceptions: string[];
};

export type StudyLearnerResult = {
  student_id: string;
  full_name: string;
  /** The total the teacher wrote on the script, such as `1/4`. */
  teacher_total: string;
  band: ClassBand;
  correct: number;
  out_of: number;
  objectives: StudyObjectiveResult[];
};

/** The evaluation's class results on a lesson; empty until they are imported. */
export type StudyResults = {
  imported: boolean;
  learners: StudyLearnerResult[];
};

const lessonPath = (workspaceId: string, lessonPeriodId: string): string =>
  `/teaching/workspaces/${workspaceId}/lessons/${lessonPeriodId}/study-results`;

export const getStudySources = (lessonPeriodId: string): Promise<StudySource[]> =>
  apiFetch<StudySource[]>(`/teaching/study-results/sources?lesson_period_id=${lessonPeriodId}`);

export const getStudyResults = (
  workspaceId: string,
  lessonPeriodId: string,
): Promise<StudyResults> =>
  apiFetch<StudyResults>(lessonPath(workspaceId, lessonPeriodId));

export const importStudyResults = (
  workspaceId: string,
  lessonPeriodId: string,
  fromPlanVersionId: string,
): Promise<StudyResults> =>
  apiFetch<StudyResults>(lessonPath(workspaceId, lessonPeriodId), {
    method: "POST",
    body: JSON.stringify({ from_plan_version_id: fromPlanVersionId }),
  });

export type StandInResult = { made: { student_id: string; study_student_id: string }[] };

/** Makes each class learner's results from a study learner's marks, so their notes can be made. */
export const standInStudents = (
  workspaceId: string,
  lessonPeriodId: string,
  pairs: { student_id: string; study_student_id: string }[],
): Promise<StandInResult> =>
  apiFetch<StandInResult>(`${lessonPath(workspaceId, lessonPeriodId)}/stand-ins`, {
    method: "POST",
    body: JSON.stringify({ pairs }),
  });

export type LearnerAnswer = {
  objective_text: string;
  question: string;
  student_answer: string;
  correct_answer: string;
  correct: boolean;
  misconception: string | null;
};

/** `missed_only` means only the questions the learner got wrong were kept. */
export type LearnerAnswers = {
  source: "answers" | "marked_work" | "missed_only" | "none";
  answers: LearnerAnswer[];
};

export const getLearnerAnswers = (
  workspaceId: string,
  lessonPeriodId: string,
  studentId: string,
): Promise<LearnerAnswers> =>
  apiFetch<LearnerAnswers>(
    `/teaching/workspaces/${workspaceId}/lessons/${lessonPeriodId}/learners/${studentId}/answers`,
  );
