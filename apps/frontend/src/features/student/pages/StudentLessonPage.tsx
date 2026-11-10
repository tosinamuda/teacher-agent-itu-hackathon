import { Link } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";
import { useStudentAuth } from "@/features/student/context/StudentContext";
import { useStudentWorkspace } from "@/features/student/hooks/useStudentWorkspace";
import { useStudentSyllabus, SyllabusLesson } from "@/features/student/hooks/useStudentSyllabus";

type StageState = "done" | "now" | "waiting" | "locked";

const STAGE_STYLE: Record<StageState, { ring: string; label: string; labelClass: string }> = {
  done: { ring: "border-(--success-ink) bg-(--success-tint) text-(--success-ink)", label: "Done", labelClass: "text-(--success-ink)" },
  now: { ring: "border-(--accent) bg-(--accent-soft) text-(--accent-deep)", label: "Now", labelClass: "text-(--accent-deep)" },
  waiting: { ring: "border-(--line) bg-(--surface) text-(--muted)", label: "Waiting", labelClass: "text-(--muted)" },
  locked: { ring: "border-(--line) bg-(--surface) text-(--faint)", label: "Locked", labelClass: "text-(--faint)" },
};

type Stage = { title: string; detail: string; state: StageState; action?: { href: string; label: string } };

/** Derive the three lesson stages (assessment → survey → revision note) from status. */
function lessonStages(lesson: SyllabusLesson): Stage[] {
  const submitted = lesson.status !== "not_released" && lesson.status !== "open";
  const assessHref = `/research/student/exit-assessment?plan_version_id=${lesson.versionId}`;
  const noteHref = lesson.pack
    ? `/research/student/pack-runner?artefact_id=${lesson.pack.artefact_id}`
    : undefined;

  const assessment: Stage =
    lesson.status === "not_released"
      ? { title: "Take the assessment", detail: "Your teacher hasn't released this assessment yet — check back soon.", state: "locked" }
      : submitted
        ? { title: "Take the assessment", detail: "You've completed this assessment.", state: "done" }
        : {
            title: "Take the assessment",
            detail: "A short multiple-choice check on this lesson.",
            state: "now",
            action: { href: assessHref, label: "Take the assessment →" },
          };

  const survey: Stage = {
    title: "Reflect with a quick survey",
    detail: "A few confidence & difficulty questions at the end of the assessment.",
    state: submitted ? "done" : lesson.status === "open" ? "now" : "locked",
  };

  let reviewNote: Stage;
  if (lesson.status === "ready" && noteHref) {
    reviewNote = {
      title: "Read your revision note",
      detail: "Your personalised revision note for this lesson is ready.",
      state: "now",
      action: { href: noteHref, label: "Read your revision note →" },
    };
  } else if (lesson.status === "awaiting_review") {
    reviewNote = { title: "Read your revision note", detail: "Your teacher is reviewing your note — it'll appear here once approved.", state: "waiting" };
  } else if (lesson.status === "generating") {
    reviewNote = { title: "Read your revision note", detail: "Your note is being prepared from your answers.", state: "waiting" };
  } else {
    reviewNote = { title: "Read your revision note", detail: "Available once you've taken the assessment and your teacher approves your note.", state: "locked" };
  }

  return [assessment, survey, reviewNote];
}

/**
 * One lesson's page for a student: the lesson's learning journey as three stages
 * — take the assessment, the end-of-assessment survey, then read the personalised
 * revision note once the teacher approves it. Opened from the syllabus on the home.
 */
export function StudentLessonPage({ planVersionId }: { planVersionId: string }) {
  const { studentId } = useStudentAuth();
  const { packs } = useStudentWorkspace(studentId);
  const { subjects, lessonsQuery } = useStudentSyllabus(studentId, packs);
  const lesson = subjects.flatMap((s) => s.lessons).find((l) => l.versionId === planVersionId);

  return (
    <main className="mx-auto flex w-full max-w-3xl flex-col gap-5 px-4 py-6 sm:px-6 sm:py-8">
      <Link href="/research/student" className="text-sm text-(--accent-deep) hover:underline">
        ← All my lessons
      </Link>

      {lessonsQuery.isLoading && !lesson ? (
        <p className="text-sm text-(--muted)">Loading lesson…</p>
      ) : !lesson ? (
        <p className="text-sm text-(--muted)">This lesson isn&rsquo;t in your syllabus.</p>
      ) : (
        <>
          <header className="space-y-1">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
              {lesson.subject} · Week {lesson.week ?? "—"}
            </p>
            <h1 className="text-2xl font-semibold text-(--ink)">{lesson.title}</h1>
          </header>

          <ol className="space-y-3 rounded-2xl border border-(--line) bg-(--surface) p-5">
            {lessonStages(lesson).map((stage, index) => {
              const style = STAGE_STYLE[stage.state];
              return (
                <li key={stage.title} className="flex gap-3">
                  <span className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full border text-xs font-semibold ${style.ring}`}>
                    {stage.state === "done" ? "✓" : index + 1}
                  </span>
                  <div className="flex-1 border-b border-(--line)/60 pb-3 last:border-b-0">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <p className="text-sm font-semibold text-(--ink)">{stage.title}</p>
                      <span className={`text-[11px] font-semibold uppercase tracking-wide ${style.labelClass}`}>
                        {style.label}
                      </span>
                    </div>
                    <p className="mt-0.5 text-xs text-(--muted)">{stage.detail}</p>
                    {stage.action ? (
                      <Link href={stage.action.href} className="mt-2 inline-block">
                        <Button size="sm">{stage.action.label}</Button>
                      </Link>
                    ) : null}
                  </div>
                </li>
              );
            })}
          </ol>
        </>
      )}
    </main>
  );
}
