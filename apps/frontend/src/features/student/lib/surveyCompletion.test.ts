import { describe, expect, it } from "vitest";

import { isSurveyComplete } from "@/features/student/lib/surveyCompletion";

const answered = {
  survey: [
    { confidence: 3 as const, perceived_difficulty: 2 as const },
    { confidence: 4 as const, perceived_difficulty: 3 as const },
  ],
  session: { interest: 5 as const, affect: 3 as const },
};

describe("isSurveyComplete", () => {
  it("is complete when every question has an answer", () => {
    expect(isSurveyComplete(answered)).toBe(true);
  });

  it("is incomplete while any objective question is unanswered", () => {
    const survey = [
      answered.survey[0],
      { confidence: 4 as const, perceived_difficulty: null },
    ];
    expect(isSurveyComplete({ ...answered, survey })).toBe(false);
  });

  it("is incomplete while a session question is unanswered", () => {
    expect(
      isSurveyComplete({ ...answered, session: { interest: 5, affect: null } }),
    ).toBe(false);
  });
});
