import { ReviewNoteSection } from "@/shared/types/review-note";

import { Pager } from "./Pager";
import { ReviewNoteSectionCard } from "./ReviewNoteSectionCard";

/** A revision note for the teacher, one section at a time, with Previous and Next. */
export function ReviewNotePager({
  sections,
  showBand = true,
  capped = false,
  section,
  onSectionChange,
}: {
  sections: ReviewNoteSection[];
  showBand?: boolean;
  capped?: boolean;
  /** The section shown, when the page keeps it; else the pager keeps its own. */
  section?: number;
  onSectionChange?: (index: number) => void;
}) {
  if (sections.length === 0) {
    return (
      <p className="text-sm text-(--muted)">
        This revision note has no sections yet.
      </p>
    );
  }
  return (
    <Pager
      count={sections.length}
      label="Section"
      index={section}
      onIndexChange={onSectionChange}
    >
      {(index) => (
        <ReviewNoteSectionCard
          section={sections[index]}
          index={index}
          showBand={showBand}
          capped={capped}
        />
      )}
    </Pager>
  );
}
