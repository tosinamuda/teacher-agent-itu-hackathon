import { Button, buttonClass } from "@/shared/components/ui/Button";
import { Link } from "@/shared/router";

import { importPlanPath, reusePlanPath, writePlanPath } from "../lib/planPaths";

function Way({
  title,
  detail,
  action,
}: {
  title: string;
  detail: string;
  action: React.ReactNode;
}) {
  return (
    <li className="flex items-center gap-4 border-t border-(--line) px-4 py-4 first:border-t-0">
      <div className="min-w-0 flex-1">
        <h2 className="text-sm font-semibold text-(--ink)">{title}</h2>
        <p className="text-sm text-(--ink-2)">{detail}</p>
      </div>
      {action}
    </li>
  );
}

/** The four ways to make a lesson's plan: the agent writes it, or the teacher brings it. */
export function PlanWays({
  lessonPeriodId,
  onGenerate,
}: {
  lessonPeriodId: string;
  onGenerate: () => void;
}) {
  const quiet = buttonClass({ variant: "secondary" });
  return (
    <ul className="border border-(--line) bg-(--surface)">
      <Way
        title="Generate with the agent"
        detail="The agent writes it from the scheme of work."
        action={<Button onClick={onGenerate}>Generate</Button>}
      />
      <Way
        title="Import a plan document"
        detail="Paste or upload your own plan."
        action={
          <Link href={importPlanPath(lessonPeriodId)} className={quiet}>
            Import
          </Link>
        }
      />
      <Way
        title="Write it by hand"
        detail="Fill it in yourself."
        action={
          <Link href={writePlanPath(lessonPeriodId)} className={quiet}>
            Write
          </Link>
        }
      />
      <Way
        title="Reuse an approved plan"
        detail="Copy one you approved before."
        action={
          <Link href={reusePlanPath(lessonPeriodId)} className={quiet}>
            Choose
          </Link>
        }
      />
    </ul>
  );
}
