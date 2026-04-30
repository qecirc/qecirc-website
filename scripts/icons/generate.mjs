// Regenerate the raster icons (apple-touch-icon, favicon-96) from a shared
// SVG so they stay in sync.
//
// Usage: node scripts/icons/generate.mjs
//
// The design intentionally departs from `public/favicon.svg`'s
// prefers-color-scheme switch: those colour-scheme media queries are
// evaluated against the OS preference (not the page or tab-strip), so the
// favicon often ends up rendered against a mismatched background. The
// raster icons render in many third-party contexts (iOS home screen,
// Google search results) where we have no control over the surrounding
// surface, so we pick a single high-contrast design: dark gate + white "Q"
// on a solid white background.
//
// The "Q" is a hand-traced SVG path rather than a `<text>` element so the
// output is deterministic across machines (sharp's text rendering depends
// on the system fonts present, which differ between macOS, Linux CI, etc.).

import sharp from "sharp";
import { Buffer } from "node:buffer";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const publicDir = path.join(projectRoot, "public");

// 64-unit viewBox keeps proportions identical to public/favicon.svg.
// The "Q" glyph is two paths: a filled ring (outer ellipse with the inner
// counter cut out via fill-rule="evenodd") plus a short diagonal tail.
const SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="0" y="0" width="64" height="64" fill="#ffffff"/>
  <line x1="0" y1="22" x2="64" y2="22" stroke="#111827" stroke-width="4" stroke-linecap="round"/>
  <line x1="0" y1="42" x2="64" y2="42" stroke="#111827" stroke-width="4" stroke-linecap="round"/>
  <rect x="12" y="10" width="40" height="44" rx="4" fill="#111827"/>
  <path fill="#ffffff" fill-rule="evenodd" d="M 20 32 C 20 24 25 18 32 18 C 39 18 44 24 44 32 C 44 40 39 46 32 46 C 25 46 20 40 20 32 Z M 26 32 C 26 28 29 24 32 24 C 35 24 38 28 38 32 C 38 36 35 40 32 40 C 29 40 26 36 26 32 Z"/>
  <path fill="#ffffff" d="M 36 38 L 38 36 L 46 44 L 44 46 Z"/>
</svg>`;

const TARGETS = [
  { file: "apple-touch-icon.png", size: 180 },
  { file: "favicon-96.png", size: 96 },
];

const svgBuffer = Buffer.from(SVG);

for (const { file, size } of TARGETS) {
  const out = path.join(publicDir, file);
  await sharp(svgBuffer, { density: Math.round((72 * size) / 64) })
    .resize(size, size)
    .png()
    .toFile(out);
  const stat = await fs.stat(out);
  console.log(`  ${file}: ${size}×${size}, ${stat.size} bytes`);
}

console.log("\nDone. Commit `public/apple-touch-icon.png` and `public/favicon-96.png`.");
