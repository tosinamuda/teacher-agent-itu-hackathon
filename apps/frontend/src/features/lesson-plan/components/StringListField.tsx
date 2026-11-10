import { useState } from "react";

const fieldClass =
  "w-full border border-(--line-2) bg-(--surface) px-3 py-2 text-sm text-(--ink) outline-none focus:border-(--accent)";
const labelClass =
  "text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)";

/** Edit a list of free-text strings: per-row edit + remove, plus an add field. */
export function StringListField({
  label,
  items,
  onChange,
}: {
  label: string;
  items: string[];
  onChange: (items: string[]) => void;
}) {
  const [draftNew, setDraftNew] = useState("");
  const add = () => {
    if (!draftNew.trim()) return;
    onChange([...items, draftNew.trim()]);
    setDraftNew("");
  };
  return (
    <section className="space-y-2">
      <p className={labelClass}>{label}</p>
      {items.map((item, index) => (
        <div key={index} className="flex items-center gap-2">
          <input
            className={fieldClass}
            value={item}
            onChange={(event) =>
              onChange(
                items.map((value, i) =>
                  i === index ? event.target.value : value,
                ),
              )
            }
          />
          <button
            type="button"
            onClick={() => onChange(items.filter((_, i) => i !== index))}
            className="shrink-0 text-xs text-(--muted) hover:text-(--danger)"
          >
            remove
          </button>
        </div>
      ))}
      <div className="flex items-center gap-2">
        <input
          className={fieldClass}
          value={draftNew}
          placeholder={`Add ${label.toLowerCase()}…`}
          onChange={(event) => setDraftNew(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              event.preventDefault();
              add();
            }
          }}
        />
        <button
          type="button"
          onClick={add}
          className="shrink-0 text-xs font-semibold text-(--accent-deep) hover:underline"
        >
          add
        </button>
      </div>
    </section>
  );
}
