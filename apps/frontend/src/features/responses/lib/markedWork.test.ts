import { describe, expect, it } from "vitest";

import {
  hasMarks,
  misconceptionCode,
  NOT_MARKED,
  toMarkedWork,
  type WorkedQuestion,
} from "./markedWork";

const question = (
  id: string,
  text = "$4n + 3n \\times 10$",
): WorkedQuestion => ({
  id,
  lesson_objective_id: "lo-1",
  question: text,
  model_answer: "$34n$",
});

describe("misconceptionCode", () => {
  it("names a mistake in snake_case", () => {
    expect(misconceptionCode("Adds before multiplying")).toBe(
      "adds_before_multiplying",
    );
    expect(misconceptionCode("  Drops the variable! ")).toBe(
      "drops_the_variable",
    );
  });

  it("gives no code for words with no letters to start it", () => {
    expect(misconceptionCode("")).toBeNull();
    expect(misconceptionCode("123")).toBeNull();
  });
});

describe("toMarkedWork", () => {
  it("keeps the misconception only for a question marked incorrect", () => {
    const work = toMarkedWork(
      [question("a"), question("b", "$32 + 8x \\div 2$")],
      {
        a: {
          mark: "incorrect",
          working: "  $7n \\times 10 = 70n$ ",
          misconception: "Adds before multiplying",
          explanation: " Adds 4n and 3n first. ",
        },
        b: {
          mark: "correct",
          working: "",
          misconception: "ignored",
          explanation: "ignored",
        },
      },
    );

    expect(work[0]).toMatchObject({
      mark: "incorrect",
      working: "$7n \\times 10 = 70n$",
      misconception_code: "adds_before_multiplying",
      misconception_why: "Adds 4n and 3n first.",
    });
    expect(work[1]).toMatchObject({
      mark: "correct",
      misconception_code: null,
    });
    expect(work[1].misconception_why).toBeNull();
  });

  it("leaves a question nobody marked as not marked", () => {
    expect(toMarkedWork([question("a")], {})[0].mark).toBe(NOT_MARKED.mark);
  });

  it("drops a question with no text or no objective", () => {
    const blank = { ...question("a", "  ") };
    const untagged = { ...question("b"), lesson_objective_id: "" };

    expect(toMarkedWork([blank, untagged], {})).toEqual([]);
  });
});

describe("hasMarks", () => {
  it("needs a question marked right or wrong", () => {
    expect(hasMarks(toMarkedWork([question("a")], {}))).toBe(false);
    expect(
      hasMarks(
        toMarkedWork([question("a")], {
          a: { ...NOT_MARKED, mark: "correct" },
        }),
      ),
    ).toBe(true);
  });
});
