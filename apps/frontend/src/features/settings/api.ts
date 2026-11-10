import { apiFetch } from "@/shared/api/client";

/** A material the app has, and whether it is on for the signed-in teacher. */
export type Material = {
  type: string;
  label: string;
  /** What it makes, in a few words. */
  description: string;
  /** Built in: always on. */
  core: boolean;
  enabled: boolean;
};

export type Preferences = {
  /** The core materials first. */
  materials: Material[];
};

export const getPreferences = (): Promise<Preferences> =>
  apiFetch<Preferences>("/content/preferences");

const put = (path: string, enabled: boolean): Promise<Preferences> =>
  apiFetch<Preferences>(`/content/preferences/${path}`, {
    method: "PUT",
    body: JSON.stringify({ enabled }),
  });

export const switchMaterial = (type: string, enabled: boolean) =>
  put(`materials/${encodeURIComponent(type)}`, enabled);

/** A plugin on hand to add. */
export type LibraryPlugin = {
  folder: string;
  description: string;
  version: string;
  /** The materials it adds, by label. */
  adds: string[];
  installed: boolean;
};

export const getLibrary = (): Promise<LibraryPlugin[]> =>
  apiFetch<LibraryPlugin[]>("/content/plugins/library");

export const addFromLibrary = (folder: string): Promise<unknown> =>
  apiFetch<unknown>(`/content/plugins/library/${encodeURIComponent(folder)}`, {
    method: "POST",
  });
