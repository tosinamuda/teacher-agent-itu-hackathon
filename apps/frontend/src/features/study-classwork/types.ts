export type ClassworkQuestion = {
  n: number;
  lesson_objective_id: string;
  text: string;
  answer: string | null;
  /** Where the answer came from: the teacher's correction, or derived by the researcher. */
  answer_source: string | null;
};

export type ClassworkAnswer = {
  n: number;
  mark: "correct" | "incorrect" | "unmarked" | string;
  /** The transcriber could not read the teacher's mark with certainty. */
  uncertain: boolean;
  working: string;
  misconception_code: string | null;
  misconception_why: string | null;
};

/** A lesson's classwork questions, and one learner's marked script if they sat it. */
export type LearnerClasswork = {
  questions: ClassworkQuestion[];
  script: { teacher_total: string; capture_complete: boolean; answers: ClassworkAnswer[] } | null;
};
