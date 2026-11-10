import { buttonClass } from "@/shared/components/ui/Button";
import {
  RightPanel,
  type NeedsItem,
} from "@/shared/components/workspace/RightPanel";
import { Link } from "@/shared/router";

/** The right panel of the learner pages: the personalised notes waiting for the teacher, if any. */
export function LearnersPanel({
  notesToReview,
  whose,
}: {
  notesToReview: number;
  whose: string;
}) {
  const needs: NeedsItem[] =
    notesToReview > 0
      ? [
          {
            id: "notes",
            title: "Personalised notes",
            detail: `${notesToReview} to review${whose ? ` for ${whose}` : ""}`,
            actions: (
              <Link
                href="/research/teacher/pack-reviews"
                className={buttonClass({ variant: "secondary", size: "sm" })}
              >
                Review
              </Link>
            ),
          },
        ]
      : [];
  return (
    <RightPanel
      needs={needs}
      agent={
        <p className="text-xs text-(--faint)">
          Each material has its own chat with the agent. Open a lesson to find
          them.
        </p>
      }
    />
  );
}
