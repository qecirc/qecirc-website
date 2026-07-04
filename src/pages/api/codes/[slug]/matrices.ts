export const prerender = false;

import type { APIRoute } from "astro";
import { getDb } from "../../../../lib/db";

interface Row {
  n: number;
  k: number;
  h: string | null;
  logical: string | null;
}

export const GET: APIRoute = ({ params }) => {
  const slug = params.slug;
  if (!slug) return new Response("Missing slug", { status: 400 });

  const db = getDb();
  const row = db.prepare("SELECT n, k, h, logical FROM codes WHERE slug = ?").get(slug) as
    Row | undefined;

  if (!row || !row.h || !row.logical) {
    return new Response("Not found", { status: 404 });
  }

  return new Response(
    JSON.stringify({
      n: row.n,
      k: row.k,
      h: JSON.parse(row.h),
      logical: JSON.parse(row.logical),
    }),
    {
      headers: {
        "Content-Type": "application/json",
        // The page passes ?v=<canonical_hash> as a cache key; when matrices
        // change between deploys the hash changes and the browser refetches.
        "Cache-Control": "public, max-age=3600",
      },
    },
  );
};
