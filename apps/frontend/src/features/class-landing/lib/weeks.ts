import type { TermClassSubject } from "@/features/curriculum/hooks/useSchemeOfWork";
import type { LessonReview } from "@/features/teaching-workspace/api/lessonReviews";
import type { TeachingWorkspace } from "@/features/teaching-workspace/types";

export type WeekRow = {
  id: string;
  number: number;
  title: string;
  /** The day the week starts, as "14 Sep"; null when the term has no dates. */
  startsOn: string | null;
  current: boolean;
  /** How many things in the week's lessons wait for the teacher. */
  waiting: number;
  lessons: { id: string; title: string; waiting: string | null }[];
};

const MONTHS = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

const dayAndMonth = (isoDate: string): string => {
  const [, month, day] = isoDate.split("-").map(Number);
  return `${day} ${MONTHS[month - 1]}`;
};

/** The class's weeks in order, each with its lessons. */
export function weekRows(
  scheme: TermClassSubject | undefined,
  reviews: LessonReview[] = [],
): WeekRow[] {
  const reviewOf = new Map(
    reviews.map((review) => [review.lesson_period_id, review]),
  );
  return [...(scheme?.weeks ?? [])]
    .sort((a, b) => a.week_number - b.week_number)
    .map((week) => ({
      id: week.id,
      number: week.week_number,
      title: week.title,
      startsOn: week.starts_on ? dayAndMonth(week.starts_on) : null,
      current: week.week_number === scheme?.current_week_number,
      waiting: week.lesson_periods.reduce(
        (sum, period) => sum + waitingCount(reviewOf.get(period.id)),
        0,
      ),
      lessons: [...week.lesson_periods]
        .sort((a, b) => a.period_number - b.period_number)
        .map((period) => ({
          id: period.id,
          title:
            period.subtopic_title ??
            period.title ??
            `Lesson ${period.period_number}`,
          waiting: waitingText(reviewOf.get(period.id)),
        })),
    }));
}

const waitingCount = (review: LessonReview | undefined): number =>
  review
    ? review.plans_to_approve +
      review.materials_to_review +
      review.notes_to_review
    : 0;

const counted = (count: number, one: string, many: string): string | null =>
  count === 0 ? null : `${count} ${count === 1 ? one : many}`;

/** What waits in a lesson, as "Plan to approve · 2 notes to review"; null when nothing does. */
export function waitingText(review: LessonReview | undefined): string | null {
  if (!review) return null;
  const parts = [
    review.plans_to_approve > 0 ? "Plan to approve" : null,
    counted(
      review.materials_to_review,
      "material to review",
      "materials to review",
    ),
    counted(review.notes_to_review, "note to review", "notes to review"),
  ].filter((part): part is string => part !== null);
  return parts.length > 0 ? parts.join(" · ") : null;
}

export type LessonToStart = { id: string; title: string; weekNumber: number };

/** The first lesson with no plan at all, starting with this week and then the weeks in order. */
export function lessonToStart(
  weeks: WeekRow[],
  lessonsWithoutApprovedPlan: Set<string>,
  reviews: LessonReview[],
): LessonToStart | null {
  const drafted = new Set(
    reviews
      .filter((review) => review.plans_to_approve > 0)
      .map((review) => review.lesson_period_id),
  );
  const ordered = [
    ...weeks.filter((week) => week.current),
    ...weeks.filter((week) => !week.current),
  ];
  for (const week of ordered) {
    const lesson = week.lessons.find(
      (l) => lessonsWithoutApprovedPlan.has(l.id) && !drafted.has(l.id),
    );
    if (lesson)
      return { id: lesson.id, title: lesson.title, weekNumber: week.number };
  }
  return null;
}

export const lessonCountText = (count: number): string =>
  `${count} ${count === 1 ? "lesson" : "lessons"}`;

/** The terms of the class and subject the teacher has open, the open one among them. */
export function termsOf(
  workspaces: TeachingWorkspace[],
  current: TeachingWorkspace | null,
): TeachingWorkspace[] {
  if (!current) return [];
  return workspaces.filter(
    (workspace) =>
      workspace.class_id === current.class_id &&
      workspace.subject_code === current.subject_code,
  );
}

const WAITING_LABEL: Record<string, string> = {
  plan: "plan",
  "lesson-note": "lesson note",
  "slide-deck": "slides",
  "revision-note": "revision note",
  "class-test": "class test",
  "exam-questions": "exam questions",
};

export type LessonWaiting = {
  id: string;
  title: string;
  weekNumber: number;
  since: string;
  action: string;
};

const DAY = 24 * 60 * 60 * 1000;
const WEEKDAYS = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];

/** "Monday" within the last week, otherwise "14 Sep". */
export function sinceText(since: string, now: Date): string {
  const at = new Date(since);
  return now.getTime() - at.getTime() < 6 * DAY
    ? WEEKDAYS[at.getDay()]
    : dayAndMonth(since.slice(0, 10));
}

/** The lesson that has had something waiting for the longest, and what the teacher does about it. */
export function longestWaiting(
  weeks: WeekRow[],
  reviews: LessonReview[],
  now: Date,
): LessonWaiting | null {
  const oldest = [...reviews].sort((a, b) =>
    a.waiting_since.localeCompare(b.waiting_since),
  )[0];
  if (!oldest) return null;
  for (const week of weeks) {
    const lesson = week.lessons.find((l) => l.id === oldest.lesson_period_id);
    if (!lesson) continue;
    const label = WAITING_LABEL[oldest.oldest_kind];
    return {
      id: lesson.id,
      title: lesson.title,
      weekNumber: week.number,
      since: sinceText(oldest.waiting_since, now),
      action: label ? `Review ${label}` : "Review",
    };
  }
  return null;
}
