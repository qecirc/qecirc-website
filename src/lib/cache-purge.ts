// Purges the Cloudflare edge cache once per server boot (= once per deploy,
// since every deploy starts a fresh process). This is what makes the 7-day
// `s-maxage` in src/middleware.ts safe: rendered output only changes at
// deploy time (the SQLite DB is built from YAML during `npm run build`), so
// long edge TTL + purge-on-deploy gives warm caches with ~zero staleness.
//
// Operator setup (values live as Railway service variables, never in the repo):
//   CLOUDFLARE_ZONE_ID    — zone Overview page, right sidebar
//   CLOUDFLARE_API_TOKEN  — custom API token with the single permission
//                           "Zone → Cache Purge → Purge", scoped to this zone
// Optional:
//   CLOUDFLARE_PURGE_DELAY_SECONDS — default 60; the delay lets the purge land
//     after the host has switched traffic to the new container, so a request
//     racing the cutover can't re-cache a page from the old one.
//   CLOUDFLARE_API_BASE — default https://api.cloudflare.com; override to
//     point at a mock when testing.
//
// Without the two required vars (local dev, CI, forks) this is a logged no-op.

const DEFAULT_DELAY_SECONDS = 60;

async function purgeEverything(zoneId: string, token: string, apiBase: string): Promise<void> {
  const url = `${apiBase}/client/v4/zones/${zoneId}/purge_cache`;
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ purge_everything: true }),
    });
    if (res.ok) {
      console.log("[cache-purge] Cloudflare cache purged.");
    } else {
      const body = await res.text().catch(() => "");
      console.error(`[cache-purge] purge failed: HTTP ${res.status} ${body.slice(0, 300)}`);
    }
  } catch (err) {
    console.error("[cache-purge] purge failed:", err);
  }
}

/** Schedule a one-shot purge-everything shortly after boot. Never throws. */
export function schedulePurgeOnBoot(): void {
  const zoneId = process.env.CLOUDFLARE_ZONE_ID;
  const token = process.env.CLOUDFLARE_API_TOKEN;
  if (!zoneId || !token) {
    console.log("[cache-purge] CLOUDFLARE_ZONE_ID/CLOUDFLARE_API_TOKEN not set — purge skipped.");
    return;
  }
  const apiBase = process.env.CLOUDFLARE_API_BASE || "https://api.cloudflare.com";
  const delaySeconds =
    Number(process.env.CLOUDFLARE_PURGE_DELAY_SECONDS) >= 0
      ? Number(process.env.CLOUDFLARE_PURGE_DELAY_SECONDS)
      : DEFAULT_DELAY_SECONDS;
  console.log(`[cache-purge] purge scheduled in ${delaySeconds}s.`);
  const timer = setTimeout(() => void purgeEverything(zoneId, token, apiBase), delaySeconds * 1000);
  // Don't keep the process alive just for the purge (e.g. fast shutdowns).
  timer.unref?.();
}
