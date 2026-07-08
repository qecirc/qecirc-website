export const prerender = false;

import type { APIRoute } from "astro";
import { getDb } from "../../../../lib/db";

interface Row {
  n: number;
  k: number;
  original_h: string | null;
  original_logical: string | null;
}

export const GET: APIRoute = ({ params }) => {
  const qecIdParam = params.qec_id;
  const qecId = Number(qecIdParam);
  if (!Number.isInteger(qecId) || qecId < 1) {
    return new Response("Invalid qec_id", { status: 400 });
  }

  const db = getDb();
  const row = db
    .prepare(
      `SELECT co.n AS n, co.k AS k, o.original_h, o.original_logical
       FROM circuit_originals o
       JOIN circuits c ON c.id = o.circuit_id
       JOIN codes co ON co.id = c.code_id
       WHERE c.qec_id = ?`,
    )
    .get(qecId) as Row | undefined;

  if (!row || !row.original_h || !row.original_logical) {
    return new Response("Not found", { status: 404 });
  }

  return new Response(
    JSON.stringify({
      n: row.n,
      k: row.k,
      h: JSON.parse(row.original_h),
      logical: JSON.parse(row.original_logical),
    }),
    {
      headers: {
        "Content-Type": "application/json",
        // Edge holds for a week — every deploy purges (src/lib/cache-purge.ts).
        "Cache-Control": "public, max-age=3600, s-maxage=604800",
      },
    },
  );
};
