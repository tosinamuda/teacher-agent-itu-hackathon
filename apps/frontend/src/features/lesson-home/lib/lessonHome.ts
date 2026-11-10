import { currentContent } from "@/features/content/status";
import type { ContentSummary, ContentTypeInfo } from "@/features/content/types";
import type { TermClassSubject } from "@/features/curriculum/hooks/useSchemeOfWork";
import type { PlanVersionSummary } from "@/features/lesson-plan/hooks/useSessionPlans";
import type { StatusKind } from "@/shared/components/ui/StatusMark";
import { makePlanPath, reusePlanPath } from "@/features/lesson-plan/lib/planPaths";

/** One line of a lesson's home: what it is, where it stands and the one thing to do next. */
export type HomeRow = {
  key: string;
  title: string;
  status: StatusKind;
  detail?: string;
  /** Opens the thing itself; shown as a chevron when the row has no button. */
  href?: string;
  /** The one thing to do now. */
  action?: { label: string; href: string; primary?: boolean };
  /** A material to make: the row carries the button that makes it. */
  create?: { type: string; label?: string };
  /** A second way to do what the row's button does, as a quiet link: reuse what exists. */
  alternative?: { label: string; href: string };
};

const PLAN_PATH = "/research/teacher/lesson-plan";
const LESSONS_PATH = "/research/teacher/lessons";
const CLASS_TEST = "class-test";

const isLive = (plan: PlanVersionSummary): boolean => plan.status === "draft" || plan.status === "approved";

const CLOSED_DETAIL: Record<string, string> = {
  rejected: "The last plan was rejected",
  withdrawn: "The last plan's approval was withdrawn",
};

/** The plan's row, from the lesson's plan versions (newest first). A closed version is not the plan. */
export function planRow(plans: PlanVersionSummary[], sessionId: string): HomeRow {
  const latest = plans.find(isLive);
  if (!latest) {
    return {
      key: "plan",
      title: "Lesson plan",
      status: "notStarted",
      detail: plans[0] ? CLOSED_DETAIL[plans[0].status] : undefined,
      action: { label: "Create plan", href: makePlanPath(sessionId), primary: true },
      alternative: { label: "Use an existing plan", href: reusePlanPath(sessionId) },
    };
  }
  const planHref = `${PLAN_PATH}/${latest.plan_id}`;
  if (latest.status !== "approved") {
    return {
      key: "plan",
      title: "Lesson plan",
      status: "needsYou",
      detail: "Waiting for your review",
      action: { label: "Review", href: planHref },
    };
  }
  return {
    key: "plan",
    title: "Lesson plan",
    status: "complete",
    detail: latest.approved_at ? `Approved ${latest.approved_at.slice(0, 10)}` : "Approved",
    href: planHref,
  };
}

/** The newest approved plan version: the one the class materials are made from. */
export const approvedVersionOf = (plans: PlanVersionSummary[]): PlanVersionSummary | undefined =>
  plans.find((plan) => plan.status === "approved");

/** The plan versions materials were made from: every version that was ever approved. */
export const versionsWithMaterials = (plans: PlanVersionSummary[]): string[] =>
  plans.filter((plan) => plan.approved_at).map((plan) => plan.version_id);

function materialRow(
  info: ContentTypeInfo,
  item: ContentSummary | undefined,
  approvedVersionId: string | null,
  lessonPeriodId: string | undefined,
): HomeRow {
  const base = { key: info.type, title: info.label };
  if (!item) {
    if (!approvedVersionId) return { ...base, status: "locked" };
    const reuse =
      info.type === "lesson-note" && lessonPeriodId
        ? { alternative: { label: "Use an existing note", href: `${LESSONS_PATH}/${lessonPeriodId}/reuse-note` } }
        : {};
    return { ...base, status: "notStarted", create: { type: info.type }, ...reuse };
  }

  const href = `/research/teacher/content/${item.id}`;
  if (approvedVersionId && item.plan_version_id !== approvedVersionId) {
    // A material made from an earlier version stays as it is; making it again uses the current one.
    return {
      ...base,
      status: "needsYou",
      detail: "The plan changed after this was made",
      href,
      create: { type: info.type, label: "Update" },
    };
  }
  if (item.review_status === "rejected") {
    return { ...base, status: "rejected", detail: "Rejected", href };
  }
  if (item.review_status !== "approved") {
    return {
      ...base,
      status: "needsYou",
      detail: "Waiting for your review",
      action: { label: "Review", href },
    };
  }
  return {
    ...base,
    status: "complete",
    detail: info.type === CLASS_TEST ? "Sent to students" : undefined,
    href,
  };
}

/** The engine variants of a type exist to compare harnesses; a lesson shows them only once made. */
const isVariant = (info: ContentTypeInfo): boolean => info.type.endsWith("-engine");

/** The order a teacher meets the materials in; any other type follows. */
const TEACHING_ORDER = ["lesson-note", "slide-deck", "revision-note", "class-test", "exam-questions"];

const placeOf = (info: ContentTypeInfo): number => {
  const place = TEACHING_ORDER.indexOf(info.type);
  return place === -1 ? TEACHING_ORDER.length : place;
};

/**
 * The class materials, from the server's types. A material not made yet is locked until a plan is
 * approved; one already made stays whatever happens to the plan.
 */
export function materialRows(
  types: ContentTypeInfo[],
  content: ContentSummary[],
  approvedVersionId: string | null,
  lessonPeriodId?: string,
): HomeRow[] {
  return types
    .filter((info) => info.made_from_a_plan_version)
    .filter((info) => (!info.retired && !isVariant(info)) || currentContent(content, info.type))
    .sort((a, b) => placeOf(a) - placeOf(b))
    .map((info) => materialRow(info, currentContent(content, info.type), approvedVersionId, lessonPeriodId));
}

/** The materials a teacher can ask for once a plan is approved, in the order they are met. */
export const materialsToMake = (types: ContentTypeInfo[]): ContentTypeInfo[] =>
  types
    .filter((info) => info.made_from_a_plan_version && !info.retired && !isVariant(info))
    .sort((a, b) => placeOf(a) - placeOf(b));

/** What the teacher has waiting on this lesson, for the panel. */
export const waitingOn = (rows: HomeRow[]): HomeRow[] => rows.filter((row) => row.status === "needsYou");

function evidenceRow(
  lessonPeriodId: string,
  testSent: boolean,
  study: { planApproved: boolean; importedLearners: number },
): HomeRow {
  const key = "evidence";
  const title = "Class evidence";
  const href = `/research/teacher/lessons/${lessonPeriodId}/evidence`;
  if (study.importedLearners > 0) {
    const imported = `${study.importedLearners} ${study.importedLearners === 1 ? "learner" : "learners"}`;
    const detail = testSent
      ? `Class test sent · results imported from the evaluation (${imported})`
      : `Imported from the evaluation · ${imported}`;
    return { key, title, status: "complete", detail, href };
  }
  if (testSent) return { key, title, status: "inProgress", detail: "How the class answered", href };
  if (study.planApproved) {
    return {
      key,
      title,
      status: "notStarted",
      detail: "Opens after the class test is sent, or import the evaluation's results",
      action: { label: "Import class results", href },
    };
  }
  return { key, title, status: "locked", detail: "Opens after the class test is sent" };
}

/**
 * The rows for the class's learners: evidence once the class test is sent, then their notes.
 * `notes.made` counts every learner who has a note, the ones awaiting review among them.
 */
export function learnerRows(
  content: ContentSummary[],
  lessonPeriodId: string,
  notes: { made: number; awaiting: number },
  study: { planApproved: boolean; importedLearners: number } = { planApproved: false, importedLearners: 0 },
): HomeRow[] {
  const testSent = currentContent(content, CLASS_TEST)?.review_status === "approved";
  const evidence = evidenceRow(lessonPeriodId, testSent, study);
  const personalised: HomeRow =
    notes.awaiting > 0
      ? {
          key: "notes",
          title: "Personalised notes",
          status: "needsYou",
          detail: `${Math.max(notes.made - notes.awaiting, 0)} approved · ${notes.awaiting} to review`,
          action: { label: "Review", href: "/research/teacher/pack-reviews" },
        }
      : notes.made > 0
        ? {
            key: "notes",
            title: "Personalised notes",
            status: "complete",
            detail: `${notes.made} approved`,
            href: "/research/teacher/pack-reviews",
          }
        : study.importedLearners > 0
          ? {
              key: "notes",
              title: "Personalised notes",
              status: "notStarted",
              detail: "Give learners the imported marks to make their notes",
              action: { label: "Make their notes", href: `/research/teacher/lessons/${lessonPeriodId}/evidence` },
            }
          : { key: "notes", title: "Personalised notes", status: "locked", detail: "Opens after learners answer" };
  return [evidence, personalised];
}

/** The lesson's title and week, found in the class's scheme of work. */
/** A lesson id as an address spells it or as the API does: the two differ only in hyphens. */
const bare = (id: string): string => id.replaceAll("-", "");

export function lessonOf(
  scheme: TermClassSubject | undefined,
  lessonPeriodId: string,
): { title: string; week: number } | null {
  for (const week of scheme?.weeks ?? []) {
    const period = week.lesson_periods.find((candidate) => bare(candidate.id) === bare(lessonPeriodId));
    if (period) return { title: period.subtopic_title ?? period.title ?? week.title, week: week.week_number };
  }
  return null;
}
