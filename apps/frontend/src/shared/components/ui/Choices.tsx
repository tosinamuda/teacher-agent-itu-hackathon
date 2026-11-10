/** Pick one of a few options: the chosen one outlined in ink, the rest quiet until hovered. */
export function Choices({
  options,
  value,
  onChange,
}: {
  options: { value: string; label: string }[];
  value: string | undefined;
  onChange: (value: string) => void;
}) {
  return (
    <div className="flex flex-wrap gap-1">
      {options.map((option) => (
        <button
          key={option.value}
          type="button"
          aria-pressed={option.value === value}
          onClick={() => onChange(option.value)}
          className={`border px-3 py-1 text-sm transition ${
            option.value === value
              ? "border-(--ink) font-medium text-(--ink)"
              : "border-transparent text-(--muted) hover:text-(--ink)"
          }`}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}
