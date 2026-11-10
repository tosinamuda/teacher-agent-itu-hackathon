import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { installPlugin, listPlugins, removePlugin, updatePlugin } from "../api";
import type { PluginFiles } from "../types";

const PLUGINS = ["plugins"] as const;

/** Every plugin at its latest revision. */
export function usePlugins() {
  return useQuery({ queryKey: PLUGINS, queryFn: listPlugins });
}

/** A change to a plugin changes the content types the app offers, so both lists are read again. */
function useAfterChange() {
  const queryClient = useQueryClient();
  return () => {
    void queryClient.invalidateQueries({ queryKey: PLUGINS });
    void queryClient.invalidateQueries({ queryKey: ["contentTypes"] });
  };
}

export function useInstallPlugin() {
  const afterChange = useAfterChange();
  return useMutation({
    mutationFn: (files: PluginFiles) => installPlugin(files),
    onSuccess: afterChange,
  });
}

export function useUpdatePlugin(name: string) {
  const afterChange = useAfterChange();
  return useMutation({
    mutationFn: (files: PluginFiles) => updatePlugin(name, files),
    onSuccess: afterChange,
  });
}

export function useRemovePlugin() {
  const afterChange = useAfterChange();
  return useMutation({
    mutationFn: (name: string) => removePlugin(name),
    onSuccess: afterChange,
  });
}
