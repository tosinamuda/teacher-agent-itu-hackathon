import { useLessonHome } from "@/features/lesson-home/hooks/useLessonHome";

/** Names the lesson a page is for, so a teacher can match it to the lesson they take from. */
export function ThisLesson({ lessonPeriodId }: { lessonPeriodId: string }) {
  const { lesson } = useLessonHome(lessonPeriodId);
  if (!lesson) return null;
  return (
    <p className="border border-(--line) bg-(--surface) px-3 py-2 text-sm text-(--ink)">
      <span className="text-(--ink-2)">For this lesson: </span>
      <span className="font-semibold">{lesson.title}</span>
      <span className="text-(--ink-2)"> · week {lesson.week}</span>
    </p>
  );
}
