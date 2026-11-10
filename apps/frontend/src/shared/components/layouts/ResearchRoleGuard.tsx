import { Link } from "@/shared/router";
import { usePathname } from "@/shared/router";
import type { ReactNode } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/Card";
import { useAuthMe } from "@/shared/hooks/useAuthMe";

/**
 * Which roles may render each `/research` area. Mirrors the backend Casbin
 * matrix (`migrations/data/casbin_policy_seed.py`) — the backend remains the
 * real enforcement (every researcher API 403s for other roles); this guard
 * stops the UI from even mounting a page the caller can't use.
 *
 * Note: admin holds `experiment:* read` in Casbin purely for the
 * user-management "students in experiment X" filter — that does NOT extend to
 * the experiments UI, which stays researcher-only here.
 */
const AREA_RULES: { prefix: string; allowed: readonly string[] }[] = [
  { prefix: "/research/teacher", allowed: ["teacher", "research_manager"] },
  { prefix: "/research/student", allowed: ["student", "research_manager"] },
  { prefix: "/research/rater", allowed: ["rater", "research_manager"] },
  { prefix: "/research/setup", allowed: ["admin", "research_manager"] },
  { prefix: "/research/learners", allowed: ["admin", "research_manager"] },
  { prefix: "/research/ops", allowed: ["admin", "research_manager"] },
];

/** Everything under `/research` not claimed above (experiments, h1, h2,
 *  investigations, story) is a researcher analysis surface. */
const RESEARCHER_ONLY = ["research_manager"] as const;

/**
 * Roles allowed on `pathname`, or `null` when every signed-in role may pass
 * (the `/research` home itself — it branches by role).
 */
function allowedRolesFor(pathname: string): readonly string[] | null {
  if (pathname === "/research") return null;
  const rule = AREA_RULES.find(
    ({ prefix }) => pathname === prefix || pathname.startsWith(`${prefix}/`)
  );
  return rule ? rule.allowed : RESEARCHER_ONLY;
}

/**
 * Blocks `/research/*` pages whose area belongs to a different role.
 *
 * Sits INSIDE `ResearchManagerGate`, so the caller is always authenticated by
 * the time this renders — anonymous never reaches it. Found 2026-06-11: a
 * teacher who signed in while parked on a researcher URL (an experiment detail
 * left behind by a previous sign-out) rendered the whole researcher surface,
 * because the gate only checked "signed in", not "signed in as whom".
 */
export function ResearchRoleGuard({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const { data: actor } = useAuthMe();
  const role = actor?.role ?? "anonymous";
  const allowed = allowedRolesFor(pathname);

  if (allowed === null || allowed.includes(role)) {
    return <>{children}</>;
  }

  return (
    <div className="flex justify-center py-16">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>This page isn&apos;t part of your workspace</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm text-(--muted)">
          <p>
            You&apos;re signed in as <span className="font-medium text-(--ink)">{role}</span>, and
            this page belongs to a different role. Head back to your home to pick up where you
            left off.
          </p>
          <Link
            href="/research"
            className="inline-block font-semibold text-(--accent-deep) underline hover:no-underline"
          >
            Go to your home
          </Link>
        </CardContent>
      </Card>
    </div>
  );
}
