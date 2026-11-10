import type { LearnerLesson, LearnerObjectiveResult, LearnerResults, LearnerTest } from "@/features/learners/types";

/** A lesson id as an address spells it or as the API does: the two differ only in hyphens. */
const bare = (id: string): string => id.replaceAll("-", "");

export type LessonLearnerResult = {
  test: LearnerTest | null;
  objectives: LearnerObjectiveResult[];
  lesson: LearnerLesson | null;
};

/** What one learner's results say about one lesson: its test, its objectives and its revision note. */
export function resultsForLesson(results: LearnerResults, lessonPeriodId: string): LessonLearnerResult {
  const here = (candidate: { lesson_period_id: string }) =>
    bare(candidate.lesson_period_id) === bare(lessonPeriodId);
  return {
    test: results.tests.find(here) ?? null,
    objectives: results.objectives.filter(here),
    lesson: results.lessons.find(here) ?? null,
  };
}
