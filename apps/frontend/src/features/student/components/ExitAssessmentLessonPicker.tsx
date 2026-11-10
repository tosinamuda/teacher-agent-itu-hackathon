import type { LessonVersionSummary } from "@/features/student/api/exitAssessment";

type Props = {
  lessons: LessonVersionSummary[];
  isLoading: boolean;
  onSelect: (versionId: string) => void;
};

/** Step 1: let the student pick the lesson they just finished. */
export function ExitAssessmentLessonPicker({ lessons, isLoading, onSelect }: Props) {
  return (
    <section className="flex flex-col gap-3">
      <h2 className="text-lg font-semibold text-(--ink)">Pick the lesson you just finished</h2>
      {isLoading && <p className="text-(--muted)">Loading lessons…</p>}
      {!isLoading && lessons.length === 0 && (
        <p className="text-(--muted)">No lessons available yet.</p>
      )}
      <ul className="flex flex-col gap-2">
        {lessons.map((lesson) => (
          <li key={lesson.version_id}>
            <button
              type="button"
              onClick={() => onSelect(lesson.version_id)}
              className="w-full rounded-2xl border border-(--line) bg-(--surface) p-4 text-left transition hover:border-(--accent)"
            >
              <span className="font-medium text-(--ink)">
                {lesson.subject}
                {lesson.week ? ` · Week ${lesson.week}` : ""}
              </span>
              <span className="block text-sm text-(--muted)">{lesson.version_id}</span>
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
