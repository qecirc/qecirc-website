import { defineMiddleware } from "astro:middleware";
import { schedulePurgeOnBoot } from "./lib/cache-purge";

// Once per server process (= once per deploy): schedule the Cloudflare
// purge that makes the long s-maxage below safe. See src/lib/cache-purge.ts.
schedulePurgeOnBoot();

export const onRequest = defineMiddleware(async (context, next) => {
  const response = await next();
  const { pathname } = context.url;

  if (pathname.startsWith("/_")) return response;
  if (response.headers.has("Cache-Control")) return response;

  // Rendered output is immutable between deploys (the DB is baked at build
  // time), so the edge may hold pages for a week; every deploy purges the
  // Cloudflare cache on boot. Browsers always revalidate (max-age=0) since
  // a purge can't reach them.
  response.headers.set(
    "Cache-Control",
    "public, max-age=0, s-maxage=604800, stale-while-revalidate=86400",
  );

  return response;
});
