import { useRouter } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";

import { useGenerateContent } from "@/features/content/hooks/useContent";
import { parseGenerateError } from "@/features/lesson-plan/lib/generateError";

/** Why a class note could not be made, when the teacher can act on the reason. */
const REFUSALS: Record<string, string> = {
  class_revision_note_is_made_by_the_lessons_experiment:
    "Made in this lesson's preparation, by “Create the class revision note”.",
};

/**
 * Opens the class-level revision note for a lesson so the teacher can review, revise and
 * approve it. It is made (as pending) on first use, as a job, and the teacher is taken to
 * its review screen once it exists; one made already opens at once.
 */
export function ReviewBasePackButton({
  planVersionId,
}: {
  planVersionId: string;
}) {
  const router = useRouter();
  const note = useGenerateContent(planVersionId, "revision-note");

  return (
    <span className="inline-flex items-center gap-2">
      <Button
        size="sm"
        variant="ghost"
        isLoading={note.isPending}
        onClick={() =>
          void note
            .createAsync({})
            .then((made) =>
              router.push(`/research/teacher/pack-reviews/${made.content_id}`),
            )
            .catch(() => undefined)
        }
      >
        {note.isPending
          ? "Writing the revision note…"
          : "Review the revision note"}
      </Button>
      {note.isError ? (
        <span className="text-xs text-(--danger-ink)">
          {REFUSALS[parseGenerateError(note.error)] ??
            "Couldn't make it — try again."}
        </span>
      ) : null}
    </span>
  );
}
