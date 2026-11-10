import { LiveThread } from "@/features/content-chat/LiveWork";
import { LessonConversations } from "@/features/lesson-home/components/LessonConversations";
import { useLessonHome } from "@/features/lesson-home/hooks/useLessonHome";
import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { RightPanel } from "@/shared/components/workspace/RightPanel";
import { WorkspacePage } from "@/shared/components/workspace/WorkspacePage";
import { Link, useRouter } from "@/shared/router";

import { PlanFailed, PlanWriting } from "../components/PlanWriting";
import { PlanWays } from "../components/PlanWays";
import { useDraftingProgress } from "../hooks/useDraftingProgress";
import { usePlanGenerator } from "../hooks/usePlanGenerator";
import { parseGenerateError } from "../lib/generateError";
import { planPath } from "../lib/planPaths";

/**
 * Where a lesson's plan is made: the agent writes it, or the teacher imports, writes or reuses one.
 * While the agent writes, the page waits for the plan and the panel shows the agent at work.
 */
export function MakePlanPage({ lessonPeriodId }: { lessonPeriodId: string }) {
  const router = useRouter();
  const { currentWorkspace } = useTeachingWorkspace();
  const { lesson } = useLessonHome(lessonPeriodId);
  const { generate, isGenerating, generateError } = usePlanGenerator();
  const { lines, outline } = useDraftingProgress(lessonPeriodId, isGenerating);
  const teacherId = currentWorkspace?.teacher_id;

  const start = () => {
    if (!teacherId) return;
    generate(
      { session_id: lessonPeriodId, teacher_id: teacherId },
      { onSuccess: (plan) => router.replace(planPath(plan.plan_id)) },
    );
  };

  const agent = isGenerating ? (
    <LiveThread events={lines} />
  ) : (
    <LessonConversations lessonPeriodId={lessonPeriodId} />
  );

  return (
    <WorkspacePage panel={<RightPanel needs={[]} agent={agent} />}>
      {isGenerating ? (
        <PlanWriting title={lesson?.title ?? "Lesson plan"} outline={outline} />
      ) : (
        <div className="flex flex-col gap-5">
          <Link
            href={`/research/teacher/lessons/${lessonPeriodId}`}
            className="text-xs text-(--ink-2) hover:text-(--ink)"
          >
            ‹ Overview
          </Link>
          <header className="flex flex-col gap-1">
            <h1 className="text-2xl font-semibold text-(--ink)">
              Make the lesson plan
            </h1>
            <p className="text-xs text-(--ink-2)">
              You read and approve it before any material is made.
            </p>
          </header>
          {generateError ? (
            <PlanFailed
              lessonPeriodId={lessonPeriodId}
              reason={parseGenerateError(generateError)}
              onRetry={start}
            />
          ) : null}
          <PlanWays lessonPeriodId={lessonPeriodId} onGenerate={start} />
        </div>
      )}
    </WorkspacePage>
  );
}
