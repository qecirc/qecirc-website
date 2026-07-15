/**
 * Signal "not found" from an SSR page (`prerender = false`).
 *
 * The body must stay empty. Astro fills in a *bodiless* 404 with the
 * prerendered /404 page (dist/client/404.html, read from disk by the node
 * adapter's `prerenderedErrorPageFetch`), so the client gets the styled 404
 * page with a 404 status. A 404 response that carries its own body — such as
 * the `Response("Not found")` returned by the /api routes — is passed through
 * untouched, so this helper is only for pages.
 *
 * Do NOT use `Astro.rewrite("/404")` here: /404 is prerendered, so the SSR
 * pipeline has no component instance for that route and the rewrite throws
 * ("Unexpectedly unable to find a component instance for route /404"),
 * turning every unknown id into a 500.
 */
export function notFound(): Response {
  return new Response(null, { status: 404 });
}
