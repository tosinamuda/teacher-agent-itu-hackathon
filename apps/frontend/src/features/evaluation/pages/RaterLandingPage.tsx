import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";

import { RaterStudyBanner } from "../components/RaterStudyBanner";
import { RaterWorkItem, RaterWorkQueueTable } from "../components/RaterWorkQueueTable";
import { useAuditQueue, useEvaluationMeta, useEvaluationQueue } from "../hooks/useEvaluation";
import { useRaterSession } from "../hooks/useRaterSession";

/**
 * Renders the rater's home: ONE flat queue of everything assigned to them, as a
 * table with a plain-language task type per row. No hypothesis ids or condition
 * codes appear anywhere — the task labels describe the work without unblinding.
 */
export function RaterLandingPage() {
  const { session, isHydrated } = useRaterSession();
  const meta = useEvaluationMeta();
  const h1Queue = useEvaluationQueue("H1", session?.rater_id);
  const h2Queue = useEvaluationQueue("H2", session?.rater_id);
  const auditQueue = useAuditQueue(session?.rater_id);

  const items: RaterWorkItem[] = [
    ...(h1Queue.data ?? []).map((packet) => ({
      id: packet.evaluation_packet_id,
      // H1 packets are anonymous candidates within a lesson block.
      code: packet.candidate_label
        ? `${packet.candidate_label} · ${packet.packet_code}`
        : packet.packet_code,
      type: "Revision note review",
      done: Boolean(packet.rating),
      href: `/research/rater/h1/${packet.evaluation_packet_id}`,
    })),
    ...(h2Queue.data ?? []).map((packet) => ({
      id: packet.evaluation_packet_id,
      code: packet.packet_code,
      type: "Learner comparison",
      done: Boolean(packet.rating),
      href: `/research/rater/h2/${packet.evaluation_packet_id}`,
    })),
    ...(auditQueue.data ?? []).map((item) => ({
      id: item.audit_item_id,
      code: item.objective_text ?? item.source_ref ?? item.audit_item_id,
      type: "Source check",
      done: item.rated,
      href: `/research/rater/audit/${item.audit_item_id}`,
    })),
  ];
  const nextItem = items.find((item) => !item.done);
  const doneCount = items.filter((item) => item.done).length;

  return (
    <main className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-8 sm:px-6 sm:py-10">
      <RaterStudyBanner meta={meta.data} />

      <header className="max-w-3xl space-y-3">
        <h1 className="text-4xl font-semibold tracking-tight text-[color:var(--ink)]">
          Review revision notes
        </h1>
        <p className="text-base leading-relaxed text-[color:var(--muted)]">
          Everything assigned to you, in one queue. Each item takes about 5–10 minutes to
          review, and your ratings stay anonymous.
        </p>
      </header>

      {!isHydrated ? (
        <p className="text-sm text-[color:var(--muted)]">Loading your queue…</p>
      ) : !session ? (
        <p className="text-sm text-[color:var(--muted)]">
          You need a rater access code to review revision notes.
        </p>
      ) : (
        <Card padding="lg" className="space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
                Your queue
              </p>
              <h2 className="text-lg font-semibold text-[color:var(--ink)]">
                {doneCount} of {items.length} item{items.length === 1 ? "" : "s"} completed
              </h2>
            </div>
            {nextItem ? (
              <Link
                className="inline-flex items-center rounded-none bg-[color:var(--accent)] px-4 py-2 text-sm font-semibold text-white transition hover:opacity-90"
                href={nextItem.href}
              >
                Continue next item →
              </Link>
            ) : null}
          </div>
          <RaterWorkQueueTable items={items} />
        </Card>
      )}
    </main>
  );
}
