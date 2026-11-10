import { Link } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import { useGenerateContent } from "@/features/content/hooks/useContent";

import type { ExperimentSummary } from "../lib/experiments";

/**
 * The step between the accepted plan and the class revision note: the teacher creates the
 * lesson note (what is taught in each step), then reads and accepts it on its review page.
 * The class revision note is grounded in the accepted note, so it waits for this.
 */
export function ExperimentLessonNoteGate({ experiment }: { experiment: ExperimentSummary }) {
  const readiness = experiment.readiness;
  const planVersionId = experiment.plan_version_id;
  const create = useGenerateContent(planVersionId, "lesson-note");
  const noteId = readiness.lesson_note_artefact_id;

  if (!planVersionId || !experiment.baseline_approved_by || readiness.lesson_note_approved) {
    return null;
  }

  if (!noteId) {
    return (
      <Card padding="lg" className="space-y-3 border border-(--warning-ink)/30 bg-(--warning-tint)/30">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--warning-ink)">
          Lesson note · ready to create
        </p>
        <p className="text-sm text-(--ink)">
          Create the note for each step of your accepted plan. You&apos;ll review and accept it
          next; the class revision note is built from it.
        </p>
        {create.isError ? (
          <p className="text-sm text-(--danger-ink)">Couldn&apos;t create it — please try again.</p>
        ) : null}
        <Button isLoading={create.isPending} onClick={() => create.create({})}>
          {create.isPending ? "Writing the lesson note…" : "Create the lesson note"}
        </Button>
      </Card>
    );
  }

  return (
    <Card padding="lg" className="space-y-3 border border-(--warning-ink)/30 bg-(--warning-tint)/30">
      <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--warning-ink)">
        Lesson note · awaiting you
      </p>
      <p className="text-sm text-(--ink)">
        Read the note for each step, refine it if you&apos;d like, and accept it when you&apos;re
        satisfied.
      </p>
      <Link
        href={`/research/teacher/content/${noteId}`}
        className="inline-flex h-9 items-center bg-(--accent) px-4 text-sm font-semibold text-white transition hover:bg-(--accent-bright)"
      >
        Review the lesson note →
      </Link>
    </Card>
  );
}
