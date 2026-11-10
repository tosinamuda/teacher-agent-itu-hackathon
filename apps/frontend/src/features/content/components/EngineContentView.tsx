import { fieldTitle, fieldsOf, kindOf, partsFor } from "../engineParts";
import { EngineManifest, PartField, Spec } from "../types";
import { NoteText } from "./NoteText";

type Row = Record<string, unknown>;

function Fields({ fields, row }: { fields: PartField[]; row: Row }) {
  return (
    <>
      {fields.map((field) => (
        <Field key={field.name} field={field} value={row[field.name]} />
      ))}
    </>
  );
}

function Item({ field, item }: { field: PartField; item: Row }) {
  const kind = field.kinds ? kindOf(item, field.kinds) : undefined;
  return (
    <li className="space-y-2 rounded-xl border border-(--line) p-3">
      {kind && (
        <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-(--ink-2)">
          {fieldTitle(kind.name)}
        </p>
      )}
      <Fields fields={kind?.fields ?? field.fields ?? []} row={item} />
    </li>
  );
}

function FieldValue({ field, value }: { field: PartField; value: unknown }) {
  if (field.type === "group" && value && typeof value === "object") {
    return (
      <div className="space-y-2 border-l-2 border-(--line) pl-3">
        <Fields fields={field.fields ?? []} row={value as Row} />
      </div>
    );
  }
  if (field.type === "items" && Array.isArray(value)) {
    return (
      <ol className="space-y-3">
        {value.map((item, index) => (
          <Item key={index} field={field} item={item as Row} />
        ))}
      </ol>
    );
  }
  if (Array.isArray(value)) {
    return (
      <ul className="list-disc space-y-1 pl-5 text-sm text-(--ink)">
        {value.map((entry, index) => (
          <li key={index}>
            <NoteText text={String(entry)} />
          </li>
        ))}
      </ul>
    );
  }
  if (field.type === "yes_no")
    return <p className="text-sm text-(--ink)">{value ? "Yes" : "No"}</p>;
  return <NoteText text={String(value)} />;
}

function Field({ field, value }: { field: PartField; value: unknown }) {
  if (value === undefined || value === null) return null;
  return (
    <div className="space-y-1">
      <p className="text-xs font-semibold text-(--ink-2)">
        {fieldTitle(field.name)}
      </p>
      <FieldValue field={field} value={value} />
    </div>
  );
}

/** Content drafted part by part: one section per unit, each drawn from its unit's schema. */
export function EngineContentView({
  manifest,
  spec,
}: {
  manifest: EngineManifest;
  spec: Spec | null;
}) {
  return (
    <ol className="space-y-5">
      {manifest.sections.map((section) => (
        <li
          key={section.unit_id}
          className="space-y-3 rounded-2xl border border-(--line) bg-(--surface) p-5"
        >
          <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
            {section.label}
          </p>
          <Fields
            fields={fieldsOf(section.part, partsFor(section, spec))}
            row={section.part}
          />
        </li>
      ))}
    </ol>
  );
}
