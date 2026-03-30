import { defineMiddleware } from "astro:middleware";
import { timingSafeEqual } from "node:crypto";

const SITE_PASSWORD = import.meta.env.SITE_PASSWORD || "";

function safeEqual(a: string, b: string): boolean {
  const bufA = Buffer.from(a);
  const bufB = Buffer.from(b);
  if (bufA.length !== bufB.length) return false;
  return timingSafeEqual(bufA, bufB);
}

const UNAUTHORIZED = new Response("Unauthorized", {
  status: 401,
  headers: { "WWW-Authenticate": 'Basic realm="QECirc"' },
});

export const onRequest = defineMiddleware((context, next) => {
  if (!SITE_PASSWORD) return next();

  const auth = context.request.headers.get("authorization");
  if (auth) {
    const [scheme, encoded] = auth.split(" ");
    if (scheme?.toLowerCase() === "basic" && encoded) {
      let decoded: string;
      try {
        decoded = atob(encoded);
      } catch {
        return UNAUTHORIZED;
      }
      const colonIndex = decoded.indexOf(":");
      const password = decoded.substring(colonIndex + 1);
      if (safeEqual(password, SITE_PASSWORD)) return next();
    }
  }

  return UNAUTHORIZED;
});
