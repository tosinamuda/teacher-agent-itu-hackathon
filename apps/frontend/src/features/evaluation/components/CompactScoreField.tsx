type CompactScoreOption = {
  value: number | string;
  label: string;
};

type CompactScoreFieldProps = {
  label: string;
  description?: string;
  value: number | string | undefined;
  options: CompactScoreOption[];
  onChange: (nextValue: number | string) => void;
};

const optionLabelText = (label: string) => {
  const trimmed = label.trim();
  const remainder = trimmed.split(" ").slice(1).join(" ");
  return remainder || trimmed;
};

/** Renders a compact discrete ordinal scale for dense rating sidebars. */
export function CompactScoreField({
  label,
  description,
  value,
  options,
  onChange,
}: CompactScoreFieldProps) {
  const selectedOption = options.find((option) => String(option.value) === String(value));
  const rangeStartLabel = options.find((option) => optionLabelText(option.label) !== "N/A");
  const rangeEndLabel = options.at(-1);

  return (
    <div className="space-y-2 rounded-none border border-[color:var(--line)] bg-white px-3 py-2.5">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 space-y-1">
          <p className="text-sm font-semibold text-[color:var(--ink)]">{label}</p>
          {description ? (
            <p className="text-xs leading-5 text-[color:var(--muted)]">{description}</p>
          ) : null}
        </div>
        <span className="shrink-0 rounded-none bg-[color:var(--panel)] px-2.5 py-1 text-[11px] font-semibold text-[color:var(--accent-deep)]">
          {selectedOption?.label ?? "Select"}
        </span>
      </div>

      <div className="flex gap-1.5">
        {options.map((option) => {
          const isSelected = String(option.value) === String(value);
          return (
            <button
              aria-label={option.label}
              key={String(option.value)}
              className={[
                "min-w-0 flex-1 rounded-none border px-0 py-2 text-center text-sm font-semibold transition",
                "focus:outline-hidden focus:ring-2 focus:ring-[color:var(--accent)] focus:ring-offset-2",
                isSelected
                  ? "border-[color:var(--accent)] bg-[color:var(--accent)] text-white"
                  : "border-[color:var(--line)] bg-[color:var(--surface)] text-[color:var(--ink)] hover:border-[color:var(--accent)]",
              ].join(" ")}
              onClick={() => onChange(option.value)}
              type="button"
            >
              {String(option.value)}
            </button>
          );
        })}
      </div>

      {rangeStartLabel && rangeEndLabel ? (
        <div className="flex items-center justify-between text-[11px] text-[color:var(--muted)]">
          <span>{optionLabelText(rangeStartLabel.label)}</span>
          <span>{optionLabelText(rangeEndLabel.label)}</span>
        </div>
      ) : null}
    </div>
  );
}
