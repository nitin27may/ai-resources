#!/usr/bin/env bash
# Every URL in the baseline (the live sitemap when the restructure began) must still be
# served after a build: either present in site/sitemap.xml, or as a redirect stub on disk.
# Usage: planning/scripts/sitemap-guard.sh [site-dir]   (run after `mkdocs build --strict`)
set -euo pipefail
SITE="${1:-site}"; BASE="planning/sitemap-baseline.txt"; PREFIX="https://nitinksingh.com/ai-resources/"
[ -f "$SITE/sitemap.xml" ] || { echo "::error::$SITE/sitemap.xml missing"; exit 1; }
missing=0
while read -r url; do
  [ -z "$url" ] && continue
  if grep -q "<loc>$url</loc>" "$SITE/sitemap.xml"; then continue; fi
  path="${url#$PREFIX}"
  if [ -f "$SITE/${path}index.html" ] && grep -qi 'http-equiv="refresh"\|window.location' "$SITE/${path}index.html"; then continue; fi
  echo "::error::baseline URL no longer served and has no redirect: $url"; missing=$((missing+1))
done < "$BASE"
[ "$missing" -eq 0 ] && echo "sitemap guard: all $(grep -c . "$BASE") baseline URLs still served"
exit $missing
