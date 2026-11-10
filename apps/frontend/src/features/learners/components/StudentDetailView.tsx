import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { buttonClass } from "@/shared/components/ui/Button";

import { useLearnerResults } from "../hooks/useLearnerResults";
import { LearnerProfile } from "../types";
import { LearnerResultsView } from "./LearnerResultsView";

type StudentDetailViewProps = {
  student: LearnerProfile;
  onEdit: () => void;
};

/** A learner: how they are doing in this class. The profile is in Edit details. */
export function StudentDetailView({ student, onEdit }: StudentDetailViewProps) {
  const results = useLearnerResults(student.student_id);
  const { currentWorkspace: workspace } = useTeachingWorkspace();

  return (
    <div className="flex flex-col gap-6">
      <header className="flex items-start justify-between gap-4">
        <div className="flex flex-col gap-1">
          <h1 className="text-2xl font-semibold text-(--ink)">
            {student.full_name}
          </h1>
          <p className="text-xs text-(--ink-2)">
            {[
              workspace?.class_name ?? student.class_name ?? student.grade,
              workspace?.subject_name,
            ]
              .filter(Boolean)
              .join(" · ")}
          </p>
        </div>
        <button
          type="button"
          className={buttonClass({ variant: "secondary", size: "sm" })}
          onClick={onEdit}
        >
          Edit details
        </button>
      </header>

      {results.data ? <LearnerResultsView results={results.data} /> : null}
      {results.isError ? (
        <p className="text-sm text-(--ink-2)">
          Results are not available for this learner in this class.
        </p>
      ) : null}
    </div>
  );
}
