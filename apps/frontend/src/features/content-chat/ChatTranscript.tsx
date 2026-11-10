import { useEffect, useRef, useState } from "react";

import { McpAppView } from "@/features/mcp-app/McpAppView";
import { RevisionSummary } from "@/shared/components/renderer/RevisionSummary";
import { Button } from "@/shared/components/ui/Button";

import { StepsCard } from "./StepsCard";
import { blocksOf, type Block } from "./steps";
import { runningLine } from "./toolLine";
import type { Line, Transcript } from "./transcript";

const BUBBLE: Record<"teacher" | "error", string> = {
  teacher: "ml-8 border border-(--line) bg-(--accent-soft) text-(--ink)",
  error: "border border-[#e7c9c5] bg-(--danger-tint) text-(--danger-ink)",
};

/**
 * The content the agent saved, drawn by the server's own page inside the chat. Only the latest
 * is open; an earlier one is a button, so a long chat does not hold a frame for every turn.
 */
function View({
  line,
  open,
}: {
  line: Extract<Line, { from: "view" }>;
  open: boolean;
}) {
  const [shown, setShown] = useState(false);
  if (!open && !shown) {
    return (
      <li>
        <Button size="sm" variant="outline" onClick={() => setShown(true)}>
          Show the content
        </Button>
      </li>
    );
  }
  return (
    <li data-chat-view>
      <p className="mb-1 text-[11px] uppercase tracking-[0.12em] text-(--muted)">
        The content now
        {line.version !== null ? ` · version ${line.version}` : ""}
      </p>
      <McpAppView
        tool={line.tool}
        input={line.input}
        revision={String(line.version)}
        fallback={
          <p className="text-xs text-(--muted)">
            This content has no page to show.
          </p>
        }
      />
    </li>
  );
}

function LineView({
  line,
  latestView,
}: {
  line: Extract<Block, { kind: "line" }>["line"];
  latestView: string | null;
}) {
  switch (line.from) {
    case "note":
      return (
        <li className="text-center text-xs text-(--muted)">{line.text}</li>
      );
    case "view":
      return <View line={line} open={line.id === latestView} />;
    case "agent":
      return line.minor ? (
        <li className="mr-8 border-l-2 border-(--line) pl-3 text-xs text-(--muted)">
          <RevisionSummary text={line.text} blocks />
        </li>
      ) : (
        <li className="px-1 py-1 text-sm text-(--ink)">
          <RevisionSummary text={line.text} blocks />
        </li>
      );
    default:
      return (
        <li className={`px-3 py-2 text-sm ${BUBBLE[line.from]}`}>
          {line.from === "teacher" && line.pointed ? (
            <p className="mb-1 border-l-2 border-(--accent) pl-2 text-xs text-(--muted)">
              {line.pointed}
            </p>
          ) : null}
          <span className="whitespace-pre-wrap">{line.text}</span>
        </li>
      );
  }
}

/** The teacher wrote after the card, so the agent has not begun its work on it. */
function lastTeacherAfter(blocks: readonly Block[], index: number): boolean {
  return blocks
    .slice(index + 1)
    .some((block) => block.kind === "line" && block.line.from === "teacher");
}

/** A chat drawn from its events: messages, the agent's text as it is written, tools, and views. */
export function ChatTranscript({
  transcript,
  queued,
}: {
  transcript: Transcript;
  queued: readonly string[];
}) {
  const end = useRef<HTMLDivElement>(null);
  const latestView =
    [...transcript.lines].reverse().find((line) => line.from === "view")?.id ??
    null;
  const blocks = blocksOf(transcript.lines);
  const lastCard = blocks.findLastIndex((block) => block.kind === "steps");
  const inSteps =
    transcript.working && lastCard >= 0 && !lastTeacherAfter(blocks, lastCard);
  const growing = transcript.partial?.text.length ?? 0;

  useEffect(() => {
    end.current?.scrollIntoView?.({ block: "end" });
  }, [transcript.lines.length, growing, queued.length]);

  return (
    <ul className="flex-1 space-y-2 overflow-y-auto" aria-live="polite">
      {blocks.map((block, index) =>
        block.kind === "steps" ? (
          <StepsCard
            key={block.id}
            steps={block.steps}
            active={transcript.working && index === lastCard}
            workingOn={transcript.workingOn}
          />
        ) : (
          <LineView
            key={block.line.id}
            line={block.line}
            latestView={latestView}
          />
        ),
      )}
      {queued.map((text, index) => (
        <li
          key={`q${index}`}
          className={`px-3 py-2 text-sm opacity-70 ${BUBBLE.teacher}`}
        >
          <span className="whitespace-pre-wrap">{text}</span>
          <span className="ml-2 text-xs text-(--muted)">queued</span>
        </li>
      ))}
      {transcript.partial ? (
        <li className="px-1 py-1 text-sm text-(--ink)" data-partial>
          <span className="whitespace-pre-wrap">{transcript.partial.text}</span>
          <span className="animate-pulse text-(--muted)"> ▍</span>
        </li>
      ) : null}
      {transcript.working && !transcript.partial && !inSteps ? (
        <li className="text-center text-xs text-(--muted)">
          {transcript.workingOn
            ? `${runningLine(transcript.workingOn)}…`
            : "The agent is working…"}
        </li>
      ) : null}
      <div ref={end} />
    </ul>
  );
}
