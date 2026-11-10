import type { ClassBand } from "@/features/learners/types";

import type { StudyLearnerResult } from "../api/studyResults";

/** One class learner whose note is made from one study learner's marks. */
export type StandInPair = { studentId: string; studyStudentId: string };

/** The bands in the order a demonstration wants them shown: a strength, a middle, then a gap. */
const BAND_ORDER: ClassBand[] = ["extend", "reinforce", "remediate"];

/**
 * A suggested pairing: the class learners who have not answered, in name order, each taking a
 * study learner from a different band while there are bands left, then the rest in turn.
 */
export function suggestStandIns(
  classLearners: { student_id: string; full_name: string; answered: boolean }[],
  studyLearners: StudyLearnerResult[],
  count = 3,
): StandInPair[] {
  const free = classLearners
    .filter((learner) => !learner.answered)
    .sort((a, b) => a.full_name.localeCompare(b.full_name))
    .slice(0, count);
  const onePerBand = BAND_ORDER.flatMap((band) => {
    const found = studyLearners.find((learner) => learner.band === band);
    return found ? [found] : [];
  });
  const rest = studyLearners.filter((learner) => !onePerBand.includes(learner));
  const order = [...onePerBand, ...rest];
  return free.flatMap((learner, at) =>
    order[at] ? [{ studentId: learner.student_id, studyStudentId: order[at].student_id }] : [],
  );
}
