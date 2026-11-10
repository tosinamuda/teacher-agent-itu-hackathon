import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { classLearnersQuery } from "@/features/learners/lib/classLearnersQuery";
import { LessonSidebar } from "@/features/lesson-home/components/LessonSidebar";
import {
  SidebarNav,
  type SidebarGroup,
} from "@/shared/components/workspace/SidebarNav";
import { usePathname, useRouter } from "@/shared/router";

import { useLessonScope } from "../hooks/useLessonScope";
import { useTeachingWorkspace } from "../context/TeachingWorkspaceContext";
import { useWaitingByClass } from "../hooks/useWaitingByClass";
import { formatClassLabel } from "../lib/labels";

const PAGES = [
  // The lesson-plan page is where a lesson is planned, so it belongs under Lessons.
  {
    href: "/research/teacher/lessons",
    label: "Lessons",
    under: ["/research/teacher/lesson-plan"],
  },
  { href: "/research/teacher/learners", label: "Learners", under: [] },
];

/** Switching class keeps a teacher on the list page they were reading, now for the new class. */
const LISTS_THAT_FOLLOW_THE_CLASS = [
  "/research/teacher/lessons",
  "/research/teacher/lesson-plan",
  "/research/teacher/lesson-preview",
];

/** The teacher's sidebar: inside a lesson, the lesson; otherwise this class's pages, then the other classes. */
export function TeacherSidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { workspaces, currentWorkspace, setWorkspace, isLoading } =
    useTeachingWorkspace();
  const { lessonPeriodId, resolving } = useLessonScope();
  // Opening a plan or a material, the page's lesson is found a moment later. The sidebar of the
  // lesson the teacher was in stays meanwhile, so it does not vanish and come back.
  const [lastLesson, setLastLesson] = useState<string | null>(null);
  if (lessonPeriodId && lessonPeriodId !== lastLesson)
    setLastLesson(lessonPeriodId);
  const learners = useQuery(classLearnersQuery(currentWorkspace?.id ?? ""));
  // Other terms of this class and subject are chosen on the class page, not listed as classes.
  const others = workspaces.filter(
    (workspace) =>
      workspace.class_id !== currentWorkspace?.class_id ||
      workspace.subject_code !== currentWorkspace?.subject_code,
  );
  const waiting = useWaitingByClass(others.map((workspace) => workspace.id));

  if (isLoading || !currentWorkspace) return null;
  if (resolving)
    return lastLesson ? <LessonSidebar lessonPeriodId={lastLesson} /> : null;
  if (lessonPeriodId) return <LessonSidebar lessonPeriodId={lessonPeriodId} />;

  const groups: SidebarGroup[] = [
    {
      heading: [currentWorkspace.class_name, currentWorkspace.subject_name]
        .filter(Boolean)
        .join(" · "),
      items: PAGES.map((page) => ({
        label: page.label,
        href: page.href,
        count: page.href.endsWith("/learners")
          ? learners.data?.learners.length
          : undefined,
        active: [page.href, ...page.under].some(
          (path) => pathname === path || pathname.startsWith(`${path}/`),
        ),
      })),
    },
  ];
  if (others.length > 0) {
    groups.push({
      heading: "Other classes",
      items: others.map((workspace) => ({
        label:
          [workspace.class_name, workspace.subject_name]
            .filter(Boolean)
            .join(" · ") || formatClassLabel(workspace),
        waiting: waiting[workspace.id] > 0,
        count: waiting[workspace.id] > 0 ? waiting[workspace.id] : undefined,
        onSelect: () => {
          setWorkspace(workspace);
          const list = LISTS_THAT_FOLLOW_THE_CLASS.find(
            (href) => pathname === href || pathname.startsWith(`${href}/`),
          );
          if (list) router.replace(list);
        },
      })),
    });
  }

  return <SidebarNav label="Class" groups={groups} />;
}
