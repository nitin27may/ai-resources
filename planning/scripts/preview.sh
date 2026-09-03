#!/usr/bin/env bash
# Build the site, serve it locally, and expose it on a temporary public URL via
# a Cloudflare quick tunnel. For showing work in progress before it is deployed.
#
#   planning/scripts/preview.sh          # build, serve, tunnel, print the URL
#   planning/scripts/preview.sh stop     # stop the server and the tunnel
#   planning/scripts/preview.sh url      # print the current URL
#
# The URL is a throwaway trycloudflare.com address: it changes on every start,
# needs no Cloudflare account, and should not be shared as anything permanent.
set -euo pipefail
cd "$(dirname "$0")/../.."

SITE_DIR="${SITE_DIR:-/tmp/ai-resources-preview}"
STATE_DIR="${STATE_DIR:-/tmp/ai-resources-preview-state}"
mkdir -p "$STATE_DIR"
PORT_FILE="$STATE_DIR/port"; URL_FILE="$STATE_DIR/url"
SRV_PID="$STATE_DIR/server.pid"; TUN_PID="$STATE_DIR/tunnel.pid"

stop() {
  for f in "$SRV_PID" "$TUN_PID"; do
    if [ -f "$f" ]; then kill "$(cat "$f")" 2>/dev/null || true; rm -f "$f"; fi
  done
  rm -f "$URL_FILE" "$PORT_FILE"
  echo "preview stopped"
}

case "${1:-start}" in
  stop) stop; exit 0 ;;
  url)  if [ -f "$URL_FILE" ]; then cat "$URL_FILE"; else echo "not running"; exit 1; fi; exit 0 ;;
esac

command -v cloudflared >/dev/null || { echo "cloudflared not found"; exit 1; }
stop >/dev/null 2>&1 || true

echo "building..."
mkdocs build --strict --clean -d "$SITE_DIR" >/dev/null

PORT=8899
while ss -ltn 2>/dev/null | grep -q ":$PORT "; do PORT=$((PORT+1)); done
echo "$PORT" > "$PORT_FILE"

# setsid so both survive the shell that started them.
cd "$SITE_DIR"
setsid nohup python3 -m http.server "$PORT" >"$STATE_DIR/server.log" 2>&1 &
echo $! > "$SRV_PID"
sleep 2

setsid nohup cloudflared tunnel --url "http://localhost:$PORT" --no-autoupdate \
  >"$STATE_DIR/tunnel.log" 2>&1 &
echo $! > "$TUN_PID"

printf 'waiting for the tunnel'
URL=""
for _ in $(seq 1 30); do
  URL=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' "$STATE_DIR/tunnel.log" 2>/dev/null | head -1 || true)
  [ -n "$URL" ] && break
  printf '.'; sleep 2
done
printf '\n'

[ -n "$URL" ] || { echo "tunnel did not report a URL; see $STATE_DIR/tunnel.log"; exit 1; }
echo "$URL" > "$URL_FILE"
code=$(curl -s -o /dev/null -L --max-time 25 -w '%{http_code}' "$URL/")
echo
echo "  local:  http://localhost:$PORT"
echo "  public: $URL   (HTTP $code)"
echo
echo "  stop with: planning/scripts/preview.sh stop"
