import { EngineSection, PartField, PartKind, Spec } from "./types";

/** A field's name as a reader sees it: `worked_examples` reads "Worked examples". */
export function fieldTitle(name: string): string {
  const words = name.replaceAll("_", " ");
  return words.charAt(0).toUpperCase() + words.slice(1);
}

/** The fields to draw: the spec's, in its order; the part's own keys while the spec loads. */
export function fieldsOf(
  part: Record<string, unknown>,
  parts: PartField[] | null,
): PartField[] {
  if (parts) return parts;
  return Object.keys(part).map((name) => ({
    name,
    description: name,
    type: Array.isArray(part[name]) ? "list" : "markdown",
    required: true,
  }));
}

/** The fields of a section's part: the lesson's own schema for the lesson's section. */
export function partsFor(
  section: EngineSection,
  spec: Spec | null,
): PartField[] | null {
  if (!spec) return null;
  if (section.unit === "lesson" && spec.lesson_parts) return spec.lesson_parts;
  return spec.parts;
}

/** The kind an item of a mixed list is, by its `kind`. */
export function kindOf(
  item: Record<string, unknown>,
  kinds: PartKind[],
): PartKind | undefined {
  return kinds.find((kind) => kind.name === item.kind);
}
