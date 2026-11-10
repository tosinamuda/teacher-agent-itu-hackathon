import { Link } from "@/shared/router";
import { useSearchParams } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";

import { ExitAssessmentLessonPicker } from "@/features/student/components/ExitAssessmentLessonPicker";
import { ExitAssessmentObjectiveCard } from "@/features/student/components/ExitAssessmentObjectiveCard";
import { ExitAssessmentQuestionList } from "@/features/student/components/ExitAssessmentQuestionList";
import { ExitAssessmentSessionCard } from "@/features/student/components/ExitAssessmentSessionCard";
import { ExitAssessmentSubmittedPanel } from "@/features/student/components/ExitAssessmentResult";
import { useStudentAuth } from "@/features/student/context/StudentContext";
import { useExitAssessment } from "@/features/student/hooks/useExitAssessment";

/**
 * Student-facing MCQ exit assessment: pick the finished lesson, answer the
 * objective-tagged multiple-choice items + a confidence/difficulty survey, then
 * submit (graded server-side into the objective-indexed diagnostic). Submitting
 * triggers the backend to build a personalised pack, held for teacher approval.
 */
export default function StudentExitAssessmentPage() {
  const { student } = useStudentAuth();
  const searchParams = useSearchParams();
  const preselectedLesson = searchParams.get("plan_version_id");
  const assessment = useExitAssessment(student?.student_id ?? null, preselectedLesson);

  if (!student) {
    return (
      <main className="mx-auto flex min-h-screen max-w-[40rem] flex-col items-center justify-center gap-4 p-8 text-center">
        <h1 className="text-2xl font-semibold text-(--ink)">Exit assessment</h1>
        <p className="text-(--muted)">Please sign in to continue.</p>
        <Link href="/research/student">
          <Button variant="primary">Go to sign in</Button>
        </Link>
      </main>
    );
  }

  const {
    step,
    phase,
    objectives,
    hasItems,
    itemOffsets,
    form,
    lessonsQuery,
    questionsQuery,
    answeredByObjective,
    alreadySubmitted,
    isCheckingSubmission,
    selectLesson,
    submit,
    isSubmitting,
    submitSurvey,
    isSubmittingSurvey,
    surveyComplete,
    hasError,
  } = assessment;

  return (
    <main className="mx-auto max-w-[52rem] p-4 sm:p-6 md:p-8">
      <header className="mb-6">
        <p className="text-sm uppercase tracking-wide text-(--accent-deep)">Post-class check</p>
        <h1 className="text-2xl font-semibold text-(--ink)">Exit assessment &amp; survey</h1>
        <p className="text-(--muted)">
          {student.full_name} · {student.grade}
        </p>
      </header>

      {step === "select" && (
        <ExitAssessmentLessonPicker
          lessons={lessonsQuery.data ?? []}
          isLoading={lessonsQuery.isLoading}
          onSelect={selectLesson}
        />
      )}

      {step === "assess" && (
        <section className="flex flex-col gap-6">
          {questionsQuery.isLoading && <p className="text-(--muted)">Loading questions…</p>}

          {questionsQuery.isError && (
            <div className="rounded-2xl border border-(--line) bg-(--surface) p-5">
              <p className="text-(--ink)">Your teacher hasn&apos;t released this assessment yet.</p>
              <p className="mt-1 text-sm text-(--muted)">
                Check back once they&apos;ve sent it to your class.
              </p>
            </div>
          )}

          {questionsQuery.isSuccess && !hasItems && (
            <div className="rounded-2xl border border-(--line) bg-(--surface) p-5">
              <p className="text-(--ink)">Your teacher hasn&apos;t sent this lesson&apos;s test yet.</p>
              <p className="mt-1 text-sm text-(--muted)">
                Check back once they&apos;ve sent it to your class.
              </p>
            </div>
          )}

          {/* Screen 1 — the test: one flat numbered list, objective tags stay
              backend metadata. Submitting grades the answers server-side; the
              survey only appears AFTER, so it can't colour the test. */}
          {hasItems && !isCheckingSubmission && phase === "questions" && (
            <>
              <ExitAssessmentQuestionList
                objectives={objectives}
                itemOffsets={itemOffsets}
                form={form}
              />
              <Button variant="primary" onClick={() => submit()} disabled={isSubmitting}>
                {isSubmitting ? "Submitting…" : "Submit my answers"}
              </Button>
            </>
          )}

          {/* Screen 2 — the post-class survey, grouped per objective. */}
          {phase === "survey" && (
            <div className="flex flex-col gap-4">
              <div className="rounded-2xl border border-(--line) bg-(--surface) p-5">
                <p className="font-medium text-(--ink)">Your answers are in! ✅</p>
                <p className="mt-1 text-sm text-(--muted)">
                  One last thing — tell us how the lesson felt. There are no right or
                  wrong answers here.
                </p>
              </div>
              {objectives.map((objective, index) => (
                <ExitAssessmentObjectiveCard
                  key={objective.lesson_objective_id}
                  objective={objective}
                  objectiveNumber={index + 1}
                  surveyIndex={index}
                  form={form}
                />
              ))}
              <ExitAssessmentSessionCard form={form} />
              <Button
                variant="primary"
                onClick={() => submitSurvey()}
                disabled={isSubmittingSurvey || !surveyComplete}
              >
                {isSubmittingSurvey ? "Sending…" : "Send my survey"}
              </Button>
              {!surveyComplete && (
                <p className="text-sm text-(--muted)">Answer every question to send your survey.</p>
              )}
            </div>
          )}

          {/* Screen 3 — confirmation (questions leave the screen on submit —
              2026-06-10 dress-rehearsal finding). */}
          {phase === "done" && (
            <ExitAssessmentSubmittedPanel
              objectives={objectives}
              answeredByObjective={answeredByObjective}
              alreadySubmitted={alreadySubmitted}
            />
          )}
          {hasError && (
            <p className="text-(--accent-deep)">Something went wrong. Please try again.</p>
          )}
        </section>
      )}
    </main>
  );
}
