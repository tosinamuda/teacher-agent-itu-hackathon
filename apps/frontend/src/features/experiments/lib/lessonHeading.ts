import { experimentTitle, type ExperimentSummary } from "./experiments";

/** A lesson's own name, and where it sits: what to show as its heading and the line under it. */
export type LessonHeading = { name: string; where: string };

/** `JSS1 Mathematics Week 9 Session 4: Prime numbers`: the slot, then the lesson's name. */
const TITLE = /^.*?\bWeek\s+(\d+)\s+Session\s+(\d+):\s*(.+)$/;

/**
 * The stored title joins the class, the subject, the week, the session and the lesson's name in
 * one line, so a page that also prints the subject and the class says them twice. This keeps the
 * name for the heading and says everything else once, on the line under it.
 */
export const lessonHeading = (experiment: ExperimentSummary): LessonHeading => {
  const title = experimentTitle(experiment);
  const found = TITLE.exec(title);
  const place = [
    experiment.subject_name,
    experiment.grade_level,
    experiment.term,
  ];
  if (!found) return { name: title, where: place.filter(Boolean).join(" · ") };
  const [, week, session, name] = found;
  return {
    name,
    where: [...place, `Week ${week}`, `Session ${session}`]
      .filter(Boolean)
      .join(" · "),
  };
};
