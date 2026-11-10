import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";

import {
  listAssessmentStatus,
  listMyClassLessons,
  listPackStatuses,
  listSubmissions,
} from "@/features/student/api/exitAssessment";
import { ArtefactSummary } from "@/features/student/lib/studentLessons";

/** Where a lesson sits in the student's flow. */
export type LessonStatus =
  | "not_released"
  | "open"
  | "generating"
  | "awaiting_review"
  | "ready";

/** One lesson in the student's syllabus map, with its assessment + pack state. */
export type SyllabusLesson = {
  versionId: string;
  subject: string;
  week: number | null;
  title: string;
  status: LessonStatus;
  pack: ArtefactSummary | null;
};

/** A subject and its ordered lessons. */
export type SubjectSyllabus = {
  subject: string;
  lessons: SyllabusLesson[];
};

/**
 * The student's syllabus, grouped by subject. Lessons come from the approved lesson
 * plans for their own class (deduped per week+title); each lesson's status is derived from
 * whether the student has submitted its exit assessment and whether an approved review
 * pack exists for them:
 *   not_released    → the teacher hasn't released the assessment yet
 *   open            → assessment released, not yet taken
 *   generating      → assessment submitted, pack not created yet
 *   awaiting_review → pack created but pending teacher approval
 *   ready           → approved review pack available
 */
export const useStudentSyllabus = (
  studentId: string | null,
  packs: ArtefactSummary[]
) => {
  const lessonsQuery = useQuery({
    queryKey: ["studentSyllabus", studentId],
    queryFn: listMyClassLessons,
    enabled: Boolean(studentId),
  });

  const submissionsQuery = useQuery({
    queryKey: ["studentSubmissions", studentId],
    queryFn: () => listSubmissions(studentId as string),
    enabled: Boolean(studentId),
  });

  const packStatusesQuery = useQuery({
    queryKey: ["studentPackStatuses", studentId],
    queryFn: () => listPackStatuses(studentId as string),
    enabled: Boolean(studentId),
  });

  // Which lessons have a released assessment — gates the "take assessment" CTA.
  const versionIds = useMemo(
    () => (lessonsQuery.data ?? []).map((lesson) => lesson.version_id),
    [lessonsQuery.data]
  );
  const releaseQuery = useQuery({
    queryKey: ["studentAssessmentStatus", [...versionIds].sort()],
    queryFn: () => listAssessmentStatus(versionIds),
    enabled: versionIds.length > 0,
  });
  const releasedVersions = useMemo(
    () =>
      new Set(
        (releaseQuery.data ?? []).filter((row) => row.released).map((row) => row.plan_version_id)
      ),
    [releaseQuery.data]
  );

  const packByVersion = useMemo(() => {
    const map = new Map<string, ArtefactSummary>();
    for (const pack of packs) {
      if (pack.plan_version_id) map.set(pack.plan_version_id, pack);
    }
    return map;
  }, [packs]);

  const submittedVersions = useMemo(
    () => new Set((submissionsQuery.data ?? []).map((s) => s.plan_version_id)),
    [submissionsQuery.data]
  );

  const packStatusByVersion = useMemo(() => {
    const map = new Map<string, string>();
    for (const row of packStatusesQuery.data ?? []) {
      map.set(row.plan_version_id, row.review_status);
    }
    return map;
  }, [packStatusesQuery.data]);

  const subjects = useMemo<SubjectSyllabus[]>(() => {
    const approved = (lessonsQuery.data ?? []).filter(
      (lesson) => (lesson.status ?? "").toLowerCase() === "approved"
    );
    const bySubject = new Map<string, Map<string, SyllabusLesson>>();
    for (const lesson of approved) {
      const subject = lesson.subject || "Other";
      const title = lesson.subtopic || lesson.topic || `Week ${lesson.week ?? "?"}`;
      const dedupeKey = `${lesson.week ?? "?"}::${title}`;
      const lessons = bySubject.get(subject) ?? new Map<string, SyllabusLesson>();
      if (!lessons.has(dedupeKey)) {
        const pack = packByVersion.get(lesson.version_id) ?? null;
        const packStatus = packStatusByVersion.get(lesson.version_id);
        let status: LessonStatus = "open";
        if (pack || packStatus === "approved") {
          status = "ready";
        } else if (packStatus) {
          status = "awaiting_review";
        } else if (submittedVersions.has(lesson.version_id)) {
          status = "generating";
        } else if (!releasedVersions.has(lesson.version_id)) {
          status = "not_released";
        }
        lessons.set(dedupeKey, {
          versionId: lesson.version_id,
          subject,
          week: lesson.week ?? null,
          title,
          status,
          pack,
        });
      }
      bySubject.set(subject, lessons);
    }
    return [...bySubject.entries()]
      .map(([subject, lessons]) => ({
        subject,
        lessons: [...lessons.values()].sort((a, b) => (a.week ?? 0) - (b.week ?? 0)),
      }))
      .sort((a, b) => a.subject.localeCompare(b.subject));
  }, [lessonsQuery.data, packByVersion, submittedVersions, packStatusByVersion, releasedVersions]);

  return { lessonsQuery, submissionsQuery, packStatusesQuery, subjects };
};
