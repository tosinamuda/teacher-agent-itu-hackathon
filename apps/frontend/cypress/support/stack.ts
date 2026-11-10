/**
 * What the full-path specs share: who is signed in, the API they poll, and the run they
 * hand from one spec to the next.
 */

export type Code = string;

export const env = (name: string, fallback?: string): string => {
  const value = (Cypress.env(name) as string | undefined) ?? fallback;
  if (!value) throw new Error(`Set CYPRESS_${name}.`);
  return value;
};

export const api = (): string => env("API_URL", "http://localhost:8010");
export const teacher = (): Code => env("TEACHER_CODE", "teacher-1");
export const researcher = (): Code => env("RESEARCHER_CODE", "researcher");
export const rater = (): Code => env("RATER_CODE", "rater-1");
export const students = (): Code[] =>
  env("STUDENT_CODES", "student-1,student-2,student-3").split(",");

/** Signs a page in as `code` before it loads. */
export const as = (code: Code) => ({
  onBeforeLoad: (win: Window) => win.localStorage.setItem("teacher_code", code),
});

export const get = <T extends object = object>(path: string, code: Code): Cypress.Chainable<T> =>
  cy
    .request<T>({ url: `${api()}${path}`, headers: { "x-teacher-code": code } })
    .its("body");

export const post = <T extends object = object>(path: string, code: Code, body?: unknown): Cypress.Chainable<T> =>
  cy
    .request<T>({
      method: "POST",
      url: `${api()}${path}`,
      headers: { "x-teacher-code": code },
      body: body ?? {},
    })
    .its("body");

/** Polls `read` until `done` holds, failing after `timeoutMs`. */
export const until = <T>(
  read: () => Cypress.Chainable<T>,
  done: (value: T) => boolean,
  timeoutMs: number,
  label: string,
): Cypress.Chainable<T> => {
  const started = Date.now();
  const attempt = (): Cypress.Chainable<T> =>
    read().then((value) => {
      if (done(value)) return cy.wrap(value, { log: false });
      if (Date.now() - started > timeoutMs) throw new Error(`Timed out waiting for ${label}.`);
      cy.wait(5000, { log: false });
      return attempt();
    });
  return attempt();
};

/** Each generation step gets this long: a plan or a class note takes one to three minutes. */
export const GENERATION_MS = 8 * 60 * 1000;

/** The run the everyday spec leaves for the research spec. */
export type Run = {
  experimentId: string;
  planVersionId: string;
  studentIds: string[];
};

export const RUN_FILE = "cypress/fixtures/e2e-run.json";
