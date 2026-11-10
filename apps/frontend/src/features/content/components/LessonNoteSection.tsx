import { Card } from "@/shared/components/ui/Card";
import type { LessonStepStructured } from "@/shared/types/lesson-schema";

import { useLessonNote } from "../hooks/useLessonNote";
import { Origin } from "../types";
import { LessonNoteView } from "./LessonNoteView";

const FROM: Record<Origin, string> = {
  teacher: "written by the teacher",
  study_record: "from the study's record",
  generated: "drafted by the app",
};

/** The lesson's note, read only, under its plan: the subject content each step teaches. */
export function LessonNoteSection({
  planVersionId,
  steps,
}: {
  planVersionId: string;
  /** The plan's steps, to show the note as the teacher prepares it. */
  steps?: LessonStepStructured[];
}) {
  const { summary, manifest, isLoading } = useLessonNote(planVersionId);

  if (isLoading) {
    return <p className="text-sm text-(--muted)">Loading the lesson note…</p>;
  }
  if (!summary || !manifest) {
    return (
      <Card padding="lg">
        <p className="text-sm text-(--muted)">
          This lesson has no lesson note.
        </p>
      </Card>
    );
  }
  const origin = summary.provenance.origin;
  return (
    <section className="space-y-3">
      <div className="border-b border-(--line) pb-2">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-(--muted)">
          Lesson note · read only
        </p>
        <p className="text-sm text-(--muted)">
          The subject content each step teaches
          {origin ? `, ${FROM[origin]}` : ""}
          {summary.review_status === "approved" ? "" : " (not yet approved)"}.
        </p>
      </div>
      <LessonNoteView manifest={manifest} steps={steps} />
    </section>
  );
}
