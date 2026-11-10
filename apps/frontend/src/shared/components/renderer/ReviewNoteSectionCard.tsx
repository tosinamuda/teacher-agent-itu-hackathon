import { ReactNode } from "react";

import { Badge } from "@/shared/components/ui/Badge";
import { ReviewNoteSection } from "@/shared/types/review-note";

import { ContentBlockRenderer } from "./ContentBlockRenderer";

/**
 * One review-note section as a card — "Section N", its title, and its
 * learner-facing content blocks spaced for reading. Shared by the all-at-once
 * teacher view and the paged student reader so they render identically.
 *
 * The personalisation band is per-section: the teacher view shows it as a raw
 * badge (`showBand`); the student view passes `bandInsight` to render a friendly
 * "based on your assessment" note for this section instead.
 *
 * ``capped`` limits the content's height so a long section scrolls in its card instead of
 * pushing the next one far down the page.
 */
export function ReviewNoteSectionCard({
  section,
  index,
  showBand = true,
  bandInsight,
  capped = false,
}: {
  section: ReviewNoteSection;
  index: number;
  showBand?: boolean;
  bandInsight?: ReactNode;
  /** Cap the section's height so a long one scrolls inside its card. */
  capped?: boolean;
}) {
  return (
    <article
      className={`rounded-2xl border border-(--line) bg-white ${capped ? "p-4 md:flex md:min-h-0 md:flex-1 md:flex-col" : "p-5"}`}
    >
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
            Section {index + 1}
          </p>
          <h3 className="text-lg font-semibold text-(--ink)">
            {section.title ?? "Untitled section"}
          </h3>
        </div>
        {showBand && section.personalisation_band ? (
          <Badge variant="accent">{section.personalisation_band}</Badge>
        ) : null}
      </div>

      {bandInsight ? <div className="mt-3">{bandInsight}</div> : null}

      {section.blocks.length > 0 ? (
        <div
          className={`mt-4 space-y-6 ${
            capped
              ? "relative max-h-[70dvh] overflow-y-auto overscroll-contain pr-2 md:max-h-none md:min-h-0 md:flex-1"
              : ""
          }`}
        >
          {section.blocks.map((block, blockIndex) => (
            <ContentBlockRenderer
              key={block.id ?? `${section.step_id}-${blockIndex}`}
              block={block}
            />
          ))}
        </div>
      ) : (
        <p className="mt-3 text-sm text-(--muted)">
          No content blocks in this section.
        </p>
      )}
    </article>
  );
}
