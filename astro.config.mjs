// @ts-check
import { defineConfig } from "astro/config";
import node from "@astrojs/node";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  site: "https://qecirc.com",
  adapter: node({ mode: "standalone" }),
  server: { host: "0.0.0.0", port: parseInt(process.env.PORT || "4321") },
  prefetch: true,
  vite: {
    plugins: [tailwindcss()],
  },
});
