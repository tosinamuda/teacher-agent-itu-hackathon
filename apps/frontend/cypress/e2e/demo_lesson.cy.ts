/**
 * Records the lesson the defence demo plays, from the study's real lesson `study-t2-w09`
 * (Week 9, simplification of algebraic expressions): its own plan, entered by hand, and the
 * classwork results of three of its real learners, one in each band. The materials are then made
 * by the real engine in the browser against the real backend, database, jobs and model.
 *
 * The experiment already holds the study's plan (entered through the manual-plan route). The
 * spec accepts it, then:
 *
 *   - makes the lesson note, revises it with feedback and approves it;
 *   - makes the class test and sends it, and makes the class revision note;
 *   - records each learner's real classwork result on their behalf (what the study's marking
 *     gave them for the first objective: 4 of 4, 2 of 3, 0 of 4);
 *   - approves the class note, so each learner's own note is written, and approves those notes;
 *   - makes the slide deck and leaves it pending, so the demo can approve it.
 *
 *   CYPRESS_EXPERIMENT_ID=EXP-... \
 *   CYPRESS_API_URL=https://lpcg-staging-api.tosinamuda.com/api \
 *   CYPRESS_BASE_URL=https://lpcg-staging.tosinamuda.com \
 *   npx cypress run --browser electron --spec cypress/e2e/demo_lesson.cy.ts
 *
 * Each step looks at the lesson first and does only what is not done, so a run that stopped can be
 * run again and carries on from where it was. The run it makes is written to
 * cypress/fixtures/demo-lesson-run.json.
 */

import {
  api,
  as,
  env,
  GENERATION_MS,
  get,
  students,
  teacher,
  until,
} from "../support/stack";

type Summary = { plan_version_id: string | null };
type Plan = {
  session_plan: { lesson_plan_objectives: { lesson_objective_id: string }[] };
};
type GenerationStatus = { student_id: string; status: string };
type PendingPack = { artefact_id: string; plan_version_id: string };
type Me = { student_id: string | null };

/** One real learner of the study lesson, and the student account that stands in for them. */
type RealLearner = {
  studied: string;
  band: string;
  score: number;
  outOf: number;
};

/**
 * What the study's marking gave each learner on the lesson's first objective (4 marked
 * classwork questions; one of ST-STUDY-03's was unmarked), in the order of `students()`.
 */
const LEARNERS: RealLearner[] = [
  { studied: "ST-STUDY-09", band: "extend", score: 4, outOf: 4 },
  { studied: "ST-STUDY-03", band: "reinforce", score: 2, outOf: 3 },
  { studied: "ST-STUDY-06", band: "remediate", score: 0, outOf: 4 },
];

const RUN_FILE = "cypress/fixtures/demo-lesson-run.json";

const run: { experimentId: string; planVersionId?: string; deckId?: string } = {
  experimentId: env("EXPERIMENT_ID"),
};
const lessonPage = () =>
  `/research/teacher/experiment-plans/${run.experimentId}`;

/** Opens the lesson page and waits until its checklist has been drawn. */
const openLesson = (): void => {
  cy.visit(lessonPage(), as(teacher()));
  cy.contains("Set up the lesson plan", { timeout: 60000 }).should(
    "be.visible",
  );
};

/** Whether the page has a button or link with this text now. */
const has = (
  selector: "button" | "a",
  text: string,
): Cypress.Chainable<boolean> =>
  cy
    .get("body")
    .then(
      ($body) =>
        $body
          .find(selector)
          .filter((_, element) => element.textContent?.includes(text) ?? false)
          .length > 0,
    );

/** Sends the feedback, and sends it again when the revision fails, up to three times. */
const reviseWithFeedback = (attempt = 1): void => {
  cy.contains("button", "Send revision").click();
  cy.get("body", { timeout: GENERATION_MS }).should(($body) => {
    const text = $body.text();
    expect(
      text.includes("Version 2") || text.includes("The revision failed"),
      "the revision ended",
    ).to.eq(true);
  });
  cy.get("body").then(($body) => {
    if (!$body.text().includes("Version 2") && attempt < 3)
      reviseWithFeedback(attempt + 1);
  });
};

describe("Demo lesson: the study's own lesson and learners, recorded end to end", () => {
  it("the teacher reviews the entered plan and accepts it", () => {
    cy.visit(`${lessonPage()}/plan`, as(teacher()));
    has("button", "Accept the plan").then((open) => {
      if (!open) return;
      cy.contains("Lesson plan objectives", { matchCase: false }).should(
        "be.visible",
      );
      cy.contains("button", "Accept the plan").click();
      cy.location("pathname").should("eq", lessonPage());
    });
    get<Summary>(`/experiments/${run.experimentId}/summary`, teacher()).then(
      (summary) => {
        expect(summary.plan_version_id).to.be.a("string");
        run.planVersionId = summary.plan_version_id as string;
      },
    );
  });

  it("the teacher creates the lesson note, revises it with feedback, and approves it", () => {
    openLesson();
    cy.contains("li", "Lesson note").then(($row) => {
      if ($row.text().includes("Approved")) return;
      if (
        $row.find("button").filter((_, b) => b.textContent === "Create it")
          .length > 0
      ) {
        cy.wrap($row).contains("button", "Create it").click();
      }
      cy.contains("a", "Review the lesson note", {
        timeout: GENERATION_MS,
      }).click();
      cy.contains("Your decision", { timeout: 60000 }).should("be.visible");
      cy.get("body").then(($body) => {
        if ($body.text().includes("Version 2")) return;
        cy.contains("summary", "Revise with feedback").click();
        cy.get("#content-feedback")
          .clear()
          .type("Add one more short worked example to the first step.");
        reviseWithFeedback();
      });
      cy.contains("button", /^Approve$/).click();
      cy.contains("Approved").should("be.visible");
    });
  });

  it("the teacher creates the class test and sends it", () => {
    openLesson();
    has("button", "Create the assessment").then((open) => {
      if (open) cy.contains("button", "Create the assessment").click();
    });
    has("button", "Send the assessment to students").then((open) => {
      if (open) {
        cy.contains("button", "Send the assessment to students", {
          timeout: GENERATION_MS,
        }).click();
      }
    });
    cy.contains("Sent to students", { timeout: GENERATION_MS }).should(
      "be.visible",
    );
  });

  it("the teacher builds the class revision note", () => {
    openLesson();
    has("button", "Create the class revision note").then((open) => {
      if (open) cy.contains("button", "Create the class revision note").click();
    });
    cy.contains(/Class revision note · (awaiting you|approved)/i, {
      timeout: GENERATION_MS,
    }).should("be.visible");
  });

  it("each learner's real classwork result is recorded on their behalf", () => {
    get<Plan>(`/artefacts/lesson-plans/${run.planVersionId}`, teacher()).then(
      ({ session_plan }) => {
        const objective =
          session_plan.lesson_plan_objectives[0].lesson_objective_id;
        students()
          .slice(0, LEARNERS.length)
          .forEach((code, index) => {
            const learner = LEARNERS[index];
            get<Me>("/auth/me", code).then(({ student_id }) => {
              cy.request({
                method: "POST",
                url: `${api()}/assessments/exit-assessment/${run.planVersionId}/responses/manual`,
                headers: { "x-teacher-code": teacher() },
                failOnStatusCode: false,
                body: {
                  student_id,
                  objective_scores: [
                    {
                      lesson_objective_id: objective,
                      score: learner.score,
                      max_score: learner.outOf,
                    },
                  ],
                },
              }).then(({ status }) => {
                // 409 is a result already recorded by an earlier run.
                expect([200, 201, 409], "the result was recorded").to.include(
                  status,
                );
              });
            });
          });
      },
    );
  });

  it("the teacher approves the class note; each learner's note is written and approved", () => {
    const taken = LEARNERS.length;
    openLesson();
    cy.contains("a", "Review the revision note", {
      timeout: GENERATION_MS,
    }).click();
    cy.get("body", { timeout: 60000 }).should(($body) => {
      expect($body.text(), "the review page has loaded").to.match(
        /Approve|Approved/,
      );
    });
    has("button", "Approve").then((open) => {
      if (open) cy.contains("button", /^Approve$/).click();
    });
    until(
      () =>
        get<GenerationStatus[]>(
          `/artefacts/post-class-review-packs/generation-statuses?plan_version_id=${run.planVersionId}`,
          teacher(),
        ),
      (rows) => {
        const failed = rows.find((row) => row.status === "failed");
        if (failed)
          throw new Error(`A learner's note failed: ${failed.student_id}`);
        return (
          rows.length === taken &&
          rows.every((row) => row.status === "succeeded")
        );
      },
      GENERATION_MS * 2,
      "every learner's note",
    );
    get<PendingPack[]>(
      "/artefacts/post-class-review-packs/pending",
      teacher(),
    ).then((packs) => {
      const ours = packs.filter(
        (pack) => pack.plan_version_id === run.planVersionId,
      );
      expect(ours).to.have.length(taken);
      ours.forEach((pack) => {
        cy.visit(
          `/research/teacher/pack-reviews/${pack.artefact_id}`,
          as(teacher()),
        );
        cy.contains("button", /^Approve$/).click();
        cy.contains("Approved").should("be.visible");
      });
    });
  });

  it("the teacher makes the slide deck, sends feedback on it, and leaves it for review", () => {
    openLesson();
    cy.contains("li", "Slides").then(($row) => {
      if (
        $row.find("button").filter((_, b) => b.textContent === "Create it")
          .length > 0
      ) {
        cy.wrap($row).contains("button", "Create it").click();
      }
    });
    cy.contains("li", "Slides")
      .contains("a", "Review it", { timeout: GENERATION_MS })
      .click();
    cy.contains("Your decision", { timeout: 60000 }).should("be.visible");
    cy.location("pathname").then((path) => {
      run.deckId = path.split("/").pop();
    });
    cy.get("body").then(($body) => {
      if ($body.text().includes("Version 2")) return;
      cy.contains("summary", "Revise with feedback").click();
      cy.get("#content-feedback")
        .clear()
        .type(
          "Shorten the speaker notes on the second slide to two sentences.",
        );
      reviseWithFeedback();
    });
    cy.writeFile(RUN_FILE, run);
  });
});
