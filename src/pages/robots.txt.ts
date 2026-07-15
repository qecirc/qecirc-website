import type { APIRoute } from "astro";

export const prerender = false;

export const GET: APIRoute = ({ site }) => {
  const sitemapUrl = new URL("/sitemap.xml", site).href;
  // /search is disallowed for every agent: free-text queries crossed with tag
  // and code filters are an unbounded crawl space, and every distinct URL is a
  // separate edge-cache entry. The content behind it is all reachable via
  // /codes and the sitemap anyway.
  const body = `User-agent: *
Content-Signal: search=yes,ai-train=no
Allow: /
Disallow: /search

User-agent: Amazonbot
Disallow: /

User-agent: Amzn-SearchBot
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: CloudflareBrowserRenderingCrawler
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: GPTBot
Disallow: /

User-agent: meta-externalagent
Disallow: /

Sitemap: ${sitemapUrl}
`;
  return new Response(body, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
};
