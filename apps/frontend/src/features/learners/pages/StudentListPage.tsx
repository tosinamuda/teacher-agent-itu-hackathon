import { Link } from "@/shared/router";
import {
  ORDER_LABEL,
  type LearnerOrder,
} from "@/features/learners/lib/arrangeLearners";
import { LearnersPanel } from "@/features/learners/components/LearnersPanel";
import { LearnerTable } from "@/features/learners/components/LearnerTable";
import { useLearnerList } from "@/features/learners/hooks/useStudentList";
import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { formatClassLabel } from "@/features/teaching-workspace/lib/labels";
import { buttonClass } from "@/shared/components/ui/Button";
import { WorkspacePage } from "@/shared/components/workspace/WorkspacePage";

export function LearnerListPage() {
  const { currentWorkspace } = useTeachingWorkspace();
  const {
    learnersQuery,
    learners,
    total,
    notesToReview,
    search,
    setSearch,
    order,
    setOrder,
  } = useLearnerList();

  return (
    <WorkspacePage
      panel={<LearnersPanel notesToReview={notesToReview} whose="" />}
    >
      <div className="flex flex-col gap-5">
        <header className="flex flex-col gap-1">
          <h1 className="text-2xl font-semibold text-(--ink)">Learners</h1>
          <p className="text-xs text-(--ink-2)">
            {currentWorkspace ? `${formatClassLabel(currentWorkspace)} · ` : ""}
            {total} {total === 1 ? "learner" : "learners"}
            {notesToReview > 0
              ? ` · ${notesToReview} ${notesToReview === 1 ? "note" : "notes"} to review`
              : ""}
          </p>
        </header>

        <div className="flex items-center justify-between gap-3">
          <input
            type="search"
            aria-label="Search learners"
            placeholder="Search learners"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            className="w-64 border border-(--line-2) bg-(--surface) px-3 py-1.5 text-sm focus:border-(--accent) focus:outline-hidden"
          />
          <div className="flex items-center gap-3">
            <select
              aria-label="Sort"
              value={order}
              onChange={(event) => setOrder(event.target.value as LearnerOrder)}
              className="border border-(--line-2) bg-(--sunken) px-3 py-1.5 text-xs font-semibold text-(--ink)"
            >
              {(Object.keys(ORDER_LABEL) as LearnerOrder[]).map((key) => (
                <option key={key} value={key}>
                  Sort: {ORDER_LABEL[key].toLowerCase()}
                </option>
              ))}
            </select>
            <Link
              href="/research/teacher/learners/new"
              className={buttonClass({ variant: "secondary", size: "sm" })}
            >
              Add learner
            </Link>
          </div>
        </div>

        {learnersQuery.isError ? (
          <p className="text-sm text-(--danger)">
            Couldn&apos;t load the learners.
          </p>
        ) : (
          <LearnerTable
            learners={learners}
            isLoading={learnersQuery.isLoading}
          />
        )}
      </div>
    </WorkspacePage>
  );
}
