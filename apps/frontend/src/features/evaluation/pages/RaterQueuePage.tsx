import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";

import { RaterQueueTable } from "../components/RaterQueueTable";
import { useEvaluationQueue } from "../hooks/useEvaluation";
import { useRaterSession } from "../hooks/useRaterSession";
import { EvaluationHypothesis } from "../types";

type RaterQueuePageProps = {
  hypothesis: EvaluationHypothesis;
};

/** Renders one rater queue at a time so H1 and H2 stay operationally separate. */
export function RaterQueuePage({ hypothesis }: RaterQueuePageProps) {
  const { session, isHydrated } = useRaterSession();
  const queueQuery = useEvaluationQueue(hypothesis, session?.rater_id);
  const nextPacket = queueQuery.data?.find((packet) => !packet.rating);

  return (
    <main className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-8 sm:px-6 sm:py-10">
      <header className="max-w-3xl space-y-3">
        <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--accent)]">
          {hypothesis === "H1" ? "Revision-note queue" : "Comparison queue"}
        </div>
        <h1 className="text-4xl font-semibold tracking-tight text-[color:var(--ink)]">
          {hypothesis === "H1" ? "Revision-note reviews" : "Learner comparisons"}
        </h1>
      </header>

      {!isHydrated ? (
        <p className="text-sm text-[color:var(--muted)]">Loading your queue…</p>
      ) : !session ? (
        <p className="text-sm text-[color:var(--muted)]">
          You need a rater access code to view this queue.
        </p>
      ) : (
        <Card padding="lg" className="space-y-4">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
                Queue
              </p>
              <h2 className="text-lg font-semibold text-[color:var(--ink)]">
                {queueQuery.data?.length ?? 0} revision notes available
              </h2>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              {nextPacket ? (
                <Link
                  className="inline-flex items-center rounded-none bg-[color:var(--accent)] px-4 py-2 text-sm font-semibold text-white transition hover:opacity-90"
                  href={`/research/rater/${hypothesis.toLowerCase()}/${nextPacket.evaluation_packet_id}`}
                >
                  Continue next revision note
                </Link>
              ) : null}
              <Link
                className="text-sm font-semibold text-[color:var(--accent-deep)] hover:underline"
                href="/research/rater"
              >
                Back to rater home
              </Link>
            </div>
          </div>
          <RaterQueueTable hypothesis={hypothesis} packets={queueQuery.data ?? []} />
        </Card>
      )}
    </main>
  );
}
