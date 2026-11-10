import { Link } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";

import { DiagnosticItemList } from "../components/DiagnosticItemList";
import { DiagnosticRevisionChatPanel } from "../components/DiagnosticRevisionChatPanel";
import { useDiagnosticReview } from "../hooks/useDiagnosticReview";
import { useReviewedPlan } from "../hooks/useReviewedPlan";

/**
 * Teacher review screen for a lesson's MCQ diagnostic: see the items (with answer
 * keys + tagged distractors), generate them if the lesson has none, and refine
 * them through human-in-the-loop revision feedback before students take it.
 */
export default function DiagnosticReviewPage({ planVersionId }: { planVersionId: string }) {
  const {
    items,
    turns,
    isLoading,
    isError,
    submit,
    isSubmitting,
    submitFailed,
    canSubmit,
    generate,
    isGenerating,
    generateFailed,
  } = useDiagnosticReview(planVersionId);
  const lessonTitle = useReviewedPlan(planVersionId).data?.title;

  return (
    <main className="mx-auto w-full max-w-[68rem] p-6 md:p-8">
      <header className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div className="space-y-1">
          <p className="text-sm uppercase tracking-wide text-(--accent-deep)">Review assessment</p>
          <h1 className="text-2xl font-semibold text-(--ink)">Exit assessment (MCQ diagnostic)</h1>
          {lessonTitle ? <p className="text-sm text-(--muted)">Lesson: {lessonTitle}</p> : null}
        </div>
        <div className="flex items-center gap-3">
          {generateFailed ? (
            <span className="text-sm text-(--danger-ink)">Couldn&apos;t write the items — try again.</span>
          ) : null}
          <Link href="/research/teacher/lesson-preview">
            <Button variant="ghost">Back to lessons</Button>
          </Link>
          <Button
            variant="secondary"
            onClick={() => generate()}
            isLoading={isGenerating}
            disabled={!planVersionId}
          >
            {items.length > 0 ? "Regenerate items" : "Generate diagnostic"}
          </Button>
        </div>
      </header>

      {isError ? (
        <p className="mb-4 text-sm text-(--danger)">Couldn&apos;t load the diagnostic.</p>
      ) : null}

      <div className="grid gap-6 lg:grid-cols-[1fr_22rem]">
        <section>
          {isLoading ? (
            <p className="text-sm text-(--muted)">Loading diagnostic…</p>
          ) : (
            <DiagnosticItemList items={items} planVersionId={planVersionId} />
          )}
        </section>
        <div className="lg:sticky lg:top-6 lg:self-start">
          <DiagnosticRevisionChatPanel
            turns={turns}
            onSubmit={(instruction, onSent) => submit({ instruction }, { onSuccess: onSent })}
            isSubmitting={isSubmitting}
            hasError={submitFailed}
            canSubmit={canSubmit && items.length > 0}
          />
        </div>
      </div>
    </main>
  );
}
