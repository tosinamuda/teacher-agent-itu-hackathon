/**
 * The everyday path, from a lesson with no plan to a student reading their own revision note,
 * in the browser against the real backend, database, jobs and model.
 *
 *   CYPRESS_API_URL=http://localhost:8010 CYPRESS_BASE_URL=http://localhost:3000 \
 *   npx cypress run --spec cypress/e2e/everyday_path.cy.ts
 *
 * A researcher opens a sandbox experiment on a lesson of the teacher's First Term workspace
 * (CYPRESS_LESSON_ID picks it; otherwise one at random). The run it makes is written to
 * cypress/fixtures/e2e-run.json for research_path.cy.ts.
 */

import {
  as,
  GENERATION_MS,
  get,
  post,
  researcher,
  Run,
  RUN_FILE,
  students,
  teacher,
  until,
} from "../support/stack";

type Workspace = { id: string; name: string };
type Lesson = { lesson_period_id: string; lesson_title: string; under_research_study: boolean };
type Summary = {
  plan_version_id: string | null;
  readiness: { base_pack_ready: boolean };
};
type GenerationStatus = { student_id: string; status: string };
type PendingPack = { artefact_id: string; plan_version_id: string; learner_name?: string | null };
type Me = { student_id: string | null };

type Study = { investigation_id: string; investigation_code: string; title: string };

/** Where the run files its experiment: an earlier run's study, else a new one of its own. */
const E2E_STUDY = "End-to-end test runs";

/**
 * The study an experiment is filed under. A database that was migrated from before studies
 * existed has an Unfiled study; a new one has none, so the run makes its own, once.
 */
const study = (): Cypress.Chainable<string> =>
  get<Study[]>("/experiments/investigations", researcher()).then((studies) => {
    const found =
      studies.find((s) => s.investigation_code === "INV-UNFILED") ??
      studies.find((s) => s.title === E2E_STUDY);
    if (found) return cy.wrap(found.investigation_id, { log: false });
    return post<Study>("/experiments/investigations", researcher(), {
      title: E2E_STUDY,
      description: "Experiments the end-to-end specs make.",
    }).then((made) => made.investigation_id);
  });

const RAW_LATEX = /\\(frac|times|div|text)\b|\$\$/;
const run: Partial<Run> = { studentIds: [] };
const lessonPage = () => `/research/teacher/experiment-plans/${run.experimentId}`;

describe("Everyday path: a lesson from no plan to a student's own revision note", () => {
  before(() => {
    get<Workspace[]>("/teaching/workspaces", teacher()).then((workspaces) => {
      const workspace = workspaces.find((w) => /First Term/.test(w.name)) ?? workspaces[0];
      get<Lesson[]>(`/experiments/workspaces/${workspace.id}/lessons`, researcher()).then(
        (lessons) => {
          const open = lessons.filter((l) => !l.under_research_study);
          const chosen =
            open.find((l) => l.lesson_period_id === Cypress.env("LESSON_ID")) ??
            open[Math.floor(Math.random() * open.length)];
          cy.log(`Lesson: ${chosen.lesson_title}`);
          study().then((investigationId) => {
            post<{ experiment_id: string }>("/experiments", researcher(), {
              investigation_id: investigationId,
              teacher_workspace_id: workspace.id,
              lesson_period_id: chosen.lesson_period_id,
            }).then(({ experiment_id }) => {
              run.experimentId = experiment_id;
              post(`/experiments/${experiment_id}/sandbox`, researcher(), { is_sandbox: true });
            });
          });
        },
      );
    });
  });

  it("the teacher authors the plan and accepts it", () => {
    cy.visit(lessonPage(), as(teacher()));
    cy.contains("button", "Author the plan").click();
    cy.location("pathname", { timeout: GENERATION_MS }).should("match", /\/plan$/);
    cy.contains("Lesson plan objectives", { matchCase: false }).should("be.visible");
    cy.get("main").should("not.contain.text", ".; ");
    cy.contains("button", "Accept the plan").click();
    cy.location("pathname").should("eq", lessonPage());
    get<Summary>(`/experiments/${run.experimentId}/summary`, teacher()).then((summary) => {
      expect(summary.plan_version_id).to.be.a("string");
      run.planVersionId = summary.plan_version_id as string;
    });
  });

  it("the teacher creates the lesson note, revises it with feedback, and approves it", () => {
    cy.visit(lessonPage(), as(teacher()));
    cy.contains("button", "Create the lesson note").click();
    cy.contains("a", "Review the lesson note", { timeout: GENERATION_MS }).click();
    cy.contains("Version 1").should("be.visible");
    cy.contains("summary", "Revise with feedback").click();
    cy.get("#content-feedback").type("Add one more short worked example to the first step.");
    cy.contains("button", "Send revision").click();
    cy.contains("Version 2", { timeout: GENERATION_MS }).should("be.visible");
    cy.contains("button", /^Approve$/).click();
    cy.contains("Approved version 2").should("be.visible");
    cy.contains("Version 2").should("be.visible");
    cy.contains("Version 3").should("not.exist");
    cy.contains("button", "← Back").click();
    cy.location("pathname").should("eq", lessonPage());
  });

  it("the teacher creates the class test and sends it", () => {
    cy.visit(lessonPage(), as(teacher()));
    cy.contains("button", "Create the assessment").click();
    cy.contains("button", "Send the assessment to students", { timeout: GENERATION_MS }).click();
    cy.contains("Sent to students").should("be.visible");
  });

  it("the teacher builds the class revision note, and the page follows the build", () => {
    cy.visit(lessonPage(), as(teacher()));
    cy.contains("Made by “Create the class revision note” above").should("be.visible");
    cy.contains("button", "Create the class revision note").click();
    cy.contains(/Class revision note · preparing/i).should("be.visible");
    cy.contains(/Class revision note · awaiting you/i, { timeout: GENERATION_MS }).should(
      "be.visible",
    );
  });

  it("each student takes the class test and the survey, and a revisit shows it was taken", () => {
    students().forEach((code, index) => {
      get<Me>("/auth/me", code).then(({ student_id }) => {
        run.studentIds?.push(student_id as string);
      });
      const exitPage = `/research/student/exit-assessment?plan_version_id=${run.planVersionId}`;
      cy.visit(exitPage, as(code));
      cy.get("input[type=radio]").then(($radios) => {
        const questions = [...new Set($radios.toArray().map((radio) => radio.getAttribute("name")))];
        questions.forEach((name, question) => {
          const letter = "ABCD"[(index + question) % 4];
          cy.get(`input[type=radio][name="${name}"][value="${letter}"]`).check();
        });
      });
      cy.contains("button", "Submit my answers").click();
      cy.contains("Your answers are in").should("be.visible");
      cy.contains("button", "Send my survey").should("be.disabled");
      cy.get("main select").each(($select, question) => {
        cy.wrap($select).select(String(((index + question) % 5) + 1));
      });
      cy.contains("button", "Send my survey").click();
      cy.contains("Recorded ✓").should("be.visible");
      cy.get("main").should("not.contain.text", "lop0");
      cy.visit(exitPage, as(code));
      cy.contains("You have already taken this assessment.").should("be.visible");
    });
  });

  it("the teacher approves the class note; each student's note is written, named, and approved", () => {
    cy.visit(lessonPage(), as(teacher()));
    cy.contains("a", "Review the revision note").click();
    cy.get("main").should("not.contain.text", "awaiting a pack");
    cy.contains("button", /^Approve$/).click();
    until(
      () =>
        get<GenerationStatus[]>(
          `/artefacts/post-class-review-packs/generation-statuses?plan_version_id=${run.planVersionId}`,
          teacher(),
        ),
      (rows) => {
        const failed = rows.find((row) => row.status === "failed");
        if (failed) throw new Error(`A student's note failed: ${failed.student_id}`);
        return (
          rows.length === students().length && rows.every((row) => row.status === "succeeded")
        );
      },
      GENERATION_MS * 2,
      "every student's note",
    );
    cy.visit("/research/teacher/pack-reviews", as(teacher()));
    cy.get("main").should("not.contain.text", "Student: ST-");
    get<PendingPack[]>("/artefacts/post-class-review-packs/pending", teacher()).then((packs) => {
      const ours = packs.filter((pack) => pack.plan_version_id === run.planVersionId);
      expect(ours).to.have.length(students().length);
      ours.forEach((pack) => {
        expect(pack.learner_name).to.be.a("string").and.not.match(/^ST-/);
        cy.visit(`/research/teacher/pack-reviews/${pack.artefact_id}`, as(teacher()));
        cy.contains("button", /^Approve$/).click();
        cy.contains("Approved").should("be.visible");
      });
    });
  });

  it("a student reads the note written for them", () => {
    const code = students()[students().length - 1];
    cy.visit(`/research/student/lesson/${run.planVersionId}`, as(code));
    cy.contains("a", "Read your revision note").click();
    cy.location("pathname").should("eq", "/research/student/pack-runner");
    cy.contains("Section 1").should("be.visible");
    cy.get("main").invoke("prop", "innerText").should("not.match", RAW_LATEX);
    cy.get("main .katex-error").should("not.exist");
    cy.writeFile(RUN_FILE, run);
  });
});
