import { apiFetchBlob } from "@/shared/api/client";
import { postForm } from "@/shared/api/multipart";

export type UploadedAttachment = {
  attachment_id: string;
  url: string;
  content_type: string;
};

/** Upload a provenance image. */
export async function uploadAttachment(file: File, kind: string): Promise<UploadedAttachment> {
  const form = new FormData();
  form.append("file", file);
  form.append("kind", kind);
  return postForm<UploadedAttachment>("/attachments", form);
}

/** Fetch an attachment's bytes (auth-gated) as an object URL for an <img>. */
export async function fetchAttachmentObjectUrl(attachmentId: string): Promise<string> {
  const { blob } = await apiFetchBlob(`/attachments/${encodeURIComponent(attachmentId)}`);
  return URL.createObjectURL(blob);
}
