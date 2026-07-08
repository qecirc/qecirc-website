export const prerender = false;

import type { APIRoute } from "astro";
import { getBodiesForCircuitByQecId } from "../../../../lib/queries";

export const GET: APIRoute = ({ params }) => {
  const qecId = Number(params.qec_id);
  if (!Number.isInteger(qecId) || qecId < 1) {
    return new Response("Invalid qec_id", { status: 400 });
  }

  const bodies = getBodiesForCircuitByQecId(qecId);
  if (bodies.length === 0) {
    return new Response("Not found", { status: 404 });
  }

  return new Response(JSON.stringify({ bodies }), {
    headers: {
      "Content-Type": "application/json",
      // qec_ids are permanent and never reused; body edits between deploys
      // tolerate <=1h of browser-cache staleness (matches originals.ts).
      "Cache-Control": "public, max-age=3600",
    },
  });
};
