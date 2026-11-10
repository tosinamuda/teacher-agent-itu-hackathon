import { BAND_INSIGHT, ReviewBand } from "../services/reviewNoteBand";

/**
 * Compact per-section "based on your assessment" note: explains how this section
 * was pitched to the student's band (extend / reinforce / remediate). Rendered
 * inside each section of the student reader; never shown in the teacher view.
 */
export function ReviewNoteInsight({ band }: { band: ReviewBand }) {
  const insight = BAND_INSIGHT[band];
  return (
    <div className="rounded-xl border-l-4 border-(--accent) bg-(--accent-soft) px-4 py-2.5">
      <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-(--accent-deep)">
        Based on your assessment
      </p>
      <p className="mt-0.5 text-sm text-(--ink-2)">
        <span className="font-semibold text-(--ink)">{insight.title}.</span> {insight.body}
      </p>
    </div>
  );
}
