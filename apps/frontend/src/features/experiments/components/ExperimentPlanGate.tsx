import { Link } from "@/shared/router";
import { useRouter } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import { useAuthorExperimentPlan, useFreezeExperimentPlan } from "../hooks/useExperiments";

type ExperimentPlanGateProps = {
  experimentId: string;
  /** Null until the teacher authors the experiment's own plan. */
  planVersionId: string | null | undefined;
  /** Set once the plan is frozen (approved) — the freeze that triggers C0–C3. */
  baselineApprovedBy: string | null | undefined;
  /** When true (teacher queue), authoring auto-navigates into the review page so
   *  the teacher can read the draft before freezing. The lab surface uses this
   *  gate without that side-effect — the lab stays in place after authoring. */
  navigateToReviewOnAuthor?: boolean;
};

const errorMessage = (error: unknown): string =>
  error instanceof Error ? error.message : "Something went wrong.";

/**
 * The teacher gate that precedes generation: the assigned teacher authors the
 * experiment's OWN plan (separate from production), then reviews + freezes it
 * — exactly the production authoring + approval, scoped to this experiment.
 *
 * Authoring + freezing used to live as two inline buttons on the same card,
 * with no chance to see the draft in between (the user-flagged Phase A gap).
 * The freeze action now only lives on the dedicated review page; this gate
 * surfaces a "Review the draft" link in the authored state.
 *
 * Once frozen this renders nothing and the generation flow takes over. The
 * author/freeze endpoints are gated server-side to a teacher who owns the
 * class (a manager bypasses).
 */
export function ExperimentPlanGate({
  experimentId,
  planVersionId,
  baselineApprovedBy,
  navigateToReviewOnAuthor = false,
}: ExperimentPlanGateProps) {
  const router = useRouter();
  // Freeze stays available for surfaces that don't go through the review page
  // (e.g. the hypothesis lab). The teacher queue passes navigateToReviewOnAuthor
  // and uses the review-page Freeze button instead.
  const freeze = useFreezeExperimentPlan(experimentId);
  const author = useAuthorExperimentPlan(experimentId);

  // Plan frozen → generation owns the surface from here.
  if (planVersionId && baselineApprovedBy) return null;

  const reviewHref = `/research/teacher/experiment-plans/${experimentId}/plan`;

  const handleAuthor = async () => {
    await author.mutateAsync();
    if (navigateToReviewOnAuthor) router.push(reviewHref);
  };

  if (!planVersionId) {
    return (
      <Card padding="lg" className="space-y-3 border border-(--warning-ink)/30 bg-(--warning-tint)/30">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--warning-ink)">
          Lesson plan · awaiting you
        </p>
        <p className="text-sm text-(--ink)">
          This lesson has no plan yet. Author the plan with AI, or enter a
          teacher-authored plan by hand — then read it through and accept it.
        </p>
        {author.isError ? (
          <p className="text-sm text-(--danger-ink)">{errorMessage(author.error)}</p>
        ) : null}
        <div className="flex items-center gap-4">
          <Button isLoading={author.isPending} onClick={() => void handleAuthor()}>
            Author the plan
          </Button>
          <Link
            href={`/research/teacher/experiment-plans/${experimentId}/manual`}
            className="text-sm font-semibold text-(--accent-deep) hover:underline"
          >
            or enter it manually →
          </Link>
          <Link
            href={`/research/teacher/experiment-plans/${experimentId}/reuse`}
            className="text-sm font-semibold text-(--accent-deep) hover:underline"
          >
            or reuse an existing plan →
          </Link>
        </div>
      </Card>
    );
  }

  if (navigateToReviewOnAuthor) {
    return (
      <Card padding="lg" className="space-y-3 border border-(--accent)/40 bg-(--accent-soft)/40">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
          Lesson plan · draft
        </p>
        <p className="text-sm text-(--ink)">
          The plan is drafted. Read it through and accept it when you&apos;re satisfied.
        </p>
        <Link
          href={reviewHref}
          className="inline-flex h-9 items-center bg-(--accent) px-4 text-sm font-semibold text-white transition hover:bg-(--accent-bright)"
        >
          Review the draft →
        </Link>
      </Card>
    );
  }

  return (
    <Card padding="lg" className="space-y-3 border border-(--accent)/40 bg-(--accent-soft)/40">
      <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
        Lesson plan · draft
      </p>
      <p className="text-sm text-(--ink)">
        The plan is drafted. <span className="font-semibold">Accept it</span> when
        you&apos;re satisfied to lock it in.
      </p>
      {freeze.isError ? (
        <p className="text-sm text-(--danger-ink)">{errorMessage(freeze.error)}</p>
      ) : null}
      <Button isLoading={freeze.isPending} onClick={() => freeze.mutate(null)}>
        Accept the plan
      </Button>
    </Card>
  );
}
