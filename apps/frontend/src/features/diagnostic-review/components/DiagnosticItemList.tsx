import { Pager } from "@/shared/components/renderer/Pager";
import { ClassTestText } from "@/shared/components/renderer/ClassTestText";
import { Badge } from "@/shared/components/ui/Badge";
import { humaniseMisconceptionCode } from "@/shared/utils/misconception";

import { useReviewedPlan } from "../hooks/useReviewedPlan";
import { objectiveLabel } from "../lib/objectiveLabel";
import { DiagnosticItem, PlanObjective } from "../types";

/** Teacher view of the MCQ diagnostic: each item with its answer key + distractor tags. */
export function DiagnosticItemList({
  items,
  planVersionId,
  paged = false,
}: {
  items: DiagnosticItem[];
  planVersionId: string;
  /** One objective's questions at a time, filling the height it is given, for the review page. */
  paged?: boolean;
}) {
  const objectives = useReviewedPlan(planVersionId).data?.objectives ?? [];

  if (items.length === 0) {
    return (
      <p className="rounded-2xl border border-dashed border-(--line) bg-(--surface) p-6 text-center text-sm text-(--muted)">
        No diagnostic items yet for this lesson — generate the assessment to
        start.
      </p>
    );
  }

  if (paged) {
    const groups = groupByObjective(items);
    return (
      <Pager count={groups.length} label="Objective">
        {(page) => (
          <div className="relative max-h-[70dvh] overflow-y-auto overscroll-contain rounded-2xl border border-(--line) bg-white px-4 md:max-h-none md:min-h-0 md:flex-1">
            <p className="sticky top-0 z-10 -mx-4 border-b border-(--line) bg-white px-4 py-3 text-xs font-semibold text-(--accent-deep)">
              {objectiveLabel(objectives, groups[page].objectiveId) ||
                "Questions"}
            </p>
            <div className="divide-y divide-(--line)">
              {groups[page].entries.map(({ item, index }) => (
                <div key={item.item_id || `item-${index}`} className="py-4">
                  <DiagnosticItemBody
                    item={item}
                    index={index}
                    objectives={objectives}
                    showObjective={false}
                  />
                </div>
              ))}
            </div>
          </div>
        )}
      </Pager>
    );
  }

  return (
    <div className="space-y-3">
      {items.map((item, index) => (
        <article
          key={item.item_id || `item-${index}`}
          className="rounded-2xl border border-(--line) bg-white p-4"
        >
          <DiagnosticItemBody
            item={item}
            index={index}
            objectives={objectives}
          />
        </article>
      ))}
    </div>
  );
}

interface ObjectiveGroup {
  objectiveId: string;
  entries: { item: DiagnosticItem; index: number }[];
}

function groupByObjective(items: DiagnosticItem[]): ObjectiveGroup[] {
  const groups = new Map<string, ObjectiveGroup>();
  items.forEach((item, index) => {
    const key = item.lesson_objective_id;
    const group = groups.get(key) ?? { objectiveId: key, entries: [] };
    group.entries.push({ item, index });
    groups.set(key, group);
  });
  return [...groups.values()];
}

function DiagnosticItemBody({
  item,
  index,
  objectives,
  showObjective = true,
}: {
  item: DiagnosticItem;
  index: number;
  objectives: PlanObjective[];
  showObjective?: boolean;
}) {
  return (
    <>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className="text-xs font-semibold text-(--muted)">
          {[
            `Q${index + 1}`,
            showObjective
              ? objectiveLabel(objectives, item.lesson_objective_id)
              : "",
          ]
            .filter(Boolean)
            .join(" · ")}
        </span>
        <Badge variant="outline">{item.difficulty}</Badge>
      </div>
      <div className="mt-2 font-medium text-(--ink)">
        <ClassTestText text={item.stem} />
      </div>

      <ul className="mt-3 space-y-1">
        {Object.entries(item.options).map(([key, text]) => {
          const isCorrect = key === item.correct_option;
          const misconception = item.distractor_misconceptions?.[key];
          return (
            <li
              key={key}
              className={`flex flex-wrap items-center gap-2 rounded-lg px-2 py-1 text-sm ${
                isCorrect
                  ? "bg-(--success-tint) text-(--success-ink)"
                  : "text-(--ink)"
              }`}
            >
              <span className="font-semibold">{key}.</span>
              <ClassTestText text={text} />
              {isCorrect ? <Badge variant="success">correct</Badge> : null}
              {misconception ? (
                <span className="text-xs text-(--muted)">
                  ↳ {humaniseMisconceptionCode(misconception)}
                </span>
              ) : null}
            </li>
          );
        })}
      </ul>
    </>
  );
}
