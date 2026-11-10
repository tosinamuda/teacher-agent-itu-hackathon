import { apiFetch } from "@/shared/api/client";

export type TranscriptKind = "teacher_record" | "teacher_cleaned" | "cleaning_log" | "learner_script";

/** A photographed page, named by file and by what it shows. The photograph is not released. */
export type CapturedPage = { file: string; role: string };

/** One published transcript of a lesson: the teacher's pages at a stage, or a learner's script. */
export type Transcript = {
  kind: TranscriptKind;
  student_id: string | null;
  pages: CapturedPage[];
  header: Record<string, unknown>;
  body: string;
  source_path: string;
};

/** One lesson's share of the study. */
export type LessonDesign = {
  experiment_id: string;
  objectives: number;
  class_notes: number;
  learners: number;
  part_1_sets: number;
  part_2_sets: number;
};

/** The study's shape, counted from its record. */
export type StudyDesign = {
  lessons: LessonDesign[];
  conditions: string[];
  draws: number;
  raters: number;
};

export const getLessonTranscripts = (experimentId: string): Promise<Transcript[]> =>
  apiFetch<Transcript[]>(`/experiments/${encodeURIComponent(experimentId)}/transcripts`);

export const getStudyDesign = (investigationId: string): Promise<StudyDesign> =>
  apiFetch<StudyDesign>(
    `/experiments/investigations/${encodeURIComponent(investigationId)}/design`,
  );

/** One change the cleaning made to the teacher's pages, and what licensed it. */
export type Cleaning = { what: string; change: string; why: string };

const text = (value: unknown): string =>
  value == null ? "" : typeof value === "string" ? value.trim() : JSON.stringify(value);

/**
 * The changes a cleaned transcript's header lists. Lessons record them under `cleaned` or
 * `cleaning_applied`, each as a stated `change` or a `from` and `to`, licensed by a `source`
 * or a `reason`.
 */
export function cleaningsOf(header: Record<string, unknown>): Cleaning[] {
  const listed = header.cleaned ?? header.cleaning_applied;
  if (!Array.isArray(listed)) return [];
  return listed.map((entry: Record<string, unknown>) => {
    const moved = entry.from != null ? `${text(entry.from)} → ${text(entry.to)}` : "";
    const dropped = entry.dropped != null ? `, dropping ${text(entry.dropped)}` : "";
    return {
      what: text(entry.field).replace(/_/g, " "),
      change: text(entry.change) || moved + dropped,
      why: text(entry.source) || text(entry.reason),
    };
  });
}

/** A page's role as its transcriber tagged it, read as words. */
export const roleOf = (page: CapturedPage): string => page.role.replace(/_/g, " ");
