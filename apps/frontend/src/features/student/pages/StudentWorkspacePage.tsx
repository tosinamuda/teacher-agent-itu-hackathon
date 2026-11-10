import { useMemo, useState } from "react";

import SubjectFilterPills from "@/features/student/components/SubjectFilterPills";
import LessonSyllabusList from "@/features/student/components/LessonSyllabusList";
import { useStudentWorkspace } from "@/features/student/hooks/useStudentWorkspace";
import { useStudentSyllabus } from "@/features/student/hooks/useStudentSyllabus";
import { useStudentAuth } from "@/features/student/context/StudentContext";

export default function StudentWorkspacePage() {
  const { student, studentId, logout } = useStudentAuth();
  const { packs } = useStudentWorkspace(studentId);
  const { subjects, lessonsQuery } = useStudentSyllabus(studentId, packs);

  const [activeSubject, setActiveSubject] = useState<string | null>(null);
  const currentSubject = activeSubject ?? subjects[0]?.subject ?? null;
  const lessons = subjects.find((s) => s.subject === currentSubject)?.lessons ?? [];
  const subjectOptions = subjects.map((s) => ({
    value: s.subject,
    label: s.subject,
    count: s.lessons.length,
  }));

  // Lessons the student can act on right now: an assessment to take, or an
  // approved revision note to read. Surfaced up top so they go straight in.
  const needsAttention = useMemo(
    () =>
      subjects
        .flatMap((s) => s.lessons)
        .filter((lesson) => lesson.status === "open" || lesson.status === "ready"),
    [subjects]
  );

  const workspaceLabel = student?.grade ? `${student.grade} Student workspace` : "Student workspace";

  return (
    <main className="mx-auto w-full max-w-[1200px] px-4 pb-12 pt-6 sm:px-6 sm:pb-16 sm:pt-10">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="max-w-2xl">
          <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
            {workspaceLabel}
          </p>
          <h1 className="mt-1 text-3xl font-semibold text-(--ink)">Your lessons</h1>
          <p className="mt-2 text-sm text-(--muted)">
            Open a lesson to take its assessment and read your revision note.
          </p>
        </div>
        <button
          onClick={logout}
          className="border border-(--line-2) px-3 py-1.5 text-sm text-(--ink-2) transition-colors hover:bg-(--sunken)"
        >
          Log out
        </button>
      </div>

      {lessonsQuery.isError && (
        <div className="mt-8 border border-(--danger-tint) bg-(--danger-tint) px-5 py-4 text-sm text-(--danger-ink)">
          We couldn&rsquo;t load your lessons right now. Please refresh in a moment.
        </div>
      )}

      {/* What to do now — actionable lessons, straight to the lesson page. */}
      {needsAttention.length > 0 ? (
        <section className="mt-8">
          <h2 className="mb-3 text-sm font-semibold text-(--ink)">Needs your attention</h2>
          <LessonSyllabusList lessons={needsAttention} />
        </section>
      ) : null}

      {/* All lessons, by subject. */}
      <section className="mt-10">
        <h2 className="mb-3 text-sm font-semibold text-(--ink)">All lessons</h2>
        {subjectOptions.length > 0 ? (
          <nav className="mb-4">
            <SubjectFilterPills
              options={subjectOptions}
              active={currentSubject ?? ""}
              onSelect={setActiveSubject}
            />
          </nav>
        ) : null}
        <LessonSyllabusList lessons={lessons} loading={lessonsQuery.isLoading} />
      </section>
    </main>
  );
}
