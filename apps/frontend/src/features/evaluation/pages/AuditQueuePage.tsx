import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";

import { SourceAuditQueueItem } from "../types";
import { useAuditQueue } from "../hooks/useEvaluation";
import { useRaterSession } from "../hooks/useRaterSession";

/** One grouped section of audit items (e.g. "To score" or "Completed"). */
function AuditItemGroup({ items, label }: { items: SourceAuditQueueItem[]; label: string }) {
  if (items.length === 0) {
    return null;
  }
  return (
    <section className="space-y-2">
      <h3 className="text-sm font-semibold text-[color:var(--ink)]">
        {label} ({items.length})
      </h3>
      <ul className="divide-y divide-[color:var(--line)]">
        {items.map((item) => (
          <li key={item.audit_item_id}>
            <Link
              className="flex items-center justify-between gap-3 py-3 transition hover:text-[color:var(--accent-deep)]"
              href={`/research/rater/audit/${item.audit_item_id}`}
            >
              <span className="min-w-0 text-sm text-[color:var(--ink)]">
                <span className="font-semibold">{item.objective_text ?? "Objective —"}</span>
                {" · cited "}
                {item.source_ref ?? "—"}
              </span>
              <span
                className={`shrink-0 rounded-none px-2.5 py-1 text-xs font-semibold ${
                  item.rated
                    ? "bg-[color:var(--accent-soft)] text-[color:var(--accent-deep)]"
                    : "bg-[color:var(--panel)] text-[color:var(--muted)]"
                }`}
              >
                {item.rated ? "Scored" : "Needs score"}
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

/** Source-grounding audit queue: items to score, split from already-scored ones. */
export function AuditQueuePage() {
  const { session, isHydrated } = useRaterSession();
  const queueQuery = useAuditQueue(session?.rater_id);
  const items = queueQuery.data ?? [];
  const toScore = items.filter((item) => !item.rated);
  const completed = items.filter((item) => item.rated);
  const pending = toScore.length;

  return (
    <main className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-4 py-8 sm:px-6 sm:py-10">
      <header className="max-w-3xl space-y-3">
        <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--accent)]">
          Source-grounding audit
        </div>
        <h1 className="text-4xl font-semibold tracking-tight text-[color:var(--ink)]">
          Source-grounding audit queue
        </h1>
        <p className="text-base leading-relaxed text-[color:var(--muted)]">
          Check whether each cited textbook source actually supports the generated excerpt. This is
          a separate evidence layer from the revision-note quality ratings.
        </p>
      </header>

      {!isHydrated ? (
        <p className="text-sm text-[color:var(--muted)]">Loading your queue…</p>
      ) : !session ? (
        <p className="text-sm text-[color:var(--muted)]">
          You need a rater access code to view this queue.
        </p>
      ) : (
        <Card padding="lg" className="space-y-4">
          <p className="text-sm text-[color:var(--muted)]">
            {pending} of {items.length} audit items still need a score.
          </p>
          {items.length === 0 ? (
            <p className="text-sm text-[color:var(--muted)]">
              No audit items yet. They appear once an experiment has been run and the audit pack
              has been built.
            </p>
          ) : (
            <div className="space-y-6">
              <AuditItemGroup items={toScore} label="To score" />
              <AuditItemGroup items={completed} label="Completed" />
            </div>
          )}
        </Card>
      )}
    </main>
  );
}
