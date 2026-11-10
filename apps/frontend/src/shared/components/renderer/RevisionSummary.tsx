import { withoutInternalIds } from "@/shared/utils/revisionSummary";

import { RichText } from "./RichText";

const BLOCKS =
  "prose prose-sm max-w-none prose-headings:mb-1 prose-headings:mt-3 prose-headings:text-sm prose-headings:font-semibold";

/**
 * What a revision changed, as markdown with its maths drawn, and no internal ids. A one-line
 * summary runs inline; with `blocks`, paragraphs, headings and lists keep their shape, as a
 * longer message needs.
 */
export function RevisionSummary({
  text,
  className = "",
  blocks = false,
}: {
  text: string;
  className?: string;
  blocks?: boolean;
}) {
  return (
    <div
      className={`${blocks ? BLOCKS : "prose max-w-none [&_p]:inline"} ${className}`}
    >
      <RichText
        text={withoutInternalIds(text)}
        breaks={false}
        tables={blocks}
      />
    </div>
  );
}
