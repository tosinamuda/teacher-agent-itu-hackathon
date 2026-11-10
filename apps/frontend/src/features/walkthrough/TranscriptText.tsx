import { RichText } from "@/shared/components/renderer/RichText";

/** A published transcript's markdown: hard-wrapped, so its newlines are not line breaks. */
export function TranscriptText({ text, muted = false }: { text: string; muted?: boolean }) {
  return (
    <div className={`prose max-w-none text-sm ${muted ? "text-(--ink-2)" : "text-(--ink)"}`}>
      <RichText text={text} tables breaks={false} />
    </div>
  );
}
