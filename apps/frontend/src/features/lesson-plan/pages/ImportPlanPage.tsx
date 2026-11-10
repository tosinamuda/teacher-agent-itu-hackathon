import { Link, useRouter } from "@/shared/router";

import { ImportFromDocument } from "../components/ImportFromDocument";
import { makePlanPath, planPath } from "../lib/planPaths";

/** Bring a plan the teacher already has. It is written into the lesson's plan as a draft to read. */
export function ImportPlanPage({ lessonPeriodId }: { lessonPeriodId: string }) {
  const router = useRouter();
  return (
    <main className="mx-auto flex w-full max-w-2xl flex-col gap-5 py-6">
      <Link
        href={makePlanPath(lessonPeriodId)}
        className="text-xs text-(--ink-2) hover:text-(--ink)"
      >
        ‹ Make the lesson plan
      </Link>
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold text-(--ink)">
          Import a plan document
        </h1>
        <p className="text-xs text-(--ink-2)">
          Paste your plan or upload a file.
        </p>
      </header>
      <ImportFromDocument
        sessionId={lessonPeriodId}
        onImported={(plan) => router.push(planPath(plan.plan_version_id))}
        cancelHref={makePlanPath(lessonPeriodId)}
      />
    </main>
  );
}
