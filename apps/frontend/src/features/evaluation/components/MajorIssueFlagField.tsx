import { UseFormRegisterReturn } from "react-hook-form";

import { EvaluationMajorIssueFlag } from "../types";

type MajorIssueFlagFieldProps = {
  flags: EvaluationMajorIssueFlag[];
  selected: string[];
  onToggle: (key: string) => void;
  showOther: boolean;
  otherProps: UseFormRegisterReturn;
};

/**
 * Renders the Protocol §3.4 H1 major-issue checklist — a categorical
 * failure-mode tag the rater ticks alongside the 1-5 dimension scores. When the
 * "Other" flag is selected a free-text detail field is revealed.
 */
export function MajorIssueFlagField({
  flags,
  selected,
  onToggle,
  showOther,
  otherProps,
}: MajorIssueFlagFieldProps) {
  return (
    <fieldset className="space-y-3">
      <div className="space-y-1">
        <legend className="text-sm font-medium text-[color:var(--ink)]">
          Flag any problems (optional)
        </legend>
        <p className="text-sm leading-6 text-[color:var(--muted)]">
          Tick all that apply. These are separate from the scores above — leave blank if none
          apply.
        </p>
      </div>
      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
        {flags.map((flag) => (
          <label
            key={flag.key}
            className="flex items-start gap-2 text-sm text-[color:var(--ink)]"
          >
            <input
              checked={selected.includes(flag.key)}
              className="mt-0.5 h-4 w-4 shrink-0 accent-[color:var(--accent)]"
              onChange={() => onToggle(flag.key)}
              type="checkbox"
            />
            <span>
              <span className="font-medium">{flag.label}</span>
              {flag.description ? (
                <span className="block text-xs leading-5 text-[color:var(--muted)]">
                  {flag.description}
                </span>
              ) : null}
            </span>
          </label>
        ))}
      </div>
      {showOther ? (
        <input
          className="w-full rounded-none border border-[color:var(--line)] bg-white px-4 py-2 text-sm text-[color:var(--ink)] outline-none transition focus:border-[color:var(--accent)]"
          placeholder="Describe the other issue"
          type="text"
          {...otherProps}
        />
      ) : null}
    </fieldset>
  );
}
