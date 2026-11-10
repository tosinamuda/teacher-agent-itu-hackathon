import type { LessonStepStructured } from "@/shared/types/lesson-schema";

export type TimelineSegment = {
  stepId: string;
  number: number;
  title: string;
  minutes: number | null;
  /** The step's share of the lesson, in percent, for the width of its segment. */
  share: number;
};

const minutesOf = (step: LessonStepStructured): number | null =>
  step.duration_minutes ?? step.estimated_minutes ?? null;

export const totalMinutes = (steps: LessonStepStructured[]): number =>
  steps.reduce((sum, step) => sum + (minutesOf(step) ?? 0), 0);

/** One segment per step, as wide as the step is long; equal widths when no step has a length. */
export function timelineOf(steps: LessonStepStructured[]): TimelineSegment[] {
  const total = totalMinutes(steps);
  return steps.map((step, at) => ({
    stepId: step.step_id,
    number: at + 1,
    title: step.title,
    minutes: minutesOf(step),
    share:
      total > 0 ? ((minutesOf(step) ?? 0) / total) * 100 : 100 / steps.length,
  }));
}

/** "SS1 · Mathematics · First Term, week 1 · 4 steps · 50 minutes". */
export function planSubtitle(plan: {
  grade?: string;
  subject?: string;
  term?: string;
  week?: number | null;
  steps: LessonStepStructured[];
}): string {
  const termAndWeek = [
    plan.term,
    plan.week != null ? `week ${plan.week}` : null,
  ]
    .filter(Boolean)
    .join(", ");
  const minutes = totalMinutes(plan.steps);
  return [
    plan.grade,
    plan.subject,
    termAndWeek || null,
    `${plan.steps.length} ${plan.steps.length === 1 ? "step" : "steps"}`,
    minutes > 0 ? `${minutes} minutes` : null,
  ]
    .filter(Boolean)
    .join(" · ");
}
