export const prerender = false;

import type { APIRoute } from "astro";
import {
  searchCodes,
  searchTools,
  searchCircuits,
  formatCodeParams,
} from "../../lib/queries";

export const GET: APIRoute = ({ url }) => {
  const q = url.searchParams.get("q")?.trim() ?? "";

  if (q.length < 2) {
    return new Response(JSON.stringify([]), {
      headers: { "Content-Type": "application/json" },
    });
  }

  const codes = searchCodes(q).map((c) => ({
    type: "code" as const,
    name: c.name,
    slug: c.slug,
    params: formatCodeParams(c),
    tags: c.tags,
    href: `/codes/${c.slug}`,
  }));

  const circuits = searchCircuits(q).map((ci) => ({
    type: "circuit" as const,
    name: ci.name,
    slug: ci.slug,
    params: [
      ci.qubit_count != null ? `${ci.qubit_count}q` : null,
      ci.depth != null ? `${ci.depth}d` : null,
    ]
      .filter(Boolean)
      .join(", "),
    tags: ci.tags,
    href: `/codes/${ci.code_slug}#${ci.slug}`,
    subtitle: ci.code_name,
  }));

  const tools = searchTools(q).map((t) => ({
    type: "tool" as const,
    name: t.name,
    slug: t.slug,
    params: "",
    tags: t.tags,
    href: `/tools`,
  }));

  return new Response(JSON.stringify([...codes, ...circuits, ...tools]), {
    headers: { "Content-Type": "application/json" },
  });
};
