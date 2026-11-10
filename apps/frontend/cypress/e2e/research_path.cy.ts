/**
 * The research path on the lesson the everyday spec played: H2 over its focal learners,
 * packet export for H1 and H2, a rater assigned and scoring a blinded packet, and the
 * results de-blinding that score. Real backend, database, jobs and model.
 *
 *   CYPRESS_API_URL=http://localhost:8010 CYPRESS_BASE_URL=http://localhost:3000 \
 *   npx cypress run --spec cypress/e2e/research_path.cy.ts
 *
 * It reads cypress/fixtures/e2e-run.json, which everyday_path.cy.ts writes;
 * CYPRESS_EXPERIMENT_ID names another experiment whose class note is approved.
 */

import {
  as,
  env,
  GENERATION_MS,
  get,
  rater,
  researcher,
  Run,
  RUN_FILE,
  until,
} from "../support/stack";

type Summary = {
  h2_summary: { latest_execution_status: string | null };
};
type Export = { packets: { evaluation_packet_id: string }[] };

const CONDITION_CODE = /\b(C[0-4]|P[01])\b/;
let experimentId = "";
let h1PacketIds: string[] = [];
const experimentPage = (tab: string) => `/research/experiments/${experimentId}/${tab}`;

describe("Research path: H2, packets, a blinded rating, and the results", () => {
  before(() => {
    const named = Cypress.env("EXPERIMENT_ID") as string | undefined;
    if (named) {
      experimentId = named;
      return;
    }
    cy.readFile<Run>(RUN_FILE).then((run) => {
      experimentId = run.experimentId;
    });
  });

  it("the researcher chooses the focal learners and generates P0 and P1", () => {
    cy.visit(experimentPage("h2"), as(researcher()));
    cy.contains("Save focal learners").should("be.visible");
    cy.get("input[type=checkbox]:not(:disabled)").check();
    cy.contains("button", "Save focal learners").click();
    cy.contains(/[1-9]\d* saved/).should("be.visible");
    cy.contains("button", "Generate P0 / P1").click();
    until(
      () => get<Summary>(`/experiments/${experimentId}/summary`, researcher()),
      ({ h2_summary }) => {
        const status = h2_summary.latest_execution_status ?? "";
        if (/fail/i.test(status)) throw new Error(`H2 ended ${status}.`);
        return status === "succeeded";
      },
      GENERATION_MS,
      "H2",
    );
  });

  it("the researcher exports the rater packets for H1 and H2", () => {
    cy.visit(experimentPage("h2"), as(researcher()));
    cy.contains("button", "Export packets").click();
    cy.contains(/[1-9]\d* packets? ready for raters/).should("be.visible");
    cy.visit(experimentPage("h1"), as(researcher()));
    cy.contains("Teacher approved", { matchCase: false }).should("be.visible");
    cy.intercept("POST", "**/packets/export").as("export");
    cy.contains("button", "Export packets").click();
    cy.wait("@export")
      .its("response.body")
      .then((body: Export) => {
        h1PacketIds = body.packets.map((packet) => packet.evaluation_packet_id);
        expect(h1PacketIds).to.have.length.greaterThan(0);
      });
    cy.contains(/[1-9]\d* packets? ready for raters/).should("be.visible");
  });

  it("the researcher assigns a rater to everything", () => {
    cy.visit(experimentPage("raters"), as(researcher()));
    cy.get("main select").first().select(env("RATER_NAME", "Rater One"));
    cy.contains("button", "Assign to everything").click();
    cy.contains(/[1-3] \/ 3 raters/).should("be.visible");
  });

  it("the rater scores one of this lesson's blinded packets", () => {
    cy.visit(`/research/rater/h1/${h1PacketIds[0]}`, as(rater()));
    cy.contains("button", "Start review").should("be.visible");
    cy.get("body").invoke("text").should("not.match", CONDITION_CODE);
    cy.contains("button", "Start review").click();
    cy.get("button").filter((_, el) => el.innerText.trim() === "4").click({ multiple: true });
    cy.location("pathname").then((packetPath) => {
      cy.contains("button", "Save & open next revision note").click();
      cy.location("pathname").should("not.eq", packetPath);
    });
  });

  it("the results de-blind the rating", () => {
    cy.visit(experimentPage("results"), as(researcher()));
    cy.contains(/H1: \d\.\d\d \([1-9]\d* ratings?\)/).should("be.visible");
  });
});
