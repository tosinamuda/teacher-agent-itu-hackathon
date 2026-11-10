import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  addFromLibrary,
  getLibrary,
  getPreferences,
  switchMaterial,
  type Preferences,
} from "./api";

const PREFERENCES = ["teacherPreferences"] as const;
const LIBRARY = ["pluginLibrary"] as const;

/** The signed-in teacher's settings, the plugins to add, and what changes them. */
export function usePreferences() {
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: PREFERENCES, queryFn: getPreferences });
  const library = useQuery({ queryKey: LIBRARY, queryFn: getLibrary });

  const saved = (preferences: Preferences) => {
    queryClient.setQueryData(PREFERENCES, preferences);
    // What a lesson offers to make comes from the types the teacher has on.
    void queryClient.invalidateQueries({ queryKey: ["contentTypes"] });
  };
  const material = useMutation({
    mutationFn: ({ type, enabled }: { type: string; enabled: boolean }) =>
      switchMaterial(type, enabled),
    onSuccess: saved,
  });
  const add = useMutation({
    mutationFn: addFromLibrary,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: PREFERENCES });
      void queryClient.invalidateQueries({ queryKey: LIBRARY });
      void queryClient.invalidateQueries({ queryKey: ["contentTypes"] });
    },
  });

  return {
    preferences: query.data,
    library: library.data ?? [],
    isLoading: query.isLoading,
    isError: query.isError,
    switchMaterial: material.mutate,
    addPlugin: add.mutate,
    adding: add.isPending ? add.variables : null,
    addFailed: add.isError,
    isSaving: material.isPending,
  };
}
