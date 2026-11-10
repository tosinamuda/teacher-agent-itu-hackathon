import path from "node:path";

import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// React Compiler stays on (it was `reactCompiler: true` under Next) — same
// babel plugin, applied through the Vite react plugin instead.
export default defineConfig({
  plugins: [
    react({
      babel: { plugins: [["babel-plugin-react-compiler", {}]] },
    }),
    tailwindcss(),
  ],
  resolve: {
    alias: { "@": path.resolve(__dirname, "src") },
  },
  server: { port: 3000 },
  preview: { port: 3000 },
});
