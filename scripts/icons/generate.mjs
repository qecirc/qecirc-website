// Regenerate the raster brand assets: apple-touch-icon (180×180 PNG) and
// the og:image social card (1200×630 PNG).
//
// Usage: node scripts/icons/generate.mjs
//
// Why these files?
//
//   - `apple-touch-icon.png` is what Google's search-result favicon panel
//     picks (largest available raster icon) and what iOS uses for the home
//     screen — both contexts render against an opaque background, so we want
//     a SOLID WHITE backdrop with the dark gate inside.
//   - `og-card.png` is the social-share card referenced by `og:image` /
//     `twitter:image` in `Layout.astro`.
//
// The rest of the icon set is hand-managed:
//
//   - `favicon.svg` uses an inline `prefers-color-scheme` media query and
//     adapts to dark / light browser themes; modern browsers prefer it.
//   - `favicon.ico` is the legacy fallback.
//
// Text is rendered with `<text>` elements to match the typographic feel of
// `favicon.svg`. Sharp/librsvg picks a system font, so the rasterised output
// is host-dependent — re-run on macOS for visual parity with the committed
// PNGs, and verify before committing if regenerating on a different OS.
// Only commit the files you intended to change.

import sharp from "sharp";
import { Buffer } from "node:buffer";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const publicDir = path.join(projectRoot, "public");

// 64-unit viewBox keeps proportions identical to public/favicon.svg.
const ICON_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="0" y="0" width="64" height="64" fill="#ffffff"/>
  <line x1="0" y1="22" x2="64" y2="22" stroke="#111827" stroke-width="4" stroke-linecap="round"/>
  <line x1="0" y1="42" x2="64" y2="42" stroke="#111827" stroke-width="4" stroke-linecap="round"/>
  <rect x="12" y="10" width="40" height="44" rx="4" fill="#111827"/>
  <text x="32" y="42" text-anchor="middle" font-family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-weight="700" font-size="36" fill="#ffffff">Q</text>
</svg>`;

// Social card: the favicon motif as a circuit diagram — filled Q gate and the
// wordmark in an outlined gate box, both sitting on two qubit wires.
const OG_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <rect width="1200" height="630" fill="#ffffff"/>
  <line x1="0" y1="235" x2="1200" y2="235" stroke="#111827" stroke-width="10" stroke-linecap="round"/>
  <line x1="0" y1="315" x2="1200" y2="315" stroke="#111827" stroke-width="10" stroke-linecap="round"/>
  <rect x="110" y="185" width="180" height="180" rx="18" fill="#111827"/>
  <text x="200" y="310" text-anchor="middle" font-family="system-ui, -apple-system, BlinkMacSystemFont, sans-serif" font-weight="700" font-size="130" fill="#ffffff">Q</text>
  <rect x="370" y="165" width="640" height="220" rx="18" fill="#ffffff" stroke="#111827" stroke-width="10"/>
  <text x="690" y="325" text-anchor="middle" font-family="system-ui, -apple-system, BlinkMacSystemFont, sans-serif" font-weight="700" font-size="132" fill="#111827">QECirc</text>
  <text x="600" y="490" text-anchor="middle" font-family="system-ui, -apple-system, BlinkMacSystemFont, sans-serif" font-weight="400" font-size="44" fill="#6b7280">A community-driven library for quantum error correction circuits</text>
  <text x="600" y="560" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-weight="500" font-size="34" fill="#9ca3af">qecirc.com</text>
</svg>`;

const TARGETS = [
  // density scales librsvg's 72dpi rasterisation up to the target size (and
  // 2× beyond it for the og card, downscaled by resize for crisp text).
  { file: "apple-touch-icon.png", svg: ICON_SVG, width: 180, height: 180, density: (72 * 180) / 64 },
  { file: "og-card.png", svg: OG_SVG, width: 1200, height: 630, density: 144 },
];

for (const { file, svg, width, height, density } of TARGETS) {
  const out = path.join(publicDir, file);
  await sharp(Buffer.from(svg), { density: Math.round(density) })
    .resize(width, height)
    .png()
    .toFile(out);
  const stat = await fs.stat(out);
  console.log(`  ${file}: ${width}×${height}, ${stat.size} bytes`);
}

console.log("\nDone. Commit only the PNGs you intended to change.");
