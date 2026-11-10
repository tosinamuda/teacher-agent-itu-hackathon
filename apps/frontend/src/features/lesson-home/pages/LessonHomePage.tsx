import { Link } from "@/shared/router";
import { buttonClass } from "@/shared/components/ui/Button";
import {
  RightPanel,
  type NeedsItem,
} from "@/shared/components/workspace/RightPanel";
import { WorkspacePage } from "@/shared/components/workspace/WorkspacePage";
import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { formatClassLabel } from "@/features/teaching-workspace/lib/labels";

import { HomeRowView } from "../components/HomeRowView";
import { StartOver } from "../components/StartOver";
import { CreationsInProgress } from "../components/CreationsInProgress";
import { LessonConversations } from "../components/LessonConversations";
import { useLessonHome } from "../hooks/useLessonHome";
import { waitingOn, type HomeRow } from "../lib/lessonHome";

const OVERLINE =
  "text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)";

function Section({
  title,
  rows,
  planVersionId,
}: {
  title: string;
  rows: HomeRow[];
  planVersionId: string | null;
}) {
  if (rows.length === 0) return null;
  return (
    <section className="flex flex-col gap-2">
      <h2 className={OVERLINE}>{title}</h2>
      <ul className="border border-(--line) bg-(--surface)">
        {rows.map((row) => (
          <HomeRowView key={row.key} row={row} planVersionId={planVersionId} />
        ))}
      </ul>
    </section>
  );
}

const needsItem = (row: HomeRow): NeedsItem => ({
  id: row.key,
  title: row.title,
  detail: row.detail,
  actions: row.action ? (
    <Link
      href={row.action.href}
      className={buttonClass({ variant: "secondary", size: "sm" })}
    >
      {row.action.label}
    </Link>
  ) : undefined,
});

/** A lesson: its plan, the materials made from it, and the learners' evidence and notes. */
export function LessonHomePage({ lessonPeriodId }: { lessonPeriodId: string }) {
  const { currentWorkspace } = useTeachingWorkspace();
  const home = useLessonHome(lessonPeriodId);
  const waiting = waitingOn([
    home.rows.plan,
    ...home.rows.materials,
    ...home.rows.learners,
  ]);

  const panel = (
    <RightPanel
      needs={waiting.map(needsItem)}
      agent={
        <div className="flex flex-col gap-4">
          <CreationsInProgress planVersionId={home.planVersionId} />
          <LessonConversations lessonPeriodId={lessonPeriodId} />
          <p className="text-xs text-(--faint)">
            Each material has its own chat with the agent. Open a material to
            talk to it.
          </p>
        </div>
      }
    />
  );

  return (
    <WorkspacePage panel={panel}>
      <div className="flex flex-col gap-5">
        <header className="flex flex-col gap-1">
          <h1 className="text-2xl font-semibold text-(--ink)">
            {home.lesson?.title ?? "Lesson"}
          </h1>
          <p className="text-xs text-(--ink-2)">
            {home.lesson ? `Week ${home.lesson.week} · ` : ""}
            {currentWorkspace ? formatClassLabel(currentWorkspace) : ""}
          </p>
        </header>

        {home.isError ? (
          <p className="text-sm text-(--danger)">
            Couldn&apos;t load this lesson.
          </p>
        ) : null}
        {home.isLoading ? (
          <p className="text-sm text-(--ink-2)">Loading lesson…</p>
        ) : null}
        {!home.isLoading ? (
          <>
            <Section
              title="Plan"
              rows={[home.rows.plan]}
              planVersionId={home.planVersionId}
            />
            <Section
              title="Class materials"
              rows={home.rows.materials}
              planVersionId={home.planVersionId}
            />
            <Section
              title="For each learner"
              rows={home.rows.learners}
              planVersionId={home.planVersionId}
            />
            <StartOver lessonPeriodId={lessonPeriodId} />
          </>
        ) : null}
      </div>
    </WorkspacePage>
  );
}
