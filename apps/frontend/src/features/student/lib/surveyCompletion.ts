import type { SurveyScale } from "@/features/student/api/exitAssessment";

type Answered = {
  survey: {
    confidence: SurveyScale | null;
    perceived_difficulty: SurveyScale | null;
  }[];
  session: { interest: SurveyScale | null; affect: SurveyScale | null };
};

/** True once the student has chosen an answer to every survey question. */
export const isSurveyComplete = ({ survey, session }: Answered): boolean =>
  survey.every(
    (row) => row.confidence !== null && row.perceived_difficulty !== null,
  ) &&
  session.interest !== null &&
  session.affect !== null;
