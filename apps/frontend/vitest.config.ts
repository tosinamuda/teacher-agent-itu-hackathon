import { defineConfig, mergeConfig } from "vitest/config";

import viteConfig from "./vite.config";

// Built on the app's own Vite config, so a component under test is compiled by the same
// React Compiler the app ships with. A component test opts into a DOM with a
// `// @vitest-environment jsdom` comment.
export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      include: ["src/**/*.test.ts", "src/**/*.test.tsx"],
      environment: "node",
    },
  })
);
