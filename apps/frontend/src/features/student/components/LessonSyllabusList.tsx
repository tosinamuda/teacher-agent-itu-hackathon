import { Link } from "@/shared/router";

import { LessonStatus, SyllabusLesson } from "@/features/student/hooks/useStudentSyllabus";

type LessonSyllabusListProps = {
  lessons: SyllabusLesson[];
  loading?: boolean;
};

const STATUS: Record<LessonStatus, { label: string; className: string; hint: string }> = {
  not_released: {
    label: "Not available yet",
    className: "bg-(--sunken) text-(--faint)",
    hint: "Your teacher hasn't released this assessment yet — check back soon.",
  },
  open: {
    label: "Assessment open",
    className: "bg-(--sunken) text-(--ink-2)",
    hint: "Take the exit assessment to unlock your personalised revision note.",
  },
  generating: {
    label: "Preparing note",
    className: "bg-(--warning-tint) text-(--warning-ink)",
    hint: "Assessment submitted — your revision note is being prepared.",
  },
  awaiting_review: {
    label: "Awaiting teacher",
    className: "bg-(--info-tint) text-(--info-ink)",
    hint: "Your revision note is ready and waiting for your teacher to approve it.",
  },
  ready: {
    label: "Revision note ready",
    className: "bg-(--success-tint) text-(--success-ink)",
    hint: "Your personalised revision note is ready.",
  },
};

/**
 * The selected subject's lessons (syllabus map). Each lesson is a link to its
 * own page (assessment → survey → revision note); the row shows the current status
 * at a glance.
 */
export default function LessonSyllabusList({ lessons, loading = false }: LessonSyllabusListProps) {
  if (loading) {
    return <p className="text-sm text-(--muted)">Loading lessons…</p>;
  }
  if (lessons.length === 0) {
    return (
      <p className="border border-dashed border-(--line) bg-(--surface) px-5 py-8 text-center text-sm text-(--muted)">
        No lessons are ready in this subject yet. Check back soon.
      </p>
    );
  }
  return (
    <ul className="divide-y divide-(--line) border border-(--line) bg-(--surface)">
      {lessons.map((lesson) => {
        const status = STATUS[lesson.status];
        return (
          <li key={lesson.versionId}>
            <Link
              href={`/research/student/lesson/${lesson.versionId}`}
              className="flex flex-wrap items-center justify-between gap-4 p-5 transition-colors hover:bg-(--sunken)"
            >
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-[11px] font-semibold uppercase tracking-[0.14em] text-(--faint)">
                    Week {lesson.week ?? "—"}
                  </span>
                  <span className={`px-2 py-0.5 text-[11px] font-medium ${status.className}`}>
                    {status.label}
                  </span>
                </div>
                <p className="mt-1 font-semibold text-(--ink)">{lesson.title}</p>
                <p className="mt-1 text-xs text-(--muted)">{status.hint}</p>
              </div>
              <span aria-hidden className="shrink-0 text-lg text-(--faint)">
                →
              </span>
            </Link>
          </li>
        );
      })}
    </ul>
  );
}
