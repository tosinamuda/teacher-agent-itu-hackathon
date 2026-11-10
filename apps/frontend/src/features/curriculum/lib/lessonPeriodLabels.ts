import type { LessonPeriod } from "../hooks/useSchemeOfWork";

type Labelled = Pick<LessonPeriod, "title" | "subtopic_title" | "subtopic_id">;

const sameText = (a: string, b: string) =>
  a.trim().toLocaleLowerCase() === b.trim().toLocaleLowerCase();

/**
 * The line under a lesson period's name: the curriculum subtopic it teaches, when that says
 * something the name does not. The scheme of work and the curriculum often spell one lesson
 * with different capitals, and that is the same lesson, not a second one.
 */
export function lessonPeriodSubtitle(period: Labelled): string | null {
  if (period.title && period.subtopic_title) {
    return sameText(period.title, period.subtopic_title) ? null : period.subtopic_title;
  }
  return period.subtopic_id || "No subtopic assigned";
}
