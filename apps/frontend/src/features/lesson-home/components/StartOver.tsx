import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { buttonClass } from "@/shared/components/ui/Button";

import { previewStartOver, startOver } from "../api/startOver";
import { summariseStartOver } from "../lib/startOver";

const BLOCKED: [RegExp, string][] = [
  [/study ran on this lesson/, "This is one of the study's own lessons, so it cannot be cleared."],
];

const blockedText = (reasons: string[]): string =>
  reasons.map((reason) => BLOCKED.find(([pattern]) => pattern.test(reason))?.[1] ?? reason).join(" ");

/** A quiet way to clear what was made for the lesson and begin it again, after a clear warning. */
export function StartOver({ lessonPeriodId }: { lessonPeriodId: string }) {
  const { currentWorkspace } = useTeachingWorkspace();
  const workspaceId = currentWorkspace?.id ?? "";
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);
  const preview = useQuery({
    queryKey: ["start-over", workspaceId, lessonPeriodId],
    queryFn: () => previewStartOver(workspaceId, lessonPeriodId),
    enabled: open && Boolean(workspaceId),
    gcTime: 0,
  });
  const clear = useMutation({
    mutationFn: () => startOver(workspaceId, lessonPeriodId),
    onSuccess: () => {
      setOpen(false);
      void queryClient.invalidateQueries();
    },
  });

  if (!open) {
    return (
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="self-start text-xs text-(--ink-2) underline hover:text-(--ink)"
      >
        Start this lesson over
      </button>
    );
  }
  const summary = summariseStartOver(preview.data?.counts ?? {});
  const blocked = preview.data?.blocked ?? [];
  return (
    <section
      aria-label="Start this lesson over"
      className="flex flex-col gap-3 border border-(--line) bg-(--surface) p-4"
    >
      <h2 className="text-sm font-semibold text-(--ink)">Start this lesson over</h2>
      {preview.isLoading ? <p className="text-sm text-(--ink-2)">Checking what would go…</p> : null}
      {preview.isError ? <p className="text-sm text-(--danger)">Couldn&apos;t check this lesson.</p> : null}
      {blocked.length > 0 ? (
        <p role="alert" className="text-sm text-(--ink)">
          {blockedText(blocked)}
        </p>
      ) : preview.data ? (
        <p className="text-sm text-(--ink)">
          {summary
            ? `This clears what was made for the lesson: ${summary}. `
            : "Nothing was made for this lesson yet. "}
          The lesson and your class stay. This cannot be undone.
        </p>
      ) : null}
      {clear.isError ? (
        <p role="alert" className="text-sm text-(--danger)">
          Couldn&apos;t clear the lesson. Nothing was changed.
        </p>
      ) : null}
      <div className="flex gap-2">
        {preview.data && blocked.length === 0 && summary ? (
          <button
            type="button"
            disabled={clear.isPending}
            onClick={() => clear.mutate()}
            className={buttonClass({ variant: "danger", size: "sm" })}
          >
            {clear.isPending ? "Clearing…" : "Clear this lesson"}
          </button>
        ) : null}
        <button
          type="button"
          onClick={() => setOpen(false)}
          className={buttonClass({ variant: "secondary", size: "sm" })}
        >
          Cancel
        </button>
      </div>
    </section>
  );
}
