import { VisualBlock as VisualBlockType } from "@/shared/types/lesson-schema";
import { localFigureSrc } from "@/shared/utils/figure-url";
import { stripSourceCitations } from "@/shared/utils/strip-source-citations";

import { RichText } from "./RichText";
import { TikzFigure } from "./TikzFigure";

export function VisualBlock({ block }: { block: VisualBlockType }) {
  return (
    <div className="my-6 flex flex-col items-center justify-center rounded-lg border border-[color:var(--line)] bg-[color:var(--surface-sunken)] p-6">
      {block.variant === "image" && block.url ? (
        <img
          src={localFigureSrc(block.url)}
          alt={block.caption || "Lesson visual"}
          className="max-h-64 rounded"
          onError={(event) => {
            // Local cache miss → fall back to the original remote URL (guarded against loop).
            const image = event.currentTarget;
            if (block.url && image.src !== block.url) image.src = block.url;
          }}
        />
      ) : block.variant === "diagram_tikz" && block.source_tikz ? (
        <TikzFigure source={block.source_tikz} caption={block.caption} />
      ) : block.variant === "image" ? (
        <div className="flex h-32 w-full items-center justify-center rounded bg-(--sunken) text-(--faint)">
          No image available
        </div>
      ) : null}
      {/* TODO: Implement Clock/NumberLine diagrams */}
      <div className="mt-2 text-sm text-[color:var(--muted)] italic prose prose-sm max-w-none">
        <RichText text={block.caption || ""} prepare={stripSourceCitations} />
      </div>
    </div>
  );
}
