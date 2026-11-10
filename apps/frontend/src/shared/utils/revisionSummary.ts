const POINTER = String.raw`(?:step|section|objective|block|item|question)s?`;

/**
 * An id the app gives a step, section, objective or block ("intro01", "step:step02"), with
 * the words that point at it ("to the", "in section", "step") and any quotes around it. A
 * reviser's summary sometimes cites one; a teacher does not know them.
 */
const INTERNAL_ID = new RegExp(
  String.raw`(?:\b(?:in|at|for|to|of|on|from)\s+)?(?:\bthe\s+)?(?:\b${POINTER}\s+)?` +
    String.raw`[("'“‘\x60]*\b(?:[a-z]+:)?[a-z]{1,8}\d{2,}\b(?:'s|’s)?[)"'”’\x60]*` +
    String.raw`(?:\s+${POINTER}\b)?`,
  "g",
);

/**
 * A revision's summary as the teacher reads it: the change, without the app's internal ids.
 * Its line breaks stay, so markdown headings, lists and paragraphs still read as written.
 */
export function withoutInternalIds(summary: string): string {
  return summary
    .replace(INTERNAL_ID, "")
    .replace(/\*\*[ \t]*\*\*|__[ \t]*__/g, "")
    .replace(/^([ \t]*[-*][ \t]+)[—–][ \t]+/gm, "$1")
    .replace(/[ \t]+([,.;:!?])/g, "$1")
    .replace(/[ \t]{2,}/g, " ")
    .trim();
}
