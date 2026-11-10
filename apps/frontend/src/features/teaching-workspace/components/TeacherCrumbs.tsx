import { useSchemeOfWork } from "@/features/curriculum/hooks/useSchemeOfWork";
import { lessonOf } from "@/features/lesson-home/lib/lessonHome";
import { useTeachingWorkspace } from "../context/TeachingWorkspaceContext";
import { useLessonScope } from "../hooks/useLessonScope";

/** Where the teacher is: the class and term, and inside a lesson the class and the lesson's name. */
export function TeacherCrumbs() {
  const { currentWorkspace } = useTeachingWorkspace();
  const { lessonPeriodId } = useLessonScope();
  const scheme = useSchemeOfWork(currentWorkspace?.term_class_subject_id);
  if (!currentWorkspace) return null;

  const classAndSubject = [
    currentWorkspace.class_name,
    currentWorkspace.subject_name,
  ]
    .filter(Boolean)
    .join(" · ");
  const lesson = lessonPeriodId ? lessonOf(scheme.data, lessonPeriodId) : null;
  if (lesson) {
    return (
      <p className="flex items-center gap-2 text-sm">
        <span className="text-(--faint)">{classAndSubject}</span>
        <span aria-hidden="true" className="text-(--faint)">
          /
        </span>
        <span className="font-semibold text-(--ink)">{lesson.title}</span>
      </p>
    );
  }
  return (
    <p className="text-sm font-semibold text-(--ink)">
      {[classAndSubject, currentWorkspace.term].filter(Boolean).join(" · ")}
    </p>
  );
}
