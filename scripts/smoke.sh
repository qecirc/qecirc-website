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

# Assert an exact status code, and (optionally) a substring in the body.
# Unlike check(), this omits -f so non-2xx responses stay inspectable.
# Body and status come from one request, with the status appended on its own
# line. Never pipe curl into `grep -q`: grep exits at the first match, and the
# resulting SIGPIPE trips `set -o pipefail` intermittently on large bodies.
check_status() {
  local path="$1" expected_status="$2" expected_body="${3:-}"
  local out status body
  if ! out=$(curl -sS -w $'\n%{http_code}' "$BASE$path" 2>&1); then
    echo "FAIL $path: curl error"; fail=1; return
  fi
  status="${out##*$'\n'}"
  body="${out%$'\n'*}"
  if [ "$status" != "$expected_status" ]; then
    echo "FAIL $path: expected HTTP $expected_status, got $status"; fail=1; return
  fi
  if [ -n "$expected_body" ] && ! grep -q "$expected_body" <<< "$body"; then
    echo "FAIL $path: HTTP $status but body missing: $expected_body"; fail=1; return
  fi
  echo "OK   $path ($status)"
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

# Unknown ids/slugs must 404 (not 500) and still serve the styled 404 page.
# The SSR pages return a bodiless 404 and rely on Astro substituting the
# prerendered /404 page (see src/lib/not-found.ts); a regression there shows up
# either as a 500 or as a 404 with an empty body.
check_status "/circuits/99999"  404 "Page Not Found"   # unknown qec_id
check_status "/circuits/abc"    404 "Page Not Found"   # non-numeric qec_id
check_status "/circuits/0"      404 "Page Not Found"   # out-of-range qec_id
check_status "/codes/nope"      404 "Page Not Found"   # unknown code slug
check_status "/not-a-page"      404 "Page Not Found"   # unmatched route (adapter)

# API routes serve their own 404 body and must not be swallowed by the above.
check_status "/api/circuits/99999/bodies" 404 "Not found"

exit $fail
