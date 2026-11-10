import {
  ExperimentStatistics as ExperimentStatisticsData,
  GroupStat,
  StatContrast,
} from "../lib/experiments";

const fmt = (value: number | null | undefined, digits = 2) =>
  value === null || value === undefined ? "—" : value.toFixed(digits);

/** A row of per-condition n / mean ± SD. */
function ConditionRow({ code, stat }: { code: string; stat: GroupStat }) {
  return (
    <div className="flex items-center justify-between gap-2 py-1 text-sm">
      <span className="font-medium text-(--ink)">{code}</span>
      <span className="text-(--muted)">
        mean <span className="font-semibold text-(--ink)">{fmt(stat.mean)}</span>
        {stat.std !== null ? ` ± ${fmt(stat.std)}` : ""} · n={stat.n}
      </span>
    </div>
  );
}

/** The mean-diff / significance / effect-size line for a two-group contrast. */
function ContrastLine({ label, contrast }: { label: string; contrast: StatContrast | null }) {
  if (!contrast) {
    return <p className="text-xs italic text-(--muted)">{label}: not enough data.</p>;
  }
  return (
    <p className="text-xs text-(--muted)">
      {label}: Δ <span className="font-semibold text-(--ink)">{fmt(contrast.mean_diff)}</span> · p{" "}
      {fmt(contrast.mann_whitney_p)} · Cliff&apos;s δ {fmt(contrast.cliffs_delta)} · d{" "}
      {fmt(contrast.cohens_d)}
    </p>
  );
}

/**
 * Renders the H1/H2 statistical analysis for a study: per-condition means, the
 * grounding (C0→C3) and personalisation (P0→P1) contrasts with significance + effect
 * sizes, and inter-rater reliability (Krippendorff's alpha). Underpowered on pilot data.
 */
export function ExperimentStatistics({
  statistics,
  isLoading,
}: {
  statistics: ExperimentStatisticsData | undefined;
  isLoading: boolean;
}) {
  if (isLoading) return <p className="text-sm text-(--muted)">Computing statistics…</p>;
  if (!statistics) return null;

  const { h1, h2, inter_rater, notes } = statistics;

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="rounded-2xl border border-(--line) bg-(--surface) p-4">
        <h3 className="text-sm font-semibold text-(--ink)">H1 · Curriculum grounding (C0→C3)</h3>
        <div className="mt-2 divide-y divide-(--line)">
          {Object.keys(h1.conditions).map((code) => (
            <ConditionRow key={code} code={code} stat={h1.conditions[code] ?? { n: 0, mean: null, std: null }} />
          ))}
        </div>
        <div className="mt-2 space-y-1 border-t border-(--line) pt-2">
          <p className="text-xs text-(--muted)">Omnibus p: {fmt(h1.kruskal_p)}</p>
          <ContrastLine label="Strongest vs C0" contrast={h1.c0_vs_strongest} />
        </div>
      </div>

      <div className="rounded-2xl border border-(--line) bg-(--surface) p-4">
        <h3 className="text-sm font-semibold text-(--ink)">H2 · Personalisation (P0→P1)</h3>
        <p className="mt-0.5 text-xs text-(--muted)">
          Paired: each rater scored the base (P0) and personalised (P1) pack for the same learner.
        </p>
        <div className="mt-2 divide-y divide-(--line)">
          <ConditionRow code="P0 · base/class" stat={h2.paired_p0_p1.p0} />
          <ConditionRow code="P1 · personalised" stat={h2.paired_p0_p1.p1} />
        </div>
        <div className="mt-2 space-y-1 border-t border-(--line) pt-2">
          {h2.paired_p0_p1.n_pairs > 0 ? (
            <p className="text-xs text-(--muted)">
              P1 vs P0 (paired): Δ{" "}
              <span className="font-semibold text-(--ink)">{fmt(h2.paired_p0_p1.mean_diff)}</span> ·
              Wilcoxon p {fmt(h2.paired_p0_p1.wilcoxon_p)} · Cliff&apos;s δ{" "}
              {fmt(h2.paired_p0_p1.cliffs_delta)} · {h2.paired_p0_p1.n_pairs} paired ratings
            </p>
          ) : (
            <p className="text-xs italic text-(--muted)">
              P1 vs P0 (paired): no ratings yet that scored both packs.
            </p>
          )}
        </div>
      </div>

      <div className="rounded-2xl border border-(--line) bg-(--surface) p-4 md:col-span-2">
        <h3 className="text-sm font-semibold text-(--ink)">Inter-rater reliability</h3>
        <p className="mt-1 text-sm text-(--muted)">
          Krippendorff&apos;s α (ordinal):{" "}
          <span className="font-semibold text-(--ink)">{fmt(inter_rater.krippendorff_alpha)}</span> ·{" "}
          {inter_rater.n_raters} raters · {inter_rater.n_items} items
        </p>
        {notes.length > 0 ? (
          <ul className="mt-2 space-y-0.5">
            {notes.map((note) => (
              <li key={note} className="text-xs italic text-(--muted)">
                • {note}
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    </div>
  );
}
