import type { APIRoute } from "astro";

export const prerender = false;

export const GET: APIRoute = ({ site }) => {
  const sitemapUrl = new URL("/sitemap.xml", site).href;
  const body = `User-agent: *
Allow: /

Sitemap: ${sitemapUrl}
`;
  return new Response(body, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
};
