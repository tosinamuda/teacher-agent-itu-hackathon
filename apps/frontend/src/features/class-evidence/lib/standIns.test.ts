import { expect, it } from "vitest";

import type { StudyLearnerResult } from "../api/studyResults";
import { suggestStandIns } from "./standIns";

const study = (id: string, band: StudyLearnerResult["band"]) =>
  ({ student_id: id, full_name: id, band }) as StudyLearnerResult;
const learner = (id: string, name: string, answered = false) => ({
  student_id: id,
  full_name: name,
  answered,
});

it("pairs the learners who have not answered with one study learner from each band", () => {
  const pairs = suggestStandIns(
    [learner("S3", "Student Three"), learner("S1", "Student One"), learner("S2", "Student Two"), learner("S9", "Ada", true)],
    [study("a", "remediate"), study("b", "reinforce"), study("c", "extend"), study("d", "extend")],
  );

  expect(pairs).toEqual([
    { studentId: "S1", studyStudentId: "c" },
    { studentId: "S3", studyStudentId: "b" },
    { studentId: "S2", studyStudentId: "a" },
  ]);
});

it("suggests nothing when every learner has answered", () => {
  expect(suggestStandIns([learner("S1", "One", true)], [study("a", "extend")])).toEqual([]);
});
