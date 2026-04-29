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
fi

# Discover a circuit qec_id by probing /api/circuits?ids=1..10
ids_payload=$(curl -fsS "$BASE/api/circuits?ids=1,2,3,4,5,6,7,8,9,10" 2>/dev/null || echo "[]")
qec_id=$(jq -r ".[0].qec_id // empty" <<< "$ids_payload" 2>/dev/null || echo "")
if [ -z "$qec_id" ]; then
  echo "FAIL: no circuits found via /api/circuits in id range 1-10"; fail=1
else
  check "/circuits/$qec_id"        "<title"
  check "/api/circuits?ids=$qec_id" "qec_id"
fi

# Search query path
check "/api/search?q=code" "{"

exit $fail
