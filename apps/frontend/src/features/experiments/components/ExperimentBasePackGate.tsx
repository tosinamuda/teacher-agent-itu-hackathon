import { Link } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import { useCreateReviewNote, useFollowExecution } from "../hooks/useExperiments";
import type { ExperimentSummary } from "../lib/experiments";

/**
 * The teacher gate that follows plan acceptance: the teacher explicitly creates
 * the class revision note (which runs the background build), then reviews and
 * accepts it. Accepting unlocks the personalised student revision notes (this is
 * the "C4" teacher-validation gate, but no internal codes surface to the teacher).
 *
 * States: nothing until the plan and its lesson note are accepted; a "Create" action while no note
 * exists; a "preparing" note while the build runs; the review link once it's
 * ready; nothing once accepted (so the lesson advances).
 */
export function ExperimentBasePackGate({ experiment }: { experiment: ExperimentSummary }) {
  const readiness = experiment.readiness;
  const planFrozen = Boolean(experiment.plan_version_id && experiment.baseline_approved_by);
  const buildStarted = experiment.h1_summary.execution_count > 0;
  // A failed last attempt is NOT "preparing" — surface a re-run here. The
  // teacher's "Create the class revision note" is the only way to (re)start the H1
  // build, so a failed run must offer it again rather than spin forever.
  const buildFailed = /fail/i.test(experiment.h1_summary.latest_execution_status ?? "");
  const create = useCreateReviewNote(experiment.experiment_id);
  const building = buildStarted && !buildFailed && !readiness.base_pack_ready;
  useFollowExecution(
    experiment.experiment_id,
    building ? (experiment.h1_summary.latest_execution_id ?? null) : null,
  );

  // Relevant once the plan and its lesson note are accepted; nothing to do once it's accepted.
  if (!planFrozen || !readiness.lesson_note_approved || readiness.base_pack_approved) return null;

  // Not generated yet (or the last attempt failed) and nothing in flight → the
  // teacher's explicit create / re-create step.
  if (!readiness.base_pack_ready && (!buildStarted || buildFailed)) {
    return (
      <Card padding="lg" className="space-y-3 border border-(--warning-ink)/30 bg-(--warning-tint)/30">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--warning-ink)">
          Class revision note · {buildFailed ? "needs another try" : "ready to create"}
        </p>
        {buildFailed ? (
          <p className="text-sm text-(--ink)">
            The last attempt to build the class revision note didn&apos;t finish. Run it again to
            regenerate it from your accepted lesson.
          </p>
        ) : (
          <p className="text-sm text-(--ink)">
            Create the class revision note from your accepted plan and lesson note. You&apos;ll
            review and accept it next, before your students&apos; personalised notes are built
            from it.
          </p>
        )}
        {create.isError ? (
          <p className="text-sm text-(--danger-ink)">Couldn&apos;t start it — please try again.</p>
        ) : null}
        <Button isLoading={create.isPending} onClick={() => create.mutate()}>
          {buildFailed ? "Try again" : "Create the class revision note"}
        </Button>
      </Card>
    );
  }

  // Build running but the note isn't ready yet.
  if (!readiness.base_pack_ready || !readiness.base_pack_artefact_id) {
    return (
      <Card padding="lg" className="space-y-2 border border-(--line) bg-(--surface)">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--muted)">
          Class revision note · preparing
        </p>
        <p className="text-sm text-(--muted)">
          The revision note for your class is being prepared from your accepted lesson. It
          will appear here for your review when it is ready, in a minute or two.
        </p>
      </Card>
    );
  }

  const reviewHref = `/research/teacher/pack-reviews/${readiness.base_pack_artefact_id}`;

  return (
    <Card padding="lg" className="space-y-3 border border-(--warning-ink)/30 bg-(--warning-tint)/30">
      <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--warning-ink)">
        Class revision note · awaiting you
      </p>
      <p className="text-sm text-(--ink)">
        The revision note generated from your lesson is ready. Read it through, refine it
        if you&apos;d like, and accept it when you&apos;re satisfied — your students&apos;
        personalised revision notes are built from the note you accept.
      </p>
      <Link
        href={reviewHref}
        className="inline-flex h-9 items-center bg-(--accent) px-4 text-sm font-semibold text-white transition hover:bg-(--accent-bright)"
      >
        Review the revision note →
      </Link>
    </Card>
  );
}
