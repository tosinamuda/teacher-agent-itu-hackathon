import { RichText } from "@/shared/components/renderer/RichText";

/** A run of note text: markdown with $LaTeX$ maths, and the teacher's drawings drawn. */
export function NoteText({ text }: { text: string }) {
  return (
    <div className="prose prose-slate max-w-none text-sm text-(--ink)">
      <RichText text={text} tables />
    </div>
  );
}
