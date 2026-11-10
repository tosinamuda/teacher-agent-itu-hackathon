import { ReactNode } from "react";

import { Badge } from "@/shared/components/ui/Badge";

import { ContentStatus, audienceLine } from "../status";
import { ContentTypeInfo } from "../types";

function Details({ info }: { info: ContentTypeInfo }) {
  const { spec } = info;
  return (
    <details className="text-xs text-(--ink-2)">
      <summary className="cursor-pointer text-(--accent-deep)">Details</summary>
      <div className="mt-2 space-y-2">
        <p>{spec.material}</p>
        <p className="text-(--muted)">For {audienceLine(spec.audience)}</p>
        <p className="font-semibold">Structure</p>
        <ul className="list-disc pl-5">
          {spec.structure.map((part) => (
            <li key={part}>{part}</li>
          ))}
        </ul>
        <p className="font-semibold">Requirements</p>
        <ul className="list-disc pl-5">
          {spec.requirements.map((requirement) => (
            <li key={requirement}>{requirement}</li>
          ))}
        </ul>
        {spec.adaptable.length > 0 ? (
          <p>
            <span className="font-semibold">Adapted to a learner in:</span>{" "}
            {spec.adaptable.join(", ")}
          </p>
        ) : (
          <p>Never adapted to a learner.</p>
        )}
        <p className="text-(--muted)">Spec revision {spec.revision}</p>
      </div>
    </details>
  );
}

/**
 * One material of a lesson: its name, where it stands and the one thing to do next, with what
 * it must do kept behind Details. Whatever else the row needs goes below as children.
 */
export function MaterialRow({
  info,
  status,
  action,
  children,
}: {
  info: ContentTypeInfo;
  status: ContentStatus;
  action?: ReactNode;
  children?: ReactNode;
}) {
  return (
    <li className="space-y-2 border-t border-(--line) pt-3 first:border-t-0 first:pt-0">
      <div className="flex flex-wrap items-center justify-between gap-x-3 gap-y-2">
        <div className="flex items-center gap-3">
          <p className="text-sm font-semibold text-(--ink)">{info.label}</p>
          <Badge variant={status.variant}>{status.label}</Badge>
        </div>
        {action}
      </div>
      <Details info={info} />
      {children}
    </li>
  );
}
