import { RevisionSummary } from "@/shared/components/renderer/RevisionSummary";

import { useContentApprovals, useContentRevisions } from "../hooks/useContent";

/** Every revision and approval of a piece of content, . */
export function ContentHistory({ contentId }: { contentId: string }) {
  const revisions = useContentRevisions(contentId);
  const approvals = useContentApprovals(contentId);
  const count = (revisions.data ?? []).length + (approvals.data ?? []).length;
  return (
    <details className="text-sm">
      <summary className="cursor-pointer text-base font-semibold text-(--ink)">
        History <span className="text-sm font-normal text-(--ink-2)">· {count}</span>
      </summary>
      <ul className="mt-2 space-y-2">
        {(revisions.data ?? []).map((revision) => (
          <li key={`r${revision.turn_number}`}>
            <span className="font-semibold">Revision {revision.turn_number}:</span> {revision.feedback}
            {revision.summary ? (
              <RevisionSummary text={revision.summary} className="text-xs text-(--ink-2)" />
            ) : null}
          </li>
        ))}
        {(approvals.data ?? []).map((approval) => (
          <li key={approval.id}>
            <span className="font-semibold">Approved</span> version {approval.approved_version}
            {approval.approved_by ? ` by ${approval.approved_by}` : ""}
          </li>
        ))}
      </ul>
      {count === 0 ? <p className="mt-2 text-xs text-(--ink-2)">No revisions or approvals yet.</p> : null}
    </details>
  );
}
