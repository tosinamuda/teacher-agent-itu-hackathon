import { SyntheticRatingsSummary } from "../lib/experiments";

const fmt = (value: number | null) => (value === null ? "—" : value.toFixed(2));

/**
 * The synthetic dry-run (proxy) ratings, rendered as a visually-demoted card: dashed
 * border + muted tone to signal it sits *off* the reported pipeline. Shows the proxy
 * mean and the per-condition breakdown (the dry-run grounding signal), explicitly
 * labelled as excluded from the reported expert findings.
 */
export function SyntheticProxyCard({ synthetic }: { synthetic: SyntheticRatingsSummary }) {
  const conditions = Object.entries(synthetic.by_condition);
  return (
    <div className="space-y-3 rounded-2xl border border-dashed border-(--accent)/50 bg-(--accent-soft)/20 p-4">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <span className="text-sm font-semibold text-(--accent-deep)">⟳ Synthetic rehearsal</span>
        <span className="text-xs text-(--muted)">proxy — excluded from results</span>
      </div>

      <div className="flex flex-wrap items-baseline gap-x-4 gap-y-1 text-sm">
        <span>
          Mean overall{" "}
          <span className="font-semibold text-(--ink)">{fmt(synthetic.mean_overall)}</span>
        </span>
        <span className="text-(--muted)">
          N={synthetic.rating_count} · {synthetic.distinct_raters} synthetic raters
        </span>
      </div>

      {conditions.length > 0 ? (
        <div className="flex flex-wrap gap-1.5">
          {conditions.map(([code, mean]) => (
            <span
              key={code}
              className="rounded-none border border-(--line) bg-(--surface) px-2.5 py-1 text-xs text-(--muted)"
            >
              <span className="font-semibold text-(--ink)">{code}</span> {fmt(mean)}
            </span>
          ))}
        </div>
      ) : null}

      <p className="text-xs italic text-(--muted)">
        A development dry run to pre-flight the pipeline. Not part of reported findings.
      </p>
    </div>
  );
}
