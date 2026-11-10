/** What the API's refusal codes say, for a person: each code is `name:subject`. */
const SENTENCES: Record<string, (subject: string) => string> = {
  plugin_ships_with_the_app: (name) =>
    `${name} ships with the app, so only a deploy changes it.`,
  plugin_installed: (name) =>
    `${name} is already installed. Use Update on its row.`,
  content_type_exists: (slug) => `A content type named ${slug} already exists.`,
  skill_name_in_use: (skill) =>
    `A different skill named ${skill} is already stored. Rename it.`,
  plugin_type_is_fixed: (name) =>
    `An update cannot change ${name}'s type, label, audience or plan-version setting.`,
  unknown_plugin: (name) => `There is no plugin ${name}.`,
  plugin_name_differs: (name) =>
    `The folder's plugin.json names a plugin other than ${name}.`,
};

function sentence(line: string): string {
  const at = line.indexOf(":");
  const say = at > 0 ? SENTENCES[line.slice(0, at)] : undefined;
  return say ? say(line.slice(at + 1)) : line;
}

/** The problems an API refusal lists, one line each; the raw text when it lists none. */
export function problemsOf(error: unknown): string[] {
  const text = error instanceof Error ? error.message : String(error);
  try {
    const detail: unknown = (JSON.parse(text) as { detail?: unknown }).detail;
    if (Array.isArray(detail)) return detail.map(String);
    if (typeof detail === "string") return [sentence(detail)];
  } catch {
    // Not JSON: show what the server said.
  }
  return [text];
}
