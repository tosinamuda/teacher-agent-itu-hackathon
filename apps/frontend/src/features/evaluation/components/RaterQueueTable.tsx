import { Link } from "@/shared/router";

import { EvaluationHypothesis, EvaluationPacketQueueItem } from "../types";

type RaterQueueTableProps = {
  hypothesis: EvaluationHypothesis;
  packets: EvaluationPacketQueueItem[];
};

/** One grouped section of the packet queue (e.g. "To rate" or "Completed"). */
function PacketGroup({
  hypothesis,
  packets,
  label,
  actionLabel,
}: {
  hypothesis: EvaluationHypothesis;
  packets: EvaluationPacketQueueItem[];
  label: string;
  actionLabel: string;
}) {
  if (packets.length === 0) {
    return null;
  }
  return (
    <section className="space-y-2">
      <h3 className="text-sm font-semibold text-[color:var(--ink)]">
        {label} ({packets.length})
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full border-separate border-spacing-y-2 text-left text-sm">
          <tbody>
            {packets.map((packet) => (
              <tr key={packet.evaluation_packet_id} className="rounded-2xl bg-(--surface)">
                <td className="px-3 py-3">
                  <div className="font-semibold text-[color:var(--ink)]">
                    {packet.candidate_label
                      ? `${packet.candidate_label} · ${packet.packet_code}`
                      : packet.packet_code}
                  </div>
                  <div className="text-xs text-[color:var(--muted)]">{packet.status}</div>
                </td>
                <td className="px-3 py-3 text-right">
                  <Link
                    className="text-sm font-semibold text-[color:var(--accent-deep)] hover:underline"
                    href={`/research/rater/${hypothesis.toLowerCase()}/${packet.evaluation_packet_id}`}
                  >
                    {actionLabel}
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

/**
 * Renders the H1/H2 packet queue, split into "To rate" (unrated) and "Completed"
 * (already scored) so the live queue isn't cluttered by finished work.
 */
export function RaterQueueTable({ hypothesis, packets }: RaterQueueTableProps) {
  if (packets.length === 0) {
    return (
      <p className="text-sm text-[color:var(--muted)]">
        No revision notes are ready for review yet.
      </p>
    );
  }

  const toRate = packets.filter((packet) => !packet.rating);
  const completed = packets.filter((packet) => packet.rating);

  return (
    <div className="space-y-6">
      <PacketGroup hypothesis={hypothesis} packets={toRate} label="To rate" actionLabel="Open" />
      <PacketGroup
        hypothesis={hypothesis}
        packets={completed}
        label="Completed"
        actionLabel="Review"
      />
    </div>
  );
}
