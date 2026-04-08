import type { APIRoute } from "astro";
import { getAllCodes } from "../lib/queries";

export const prerender = false;

const STATIC_PATHS = ["/", "/about", "/contribute", "/tools"];

export const GET: APIRoute = ({ site }) => {
  const codes = getAllCodes();
  const base = site!.origin;

  const urls = [
    ...STATIC_PATHS.map((path) => `  <url><loc>${base}${path}</loc></url>`),
    ...codes.map((c) => `  <url><loc>${base}/codes/${c.slug}</loc></url>`),
  ];

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.join("\n")}
</urlset>
`;

  return new Response(body, {
    headers: { "Content-Type": "application/xml; charset=utf-8" },
  });
};
