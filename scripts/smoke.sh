#!/usr/bin/env bash
# Hit a running qecirc-website server and verify key routes return 200 with
# expected content. Discovers a code slug from the sitemap and a circuit
# qec_id from the API so the test is data-agnostic.
#
# Usage: ./scripts/smoke.sh [base_url]   (default http://localhost:4321)

set -euo pipefail
BASE="${1:-http://localhost:4321}"
fail=0

check() {
  local path="$1" expected="$2"
  local body
  if ! body=$(curl -fsS "$BASE$path" 2>&1); then
    echo "FAIL $path: HTTP error"; fail=1; return
  fi
  if ! grep -q "$expected" <<< "$body"; then
    echo "FAIL $path: expected substring not found: $expected"; fail=1; return
  fi
  echo "OK   $path"
}

# Static / always-present routes
check "/"            "<title"     # codes index renders SSR
check "/about"       "QECirc"     # static prerender sanity
check "/sitemap.xml" "<urlset"    # exercises getAllCodes

# Discover a code slug from the sitemap
slug=$(curl -fsS "$BASE/sitemap.xml" \
       | grep -oE "/codes/[a-z0-9-]+" | head -1 | sed "s|/codes/||")
if [ -z "$slug" ]; then
  echo "FAIL: no code slug found in sitemap"; fail=1
else
  check "/codes/$slug" "<title"
  # Filtering is client-side: the server must ignore filter params and render
  # the same rows for a filtered URL as for the canonical page.
  canonical_rows=$(curl -fsS "$BASE/codes/$slug" | grep -o "circuit-bodies-status" | wc -l | tr -d " ")
  filtered_rows=$(curl -fsS "$BASE/codes/$slug?gate_count=%3E999999" | grep -o "circuit-bodies-status" | wc -l | tr -d " ")
  if [ "$canonical_rows" = "$filtered_rows" ] && [ "$canonical_rows" != "0" ]; then
    echo "OK   /codes/$slug (server ignores filter params, $canonical_rows rows)"
  else
    echo "FAIL /codes/$slug: filtered rows ($filtered_rows) != canonical ($canonical_rows)"; fail=1
  fi
  check "/?n=%3E9999" "<title"
fi

# Discover a circuit qec_id by probing /api/circuits?ids=1..10
ids_payload=$(curl -fsS "$BASE/api/circuits?ids=1,2,3,4,5,6,7,8,9,10" 2>/dev/null || echo "[]")
qec_id=$(jq -r ".[0].qec_id // empty" <<< "$ids_payload" 2>/dev/null || echo "")
if [ -z "$qec_id" ]; then
  echo "FAIL: no circuits found via /api/circuits in id range 1-10"; fail=1
else
  check "/circuits/$qec_id"        "<title"
  check "/api/circuits?ids=$qec_id" "qec_id"
  check "/api/circuits/$qec_id/bodies" '"format":"stim"'
fi

# Search query path
check "/api/search?q=code" "{"

exit $fail
