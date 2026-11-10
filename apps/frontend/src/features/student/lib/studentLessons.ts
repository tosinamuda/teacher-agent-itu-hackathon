export type StudentSummary = {
  student_id: string;
  full_name: string;
  grade: string;
  track: string;
  class_id?: string | null;
  class_name?: string | null;
  field_of_study?: string | null;
  language_level?: string | null;
  pace_preference?: string | null;
  time_budget_minutes?: number | null;
};

export type ArtefactSummary = {
  artefact_id: string;
  plan_version_id: string;
  student_id?: string | null;
  subject?: string | null;
  track?: string | null;
  grade?: string | null;
  term?: string | null;
  week?: number | null;
  topic?: string | null;
  subtopic?: string | null;
  created_at?: string | null;
};

export type SubjectFilterOption = {
  value: string;
  label: string;
  count: number;
};

/** Raw per-student pack artefact from the API (the student endpoint returns approved-only). */
export type StudentPackResponse = {
  artefact_id: string;
  plan_version_id: string;
  learner_id?: string | null;
  created_at?: string | null;
  manifest?: {
    subject?: string | null;
    track?: string | null;
    grade?: string | null;
    term?: string | null;
    week?: number | null;
    topic?: string | null;
    subtopic?: string | null;
  } | null;
};

/** Flatten an approved pack artefact into the summary the lesson list renders. */
export const artefactResponseToSummary = (pack: StudentPackResponse): ArtefactSummary => ({
  artefact_id: pack.artefact_id,
  plan_version_id: pack.plan_version_id,
  student_id: pack.learner_id ?? null,
  subject: pack.manifest?.subject ?? null,
  track: pack.manifest?.track ?? null,
  grade: pack.manifest?.grade ?? null,
  term: pack.manifest?.term ?? null,
  week: pack.manifest?.week ?? null,
  topic: pack.manifest?.topic ?? null,
  subtopic: pack.manifest?.subtopic ?? null,
  created_at: pack.created_at ?? null,
});

export const buildStudentLabel = (student: StudentSummary) => {
  const parts = [student.full_name, student.grade].filter(Boolean);
  const track = student.track ? `(${student.track})` : "";
  return `${parts.join(" · ")} ${track}`.trim();
};

export const formatSubject = (subject?: string | null) => subject || "General studies";

export const formatArtefactTitle = (artefact: ArtefactSummary) =>
  artefact.topic || artefact.subtopic || "Lesson preview";

export const formatArtefactSubtitle = (artefact: ArtefactSummary) => {
  if (artefact.subtopic && artefact.topic && artefact.subtopic !== artefact.topic) {
    return artefact.subtopic;
  }
  return artefact.term ? `${artefact.term}` : "";
};

export const formatTermWeek = (artefact: ArtefactSummary) => {
  const term = artefact.term ? artefact.term : "Term";
  const week = artefact.week ? `Week ${artefact.week}` : "Week";
  return `${term} · ${week}`;
};

export const sortArtefactsByCreatedAt = (artefacts: ArtefactSummary[]) =>
  [...artefacts].sort((a, b) => {
    const aTime = a.created_at ? new Date(a.created_at).getTime() : 0;
    const bTime = b.created_at ? new Date(b.created_at).getTime() : 0;
    return bTime - aTime;
  });

export const getSubjectOptions = (artefacts: ArtefactSummary[]) => {
  const counts = new Map<string, number>();
  artefacts.forEach((artefact) => {
    const subject = formatSubject(artefact.subject);
    counts.set(subject, (counts.get(subject) ?? 0) + 1);
  });
  const options = Array.from(counts.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([subject, count]) => ({ value: subject, label: subject, count }));
  return [{ value: "all", label: "All subjects", count: artefacts.length }, ...options];
};

export const filterArtefactsBySubject = (artefacts: ArtefactSummary[], subject: string) => {
  if (subject === "all") return artefacts;
  return artefacts.filter((artefact) => formatSubject(artefact.subject) === subject);
};
