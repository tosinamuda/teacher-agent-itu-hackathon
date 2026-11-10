import type { LearnerTest } from "../types";

const RECENT = 3;

/** The learner's latest tests, oldest first, so they read left to right as time passes. */
export function recentTests(tests: LearnerTest[]): LearnerTest[] {
  return tests.slice(0, RECENT).reverse();
}

/** One line on where the scores are heading, when the tests can be compared. */
export function trendSentence(recent: LearnerTest[]): string | null {
  const first = recent[0];
  const last = recent[recent.length - 1];
  const comparable =
    recent.length >= 2 &&
    recent.every((test) => test.correct !== null && test.out_of === first.out_of);
  if (!comparable || first.correct === null || last.correct === null) return null;

  const span = `over the last ${recent.length} lessons`;
  if (last.correct < first.correct) return `Scores fell from ${first.correct} to ${last.correct} ${span}.`;
  if (last.correct > first.correct) return `Scores rose from ${first.correct} to ${last.correct} ${span}.`;
  return `Scores held at ${last.correct} ${span}.`;
}

/** A score as a teacher reads it, or nothing when the test was recorded without counts. */
export function scoreText(correct: number | null, outOf: number | null): string {
  return correct === null || outOf === null ? "Taken" : `${correct} of ${outOf}`;
}

/** Where a lesson opens for the teacher. */
export const lessonHref = (lessonPeriodId: string): string =>
  `/research/teacher/lessons/${encodeURIComponent(lessonPeriodId)}`;

/** Where a revision note opens for the teacher to review. */
export const noteHref = (artefactId: string): string =>
  `/research/teacher/pack-reviews/${encodeURIComponent(artefactId)}`;
