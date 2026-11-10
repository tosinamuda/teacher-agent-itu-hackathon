import { ResearchDefaults } from "../lib/experiments";

/** The lesson context a synthetic experiment is scoped to (from the experiment detail). */
export type LessonContext = {
  schoolName?: string | null;
  className?: string | null;
  subjectName?: string | null;
  gradeLevel?: string | null;
  term?: string | null;
  lessonTitle?: string | null;
};

/**
 * Step 1 of the synthetic harness: the lesson context the synthetic teacher works from
 * (school · class · subject · grade · term — subtopic), plus the configured default
 * subtopic. Display-only — the context itself is chosen when the experiment is created.
 */
export function SyntheticContextStep({
  context,
  defaults,
}: {
  context?: LessonContext;
  defaults?: ResearchDefaults;
}) {
  const parts = [
    context?.schoolName,
    context?.className,
    context?.subjectName,
    context?.gradeLevel,
    context?.term,
  ].filter((part, index, all) => Boolean(part) && all.indexOf(part) === index);
  return (
    <div className="flex items-start gap-3">
      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-none bg-(--accent) text-xs font-semibold text-white">
        1
      </span>
      <div className="space-y-0.5">
        <p className="text-xs font-semibold text-(--ink)">Lesson context (subtopic)</p>
        <p className="text-[11px] text-(--muted)">
          {parts.length ? parts.join(" · ") : "Lesson context unavailable"}
          {context?.lessonTitle ? ` — ${context.lessonTitle}` : ""}
        </p>
        {defaults ? (
          <p className="text-[11px] text-(--muted)">
            Configured default: {defaults.term} · {defaults.subtopic}
          </p>
        ) : null}
      </div>
    </div>
  );
}
