/** One plugin at its latest revision, as the API lists it. */
export type PluginRevision = {
  /** What it makes: a type, or a generator for one. */
  name: string;
  /** The plugin folder it belongs to, which may make more than one thing. */
  plugin: string;
  revision: number;
  version: string;
  /** The slug of the content type the plugin adds. */
  type: string;
  spec_revision: number;
  status: "installed" | "removed";
  /** It adds a generator to `type` instead of adding the type. */
  implements: boolean;
  installed_by: string | null;
  /** Ships with the app: only a deploy changes it. */
  system: boolean;
};

/** A plugin folder as the API takes it: each path inside the folder, and its text. */
export type PluginFiles = Record<string, string>;
