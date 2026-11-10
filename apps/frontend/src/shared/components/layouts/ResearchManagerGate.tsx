import { useForm } from "react-hook-form";
import { useEffect, type ReactNode } from "react";

import { Button } from "@/shared/components/ui/Button";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/Card";
import { Input } from "@/shared/components/ui/Form";
import { setAuthCode } from "@/shared/lib/auth";
import { useAuthMe, useRefreshAuthMe } from "@/shared/hooks/useAuthMe";

type CodeForm = { code: string };

/**
 * Classify an auth-me failure so we can show a meaningful error.
 *
 * `fetch()` itself throws a `TypeError` ("Failed to fetch") when the
 * connection is refused (backend down, wrong port, CORS-rejected
 * preflight); a successfully-issued request that returns 4xx/5xx is
 * wrapped in a regular `Error` by `apiRequest`. Distinguishing the two
 * matters because the fix is different — restart the backend vs. give a
 * different code.
 */
function describeError(error: unknown): { kind: "network" | "http"; message: string } {
  if (error instanceof TypeError) {
    return {
      kind: "network",
      message: error.message || "Could not reach the backend.",
    };
  }
  if (error instanceof Error) {
    return { kind: "http", message: error.message || "Request failed." };
  }
  return { kind: "http", message: "Unknown error." };
}

/**
 * Gates the research workspace behind any authenticated role. Anonymous callers
 * get a sign-in panel; teacher / rater / student / admin / research-manager all
 * pass through and the role-aware home picks their landing. WHICH pages a
 * signed-in role may render is `ResearchRoleGuard`'s job (it sits just inside
 * this gate); the backend independently enforces the per-action policy on
 * every request.
 *
 * Previously this gate would silently rerender the sign-in form whenever the
 * `/auth/me` fetch failed — backend down, port wrong, anything network-side.
 * The user typed a code, hit Enter, saw no feedback, no error, no progress.
 * Now we read `isError` explicitly: a network failure renders a distinct
 * "Backend unreachable" panel with the URL we tried and a retry button; an
 * HTTP error after submit surfaces inline next to the form.
 */
export function ResearchManagerGate({ children }: { children: ReactNode }) {
  const { data, isLoading, isFetching, isError, error, refetch } = useAuthMe();
  const refreshAuthMe = useRefreshAuthMe();
  const { register, handleSubmit, formState, reset } = useForm<CodeForm>({
    defaultValues: { code: "" },
  });
  const isAuthenticated = Boolean(data && data.role !== "anonymous");

  // The form outlives a sign-in, so a code left in it would greet the next person at sign-out.
  useEffect(() => {
    if (isAuthenticated) reset();
  }, [isAuthenticated, reset]);

  if (isLoading) {
    return <p className="py-10 text-sm text-(--muted)">Checking research access…</p>;
  }

  if (isAuthenticated) {
    return <>{children}</>;
  }
  const onSubmit = ({ code }: CodeForm) => {
    if (!code.trim()) return;
    setAuthCode(code.trim());
    refreshAuthMe();
  };
  const describe = isError ? describeError(error) : null;
  const isNetworkError = describe?.kind === "network";

  return (
    <div className="flex justify-center py-16">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Research workspace sign-in</CardTitle>
        </CardHeader>
        <CardContent>
          {/* Error banner sits ABOVE the form rather than replacing it.
              When the service is down, the user can still: (a) hit Try
              again to re-verify the current code, (b) clear / type a
              different code and submit. Replacing the form with a panel
              (the previous shape) locked them out — they couldn't even
              change the code while the backend was unreachable. */}
          {isError ? (
            <div className="mb-4 space-y-2 border border-(--line) bg-(--sunken) p-3 text-sm">
              <p className="font-semibold text-(--ink)">
                {isNetworkError ? "We can't reach the service" : "Something went wrong"}
              </p>
              <p className="text-xs text-(--muted)">
                {isNetworkError
                  ? "The system is temporarily unavailable. Try again in a moment, or check that your code is correct."
                  : "We couldn't verify your access just now. Try again, or check that your code is correct."}
              </p>
              <button
                type="button"
                onClick={() => {
                  void refetch();
                }}
                disabled={isFetching}
                className="text-xs font-semibold text-(--accent-deep) underline hover:no-underline disabled:opacity-60"
              >
                {isFetching ? "Trying…" : "Try again"}
              </button>
              <details className="text-[11px] text-(--muted)">
                <summary className="cursor-pointer">Technical details</summary>
                <p className="mt-1 break-words font-mono text-(--ink-2)">{describe?.message}</p>
              </details>
            </div>
          ) : null}
          <p className="mb-4 text-sm text-(--muted)">
            Enter your access code to continue. Researcher, teacher, rater, student and
            admin codes all sign in here; the workspace adapts to your role.
          </p>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
            <Input
              placeholder="e.g. uncle-tosin, aunty-blessing, rater-tosin"
              autoFocus
              aria-label="Access code"
              {...register("code", { required: true })}
            />
            <Button
              type="submit"
              className="w-full"
              isLoading={formState.isSubmitting || isFetching}
            >
              Enter research workspace
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
