import { ExplanationBlock as ExplanationBlockType } from "@/shared/types/lesson-schema";
import { stripSourceCitations } from "@/shared/utils/strip-source-citations";

import { RichText } from "./RichText";

/**
 * Render an `ExplanationBlock`'s markdown content as HTML.
 *
 * Strips textbook source citations by default — H1/H2 raters judge
 * fit-to-objective, not source grounding (the audit pack covers that). Pass
 * `keepSourceCitations` when the consumer is the source-grounding audit
 * surface and needs the citations preserved.
 */
export function ExplanationBlock({
  block,
  keepSourceCitations = false,
}: {
  block: ExplanationBlockType;
  keepSourceCitations?: boolean;
}) {
  return (
    <div className="prose prose-slate max-w-none text-[color:var(--ink)]">
      <RichText
        text={block.content}
        prepare={keepSourceCitations ? undefined : stripSourceCitations}
        tables
      />
    </div>
  );
}
