const LESSONS = "/research/teacher/lessons";

/** Where each way of making a lesson's plan lives. They sit under the lesson so its sidebar stays. */
export const makePlanPath = (lessonPeriodId: string): string =>
  `${LESSONS}/${lessonPeriodId}/plan/new`;
export const importPlanPath = (lessonPeriodId: string): string =>
  `${LESSONS}/${lessonPeriodId}/plan/import`;
export const writePlanPath = (lessonPeriodId: string): string =>
  `${LESSONS}/${lessonPeriodId}/plan/write`;
export const reusePlanPath = (lessonPeriodId: string): string =>
  `${LESSONS}/${lessonPeriodId}/reuse-plan`;

/** A plan's own page, opened by the plan's id or one of its versions'. */
export const planPath = (planId: string): string =>
  `/research/teacher/lesson-plan/${planId}`;
