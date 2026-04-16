export const prerender = false;

import type { APIRoute } from "astro";
import { getCircuitsByQecIds } from "../../lib/queries";

export const GET: APIRoute = ({ url }) => {
  const idsParam = url.searchParams.get("ids");
  if (!idsParam) {
    return new Response("Missing 'ids' parameter", { status: 400 });
  }

  const qecIds = [
    ...new Set(
      idsParam
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => Number.isInteger(n) && n > 0),
    ),
  ];

  if (qecIds.length === 0) {
    return Response.json([]);
  }

  // Cap at 200 to prevent abuse
  const capped = qecIds.slice(0, 200);
  const circuits = getCircuitsByQecIds(capped);

  const result = circuits.map((c) => ({
    qec_id: c.qec_id,
    name: c.name,
    slug: c.slug,
    code_name: c.code_name,
    code_slug: c.code_slug,
    gate_count: c.gate_count,
    two_qubit_gate_count: c.two_qubit_gate_count,
    depth: c.depth,
    qubit_count: c.qubit_count,
    tags: c.tags,
  }));

  return Response.json(result);
};
