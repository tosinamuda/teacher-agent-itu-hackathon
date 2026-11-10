import { RichText } from "@/shared/components/renderer/RichText";

/**
 * Render a plain string of LLM-authored markdown for the audit pack online.
 *
 * Pairs with the audit pack PDF renderer — both surfaces convert
 * ``**bold**``, lists, and ``$math$`` so the rater sees the same shaped text
 * online and on paper. Used for the generated excerpt + the cited source
 * snippet on the audit item page.
 *
 * Source citations are kept — this is the source-grounding surface, so raters need
 * to see the `REF-N` markers.
 */
export function AuditMarkdown({
  text,
  tone = "ink",
}: {
  text: string;
  tone?: "ink" | "muted";
}) {
  const color = tone === "muted" ? "var(--muted)" : "var(--ink)";
  return (
    <div
      className="prose prose-sm max-w-none leading-6"
      style={{ color: `color-mix(in srgb, ${color} 100%, transparent)` }}
    >
      <RichText text={text} tables />
    </div>
  );
}
