import { LegendPayload } from "recharts";

import { CHART } from "@/features/experiments/components/charts/chartTheme";

/** The conditions from least to most grounded, the most grounded in the accent. */
export const CONDITION_FILL: Record<string, string> = {
  C0: "#c9c3ba",
  C1: "#a39c93",
  C2: CHART.info,
  C3: CHART.accent,
};

/** P1's side in the accent, P0's in greys, "the same" between them. */
export const OUTCOME_FILL = [CHART.accent, "#e3a684", "#e7e4dd", "#a39c93", CHART.muted];

export const AXIS = { stroke: CHART.muted, fontSize: 12 } as const;

/** Legend labels in ink, whatever colour they name, so a pale series stays readable. */
export const inkLabel = (value: string) => <span style={{ color: CHART.ink }}>{value}</span>;

/** The legend in the order the bars are drawn, not alphabetical. */
export const inOrder = (order: string[]) => (item: LegendPayload) => order.indexOf(String(item.value));
