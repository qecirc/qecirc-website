// `crumbleUrl` must agree with stim, byte for byte, on every committed body.
//
// The Crumble link used to be computed by stim in the ingestion pipeline and
// stored per circuit. It is now derived in src/lib/stim-format.ts by a
// hand-written reimplementation of `stim.Circuit.to_crumble_url()` — line join,
// three abbreviated instruction names, the comma/paren spacing rules, the
// trailing underscore. Nothing else in the repository exercises that function
// against the thing it imitates, so without this test a stim upgrade, or an edit
// to CRUMBLE_ABBREVIATIONS or PAREN_ARGS, would break every link on the site and
// pass every check.
//
// `crumble_reference.py` prints what stim says for each body; this diffs it.
//
// Scope: exact agreement holds for *canonical* stim text — what `str(circuit)`
// emits, which is what the pipeline writes and what is committed. It is not a
// general stim parser: a hand-edited body using a gate alias (`CORRELATED_ERROR`
// for `E`) or carrying a `#` comment would round-trip through stim to different
// text and so derive a different URL. No committed body does either, and the
// assertion below is what keeps that true.

import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { crumbleUrl } from "../../src/lib/stim-format.ts";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const circuitsDir = path.join(root, "data_yaml", "circuits");

function stimReferenceUrls() {
  // maxBuffer: the corpus is a few MB of URLs and the default is 1 MB.
  const stdout = execFileSync("uv", ["run", "python", "scripts/tests/crumble_reference.py"], {
    cwd: root,
    encoding: "utf-8",
    maxBuffer: 256 * 1024 * 1024,
  });
  return stdout
    .split("\n")
    .filter(Boolean)
    .map((line) => {
      const [name, canonical, url] = line.split("\t");
      return { name, canonical: canonical === "1", url };
    });
}

test("crumbleUrl reproduces stim.Circuit.to_crumble_url for every body", () => {
  const reference = stimReferenceUrls();
  assert.ok(reference.length > 0, "reference produced no rows — is stim installed?");

  const mismatches = [];
  for (const { name, url } of reference) {
    const body = fs.readFileSync(path.join(circuitsDir, name), "utf-8");
    const got = crumbleUrl(body);
    if (got !== url) {
      let i = 0;
      while (i < Math.min(got.length, url.length) && got[i] === url[i]) i++;
      mismatches.push(
        `${name}: diverges at ${i}\n  stim: …${url.slice(Math.max(0, i - 40), i + 40)}…` +
          `\n  ours: …${got.slice(Math.max(0, i - 40), i + 40)}…`,
      );
    }
  }

  assert.deepEqual(
    mismatches,
    [],
    `${mismatches.length} of ${reference.length} bodies disagree with stim:\n${mismatches
      .slice(0, 5)
      .join("\n")}`,
  );
});

test("every committed body is canonical stim text", () => {
  // The guarantee above is only exact for canonical text, so assert the corpus
  // is canonical rather than hoping. A body that fails this — a gate alias, a
  // `#` comment, odd spacing — would still load in stim; it would just derive a
  // Crumble link for differently-spelled text than the page displays.
  const notCanonical = stimReferenceUrls()
    .filter((r) => !r.canonical)
    .map((r) => r.name);
  assert.deepEqual(notCanonical, [], "bodies are not a fixed point of str(stim.Circuit(...))");
});
