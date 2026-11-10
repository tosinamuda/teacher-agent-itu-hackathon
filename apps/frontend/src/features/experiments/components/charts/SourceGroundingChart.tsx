import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { SourceAuditDescriptives } from "../../lib/experiments";
import { AUDIT_CRITERION_LABELS, CHART, labelFor } from "./chartTheme";

/** Source-grounding audit pass/partial/fail proportions per criterion (stacked). */
export function SourceGroundingChart({ audit }: { audit: SourceAuditDescriptives }) {
  if (!audit || audit.n_ratings === 0) {
    return (
      <p className="py-8 text-center text-sm text-[color:var(--muted)]">
        No source-grounding ratings yet (C2–C4 audit).
      </p>
    );
  }
  const data = Object.entries(audit.criteria).map(([criterion, counts]) => {
    const total = counts.pass + counts.partial + counts.fail || 1;
    return {
      criterion: labelFor(AUDIT_CRITERION_LABELS, criterion),
      Pass: Math.round((100 * counts.pass) / total),
      Partial: Math.round((100 * counts.partial) / total),
      Fail: Math.round((100 * counts.fail) / total),
    };
  });
  return (
    <ResponsiveContainer width="100%" height={240}>
      <BarChart layout="vertical" data={data} margin={{ top: 8, right: 8, bottom: 4, left: 24 }}>
        <CartesianGrid stroke={CHART.line} horizontal={false} />
        <XAxis type="number" domain={[0, 100]} stroke={CHART.muted} fontSize={12} unit="%" />
        <YAxis type="category" dataKey="criterion" stroke={CHART.muted} fontSize={11} width={104} />
        <Tooltip formatter={(value) => `${Number(value)}%`} />
        <Legend wrapperStyle={{ fontSize: 11 }} />
        <Bar dataKey="Pass" stackId="a" fill={CHART.success} />
        <Bar dataKey="Partial" stackId="a" fill={CHART.warning} />
        <Bar dataKey="Fail" stackId="a" fill={CHART.danger} />
      </BarChart>
    </ResponsiveContainer>
  );
}
