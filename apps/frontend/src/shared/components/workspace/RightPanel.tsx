import { useEffect, useId, useState, type ReactNode } from "react";

/** Dispatch on `window` to bring the Agent tab forward, for example to start a message. */
export const OPEN_AGENT_EVENT = "open-agent-panel";

export type NeedsItem = {
  id: string;
  title: string;
  detail?: string;
  /** Anything the decision needs the teacher to see first: checks, a before and after. */
  body?: ReactNode;
  /** The buttons. At most one is primary. A function gets to send the teacher to the agent. */
  actions?: ReactNode | ((panel: { openAgent: () => void }) => ReactNode);
};

type TabName = "needs" | "agent";

function NeedsCard({
  item,
  openAgent,
}: {
  item: NeedsItem;
  openAgent: () => void;
}) {
  return (
    <section className="flex flex-col gap-3 border border-(--line) bg-(--surface) p-4">
      <div className="flex flex-col gap-0.5">
        <h3 className="text-sm font-semibold text-(--ink)">{item.title}</h3>
        {item.detail ? (
          <p className="text-xs text-(--ink-2)">{item.detail}</p>
        ) : null}
      </div>
      {item.body}
      {item.actions ? (
        <div className="flex flex-wrap gap-2">
          {typeof item.actions === "function"
            ? item.actions({ openAgent })
            : item.actions}
        </div>
      ) : null}
    </section>
  );
}

/**
 * The right panel. The same two tabs on every page, in this order: "Agent" (a chat about
 * the page) and "Needs you" (decisions waiting here). It opens on
 * "Needs you" only when the page itself is a decision.
 */
export function RightPanel({
  needs,
  agent,
  defaultTab = "agent",
}: {
  needs: NeedsItem[];
  agent: ReactNode;
  defaultTab?: TabName;
}) {
  const [tab, setTab] = useState<TabName>(defaultTab);
  const id = useId();
  useEffect(() => {
    const open = () => setTab("agent");
    window.addEventListener(OPEN_AGENT_EVENT, open);
    return () => window.removeEventListener(OPEN_AGENT_EVENT, open);
  }, []);
  const tabs: { name: TabName; label: string }[] = [
    { name: "agent", label: "Agent" },
    {
      name: "needs",
      label: needs.length > 0 ? `Needs you · ${needs.length}` : "Needs you",
    },
  ];

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div
        role="tablist"
        aria-label="Panel"
        className="flex gap-6 border-b border-(--line) px-6"
      >
        {tabs.map(({ name, label }) => (
          <button
            key={name}
            id={`${id}-${name}-tab`}
            role="tab"
            type="button"
            aria-selected={tab === name}
            aria-controls={`${id}-${name}-panel`}
            onClick={() => setTab(name)}
            className={`-mb-px border-b-2 py-3.5 text-sm ${
              tab === name
                ? "border-(--ink) font-semibold text-(--ink)"
                : "border-transparent text-(--ink-2) hover:text-(--ink)"
            }`}
          >
            {label}
          </button>
        ))}
      </div>
      {tabs.map(({ name }) => (
        <div
          key={name}
          id={`${id}-${name}-panel`}
          role="tabpanel"
          aria-labelledby={`${id}-${name}-tab`}
          hidden={tab !== name}
          className="flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto px-6 py-5 data-[hidden]:hidden"
          data-hidden={tab !== name ? "" : undefined}
        >
          {name === "agent" ? (
            agent
          ) : needs.length === 0 ? (
            <p className="text-xs text-(--faint)">
              Nothing is waiting for you here.
            </p>
          ) : (
            needs.map((item) => (
              <NeedsCard
                key={item.id}
                item={item}
                openAgent={() => setTab("agent")}
              />
            ))
          )}
        </div>
      ))}
    </div>
  );
}
