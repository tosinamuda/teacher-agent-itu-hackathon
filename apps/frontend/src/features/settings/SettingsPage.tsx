import type { ReactNode } from "react";

import { Button } from "@/shared/components/ui/Button";

import type { Material } from "./api";
import { usePreferences } from "./usePreferences";

const Heading = ({ children }: { children: ReactNode }) => (
  <h2 className="text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)">
    {children}
  </h2>
);

function Card({
  title,
  detail,
  children,
}: {
  title: string;
  detail: string;
  children: ReactNode;
}) {
  return (
    <li className="flex flex-col justify-between gap-4 border border-(--line) bg-(--surface) p-4">
      <div className="flex flex-col gap-1">
        <span className="text-sm font-semibold text-(--ink)">{title}</span>
        <span className="text-xs text-(--ink-2)">{detail}</span>
      </div>
      <div className="flex items-center justify-between gap-3">{children}</div>
    </li>
  );
}

/** A small switch: a thin track and a round knob. */
function Toggle({
  label,
  checked,
  disabled,
  onChange,
}: {
  label: string;
  checked: boolean;
  disabled: boolean;
  onChange: (next: boolean) => void;
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      aria-label={label}
      disabled={disabled}
      onClick={() => onChange(!checked)}
      className={`relative h-5 w-9 shrink-0 rounded-full transition-colors disabled:opacity-60 ${
        checked ? "bg-(--ink)" : "bg-(--line-2)"
      }`}
    >
      <span
        aria-hidden="true"
        className={`absolute top-0.5 size-4 rounded-full bg-white transition-all ${
          checked ? "left-[18px]" : "left-0.5"
        }`}
      />
    </button>
  );
}

const state = (material: Material): string => (material.enabled ? "On" : "Off");

/** What the signed-in teacher has switched, and the plugins they can add. */
export function SettingsPage() {
  const {
    preferences,
    library,
    isLoading,
    isError,
    switchMaterial,
    addPlugin,
    adding,
    addFailed,
    isSaving,
  } = usePreferences();
  const toAdd = library.filter((plugin) => !plugin.installed);

  return (
    <div className="mx-auto flex w-full max-w-4xl flex-col gap-8 px-8 py-6">
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold text-(--ink)">Settings</h1>
        <p className="text-xs text-(--ink-2)">These apply to you alone.</p>
      </header>

      {isLoading ? <p className="text-sm text-(--ink-2)">Loading…</p> : null}
      {isError ? (
        <p className="text-sm text-(--danger)">
          The settings could not be loaded.
        </p>
      ) : null}

      {preferences ? (
        <>
          <section aria-label="Plugins" className="flex flex-col gap-3">
            <Heading>Plugins</Heading>
            <p className="text-sm text-(--ink-2)">
              Each plugin adds a material to your lessons.
            </p>
            <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {preferences.materials.map((material) => (
                <Card
                  key={material.type}
                  title={material.label}
                  detail={material.description}
                >
                  {material.core ? (
                    <span className="text-xs text-(--ink-2)">Built in</span>
                  ) : (
                    <>
                      <span className="text-xs text-(--ink-2)">
                        {state(material)}
                      </span>
                      <Toggle
                        label={material.label}
                        checked={material.enabled}
                        disabled={isSaving}
                        onChange={(enabled) =>
                          switchMaterial({ type: material.type, enabled })
                        }
                      />
                    </>
                  )}
                </Card>
              ))}
            </ul>
          </section>

          <section
            aria-label="Available to add"
            className="flex flex-col gap-3"
          >
            <Heading>Available to add</Heading>
            {toAdd.length === 0 ? (
              <p className="text-sm text-(--ink-2)">
                Every plugin on hand is added.
              </p>
            ) : (
              <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {toAdd.map((plugin) => (
                  <Card
                    key={plugin.folder}
                    title={plugin.adds.join(", ") || plugin.folder}
                    detail={plugin.description || `Version ${plugin.version}`}
                  >
                    <span className="text-xs text-(--ink-2)">
                      Version {plugin.version}
                    </span>
                    <Button
                      size="sm"
                      isLoading={adding === plugin.folder}
                      disabled={adding !== null}
                      aria-label={`Add ${plugin.adds.join(", ") || plugin.folder}`}
                      onClick={() => addPlugin(plugin.folder)}
                    >
                      Add
                    </Button>
                  </Card>
                ))}
              </ul>
            )}
            {addFailed ? (
              <p className="text-sm text-(--danger)">
                The plugin could not be added.
              </p>
            ) : null}
          </section>
        </>
      ) : null}
    </div>
  );
}
