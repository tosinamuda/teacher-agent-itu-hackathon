import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { formatClassLabel } from "@/features/teaching-workspace/lib/labels";
import { SidebarNav } from "@/shared/components/workspace/SidebarNav";
import { Link, usePathname } from "@/shared/router";

import { useCreationsInProgress } from "../hooks/useCreationsInProgress";
import { useLessonHome } from "../hooks/useLessonHome";
import { lessonSidebarGroups } from "../lib/lessonSidebar";

/** Inside a lesson: the way back to the class, the lesson's name, and its plan and materials. */
export function LessonSidebar({ lessonPeriodId }: { lessonPeriodId: string }) {
  const pathname = usePathname();
  const { currentWorkspace } = useTeachingWorkspace();
  const home = useLessonHome(lessonPeriodId);
  const lessonHome = `/research/teacher/lessons/${lessonPeriodId}`;
  const working = new Set(
    useCreationsInProgress(home.planVersionId)
      .filter((creation) => creation.running)
      .map((creation) => creation.info.type),
  );

  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-col gap-1 px-4">
        <Link
          href="/research/teacher/lessons"
          className="text-xs text-(--ink-2) hover:text-(--ink)"
        >
          ‹{" "}
          {currentWorkspace
            ? [currentWorkspace.class_name, currentWorkspace.subject_name]
                .filter(Boolean)
                .join(" · ") || formatClassLabel(currentWorkspace)
            : "Lessons"}
        </Link>
        <Link
          href={lessonHome}
          aria-current={pathname === lessonHome ? "page" : undefined}
          className="text-base font-semibold text-(--ink)"
        >
          {home.lesson?.title ?? "Lesson"}
        </Link>
      </div>
      {home.isLoading ? null : (
        <SidebarNav
          label="Lesson"
          groups={lessonSidebarGroups(lessonHome, home.rows, pathname, working)}
        />
      )}
    </div>
  );
}
