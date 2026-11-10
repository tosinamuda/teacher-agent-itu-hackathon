import { Badge } from "@/shared/components/ui/Badge";
import { Button } from "@/shared/components/ui/Button";

import {
  useGenerationStatuses,
  isGenerationInFlight,
} from "../hooks/useGenerationStatuses";
import { useMissingPacks } from "../hooks/useMissingPacks";
import { StudentPackGenerationStatusRow } from "../types";

/** Render the generation-status badge for a student (generating / failed), if any. */
function StatusBadge({ status }: { status?: StudentPackGenerationStatusRow }) {
  if (!status) return null;
  if (isGenerationInFlight(status.status)) {
    return <Badge variant="accent">Generating…</Badge>;
  }
  if (status.status === "failed") {
    return (
      <Badge variant="error">
        Failed{status.error_category ? ` (${status.error_category})` : ""}
      </Badge>
    );
  }
  return null;
}

/**
 * For one lesson (plan version), lists students who submitted the exit assessment
 * but have no pack yet — generation pending or failed — and lets the teacher
 * regenerate one student or all of them via the same worker that runs on submit.
 * Each student's current generation status (generating… / failed) is shown so the
 * teacher knows whether to wait or retry. Shows nothing when no student is awaiting
 * a pack. (The status row falls back to the failure reason when a generation failed.)
 */
export function MissingPackPanel({ planVersionId }: { planVersionId: string }) {
  const { students, isLoading, refetch, regenerate } =
    useMissingPacks(planVersionId);
  const { byStudent } = useGenerationStatuses(planVersionId);

  if (isLoading || students.length === 0) return null;

  return (
    <section className="space-y-3 rounded-2xl border border-(--warning-tint) bg-(--warning-tint)/60 p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-sm font-semibold text-(--ink)">
            {students.length} student{students.length === 1 ? "" : "s"} awaiting
            a pack
          </h2>
          <p className="text-[11px] text-(--muted)">
            Submitted the exit assessment but have no pack yet — regenerate via
            the same worker. Each lands as{" "}
            <span className="font-medium">pending</span> for review.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button size="sm" variant="ghost" onClick={() => refetch()}>
            Refresh
          </Button>
          <Button
            size="sm"
            onClick={() => regenerate.mutate(undefined)}
            isLoading={regenerate.isPending}
          >
            Regenerate all
          </Button>
        </div>
      </div>

      <ul className="divide-y divide-amber-200/70 rounded-xl border border-(--warning-tint)/70 bg-(--surface)">
        {students.map((student) => {
          const status = byStudent.get(student.student_id);
          const generating = isGenerationInFlight(status?.status);
          return (
            <li
              key={student.student_id}
              className="flex items-center justify-between gap-3 px-3 py-2"
            >
              <span className="flex items-center gap-2 text-sm text-(--ink)">
                {student.full_name}
                <StatusBadge status={status} />
              </span>
              <Button
                size="sm"
                variant="secondary"
                onClick={() => regenerate.mutate(student.student_id)}
                disabled={generating}
                isLoading={
                  generating ||
                  (regenerate.isPending &&
                    regenerate.variables === student.student_id)
                }
              >
                {status?.status === "failed" ? "Retry" : "Regenerate"}
              </Button>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
