import type { MarkedWork, Mark } from "../api/onBehalf";

/** One question of the classwork, entered once and marked for each student. */
export type WorkedQuestion = {
  id: string;
  lesson_objective_id: string;
  question: string;
  model_answer: string;
};

/** How one student's work on one question was marked. */
export type WorkMark = {
  mark: Mark;
  working: string;
  /** The mistake the working shows, in the teacher's words. */
  misconception: string;
  explanation: string;
};

export const NOT_MARKED: WorkMark = {
  mark: "unmarked",
  working: "",
  misconception: "",
  explanation: "",
};

/** A short snake_case name for a mistake: "Adds before multiplying" is `adds_before_multiplying`. */
export const misconceptionCode = (words: string): string | null => {
  const code = words
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "");
  return /^[a-z]/.test(code) ? code : null;
};

/** The marks to send: one entry for each question that has text. */
export const toMarkedWork = (
  questions: WorkedQuestion[],
  marks: Record<string, WorkMark>,
): MarkedWork[] =>
  questions
    .filter(
      (question) => question.question.trim() && question.lesson_objective_id,
    )
    .map((question) => {
      const given = marks[question.id] ?? NOT_MARKED;
      const missed = given.mark === "incorrect";
      return {
        lesson_objective_id: question.lesson_objective_id,
        question: question.question.trim(),
        model_answer: question.model_answer.trim(),
        mark: given.mark,
        working: given.working.trim(),
        misconception_code: missed
          ? misconceptionCode(given.misconception)
          : null,
        misconception_why:
          missed && given.explanation.trim() ? given.explanation.trim() : null,
      };
    });

/** Marked work can be saved once a question has been marked right or wrong. */
export const hasMarks = (work: MarkedWork[]): boolean =>
  work.some((entry) => entry.mark !== "unmarked");
