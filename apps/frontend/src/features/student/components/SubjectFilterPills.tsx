import { SubjectFilterOption } from "@/features/student/lib/studentLessons";

type SubjectFilterPillsProps = {
  options: SubjectFilterOption[];
  active: string;
  onSelect: (value: string) => void;
};

/** Subject tab rail (underline-active) — the primary organizer of the student workspace. */
export default function SubjectFilterPills({
  options,
  active,
  onSelect,
}: SubjectFilterPillsProps) {
  return (
    <nav className="flex flex-wrap gap-6 border-b border-(--line) text-sm">
      {options.map((option) => {
        const isActive = active === option.value;
        return (
          <button
            key={option.value}
            type="button"
            onClick={() => onSelect(option.value)}
            className={`-mb-px border-b-2 pb-2 font-medium transition-colors ${
              isActive
                ? "border-(--accent) text-(--ink)"
                : "border-transparent text-(--ink-2) hover:text-(--ink)"
            }`}
          >
            {option.label} <span className="text-(--faint)">({option.count})</span>
          </button>
        );
      })}
    </nav>
  );
}
