export const prerender = false;

import type { APIRoute } from "astro";
import { getCircuitsByQecIds } from "../../lib/queries";
import { MAX_CIRCUIT_IDS_PER_REQUEST } from "../../lib/constants";

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

  // Bound the query the ids become. Truncating is a last resort, not the
  // normal case (see MAX_CIRCUIT_IDS_PER_REQUEST), and when it happens the
  // response says so instead of quietly returning a prefix.
  const capped = qecIds.slice(0, MAX_CIRCUIT_IDS_PER_REQUEST);
  const truncated = capped.length < qecIds.length;
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

  // Headers, not a wrapper object: the body stays a plain array, so nothing
  // that already reads this endpoint has to change to learn about truncation.
  return Response.json(result, {
    headers: {
      "X-Truncated": truncated ? "true" : "false",
      "X-Requested-Ids": String(qecIds.length),
      "X-Id-Limit": String(MAX_CIRCUIT_IDS_PER_REQUEST),
    },
  });
};
