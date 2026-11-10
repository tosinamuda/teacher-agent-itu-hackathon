import { useMemo } from "react";

import { useAssessmentStatus } from "./useAssessmentStatus";
import { useExperiments } from "./useExperiments";
import { usePendingStudentNotes } from "./usePendingStudentNotes";
import { useStudentNotesMade } from "./useStudentNotesMade";
import { ExperimentSummary } from "../lib/experiments";
import { buildLessonPrepSteps, summariseLessonPrep, LessonPrepStep } from "../services/lessonPrep";

/** An ended lesson is closed: it takes no more work, so it is not the teacher's to prepare. */
export const isOpen = (experiment: ExperimentSummary): boolean =>
  experiment.lifecycle_status !== "ended";

/** One lesson, with its progress summary. */
export type PreparedLesson = {
  experiment: ExperimentSummary;
  doneCount: number;
  total: number;
  current?: LessonPrepStep;
  /** Whether the teacher still has something to do on it. */
  needsAttention: boolean;
};

/**
 * The teacher's lessons, each with its progress, and those that still need
 * attention — anywhere in the prep lifecycle (plan → revision note → assessment
 * → per-student notes) that isn't done. Shared by the "Lessons to prepare" page,
 * its "All lessons" view and the home preview so all agree on what's pending and
 * the current step per lesson.
 */
export const useLessonsToPrepare = (teacherId?: string) => {
  const enabled = Boolean(teacherId);
  const experimentsQuery = useExperiments({ teacherId });
  const pendingNotesQuery = usePendingStudentNotes(enabled);
  const notesMadeQuery = useStudentNotesMade(enabled);
  const notesMade = notesMadeQuery.data;

  const planVersionIds = useMemo(
    () =>
      (experimentsQuery.data ?? [])
        .map((experiment) => experiment.plan_version_id)
        .filter((id): id is string => Boolean(id)),
    [experimentsQuery.data],
  );
  const assessmentQuery = useAssessmentStatus(planVersionIds, enabled);

  const assessmentByPlan = useMemo(() => {
    const byPlan = new Map<string, { ready: boolean; sent: boolean }>();
    for (const row of assessmentQuery.data ?? []) {
      byPlan.set(row.plan_version_id, { ready: row.has_assessment, sent: row.released });
    }
    return byPlan;
  }, [assessmentQuery.data]);

  const pendingNotesByPlan = useMemo(() => {
    const counts = new Map<string, number>();
    for (const note of pendingNotesQuery.data ?? []) {
      if (note.plan_version_id) {
        counts.set(note.plan_version_id, (counts.get(note.plan_version_id) ?? 0) + 1);
      }
    }
    return counts;
  }, [pendingNotesQuery.data]);

  const lessons = useMemo<PreparedLesson[]>(() => {
    const assessmentFor = (pv: string | null | undefined) =>
      (pv && assessmentByPlan.get(pv)) || { ready: false, sent: false };
    const notesFor = (pv: string | null | undefined) => ({
      made: pv ? (notesMade?.get(pv) ?? 0) : 0,
      awaiting: pv ? (pendingNotesByPlan.get(pv) ?? 0) : 0,
    });

    return (experimentsQuery.data ?? []).filter(isOpen).map((experiment) => {
      const planIncomplete = !experiment.plan_version_id || !experiment.baseline_approved_by;
      const notePending =
        Boolean(experiment.baseline_approved_by) && !experiment.readiness.base_pack_approved;
      const assessmentPending =
        Boolean(experiment.baseline_approved_by) && !assessmentFor(experiment.plan_version_id).sent;
      const studentNotesPending = notesFor(experiment.plan_version_id).awaiting > 0;
      const steps = buildLessonPrepSteps(
        experiment,
        notesFor(experiment.plan_version_id),
        assessmentFor(experiment.plan_version_id),
      );
      const { doneCount, total, current } = summariseLessonPrep(steps);
      return {
        experiment,
        doneCount,
        total,
        current,
        needsAttention: planIncomplete || notePending || assessmentPending || studentNotesPending,
      };
    });
  }, [experimentsQuery.data, assessmentByPlan, pendingNotesByPlan, notesMade]);

  const pending = useMemo(() => lessons.filter((lesson) => lesson.needsAttention), [lessons]);

  return {
    pending,
    all: lessons,
    isLoading: experimentsQuery.isLoading,
    hasTeacher: enabled,
  };
};
