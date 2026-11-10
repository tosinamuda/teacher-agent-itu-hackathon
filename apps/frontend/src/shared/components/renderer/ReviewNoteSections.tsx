import { ReviewNoteSection } from "@/shared/types/review-note";

import { ReviewNoteSectionCard } from "./ReviewNoteSectionCard";

/**
 * Read-only render of a revision note's sections, all at once (one card per
 * section). Used by the teacher review surface; the student reader pages through
 * the same cards one at a time. The personalisation band shows only when
 * `showBand` is set.
 */
export function ReviewNoteSections({
  sections,
  showBand = true,
  capped = false,
}: {
  sections: ReviewNoteSection[];
  showBand?: boolean;
  capped?: boolean;
}) {
  return (
    <div className="space-y-5">
      {sections.map((section, index) => (
        <ReviewNoteSectionCard
          key={section.step_id}
          section={section}
          index={index}
          showBand={showBand}
          capped={capped}
        />
      ))}
    </div>
  );
}
