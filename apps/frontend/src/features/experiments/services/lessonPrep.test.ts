import { describe, expect, it } from "vitest";

import type { ExperimentReadiness, ExperimentSummary } from "../lib/experiments";
import { buildLessonPrepSteps } from "./lessonPrep";

const lesson = (readiness: Partial<ExperimentReadiness>): ExperimentSummary =>
  ({
    experiment_id: "EXP-1",
    plan_version_id: "LPV-1",
    baseline_approved_by: "Teacher One",
    h1_summary: { execution_count: 0 },
    readiness: {
      lesson_approved: true,
      baseline_selected: true,
      h1_ready: false,
      base_pack_ready: false,
      learner_evidence_ready: false,
      h2_ready: false,
      ...readiness,
    },
  }) as unknown as ExperimentSummary;

const statusOf = (steps: ReturnType<typeof buildLessonPrepSteps>, title: string) =>
  steps.find((step) => step.title === title);

describe("buildLessonPrepSteps", () => {
  it("asks for the lesson note once the plan is accepted, before the class revision note", () => {
    const steps = buildLessonPrepSteps(lesson({}));

    expect(steps.map((step) => step.title).slice(2, 5)).toEqual([
      "Create the lesson note",
      "Review & accept the lesson note",
      "Create the class revision note",
    ]);
    expect(statusOf(steps, "Create the lesson note")?.status).toBe("current");
    expect(statusOf(steps, "Create the class revision note")?.status).toBe("upcoming");
  });

  it("sends the teacher to review a created note, and holds the class note until it is accepted", () => {
    const steps = buildLessonPrepSteps(lesson({ lesson_note_artefact_id: "AT-note" }));

    expect(statusOf(steps, "Review & accept the lesson note")).toMatchObject({
      status: "current",
      href: "/research/teacher/content/AT-note",
    });
    expect(statusOf(steps, "Create the class revision note")?.status).toBe("upcoming");
  });

  it("opens the class revision note once the lesson note is accepted", () => {
    const steps = buildLessonPrepSteps(
      lesson({ lesson_note_artefact_id: "AT-note", lesson_note_approved: true }),
    );

    expect(statusOf(steps, "Review & accept the lesson note")?.status).toBe("done");
    expect(statusOf(steps, "Create the class revision note")?.status).toBe("current");
  });

  describe("students taking the assessment", () => {
    const TAKE = "Students take the assessment";
    const sent = { ready: true, sent: true };

    it("waits until the assessment is sent", () => {
      expect(statusOf(buildLessonPrepSteps(lesson({})), TAKE)?.status).toBe("upcoming");
    });

    it("is current once it is sent, and while only some students have answered", () => {
      const justSent = buildLessonPrepSteps(lesson({}), { made: 0, awaiting: 0 }, sent);
      const someAnswered = buildLessonPrepSteps(lesson({ learner_evidence_ready: true }));

      expect(statusOf(justSent, TAKE)?.status).toBe("current");
      expect(statusOf(someAnswered, TAKE)?.status).toBe("current");
    });

    it("is done once students' notes exist, whether or not they are accepted yet", () => {
      const submitted = lesson({ learner_evidence_ready: true });
      const made = buildLessonPrepSteps(submitted, { made: 3, awaiting: 0 });
      const awaiting = buildLessonPrepSteps(submitted, { made: 0, awaiting: 2 });

      expect(statusOf(made, TAKE)?.status).toBe("done");
      expect(statusOf(awaiting, TAKE)?.status).toBe("done");
    });
  });

  describe("reviewing each student's note", () => {
    const REVIEW = "Review, revise & accept each student's note";
    const submitted = lesson({ learner_evidence_ready: true });

    it("is not done while students have submitted but no note exists", () => {
      const steps = buildLessonPrepSteps(submitted, { made: 0, awaiting: 0 });

      expect(statusOf(steps, REVIEW)?.status).toBe("upcoming");
      expect(statusOf(steps, "Create each student's draft revision note")?.status).toBe("auto");
    });

    it("is current while any student's note awaits the teacher", () => {
      const steps = buildLessonPrepSteps(submitted, { made: 3, awaiting: 1 });

      expect(statusOf(steps, REVIEW)).toMatchObject({
        status: "current",
        href: "/research/teacher/pack-reviews",
      });
    });

    it("is done once the notes exist and every one is accepted", () => {
      const steps = buildLessonPrepSteps(submitted, { made: 3, awaiting: 0 });

      expect(statusOf(steps, REVIEW)?.status).toBe("done");
      expect(statusOf(steps, "Create each student's draft revision note")?.status).toBe("done");
    });
  });
});
