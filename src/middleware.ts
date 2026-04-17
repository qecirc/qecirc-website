import { defineMiddleware } from "astro:middleware";

export const onRequest = defineMiddleware(async (context, next) => {
  const response = await next();
  const { pathname } = context.url;

  if (pathname.startsWith("/_")) return response;
  if (response.headers.has("Cache-Control")) return response;

  if (pathname.startsWith("/api/")) {
    response.headers.set(
      "Cache-Control",
      "public, max-age=0, s-maxage=3600, stale-while-revalidate=86400",
    );
  } else {
    response.headers.set(
      "Cache-Control",
      "public, max-age=0, s-maxage=600, stale-while-revalidate=3600",
    );
  }

  return response;
});
