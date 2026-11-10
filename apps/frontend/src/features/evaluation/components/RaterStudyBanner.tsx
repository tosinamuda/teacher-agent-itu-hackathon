import { EvaluationMeta } from "../types";

/**
 * Slim study-identity banner (institution + study title) shown atop the rater
 * workspace, so the digital experience matches the printed rater packs.
 */
export function RaterStudyBanner({ meta }: { meta?: EvaluationMeta }) {
  if (!meta) {
    return null;
  }

  return (
    <div className="border-b border-[color:var(--line)] pb-4">
      <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--ink)]">
        {meta.institution_name}
      </p>
      <p className="mt-1 text-sm leading-6 text-[color:var(--muted)]">{meta.study_title}</p>
    </div>
  );
}
