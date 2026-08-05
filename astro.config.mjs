// @ts-check
import { defineConfig } from "astro/config";
import node from "@astrojs/node";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  site: "https://qecirc.com",
  // One URL per page. Astro's default ("ignore") served /codes and /codes/ as
  // two 200s that self-canonicalised differently, while the prerendered pages
  // baked "/about/" against a sitemap that lists "/about". Layout.astro strips
  // the trailing slash from the canonical URL for the same reason.
  trailingSlash: "never",
  adapter: node({ mode: "standalone" }),
  server: { host: "0.0.0.0", port: parseInt(process.env.PORT || "4321") },
  prefetch: true,
  vite: {
    plugins: [tailwindcss()],
  },
});
