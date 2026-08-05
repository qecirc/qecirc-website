export const prerender = false;

import type { APIRoute } from "astro";
import {
  searchCodes,
  searchTools,
  searchCircuits,
  correctTokens,
  tokenizeQuery,
  formatCodeParams,
  showCodeParams,
  formatCircuitId,
  MIN_QUERY_LENGTH,
} from "../../lib/queries";

// Same reasoning as /search (src/pages/search.astro): this route varies by an
// unbounded, attacker-fillable `?q=`, so it must not inherit the week-long
// s-maxage that middleware.ts stamps on responses without their own value.
const CACHE_CONTROL = "public, max-age=0, s-maxage=600";

export const GET: APIRoute = ({ url }) => {
  const raw = url.searchParams.get("q")?.trim() ?? "";

  if (raw.length < MIN_QUERY_LENGTH) {
    return new Response(JSON.stringify([]), {
      headers: { "Content-Type": "application/json", "Cache-Control": CACHE_CONTROL },
    });
  }

  // Fix typos before matching, so this dropdown and /search agree about what
  // exists — "staene" finding nothing here while /search returns 71 hits reads
  // as a bug. Only the spelling is shared, not the engine: the LIKE matching
  // below is substring-based, which /search's token-based FTS is not, and that
  // is what lets a half-typed "ycle" reach the Bicycle codes. Correction is
  // silent; the correction notice belongs on /search, which has room for it.
  const { tokens, changed } = correctTokens(tokenizeQuery(raw));
  const q = changed ? tokens.join(" ") : raw;

  const codes = searchCodes(q).map((c) => {
    return {
      type: "code" as const,
      name: c.name,
      slug: c.slug,
      // The dropdown renders name and params as adjacent spans, so a name that
      // already carries them ("Gottesman [[8,3,3]] Code") must send none.
      params: showCodeParams(c) ? formatCodeParams(c) : "",
      tags: c.tags,
      href: `/codes/${c.slug}`,
    };
  });

  const circuits = searchCircuits(q).map((ci) => ({
    type: "circuit" as const,
    name: ci.name,
    slug: ci.slug,
    qec_id: formatCircuitId(ci.qec_id),
    params: [
      ci.qubit_count != null ? `${ci.qubit_count}q` : null,
      ci.depth != null ? `${ci.depth}d` : null,
    ]
      .filter(Boolean)
      .join(", "),
    tags: ci.tags,
    href: `/circuits/${ci.qec_id}`,
    subtitle: ci.code_name,
  }));

  const tools = searchTools(q).map((t) => ({
    type: "tool" as const,
    name: t.name,
    slug: t.slug,
    params: "",
    tags: t.tags,
    href: `/tools#${t.slug}`,
  }));

  return new Response(JSON.stringify([...codes, ...circuits, ...tools]), {
    headers: { "Content-Type": "application/json", "Cache-Control": CACHE_CONTROL },
  });
};
