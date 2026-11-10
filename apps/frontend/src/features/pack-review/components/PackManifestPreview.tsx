import { ReviewNotePager } from "@/shared/components/renderer/ReviewNotePager";

import { PackManifest } from "../types";

/** Read-only render of a pack manifest: header + each section's learner-facing blocks. */
export function PackManifestPreview({
  manifest,
  section,
  onSectionChange,
}: {
  manifest: PackManifest;
  section?: number;
  onSectionChange?: (index: number) => void;
}) {
  const heading = manifest.subtopic || manifest.topic || "Revision note";
  const sectionCount = manifest.steps.length;
  const meta = [
    manifest.subject,
    manifest.grade,
    `${sectionCount} section${sectionCount === 1 ? "" : "s"}`,
  ]
    .filter(Boolean)
    .join(" · ");

  return (
    <div className="flex min-h-0 flex-1 flex-col gap-3">
      <div className="flex shrink-0 flex-wrap items-baseline gap-x-3">
        <h2 className="text-xl font-semibold text-(--ink)">{heading}</h2>
        <p className="text-xs text-(--muted)">{meta}</p>
      </div>

      <ReviewNotePager
        sections={manifest.steps}
        capped
        section={section}
        onSectionChange={onSectionChange}
      />
    </div>
  );
}
