import { buttonClass } from "@/shared/components/ui/Button";
import { StatusMark } from "@/shared/components/ui/StatusMark";
import { Link } from "@/shared/router";

import { PackArtefact } from "../types";

type PendingPackListProps = {
  packs: PackArtefact[];
  isLoading: boolean;
  /** `approved` lists notes the teacher has already approved. */
  kind?: "waiting" | "approved";
};

const packTitle = (pack: PackArtefact) =>
  pack.manifest?.subtopic || pack.manifest?.topic || "Personalised study pack";

/** Names the lesson a note belongs to, since each learner has one note per lesson. */
const packMeta = (pack: PackArtefact) =>
  [pack.manifest?.week ? `Week ${pack.manifest.week}` : null, packTitle(pack), pack.manifest?.subject, pack.manifest?.grade]
    .filter(Boolean)
    .join(" · ");

/** The notes waiting for the teacher: one line per learner, each with the button that opens it. */
export function PendingPackList({ packs, isLoading, kind = "waiting" }: PendingPackListProps) {
  if (isLoading) {
    return <p className="text-sm text-(--ink-2)">Loading the notes…</p>;
  }
  if (packs.length === 0) {
    return kind === "approved" ? (
      <p className="text-sm text-(--ink-2)">No note has been approved yet.</p>
    ) : (
      <p className="text-sm text-(--ink-2)">
        No notes are waiting. A learner&apos;s note arrives here once they answer the class test.
      </p>
    );
  }

  return (
    <ul className="border border-(--line) bg-(--surface)">
      {packs.map((pack) => (
        <li
          key={pack.artefact_id}
          className="flex items-center gap-4 border-t border-(--line) px-4 py-3 first:border-t-0"
        >
          <StatusMark kind={kind === "approved" ? "complete" : "needsYou"} label={kind === "approved" ? "Approved" : "Waiting for your review"} />
          <span className="flex min-w-0 flex-1 flex-col">
            <span className="text-sm font-semibold text-(--ink)">{pack.learner_name ?? pack.learner_id ?? "A learner"}</span>
            <span className="text-xs text-(--ink-2)">{packMeta(pack)}</span>
          </span>
          <Link
            href={`/research/teacher/pack-reviews/${pack.artefact_id}`}
            className={buttonClass({ variant: "secondary", size: "sm" })}
          >
            {kind === "approved" ? "Open" : "Review"}
          </Link>
        </li>
      ))}
    </ul>
  );
}
