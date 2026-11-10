import type { ClassBand } from "../types";

/** The words a teacher reads for each band. */
export const BAND_LABEL: Record<ClassBand, string> = {
  remediate: "Needs more practice",
  reinforce: "On track",
  extend: "Ready for extension",
};

/** Greatest need first. */
export const BAND_ORDER: ClassBand[] = ["remediate", "reinforce", "extend"];

/** An objective's band as a standing: a gap to close, on track, or a strength. */
export const STANDING_LABEL: Record<ClassBand, string> = {
  remediate: "Gap",
  reinforce: "On track",
  extend: "Strength",
};
