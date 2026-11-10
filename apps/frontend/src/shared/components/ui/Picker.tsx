/** Pick one of many options from a labelled dropdown: on one line, or stacked in a narrow column. */
export function Picker({
  label,
  options,
  value,
  onChange,
  stacked = false,
}: {
  label: string;
  options: { value: string; label: string }[];
  value: string | undefined;
  onChange: (value: string) => void;
  stacked?: boolean;
}) {
  return (
    <label
      className={
        stacked ? "flex flex-col gap-1.5 text-sm" : "inline-flex items-center gap-3 text-sm"
      }
    >
      <span className="text-(--muted)">{label}</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className={`h-9 border border-(--line-2) bg-(--surface) px-3 text-(--ink) outline-none focus:border-(--ink) ${
          stacked ? "w-full" : "min-w-56"
        }`}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}
