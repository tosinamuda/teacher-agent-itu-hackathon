import { makePlanPath } from "@/features/lesson-plan/lib/planPaths";
import { Link } from "@/shared/router";

import { Badge } from "@/shared/components/ui/Badge";
import { Button } from "@/shared/components/ui/Button";

import { useTeachingWorkspace } from "../context/TeachingWorkspaceContext";
import { useWorkspaceLessons } from "../hooks/useWorkspaceLessons";

/**
 * Teacher "lessons to create" to-do: the subtopics in the current workspace that
 * still need a lesson plan, with an "under research study" badge so the teacher can
 * prioritise the ones a researcher has scoped into an investigation.
 */
export default function TeacherTodoPage() {
  const { currentWorkspace, isLoading: workspaceLoading } =
    useTeachingWorkspace();
  const { todo, lessons, isLoading, isError } = useWorkspaceLessons(
    currentWorkspace?.id ?? null,
  );

  return (
    <main className="mx-auto w-full max-w-4xl p-6 md:p-8">
      <header className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold text-(--ink)">
            Lessons to create
          </h1>
          <p className="text-sm text-(--muted)">
            {currentWorkspace
              ? `${currentWorkspace.name} · ${currentWorkspace.subject_name}`
              : "Subtopics that still need a lesson plan."}
          </p>
        </div>
        <Link href="/research/teacher/lesson-plan">
          <Button>Open lesson plan</Button>
        </Link>
      </header>

      {!workspaceLoading && !currentWorkspace ? (
        <p className="rounded-2xl border border-dashed border-(--line) bg-(--surface) p-6 text-center text-sm text-(--muted)">
          You aren&apos;t assigned to a workspace yet. Ask a researcher to
          assign your class — subjects, term and the scheme of work are
          configured under Setup.
        </p>
      ) : null}
      {isError ? (
        <p className="mb-4 text-sm text-(--danger)">
          Couldn&apos;t load lessons.
        </p>
      ) : null}
      {isLoading ? (
        <p className="text-sm text-(--muted)">Loading lessons…</p>
      ) : null}

      {!isLoading && currentWorkspace ? (
        <>
          <p className="mb-3 text-sm text-(--muted)">
            {todo.length} of {lessons.length} lessons still need a plan.
          </p>
          {todo.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-(--line) bg-(--surface) p-8 text-center">
              <h3 className="font-semibold text-(--ink)">All caught up 🎉</h3>
              <p className="mt-1 text-sm text-(--muted)">
                Every lesson in this class has a plan.
              </p>
            </div>
          ) : (
            <ul className="space-y-2">
              {todo.map((lesson) => (
                <li
                  key={lesson.lesson_period_id}
                  className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-(--line) bg-(--surface) p-4"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-(--ink)">
                        {lesson.lesson_title}
                      </span>
                      {lesson.under_research_study ? (
                        <Badge variant="accent">Under research study</Badge>
                      ) : null}
                    </div>
                    <p className="text-xs text-(--muted)">
                      Week {lesson.week_number} · Period {lesson.period_number}
                    </p>
                  </div>
                  <Link href={makePlanPath(lesson.lesson_period_id)}>
                    <Button size="sm" variant="secondary">
                      Create plan
                    </Button>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </>
      ) : null}
    </main>
  );
}
