export const prerender = false;

import type { APIRoute } from "astro";
import {
  getCodeBySlug,
  getCircuitsWithBodies,
  getCircuitsByQecIds,
  getBodiesForCircuits,
} from "../../lib/queries";
import { parseCircuitParams } from "../../lib/url";
import { buildStimFilename } from "../../lib/filename";
import { createZip } from "../../lib/zip";

export const GET: APIRoute = ({ url }) => {
  const idsParam = url.searchParams.get("ids");

  let circuits: {
    id: number;
    slug: string;
    gate_count: number | null;
    two_qubit_gate_count: number | null;
    depth: number | null;
    qubit_count: number | null;
    code_slug?: string;
  }[];
  let bodiesMap: Map<number, { format: string; body: string }[]>;
  let zipName: string;

  if (idsParam) {
    // Download by qec_ids (favorites)
    const qecIds = [
      ...new Set(
        idsParam
          .split(",")
          .map((s) => Number(s.trim()))
          .filter((n) => Number.isInteger(n) && n > 0),
      ),
    ].slice(0, 200);

    if (qecIds.length === 0) {
      return new Response("No valid ids provided", { status: 400 });
    }

    const rows = getCircuitsByQecIds(qecIds);
    circuits = rows.map((r) => ({ ...r, code_slug: r.code_slug }));
    bodiesMap = getBodiesForCircuits(rows.map((r) => r.id));
    zipName = "qecirc_favorites.stim.zip";
  } else {
    const codeSlug = url.searchParams.get("code");
    if (!codeSlug) {
      return new Response("Missing 'code' or 'ids' parameter", { status: 400 });
    }

    const code = getCodeBySlug(codeSlug);
    if (!code) {
      return new Response("Code not found", { status: 404 });
    }

    const { filters, sort } = parseCircuitParams(url);
    const result = getCircuitsWithBodies(code.id, filters, sort);
    circuits = result.circuits.map((c) => ({ ...c, code_slug: codeSlug }));
    bodiesMap = result.bodiesMap;
    zipName = `${codeSlug}_circuits.stim.zip`;
  }

  if (circuits.length === 0) {
    return new Response("No circuits found", { status: 404 });
  }

  // Collect stim entries
  const entries: { name: string; body: string }[] = [];
  for (const circuit of circuits) {
    const bodies = bodiesMap.get(circuit.id) ?? [];
    const stim = bodies.find((b) => b.format === "stim");
    if (!stim) continue;

    const filename = buildStimFilename({
      codeSlug: circuit.code_slug ?? "unknown",
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
      "Content-Disposition": `attachment; filename="${zipName}"`,
    },
  });
};
