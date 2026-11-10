import type { EngineManifest } from "./types";

export type ExamQuestion = {
  question: string;
  marks: number | null;
  answer: string;
  markingScheme: string;
};

export type ObjectiveQuestions = {
  unitId: string;
  /** The objective the questions are for. */
  label: string;
  questions: ExamQuestion[];
  totalMarks: number;
};

const text = (value: unknown): string =>
  typeof value === "string" ? value.trim() : "";

const marksOf = (value: unknown): number | null =>
  typeof value === "number" && Number.isFinite(value) ? value : null;

/** The exam questions of a draft, one group for each objective, in the order written. */
export function questionsByObjective(
  manifest: EngineManifest,
): ObjectiveQuestions[] {
  return manifest.sections.map((section) => {
    const written = (section.part as { questions?: unknown }).questions;
    const questions = (Array.isArray(written) ? written : [])
      .filter(
        (entry): entry is Record<string, unknown> =>
          typeof entry === "object" && entry !== null,
      )
      .map((entry) => ({
        question: text(entry.question),
        marks: marksOf(entry.marks),
        answer: text(entry.answer),
        markingScheme: text(entry.marking_scheme),
      }));
    return {
      unitId: section.unit_id,
      label: section.label,
      questions,
      totalMarks: questions.reduce(
        (sum, question) => sum + (question.marks ?? 0),
        0,
      ),
    };
  });
}

/** "2 marks", or "1 mark". */
export const marksText = (marks: number): string =>
  `${marks} ${marks === 1 ? "mark" : "marks"}`;
