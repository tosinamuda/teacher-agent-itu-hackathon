import { Link } from "@/shared/router";

import { useAuthMe } from "@/shared/hooks/useAuthMe";

import { useLessonsToPrepare } from "../hooks/useLessonsToPrepare";
import { experimentTitle } from "../lib/experiments";

const MAX_PREVIEW = 4;

/**
 * "Needs your attention" preview for the teacher home: the lessons that need a
 * next action right now, each linking straight to its prep hub. Renders nothing
 * when there's nothing pending (the home then just shows the nav cards).
 */
export function TeacherAttentionPreview() {
  const me = useAuthMe();
  const teacherId = me.data?.teacher_id ?? undefined;
  const { pending, isLoading } = useLessonsToPrepare(teacherId);

  if (!teacherId || isLoading || pending.length === 0) return null;

  const top = pending.slice(0, MAX_PREVIEW);

  return (
    <section>
      <div className="mb-3 flex items-center justify-between gap-2">
        <h2 className="text-sm font-semibold text-(--ink)">Needs your attention</h2>
        <Link
          href="/research/teacher/experiment-plans"
          className="text-xs font-semibold text-(--accent-deep) hover:underline"
        >
          See all ({pending.length}) →
        </Link>
      </div>
      <ul className="divide-y divide-(--line) border border-(--line) bg-(--surface)">
        {top.map(({ experiment, doneCount, total, current }) => (
          <li key={experiment.experiment_id}>
            <Link
              href={`/research/teacher/experiment-plans/${experiment.experiment_id}`}
              className="flex items-center justify-between gap-4 p-4 transition-colors hover:bg-(--sunken)"
            >
              <div className="min-w-0">
                <p className="truncate font-semibold text-(--ink)">{experimentTitle(experiment)}</p>
                <p className="mt-0.5 text-xs">
                  <span className="font-semibold text-(--accent-deep)">
                    {current ? `Next: ${current.title}` : "Ready"}
                  </span>
                  <span className="text-(--muted)"> · {doneCount}/{total} steps done</span>
                </p>
              </div>
              <span aria-hidden className="shrink-0 text-lg text-(--faint)">
                →
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
