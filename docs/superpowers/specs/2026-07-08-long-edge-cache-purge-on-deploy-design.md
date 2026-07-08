# Long edge-cache TTL + Cloudflare purge on deploy — design

**Date:** 2026-07-08
**Status:** Approved (option C of the caching discussion)

## Rationale

The SQLite DB is built from YAML at build time; the running server never
mutates it, so rendered output is immutable **between deploys**. Cloudflare
caches per data center and traffic is sparse, so the current 10-minute
`s-maxage` yields mostly cache misses. A long TTL plus an automatic
purge-everything on each deploy gives warm edge caches worldwide with ~zero
staleness.

## Design

### 1. Middleware TTL (`src/middleware.ts`)

Both branches (pages and `/api/`) become the same header, so they collapse
into one:

```
Cache-Control: public, max-age=0, s-maxage=604800, stale-while-revalidate=86400
```

- `s-maxage=604800` (7 days) — edge lifetime; correctness is guaranteed by
  the purge-on-deploy, not by expiry.
- `max-age=0` — browsers always revalidate (a purge can't reach browsers).
- Existing skips unchanged: `/_` paths and responses that set their own
  `Cache-Control`.

### 2. Per-endpoint headers (`bodies.ts`, `originals.ts`, `matrices.ts`)

`public, max-age=3600` → `public, max-age=3600, s-maxage=604800`.
Browser behavior unchanged (1 h); edge lifetime extended to match the pages.

### 3. Purge module (`src/lib/cache-purge.ts`), scheduled from middleware

- `schedulePurgeOnBoot()` called at module top-level of `src/middleware.ts`,
  i.e. once per server process start (each deploy starts a fresh process).
- No-op unless both `CLOUDFLARE_ZONE_ID` and `CLOUDFLARE_API_TOKEN` env vars
  are set (absent in local dev and CI).
- Waits `CLOUDFLARE_PURGE_DELAY_SECONDS` (default 60) before purging, so the
  purge lands **after** Railway has switched traffic to the new container —
  otherwise a request racing the cutover could re-cache a page from the old
  container for 7 days.
- `POST {CLOUDFLARE_API_BASE|https://api.cloudflare.com}/client/v4/zones/{zone}/purge_cache`
  with `{"purge_everything": true}`. `CLOUDFLARE_API_BASE` is overridable
  for testing against a local mock.
- Logs success/failure; never throws — a failed purge must not affect
  serving. Multiple replicas/restarts each purge; harmless.

### 4. Token management (operator setup, documented in module comment)

- Cloudflare dashboard → My Profile → API Tokens → Create custom token with
  the single permission **Zone → Cache Purge → Purge**, scoped to the
  qecirc.com zone only. Worst case if leaked: someone can empty the cache
  (nuisance, no data access).
- Zone ID from the zone's Overview page sidebar.
- Both values set as Railway service variables; never committed.

## Non-goals

- No purge CLI / npm script (the Cloudflare dashboard purge button covers
  manual needs).
- No per-URL selective purge (purge-everything is fine at this scale;
  hashed static assets repopulate on first request).

## Testing & verification

- Dev server without env vars → single "purge skipped" log line, no request.
- Dev server with env vars + `CLOUDFLARE_API_BASE` pointing at a local mock
  and delay=1 → mock receives the POST with the right path/body/auth header.
- Failure path: mock returns 500 → logged, server unaffected.
- `lint`, `format:check`, `build`, `scripts/smoke.sh`.
- Post-deploy (after operator sets the token): Railway logs show the purge
  line; `cf-cache-status` flips to `MISS` right after a deploy, `HIT` on
  repeat requests.

## Rollout

- Branch `feat/cloudflare-purge-on-deploy` off `main`; PR; patch bump
  0.4.8 → 0.4.9.
- The feature activates only when the operator adds the two Railway env
  vars — merging without them changes edge TTL only after the operator has
  the purge in place? **No** — see risk below.

## Risk & ordering

The TTL bump and the purge ship in the same PR, but the purge only works
once the env vars exist. If the PR deploys before the vars are set, pages
could be cached for up to 7 days with no purge to clear them. Mitigation:
the operator sets the Railway variables **before** merging this PR (they
are inert until the code arrives), making activation atomic.
