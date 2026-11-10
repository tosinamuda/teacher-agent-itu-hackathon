import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";
import { TabBar } from "@/shared/components/ui/TabBar";
import { useAuthMe } from "@/shared/hooks/useAuthMe";

import { useLessonsToPrepare } from "../hooks/useLessonsToPrepare";
import { lessonHeading } from "../lib/lessonHeading";

const TABS = [
  { href: "/research/teacher/experiment-plans", label: "To prepare", view: "to-prepare" },
  { href: "/research/teacher/experiment-plans/all", label: "All lessons", view: "all" },
] as const;

/**
 * The teacher's lessons. **To prepare** is the queue: each lesson links to its prep hub
 * (plan → revision note → assessment → per-student notes), showing the current
 * step at a glance, and stays until every step is done. **All lessons** also lists the
 * finished ones, so a lesson can be reopened. The research conditions run in the
 * background and never surface here.
 */
export function TeacherExperimentPlansPage({ view }: { view: (typeof TABS)[number]["view"] }) {
  const me = useAuthMe();
  const teacherId = me.data?.teacher_id ?? undefined;
  const { pending, all, isLoading } = useLessonsToPrepare(teacherId);
  const shown = view === "all" ? all : pending;

  return (
    <main className="mx-auto flex w-full max-w-3xl flex-col gap-5 px-6 py-8">
      <header className="space-y-1">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
          Teacher
        </p>
        <h1 className="text-2xl font-semibold text-(--ink)">
          {view === "all" ? "All lessons" : "Lessons to prepare"}
        </h1>
        <p className="text-sm text-(--muted)">
          Each lesson goes through a few steps: author and accept its plan, review and
          accept the class revision note built from it, then accept each student&apos;s
          personalised revision note once they&apos;ve taken the assessment.
        </p>
        <Link href="/research" className="inline-block pt-1 text-sm text-(--accent-deep) hover:underline">
          ← Back to workspace
        </Link>
      </header>

      <TabBar
        label="Lessons"
        tabs={TABS.map((tab) => ({ ...tab, active: tab.view === view }))}
      />

      {me.data && !teacherId ? (
        <Card padding="lg">
          <p className="text-sm text-(--muted)">
            Sign in with a teacher code to see your lessons.
          </p>
        </Card>
      ) : isLoading || me.isLoading ? (
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Loading your lessons…</p>
        </Card>
      ) : shown.length === 0 ? (
        <Card padding="lg">
          <h3 className="font-semibold text-(--ink)">
            {view === "all" ? "No lessons yet" : "You're all caught up"}
          </h3>
          <p className="mt-1 text-sm text-(--muted)">
            {view === "all"
              ? "When a lesson is queued for you it lands here."
              : "No lessons need preparing right now. When a new lesson is queued for you it lands here."}
          </p>
        </Card>
      ) : (
        <div className="space-y-3">
          {shown.map(({ experiment, doneCount, total, current }) => (
            <Link
              key={experiment.experiment_id}
              href={`/research/teacher/experiment-plans/${experiment.experiment_id}`}
              className="block"
            >
              <Card
                padding="lg"
                className="flex items-center justify-between gap-4 transition hover:border-(--accent)/50"
              >
                <div className="min-w-0">
                  {/* A teacher sees their lesson, not the study's internal identifiers. */}
                  <h3 className="truncate font-semibold text-(--ink)">
                    {lessonHeading(experiment).name}
                  </h3>
                  <p className="text-xs text-(--muted)">{lessonHeading(experiment).where}</p>
                  <p className="mt-1 text-xs">
                    <span className="font-semibold text-(--accent-deep)">
                      {current ? `Next: ${current.title}` : "Ready"}
                    </span>
                    <span className="text-(--muted)"> · {doneCount}/{total} steps done</span>
                  </p>
                </div>
                <span aria-hidden className="shrink-0 text-lg text-(--faint)">
                  →
                </span>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}
