import { Link } from "@/shared/router";
import type { ReactNode } from "react";

import { Card } from "@/shared/components/ui/Card";

type ExperimentPageShellProps = {
  children: ReactNode;
};

/** Provides the shared researcher workspace shell for experiment routes. */
export function ExperimentPageShell({ children }: ExperimentPageShellProps) {
  return (
    <div className="min-h-screen bg-(--bg)">
      <div className="mx-auto flex w-full max-w-[1320px] flex-col gap-6 px-6 py-6">
        <Card variant="glass" padding="md" className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-xl font-semibold text-[color:var(--ink)]">
              Lesson-scoped experiments
            </h1>
          </div>
          <nav className="flex flex-wrap items-center gap-2 text-sm font-semibold">
            <Link
              href="/experiments/setup"
              className="rounded-none border border-[color:var(--line)] px-4 py-2 text-[color:var(--ink)] hover:border-[color:var(--accent)]"
            >
              School setup
            </Link>
            <Link
              href="/experiments"
              className="rounded-none border border-[color:var(--line)] px-4 py-2 text-[color:var(--ink)] hover:border-[color:var(--accent)]"
            >
              List
            </Link>
            <Link
              href="/experiments/new"
              className="rounded-none bg-[color:var(--accent)] px-4 py-2 text-white hover:bg-[color:var(--accent-deep)]"
            >
              New experiment
            </Link>
          </nav>
        </Card>
        {children}
      </div>
    </div>
  );
}
