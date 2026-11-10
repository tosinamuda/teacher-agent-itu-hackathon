import { apiFetch, apiFetchBlob } from "@/shared/api/client";
import type { JobAccepted } from "@/shared/api/jobs";

import {
  Approval,
  Level,
  ContentItem,
  ContentSummary,
  ContentTypeInfo,
  ContentTypeSlug,
  ExpertSources,
  Revision,
  Spec,
} from "../types";

const CONTENT = "/content";
const id = (contentId: string) => `${CONTENT}/${encodeURIComponent(contentId)}`;

/** Every content type with its current spec. */
export const listContentTypes = (): Promise<ContentTypeInfo[]> =>
  apiFetch<ContentTypeInfo[]>(`${CONTENT}/types`);

/** Make a generator the one new content of the type is made with. */
export const setDefaultGenerator = (
  type: ContentTypeSlug,
  level: Level,
  generator: string,
): Promise<ContentTypeInfo> =>
  apiFetch<ContentTypeInfo>(
    `${CONTENT}/types/${encodeURIComponent(type)}/default-generator`,
    {
      method: "PUT",
      body: JSON.stringify({ level, generator }),
    },
  );

/** One revision of a type's spec: what content built against it was asked to be. */
export const getSpec = (
  type: ContentTypeSlug,
  revision: number,
): Promise<Spec> =>
  apiFetch<Spec>(
    `${CONTENT}/types/${encodeURIComponent(type)}/specs/${revision}`,
  );

/** The content made from one plan version, newest first; one type of it when named. */
export const findContent = (
  planVersionId: string,
  type?: ContentTypeSlug,
): Promise<ContentSummary[]> =>
  apiFetch<ContentSummary[]>(
    `${CONTENT}?plan_version_id=${encodeURIComponent(planVersionId)}` +
      (type ? `&type=${encodeURIComponent(type)}` : ""),
  );

/** Every per-student revision note the caller may read, newest first. */
export const findLearnerRevisionNotes = (): Promise<ContentSummary[]> =>
  apiFetch<ContentSummary[]>(`${CONTENT}?type=revision-note&level=learner`);

export const getContent = (contentId: string): Promise<ContentItem> =>
  apiFetch<ContentItem>(id(contentId));

/** The job kind that generates content, as the server names it. */
export const GENERATE_CONTENT = "content.generate";

/** What one generation acts on, spelled as the server spells it, so a page can follow it. */
export const contentGenerationSubject = (
  planVersionId: string,
  type: ContentTypeSlug,
  level: Level = "class",
): string => `${planVersionId}:${type}:${level}`;

/**
 * Queue content of one type from a frozen plan version; it stays pending until approved.
 * A revision note can name the expert content it is grounded in; the lesson note otherwise.
 * An engine type can be given `instructions`, what the teacher wants in their own words.
 * Answers with the job making it, or the one already making it.
 */
export const generateContent = (
  planVersionId: string,
  type: ContentTypeSlug,
  level: Level = "class",
  sources?: ExpertSources,
  instructions?: string,
): Promise<JobAccepted> =>
  apiFetch<JobAccepted>(CONTENT, {
    method: "POST",
    body: JSON.stringify({
      plan_version_id: planVersionId,
      type,
      level,
      sources,
      instructions,
    }),
  });

/** Revise it with the teacher's feedback; it goes back to pending review. */
export const reviseContent = (
  contentId: string,
  feedback: string,
): Promise<Revision> =>
  apiFetch<Revision>(`${id(contentId)}/revisions`, {
    method: "POST",
    body: JSON.stringify({ feedback }),
  });

export const listRevisions = (contentId: string): Promise<Revision[]> =>
  apiFetch<Revision[]>(`${id(contentId)}/revisions`);

/** Approve the version the teacher reviewed; a class test is then sent to its students. */
export const approveContent = (
  contentId: string,
  expectedVersion: number,
): Promise<ContentItem> =>
  apiFetch<ContentItem>(`${id(contentId)}/approvals`, {
    method: "POST",
    body: JSON.stringify({ expected_version: expectedVersion }),
  });

/** Reject the pending version the teacher reviewed, or withdraw an approved one, and say why. */
export const rejectContent = (
  contentId: string,
  expectedVersion: number,
  reason: string,
): Promise<ContentItem> =>
  apiFetch<ContentItem>(`${id(contentId)}/rejections`, {
    method: "POST",
    body: JSON.stringify({ expected_version: expectedVersion, reason }),
  });


export const listApprovals = (contentId: string): Promise<Approval[]> =>
  apiFetch<Approval[]>(`${id(contentId)}/approvals`);

/** Approve the lesson plan a version belongs to, only while that version is still its latest. */
export const approveLessonPlan = async (
  planVersionId: string,
): Promise<ContentItem> => {
  const [plan] = await findContent(planVersionId, "lesson-plan");
  if (!plan) throw new Error("This lesson plan was not found.");
  if (plan.plan_version_id !== planVersionId) {
    throw new Error(
      "This plan has a newer version. Review that one before approving.",
    );
  }
  return approveContent(plan.id, plan.version);
};

/**
 * Discard the lesson plan's draft, or take back its approval, and say why. A plan is content, so
 * this is the same rejection a material has; the server decides which it is.
 */
export const closeLessonPlan = async (
  planVersionId: string,
  reason: string,
): Promise<ContentItem> => {
  const [plan] = await findContent(planVersionId, "lesson-plan");
  if (!plan) throw new Error("This lesson plan was not found.");
  return rejectContent(plan.id, plan.version, reason);
};

/** The file made of saved content, with the name the server gave it. */
export const downloadContentFile = async (
  contentId: string,
): Promise<{ blob: Blob; filename: string }> => {
  const { blob, response } = await apiFetchBlob(`${id(contentId)}/file`);
  const named = /filename="?([^"]+)"?/.exec(
    response.headers.get("content-disposition") ?? "",
  );
  return { blob, filename: named?.[1] ?? contentId };
};
