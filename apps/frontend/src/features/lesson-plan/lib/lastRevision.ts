import type { NumberedVersion } from "./planVersions";

/**
 * The agent's latest revision of a plan still being worked on, and the version before it. None when
 * the newest version was not a revision by the agent, or is no longer a draft.
 */
export function lastRevision(
  versions: readonly NumberedVersion[],
): { latest: NumberedVersion; before: NumberedVersion } | null {
  const latest = versions.at(-1);
  const before = versions.at(-2);
  if (!latest || !before) return null;
  if (latest.source_type !== "revised" || latest.status !== "draft")
    return null;
  return { latest, before };
}

/** Whether a version was saved from the teacher's own edit, which includes going back to an earlier one. */
export const savedByHand = (
  runMetadata: Record<string, unknown> | undefined,
): boolean => runMetadata?.source === "manual_edit";
