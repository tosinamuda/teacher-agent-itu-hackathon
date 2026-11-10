import { ReactNode, useState } from "react";

import { Button } from "@/shared/components/ui/Button";
import { ReviewNoteSection } from "@/shared/types/review-note";

import { ReviewNoteSectionCard } from "./ReviewNoteSectionCard";

/**
 * Paged reader for a revision note: shows one section card at a time with
 * Previous / Next, a "Section X of Y" indicator and progress dots — the slider
 * the old pack runner had, over the shared section card. The last section's
 * forward button reads "Done" and calls `onDone` (e.g. back to the lesson).
 *
 * `renderBandInsight` lets the caller render a per-section "based on your
 * assessment" note from that section's band (student reader).
 */
export function ReviewNoteReader({
  sections,
  showBand = false,
  onDone,
  renderBandInsight,
}: {
  sections: ReviewNoteSection[];
  showBand?: boolean;
  onDone?: () => void;
  renderBandInsight?: (band: string) => ReactNode;
}) {
  const [index, setIndex] = useState(0);
  const total = sections.length;
  const section = sections[index];
  const isLast = index >= total - 1;

  if (!section) {
    return (
      <p className="text-sm text-(--muted)">
        This revision note has no sections yet.
      </p>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <span className="text-xs font-semibold text-(--muted)">
          Section {index + 1} of {total}
        </span>
        <div className="flex flex-wrap gap-1.5" aria-hidden>
          {sections.map((dot, dotIndex) => (
            <span
              key={dot.step_id}
              className={`h-2.5 w-2.5 rounded-full ${
                dotIndex === index
                  ? "bg-(--accent)"
                  : dotIndex < index
                    ? "bg-(--accent)/40"
                    : "bg-(--line)"
              }`}
            />
          ))}
        </div>
      </div>

      <ReviewNoteSectionCard
        section={section}
        index={index}
        showBand={showBand}
        bandInsight={
          renderBandInsight && section.personalisation_band
            ? renderBandInsight(section.personalisation_band)
            : undefined
        }
      />

      <div className="flex items-center justify-between gap-3">
        <Button
          variant="outline"
          onClick={() => setIndex((prev) => Math.max(prev - 1, 0))}
          disabled={index === 0}
        >
          Previous
        </Button>
        {isLast ? (
          <Button variant="primary" onClick={onDone} disabled={!onDone}>
            Done
          </Button>
        ) : (
          <Button
            variant="primary"
            onClick={() => setIndex((prev) => Math.min(prev + 1, total - 1))}
          >
            Next
          </Button>
        )}
      </div>
    </div>
  );
}
