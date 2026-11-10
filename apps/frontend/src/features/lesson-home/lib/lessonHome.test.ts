import { expect, it } from "vitest";

import type { ContentSummary, ContentTypeInfo } from "@/features/content/types";
import type { PlanVersionSummary } from "@/features/lesson-plan/hooks/useSessionPlans";

import type { TermClassSubject } from "@/features/curriculum/hooks/useSchemeOfWork";

import {
  approvedVersionOf,
  learnerRows,
  lessonOf,
  materialRows,
  planRow,
  versionsWithMaterials,
  waitingOn,
} from "./lessonHome";

const plan = (status: string, version_id = "LPV-1"): PlanVersionSummary => ({
  plan_id: "LP-1",
  version_id,
  session_id: "S",
  subject: "Maths",
  grade: "JSS1",
  status,
  created_at: "2026-11-01T00:00:00Z",
  approved_at: status === "approved" ? "2026-11-04T10:00:00Z" : undefined,
});
const type = (slug: string, label: string, over: Partial<ContentTypeInfo> = {}): ContentTypeInfo =>
  ({ type: slug, label, made_from_a_plan_version: true, retired: false, ...over }) as ContentTypeInfo;
const item = (slug: string, review_status: string): ContentSummary =>
  ({ id: `C-${slug}`, type: slug, level: "class", review_status, plan_version_id: "LPV-1" }) as ContentSummary;

it("offers to create the plan when the lesson has none", () => {
  const row = planRow([], "S");

  expect(row.status).toBe("notStarted");
  expect(row.action).toEqual({ label: "Create plan", href: "/research/teacher/lessons/S/plan/new", primary: true });
});

it("asks for a review while the latest plan is a draft, and opens an approved plan", () => {
  expect(planRow([plan("draft")], "S").status).toBe("needsYou");

  const approved = planRow([plan("approved")], "S");
  expect(approved.status).toBe("complete");
  expect(approved.detail).toBe("Approved 2026-11-04");
  expect(approved.action).toBeUndefined();
});

it("makes materials from the newest approved version, not from a newer draft", () => {
  const plans = [plan("draft", "LPV-3"), plan("approved", "LPV-2"), plan("approved", "LPV-1")];

  expect(approvedVersionOf(plans)?.version_id).toBe("LPV-2");
});

it("locks every material until the plan is approved", () => {
  const rows = materialRows([type("lesson-note", "Lesson note")], [], null);

  expect(rows.map((row) => row.status)).toEqual(["locked"]);
  expect(rows[0].create).toBeUndefined();
});

it("offers to make a material that is not made, and reads one that is", () => {
  const types = [type("lesson-note", "Lesson note"), type("slide-deck", "Slides"), type("class-test", "Class test")];
  const rows = materialRows(types, [item("slide-deck", "pending"), item("class-test", "approved")], "LPV-1");

  expect(rows[0].create).toEqual({ type: "lesson-note" });
  expect(rows[1].action?.label).toBe("Review");
  expect(rows[2]).toMatchObject({ status: "complete", detail: "Sent to students" });
  expect(waitingOn(rows).map((row) => row.key)).toEqual(["slide-deck"]);
});

it("lists the materials in the order a teacher meets them, others last", () => {
  const types = [
    type("worked-examples", "Worked examples"),
    type("class-test", "Class test"),
    type("slide-deck", "Slides"),
    type("lesson-note", "Lesson note"),
    type("exam-questions", "Exam questions"),
    type("revision-note", "Revision note"),
  ];

  expect(materialRows(types, [], "LPV-1").map((row) => row.key)).toEqual([
    "lesson-note",
    "slide-deck",
    "revision-note",
    "class-test",
    "exam-questions",
    "worked-examples",
  ]);
});

it("leaves out a type that is not made from a plan version, and a retired type with nothing made", () => {
  const types = [type("lesson-plan", "Lesson plan", { made_from_a_plan_version: false }), type("old", "Old", { retired: true })];

  expect(materialRows(types, [], "LPV-1")).toEqual([]);
});

it("shows an engine variant only once it has been made", () => {
  const types = [type("class-test", "Class test"), type("class-test-engine", "Class test (engine)")];

  expect(materialRows(types, [], "LPV-1").map((row) => row.key)).toEqual(["class-test"]);
  expect(materialRows(types, [item("class-test-engine", "pending")], "LPV-1").map((row) => row.key)).toEqual([
    "class-test",
    "class-test-engine",
  ]);
});

it("opens class evidence only once the class test is sent", () => {
  const notes = { made: 0, awaiting: 0 };

  expect(learnerRows([], "P-1", notes)[0].status).toBe("locked");
  expect(learnerRows([item("class-test", "approved")], "P-1", notes)[0].href).toBe("/research/teacher/lessons/P-1/evidence");
});

it("asks for a review when personalised notes wait, and counts the approved ones", () => {
  const waiting = learnerRows([], "P-1", { made: 3, awaiting: 1 })[1];

  expect(waiting).toMatchObject({ status: "needsYou", detail: "2 approved · 1 to review" });
});

it("finds a lesson in the scheme of work, with its week", () => {
  const scheme = {
    weeks: [
      { week_number: 2, title: "Fractions", lesson_periods: [{ id: "P1", title: null, subtopic_title: "Mixed fractions" }] },
    ],
  } as unknown as TermClassSubject;

  expect(lessonOf(scheme, "P1")).toEqual({ title: "Mixed fractions", week: 2 });
  expect(lessonOf(scheme, "missing")).toBeNull();
  expect(lessonOf(undefined, "P1")).toBeNull();
});

it("does not read a rejected or withdrawn version as the plan", () => {
  expect(planRow([plan("rejected")], "S").status).toBe("notStarted");
  expect(planRow([plan("rejected")], "S").detail).toBe("The last plan was rejected");
  expect(planRow([plan("withdrawn")], "S").detail).toBe("The last plan's approval was withdrawn");
  expect(planRow([plan("rejected", "LPV-2"), plan("approved", "LPV-1")], "S").status).toBe("complete");
});

it("keeps the materials already made when the plan's approval is withdrawn", () => {
  const types = [type("lesson-note", "Lesson note"), type("slides", "Slides")];
  const rows = materialRows(types, [item("lesson-note", "approved")], null);

  expect(rows[0]).toMatchObject({ status: "complete", href: "/research/teacher/content/C-lesson-note" });
  expect(rows[1].status).toBe("locked");
});

it("offers to update a material made from an earlier version of the plan", () => {
  const rows = materialRows([type("lesson-note", "Lesson note")], [item("lesson-note", "approved")], "LPV-2");

  expect(rows[0]).toMatchObject({
    status: "needsYou",
    detail: "The plan changed after this was made",
    href: "/research/teacher/content/C-lesson-note",
    create: { type: "lesson-note", label: "Update" },
  });
});

it("reads materials from every version that was ever approved", () => {
  const plans = [plan("draft", "LPV-3"), plan("withdrawn", "LPV-2"), plan("approved", "LPV-1")].map((p, i) => ({
    ...p,
    approved_at: i === 0 ? undefined : "2026-11-04T10:00:00Z",
  }));

  expect(versionsWithMaterials(plans)).toEqual(["LPV-2", "LPV-1"]);
});

it("offers to use an existing plan on a lesson with none, and an existing note once the plan is approved", () => {
  expect(planRow([], "S-1").alternative).toEqual({
    label: "Use an existing plan",
    href: "/research/teacher/lessons/S-1/reuse-plan",
  });

  const rows = materialRows([type("lesson-note", "Lesson note"), type("class-test", "Class test")], [], "LPV-1", "S-1");

  expect(rows[0].alternative).toEqual({
    label: "Use an existing note",
    href: "/research/teacher/lessons/S-1/reuse-note",
  });
  expect(rows[1].alternative).toBeUndefined();
});

it("offers no existing note while the plan is not approved, or once a note exists", () => {
  expect(materialRows([type("lesson-note", "Lesson note")], [], null, "S-1")[0].alternative).toBeUndefined();
  expect(
    materialRows([type("lesson-note", "Lesson note")], [item("lesson-note", "pending")], "LPV-1", "S-1")[0].alternative,
  ).toBeUndefined();
});

it("lets an approved plan import the evaluation's results before any class test, then shows them", () => {
  const notes = { made: 0, awaiting: 0 };
  const asked = learnerRows([], "P-1", notes, { planApproved: true, importedLearners: 0 })[0];
  const done = learnerRows([], "P-1", notes, { planApproved: true, importedLearners: 12 })[0];

  expect(asked.action?.label).toBe("Import class results");
  expect(done.status).toBe("complete");
  expect(done.detail).toBe("Imported from the evaluation · 12 learners");
});

it("reads class evidence as done once the evaluation's results are imported, even after the class test is sent", () => {
  const sent = [item("class-test", "approved")];
  const row = learnerRows(sent, "P-1", { made: 0, awaiting: 0 }, { planApproved: true, importedLearners: 8 })[0];

  expect(row.status).toBe("complete");
  expect(row.detail).toBe("Class test sent · results imported from the evaluation (8 learners)");
});

it("points the teacher at Make their notes once results are imported and no learner has a note", () => {
  const row = learnerRows([], "P-1", { made: 0, awaiting: 0 }, { planApproved: true, importedLearners: 8 })[1];

  expect(row).toMatchObject({
    status: "notStarted",
    action: { label: "Make their notes", href: "/research/teacher/lessons/P-1/evidence" },
  });
});

it("keeps personalised notes locked while there are no results at all", () => {
  expect(learnerRows([], "P-1", { made: 0, awaiting: 0 })[1].status).toBe("locked");
});
