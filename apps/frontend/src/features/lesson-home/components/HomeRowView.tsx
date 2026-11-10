import { useGenerateContent } from "@/features/content/hooks/useContent";
import { buttonClass } from "@/shared/components/ui/Button";
import { StatusMark } from "@/shared/components/ui/StatusMark";
import { Link } from "@/shared/router";

import type { HomeRow } from "../lib/lessonHome";

const ROW = "flex items-center gap-4 border-t border-(--line) px-4 py-3 first:border-t-0";

function Chevron() {
  return (
    <svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" className="shrink-0 text-(--ink-2)">
      <path d="M6 3.5L10.5 8 6 12.5" fill="none" stroke="currentColor" strokeWidth="1.5" />
    </svg>
  );
}

function Text({ title, detail, muted }: { title: string; detail?: string; muted?: boolean }) {
  return (
    <span className="flex min-w-0 flex-1 flex-col">
      <span className={`text-sm ${muted ? "text-(--faint)" : "font-semibold text-(--ink)"}`}>{title}</span>
      {detail ? <span className="text-xs text-(--ink-2)">{detail}</span> : null}
    </span>
  );
}

/** A material not made yet: its row carries the button that makes it, and follows the job. */
function CreateRow({ row, planVersionId }: { row: HomeRow; planVersionId: string }) {
  const type = row.create?.type ?? row.key;
  const generate = useGenerateContent(planVersionId, type);
  const stopped = !generate.isPending && (generate.failure !== null || generate.isError);

  return (
    <li className={ROW}>
      <StatusMark kind={generate.isPending ? "inProgress" : stopped ? "rejected" : row.status} />
      <Text
        title={row.title}
        detail={generate.isPending ? "The agent is writing it" : stopped ? "Could not finish. Nothing was saved." : undefined}
      />
      {row.alternative && !generate.isPending ? (
        <Link href={row.alternative.href} className="text-xs text-(--ink-2) underline hover:text-(--ink)">
          {row.alternative.label}
        </Link>
      ) : null}
      <button
        type="button"
        disabled={generate.isPending}
        className={buttonClass({ variant: "secondary", size: "sm" })}
        onClick={() => generate.create({ sources: type === "revision-note" ? "lesson-note" : undefined })}
      >
        {stopped ? "Try again" : (row.create?.label ?? "Create")}
      </button>
    </li>
  );
}

/** One line of a lesson's home. A line shows a button or a chevron, never both. */
export function HomeRowView({ row, planVersionId }: { row: HomeRow; planVersionId: string | null }) {
  if (row.create && planVersionId) return <CreateRow row={row} planVersionId={planVersionId} />;

  const body = (
    <>
      <StatusMark kind={row.status} />
      <Text title={row.title} detail={row.detail} muted={row.status === "locked"} />
    </>
  );
  if (row.action) {
    return (
      <li className={ROW}>
        {body}
        {row.alternative ? (
          <Link href={row.alternative.href} className="text-xs text-(--ink-2) underline hover:text-(--ink)">
            {row.alternative.label}
          </Link>
        ) : null}
        <Link
          href={row.action.href}
          className={buttonClass({ variant: row.action.primary ? "primary" : "secondary", size: "sm" })}
        >
          {row.action.label}
        </Link>
      </li>
    );
  }
  if (row.href) {
    return (
      <li>
        <Link href={row.href} className={`${ROW} hover:bg-(--sunken)`}>
          {body}
          <Chevron />
        </Link>
      </li>
    );
  }
  return <li className={ROW}>{body}</li>;
}
