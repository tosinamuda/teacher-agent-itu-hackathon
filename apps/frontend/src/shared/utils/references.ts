export type ParsedReference = { label: string; recordId: string | null };

/** A record id leads a reference as `ch09-b027: ` or `ch09-b030-i01: `. */
const LEADING_ID = /^([a-z]{2,}\d+-[\w-]+):\s+(.*)$/i;

/**
 * Splits a reference into its human label and the textbook record id (if present). Two forms
 * are read: "Chapter 2: Highest common factor (ch02-b005)", and the engine's
 * "ch02-b005: Chapter 2: Highest common factor (exposition)", where the trailing bracket
 * names the kind of passage and is dropped.
 */
export function parseReference(ref: string): ParsedReference {
  const leading = ref.match(LEADING_ID);
  if (leading) {
    return { label: leading[2].replace(/\s*\([^()]*\)\s*$/, "").trim(), recordId: leading[1] };
  }
  const match = ref.match(/^(.*?)\s*\(([^()]+)\)\s*$/);
  if (match) return { label: match[1].trim(), recordId: match[2].trim() };
  return { label: ref.trim(), recordId: null };
}

/**
 * Collapses a flat reference list to unique chapter-level labels — dropping the many
 * per-chunk record ids (ch02-b001, b002, …) that otherwise blow up the references list.
 */
export function dedupeReferenceLabels(refs: string[]): string[] {
  const seen = new Set<string>();
  const labels: string[] = [];
  for (const ref of refs) {
    const { label } = parseReference(ref);
    if (label && !seen.has(label)) {
      seen.add(label);
      labels.push(label);
    }
  }
  return labels;
}

/** A chapter and the individual source records cited from it. */
export type ReferenceGroup = {
  label: string;
  records: { recordId: string; raw: string }[];
};

/**
 * Groups a flat reference list by chapter label, collecting each chapter's source
 * record ids — so the UI can show one collapsible entry per chapter, expandable to
 * its individual (clickable) source chunks.
 */
export function groupReferencesByChapter(refs: string[]): ReferenceGroup[] {
  const groups = new Map<string, ReferenceGroup>();
  for (const ref of refs) {
    const { label, recordId } = parseReference(ref);
    const key = label || ref;
    const group = groups.get(key) ?? { label: key, records: [] };
    if (recordId && !group.records.some((r) => r.recordId === recordId)) {
      group.records.push({ recordId, raw: ref });
    }
    groups.set(key, group);
  }
  return [...groups.values()];
}
