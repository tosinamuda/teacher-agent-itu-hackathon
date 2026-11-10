import { useState } from "react";

import { useContentTypes } from "@/features/content/hooks/useContent";
import { Badge } from "@/shared/components/ui/Badge";
import { Button } from "@/shared/components/ui/Button";
import { TabBar } from "@/shared/components/ui/TabBar";

import {
  useInstallPlugin,
  usePlugins,
  useRemovePlugin,
  useUpdatePlugin,
} from "../hooks/usePlugins";
import { problemsOf } from "../lib/problems";
import type { PluginRevision } from "../types";
import { FolderPicker } from "./FolderPicker";
import { GeneratorsPanel } from "./GeneratorsPanel";

const SHIPS_WITH_APP = "Ships with the app: a deploy installs and updates it.";

const TABS = [
  { href: "/research/plugins", label: "Plugins", tab: "plugins" },
  {
    href: "/research/plugins/generators",
    label: "Generators",
    tab: "generators",
  },
] as const;

/** Researcher: the plugins that add kinds of content, and the generators each kind can use. */
export function PluginsPage({ tab }: { tab: (typeof TABS)[number]["tab"] }) {
  const { data: plugins, isLoading, isError } = usePlugins();
  const types = useContentTypes();
  const install = useInstallPlugin();
  const [problems, setProblems] = useState<string[]>([]);
  const labels = new Map(types.data?.map((type) => [type.type, type.label]));

  return (
    <main className="flex w-full flex-col gap-6 py-8">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div className="space-y-1">
          <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent)">
            Researcher · Plugins
          </p>
          <h1 className="text-2xl font-semibold text-(--ink)">Plugins</h1>
          <p className="max-w-2xl text-sm text-(--muted)">
            Each plugin adds one kind of content, or a generator for a kind that
            exists: its spec, its skills and its tools. Add a plugin by choosing
            its folder. Teachers can generate an installed kind from any lesson.
          </p>
        </div>
        <FolderPicker
          label="Add a plugin"
          variant="primary"
          busy={install.isPending}
          onFiles={(files) => {
            setProblems([]);
            install.mutate(files, {
              onError: (error) => setProblems(problemsOf(error)),
            });
          }}
          onProblem={(problem) => setProblems([problem])}
        />
      </header>

      <Problems lines={problems} onClose={() => setProblems([])} />

      <TabBar
        label="Plugins"
        tabs={TABS.map((item) => ({ ...item, active: item.tab === tab }))}
      />

      {tab === "generators" ? (
        <GeneratorsPanel />
      ) : (
        <>
          {isLoading ? (
            <p className="text-sm text-(--muted)">Loading plugins…</p>
          ) : isError ? (
            <p className="text-sm text-(--danger)">
              Couldn&apos;t load plugins.
            </p>
          ) : !plugins?.length ? (
            <p className="text-sm text-(--muted)">No plugin is installed.</p>
          ) : (
            <div className="overflow-x-auto border border-(--line) bg-(--surface)">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-(--line) text-[11px] font-semibold uppercase tracking-[0.08em] text-(--muted)">
                  <tr>
                    <th className="px-4 py-3">Plugin</th>
                    <th className="px-4 py-3">Content type</th>
                    <th className="px-4 py-3">Revision</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {inPluginOrder(plugins).map((plugin, index, rows) => (
                    <PluginRow
                      key={plugin.name}
                      first={
                        index === 0 || rows[index - 1].plugin !== plugin.plugin
                      }
                      plugin={plugin}
                      label={labels.get(plugin.type)}
                      onProblems={setProblems}
                    />
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </main>
  );
}

function Problems({
  lines,
  onClose,
}: {
  lines: string[];
  onClose: () => void;
}) {
  if (lines.length === 0) return null;
  return (
    <div
      role="alert"
      className="border border-[#e7c9c5] bg-(--danger-tint) p-4 text-sm text-(--danger-ink)"
    >
      <div className="flex items-start justify-between gap-4">
        <p className="font-semibold">The plugin was not changed.</p>
        <button type="button" onClick={onClose} className="text-xs underline">
          Dismiss
        </button>
      </div>
      <ul className="mt-2 list-disc space-y-1 pl-5">
        {lines.map((line) => (
          <li key={line}>{line}</li>
        ))}
      </ul>
    </div>
  );
}

/** The rows of one plugin together, so a plugin that makes several things is one block. */
function inPluginOrder(plugins: PluginRevision[]): PluginRevision[] {
  return [...plugins].sort(
    (a, b) => a.plugin.localeCompare(b.plugin) || a.name.localeCompare(b.name),
  );
}

function PluginRow({
  plugin,
  first,
  label,
  onProblems,
}: {
  plugin: PluginRevision;
  /** The first row of its plugin, which names the plugin. */
  first: boolean;
  label: string | undefined;
  onProblems: (problems: string[]) => void;
}) {
  const update = useUpdatePlugin(plugin.name);
  const remove = useRemovePlugin();
  const [confirming, setConfirming] = useState(false);
  const removed = plugin.status === "removed";
  const locked = plugin.system;

  return (
    <tr
      className={`border-b border-(--line) align-top last:border-b-0 ${removed ? "opacity-60" : ""}`}
    >
      <td className="px-4 py-3">
        {first ? (
          <div className="font-medium text-(--ink)">{plugin.plugin}</div>
        ) : null}
        <div className="font-mono text-[11px] text-(--muted)">
          {plugin.name} · v{plugin.version}
        </div>
      </td>
      <td className="px-4 py-3">
        <div className="text-(--ink)">{label ?? plugin.type}</div>
        {plugin.implements ? (
          <div className="text-[11px] text-(--muted)">
            Generator for this kind
          </div>
        ) : null}
        <div className="font-mono text-[11px] text-(--muted)">
          {plugin.type}
        </div>
      </td>
      <td className="px-4 py-3 text-(--ink-2)">
        {plugin.revision} · spec {plugin.spec_revision}
        {plugin.installed_by ? (
          <div className="text-[11px] text-(--muted)">
            by {plugin.installed_by}
          </div>
        ) : null}
      </td>
      <td className="px-4 py-3">
        <div className="flex flex-wrap gap-1.5">
          <Badge variant={removed ? "outline" : "success"}>
            {removed ? "Removed" : "Installed"}
          </Badge>
          {locked ? (
            <Badge variant="accent" title={SHIPS_WITH_APP}>
              System
            </Badge>
          ) : null}
        </div>
      </td>
      <td className="px-4 py-3">
        <div className="flex flex-wrap justify-end gap-2">
          <FolderPicker
            label="Update"
            disabled={locked || removed}
            title={
              locked
                ? SHIPS_WITH_APP
                : removed
                  ? "A removed plugin is not updated."
                  : undefined
            }
            busy={update.isPending}
            onFiles={(files) => {
              onProblems([]);
              update.mutate(files, {
                onError: (error) => onProblems(problemsOf(error)),
              });
            }}
            onProblem={(problem) => onProblems([problem])}
          />
          {confirming ? (
            <>
              <Button
                size="sm"
                variant="danger"
                isLoading={remove.isPending}
                onClick={() => {
                  onProblems([]);
                  remove.mutate(plugin.name, {
                    onError: (error) => onProblems(problemsOf(error)),
                    onSettled: () => setConfirming(false),
                  });
                }}
              >
                Confirm removal
              </Button>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => setConfirming(false)}
              >
                Keep
              </Button>
            </>
          ) : (
            <Button
              size="sm"
              variant="outline"
              disabled={locked || removed}
              title={
                locked
                  ? SHIPS_WITH_APP
                  : removed
                    ? "Already removed."
                    : "Stops new drafts of this kind."
              }
              onClick={() => setConfirming(true)}
            >
              Remove
            </Button>
          )}
        </div>
      </td>
    </tr>
  );
}
