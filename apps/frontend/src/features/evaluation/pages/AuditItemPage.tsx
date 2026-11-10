import { Link } from "@/shared/router";
import { useRouter } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";
import { localFigureSrc } from "@/shared/utils/figure-url";

import { AuditMarkdown } from "../components/AuditMarkdown";
import { AuditRatingForm } from "../components/AuditRatingForm";
import { useAuditItem, useAuditQueue, useSaveAuditRating } from "../hooks/useEvaluation";
import { useRaterSession } from "../hooks/useRaterSession";

/** Source-grounding audit workspace for one audit item (excerpt vs cited source). */
export function AuditItemPage({ auditItemId }: { auditItemId: string }) {
  const router = useRouter();
  const { session, isHydrated } = useRaterSession();
  const itemQuery = useAuditItem(auditItemId, session?.rater_id);
  const queueQuery = useAuditQueue(session?.rater_id);
  const saveMutation = useSaveAuditRating(auditItemId, session?.rater_id);
  const detail = itemQuery.data;

  // After scoring, advance to the next unrated audit item (or back to the queue
  // when none remain) — matching the H1/H2 "save and open next" flow.
  const nextItem = (queueQuery.data ?? []).find(
    (item) => item.audit_item_id !== auditItemId && !item.rated,
  );
  const goToNext = () => {
    router.push(
      nextItem ? `/research/rater/audit/${nextItem.audit_item_id}` : "/research/rater/audit",
    );
  };

  return (
    <main className="mx-auto flex w-full max-w-5xl flex-col gap-5 px-4 py-6 sm:px-6 sm:py-8">
      <div className="flex items-center justify-between">
        <Link
          className="text-sm font-semibold text-[color:var(--accent-deep)] hover:underline"
          href="/research/rater/audit"
        >
          ← Audit queue
        </Link>
      </div>

      {!isHydrated ? (
        <p className="text-sm text-[color:var(--muted)]">Restoring rater workspace…</p>
      ) : !session ? (
        <p className="text-sm text-[color:var(--muted)]">
          Open the <Link className="underline" href="/research/rater/audit">audit queue</Link> to sign in first.
        </p>
      ) : itemQuery.isLoading || !detail ? (
        <p className="text-sm text-[color:var(--muted)]">Loading audit item…</p>
      ) : (
        <div className="space-y-4">
          <Card padding="lg" className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
              Lesson objective
            </p>
            <p className="text-sm text-[color:var(--ink)]">
              {detail.objective_text ?? detail.lesson_objective_id ?? "—"}
            </p>
            {detail.scope_boundary ? (
              <p className="text-xs text-[color:var(--faint)]">Scope: {detail.scope_boundary}</p>
            ) : null}
          </Card>

          <div className="grid gap-4 lg:grid-cols-2">
            <Card padding="lg" className="space-y-2">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
                Generated excerpt
              </p>
              <AuditMarkdown text={detail.generated_excerpt ?? ""} tone="ink" />
            </Card>
            <Card padding="lg" className="space-y-2">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
                Cited source {detail.source_record_id ? `(${detail.source_record_id})` : ""}
              </p>
              <AuditMarkdown
                text={
                  detail.source_excerpt ?? "Source snippet unavailable — consult the textbook."
                }
                tone="muted"
              />
              {detail.figure_url ? (
                <figure className="mt-2 flex flex-col items-center rounded-md border border-[color:var(--line)] bg-[color:var(--surface-sunken)] p-3">
                  <img
                    src={localFigureSrc(detail.figure_url)}
                    alt={detail.figure_caption ?? "Cited textbook figure"}
                    className="max-h-64 rounded"
                    onError={(event) => {
                      // Local cache miss → fall back to the original remote URL
                      // (guarded against an infinite loop if the original is the
                      // same as the cache-rewritten src).
                      const image = event.currentTarget;
                      if (detail.figure_url && image.src !== detail.figure_url) {
                        image.src = detail.figure_url;
                      }
                    }}
                  />
                  {detail.figure_caption ? (
                    <figcaption className="mt-2 text-xs italic text-[color:var(--muted)]">
                      {detail.figure_caption}
                    </figcaption>
                  ) : null}
                </figure>
              ) : null}
            </Card>
          </div>

          <Card padding="lg" className="space-y-3">
            <h2 className="text-lg font-semibold text-[color:var(--ink)]">Source-grounding score</h2>
            <p className="text-xs text-[color:var(--muted)]">
              0 = fail · 1 = partial/unclear · 2 = pass. Judge the source against the excerpt only.
            </p>
            <AuditRatingForm
              detail={detail}
              isSaving={saveMutation.isPending}
              onSubmit={(payload) =>
                saveMutation.mutateAsync(payload).then(() => {
                  goToNext();
                })
              }
            />
          </Card>
        </div>
      )}
    </main>
  );
}
