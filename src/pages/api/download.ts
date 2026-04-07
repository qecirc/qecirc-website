export const prerender = false;

import type { APIRoute } from "astro";
import {
  getCodeBySlug,
  filterCircuitsForCode,
  getCircuitsForCode,
  getBodiesForCircuits,
  hasActiveFilters,
} from "../../lib/queries";
import { parseCircuitParams } from "../../lib/url";
import { buildStimFilename } from "../../lib/filename";
import { createZip } from "../../lib/zip";

export const GET: APIRoute = ({ url }) => {
  const codeSlug = url.searchParams.get("code");
  if (!codeSlug) {
    return new Response("Missing 'code' parameter", { status: 400 });
  }

  const code = getCodeBySlug(codeSlug);
  if (!code) {
    return new Response("Code not found", { status: 404 });
  }

  const { filters, sort } = parseCircuitParams(url);

  const circuits = hasActiveFilters(filters)
    ? filterCircuitsForCode(code.id, filters, sort)
    : getCircuitsForCode(code.id, sort);

  if (circuits.length === 0) {
    return new Response("No circuits found", { status: 404 });
  }

  const circuitIds = circuits.map((c) => c.id);
  const bodiesMap = getBodiesForCircuits(circuitIds);

  // Collect stim entries
  const entries: { name: string; body: string }[] = [];
  for (const circuit of circuits) {
    const bodies = bodiesMap.get(circuit.id) ?? [];
    const stim = bodies.find((b) => b.format === "stim");
    if (!stim) continue;

    const filename = buildStimFilename({
      codeSlug,
      circuitSlug: circuit.slug,
      gateCount: circuit.gate_count,
      twoQubitGateCount: circuit.two_qubit_gate_count,
      depth: circuit.depth,
      qubitCount: circuit.qubit_count,
    });
    entries.push({ name: filename, body: stim.body });
  }

  if (entries.length === 0) {
    return new Response("No stim bodies found", { status: 404 });
  }

  // Single circuit: return plain .stim file
  if (entries.length === 1) {
    return new Response(entries[0].body, {
      headers: {
        "Content-Type": "text/plain",
        "Content-Disposition": `attachment; filename="${entries[0].name}"`,
      },
    });
  }

  // Multiple circuits: return zip
  const zipBuffer = createZip(
    entries.map((e) => ({ name: e.name, data: Buffer.from(e.body, "utf8") })),
  );

  return new Response(zipBuffer, {
    headers: {
      "Content-Type": "application/zip",
      "Content-Disposition": `attachment; filename="${codeSlug}_circuits.stim.zip"`,
    },
  });
};
