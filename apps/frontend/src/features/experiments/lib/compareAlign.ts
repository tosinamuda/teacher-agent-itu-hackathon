import { ComparePackManifest, ComparePackStep } from "./experiments";

/** A section aligned across two packs (same lesson objective on the left + right). */
export type AlignedSection = {
  key: string;
  title: string;
  objectiveId: string | null;
  left: ComparePackStep | null;
  right: ComparePackStep | null;
};

const keyOf = (step: ComparePackStep, index: number) =>
  step.lesson_objective_id || step.step_id || String(index);

/**
 * Aligns two packs section-by-section (by lesson objective) so the same section can
 * be compared left-vs-right. Left order leads; right-only sections are appended.
 */
export function alignSections(
  left: ComparePackManifest | null,
  right: ComparePackManifest | null
): AlignedSection[] {
  const leftSteps = left?.steps ?? [];
  const rightSteps = right?.steps ?? [];
  const rightByKey = new Map<string, ComparePackStep>();
  rightSteps.forEach((step, index) => rightByKey.set(keyOf(step, index), step));

  const seen = new Set<string>();
  const rows: AlignedSection[] = [];
  leftSteps.forEach((step, index) => {
    const key = keyOf(step, index);
    seen.add(key);
    const counterpart = rightByKey.get(key) ?? null;
    rows.push({
      key,
      title: step.title || counterpart?.title || "Section",
      objectiveId: step.lesson_objective_id ?? counterpart?.lesson_objective_id ?? null,
      left: step,
      right: counterpart,
    });
  });
  rightSteps.forEach((step, index) => {
    const key = keyOf(step, index);
    if (seen.has(key)) return;
    rows.push({
      key,
      title: step.title || "Section",
      objectiveId: step.lesson_objective_id ?? null,
      left: null,
      right: step,
    });
  });
  return rows;
}
