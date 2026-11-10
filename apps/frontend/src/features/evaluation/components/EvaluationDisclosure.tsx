import { ReactNode, useState } from "react";

type EvaluationDisclosureProps = {
  title: string;
  summary?: string;
  defaultOpen?: boolean;
  children: ReactNode;
};

/** A restrained disclosure surface for secondary evaluation context. */
export function EvaluationDisclosure({
  title,
  summary,
  defaultOpen = false,
  children,
}: EvaluationDisclosureProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <section className="overflow-hidden rounded-3xl border border-[color:var(--line)] bg-[color:var(--panel)]">
      <button
        className="flex w-full items-center justify-between gap-4 px-4 py-3 text-left"
        onClick={() => setIsOpen((current) => !current)}
        type="button"
      >
        <div className="space-y-1">
          <p className="text-sm font-semibold text-[color:var(--ink)]">{title}</p>
          {summary ? (
            <p className="text-sm text-[color:var(--muted)]">{summary}</p>
          ) : null}
        </div>
        <span
          className={`text-xs font-semibold text-[color:var(--accent-deep)] transition ${
            isOpen ? "rotate-180" : ""
          }`}
        >
          ▾
        </span>
      </button>
      {isOpen ? (
        <div className="border-t border-[color:var(--line)] px-4 py-4">{children}</div>
      ) : null}
    </section>
  );
}
