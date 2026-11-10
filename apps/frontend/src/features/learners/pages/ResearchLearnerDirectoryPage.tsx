import { useSearchParams } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";

import { useResearchLearnerDirectory } from "../hooks/useResearchLearnerDirectory";

const fieldClass =
  "rounded-none border border-[color:var(--line)] bg-(--surface) px-4 py-2 text-sm text-[color:var(--ink)] outline-none transition focus:border-[color:var(--accent)]";

/** Renders the researcher-facing study roster separate from the teacher roster UI. */
export function ResearchLearnerDirectoryPage() {
  const searchParams = useSearchParams();
  const {
    schoolId,
    setSchoolId,
    selectedWorkspaceId,
    setSelectedWorkspaceId,
    classId,
    setClassId,
    grade,
    setGrade,
    track,
    setTrack,
    schoolsQuery,
    experimentContextQuery,
    workspaces,
    classes,
    learnersQuery,
  } = useResearchLearnerDirectory({
    experimentId: searchParams.get("experimentId"),
    workspaceId: searchParams.get("workspaceId"),
  });

  return (
    <main className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-6 py-10">
      <header className="max-w-3xl space-y-3">
        <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--accent)]">
          Learners
        </div>
        <h1 className="text-4xl font-semibold tracking-tight text-[color:var(--ink)]">
          Study roster and learner evidence context
        </h1>
        <p className="text-base leading-relaxed text-[color:var(--muted)]">
          This view is for research only. Students still see their own work, and
          teachers still manage the editable class roster inside the teacher
          workspace.
        </p>
      </header>

      {experimentContextQuery.data && (
        <Card variant="glass" padding="lg" className="space-y-2">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
            Opened from experiment
          </p>
          <p className="text-sm font-semibold text-[color:var(--ink)]">
            {experimentContextQuery.data.experiment_code}
          </p>
          <p className="text-sm text-[color:var(--muted)]">
            {experimentContextQuery.data.lesson_title ?? "Lesson context"}
          </p>
        </Card>
      )}

      <Card variant="glass" padding="lg" className="space-y-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
            Filters
          </p>
          <h2 className="mt-1 text-lg font-semibold text-[color:var(--ink)]">
            Narrow the study roster
          </h2>
        </div>
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
          <select
            className={fieldClass}
            value={schoolId}
            onChange={(e) => setSchoolId(e.target.value)}
          >
            <option value="">All schools</option>
            {(schoolsQuery.data ?? []).map((school) => (
              <option key={school.id} value={school.id}>
                {school.name} ({school.school_code})
              </option>
            ))}
          </select>
          <select
            className={fieldClass}
            value={selectedWorkspaceId}
            onChange={(e) => setSelectedWorkspaceId(e.target.value)}
          >
            <option value="">All workspaces</option>
            {workspaces.map((workspace) => (
              <option
                key={workspace.teacher_workspace_id}
                value={workspace.teacher_workspace_id}
              >
                {workspace.workspace_name}
              </option>
            ))}
          </select>
          <select
            className={fieldClass}
            value={classId}
            onChange={(e) => setClassId(e.target.value)}
          >
            <option value="">All classes</option>
            {classes.map((item) => (
              <option key={item.id} value={item.id}>
                {item.name}
              </option>
            ))}
          </select>
          <input
            className={fieldClass}
            placeholder="Class"
            value={grade}
            onChange={(e) => setGrade(e.target.value)}
          />
          <input
            className={fieldClass}
            placeholder="Track"
            value={track}
            onChange={(e) => setTrack(e.target.value)}
          />
        </div>
      </Card>

      <Card padding="lg" className="space-y-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
              Learner list
            </p>
            <h2 className="text-lg font-semibold text-[color:var(--ink)]">
              Current study cohort
            </h2>
          </div>
          <span className="text-sm text-[color:var(--muted)]">
            {learnersQuery.data?.total ?? 0} learners
          </span>
        </div>
        {learnersQuery.isLoading && (
          <p className="text-sm text-[color:var(--muted)]">Loading learners…</p>
        )}
        {learnersQuery.data?.data.length ? (
          <div className="grid gap-3 md:grid-cols-2">
            {learnersQuery.data.data.map((learner) => (
              <div
                key={learner.student_id}
                className="rounded-3xl border border-[color:var(--line)] bg-(--surface) p-4"
              >
                <p className="font-semibold text-[color:var(--ink)]">
                  {learner.full_name}
                </p>
                <p className="mt-1 text-sm text-[color:var(--muted)]">
                  {learner.code ?? learner.student_id} ·{" "}
                  {learner.class_name ?? "No class"}
                </p>
                <p className="mt-1 text-sm text-[color:var(--muted)]">
                  {learner.grade} · {learner.track}
                </p>
              </div>
            ))}
          </div>
        ) : (
          !learnersQuery.isLoading && (
            <p className="text-sm text-[color:var(--muted)]">
              No learners match the current study filters.
            </p>
          )
        )}
      </Card>
    </main>
  );
}
