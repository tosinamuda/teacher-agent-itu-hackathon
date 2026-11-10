/**
 * Engine content shown in the page of an MCP server: the content page loads the `ui://` page
 * the server's `show_content` tool is bound to and draws it in a frame of its own, instead of
 * drawing the content with the app's own components.
 *
 *   CYPRESS_API_URL=http://localhost:8010 CYPRESS_BASE_URL=http://localhost:3000 \
 *   npx cypress run --spec cypress/e2e/mcp_app_view.cy.ts
 *
 * It needs the run everyday_path.cy.ts leaves in cypress/fixtures/e2e-run.json, and the lesson
 * note plugin's generator as the lesson note's default on the server. The engine writes another
 * lesson note for that run's plan with the real model, which takes a few minutes.
 */

import {
  as,
  GENERATION_MS,
  get,
  post,
  Run,
  RUN_FILE,
  teacher,
  until,
} from "../support/stack";

type Summary = { id: string; type: string };

/** The built-in type the engine writes through the lesson note plugin's generator. */
const NOTE_TYPE = "lesson-note";
/** The height a frame has before the page it holds has told the host its own. */
const FIRST_HEIGHT = 160;

describe("engine content in the page of an MCP server", () => {
  let contentId = "";

  it("has the engine write a lesson note for the everyday run's plan", () => {
    cy.readFile<Run>(RUN_FILE).then((run) => {
      const planVersionId = encodeURIComponent(run.planVersionId);
      const notes = () =>
        get<Summary[]>(
          `/content?plan_version_id=${planVersionId}&type=${NOTE_TYPE}`,
          teacher(),
        );
      notes().then((before) => {
        const known = new Set(before.map((note) => note.id));
        post("/content", teacher(), {
          plan_version_id: run.planVersionId,
          type: NOTE_TYPE,
        });
        until(
          notes,
          (found) => found.some((note) => !known.has(note.id)),
          GENERATION_MS,
          "the engine's lesson note",
        ).then((found) => {
          contentId = found.find((note) => !known.has(note.id))?.id ?? "";
        });
      });
    });
  });

  it("draws it in a sandboxed frame that holds the server's page", () => {
    cy.visit(`/research/teacher/content/${contentId}`, as(teacher()));

    cy.get('iframe[data-mcp-view="ready"]').as("view");
    cy.get("@view").should("have.attr", "sandbox", "allow-scripts");
    cy.get("@view")
      .its("0.offsetHeight")
      .should("be.greaterThan", FIRST_HEIGHT);
    cy.get('[data-mcp-view="failed"], [data-mcp-view="none"]').should(
      "not.exist",
    );
  });

  it("draws the item again once it is approved", () => {
    cy.visit(`/research/teacher/content/${contentId}`, as(teacher()));
    cy.get('iframe[data-mcp-view="ready"]').should("exist");

    cy.contains("button", "Approve").click();

    cy.contains("Approved").should("be.visible");
    cy.get('iframe[data-mcp-view="ready"]')
      .its("0.offsetHeight")
      .should("be.greaterThan", FIRST_HEIGHT);
  });
});
