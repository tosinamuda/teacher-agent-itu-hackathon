import { apiFetch } from "@/shared/api/client";

import type { PluginFiles, PluginRevision } from "./types";

const PLUGINS = "/content/plugins";

export const listPlugins = (): Promise<PluginRevision[]> =>
  apiFetch<PluginRevision[]>(PLUGINS);

/** Installs every type and generator the folder makes: one revision for each. */
export const installPlugin = (files: PluginFiles): Promise<PluginRevision[]> =>
  apiFetch<PluginRevision[]>(PLUGINS, {
    method: "POST",
    body: JSON.stringify({ files }),
  });

/** Updates every artefact the folder holds; `name` is one of them. */
export const updatePlugin = (
  name: string,
  files: PluginFiles,
): Promise<PluginRevision[]> =>
  apiFetch<PluginRevision[]>(`${PLUGINS}/${encodeURIComponent(name)}`, {
    method: "PUT",
    body: JSON.stringify({ files }),
  });

/** Stops new drafts of the plugin's type; content already made stays readable. */
export const removePlugin = (name: string): Promise<PluginRevision> =>
  apiFetch<PluginRevision>(`${PLUGINS}/${encodeURIComponent(name)}`, {
    method: "DELETE",
  });
