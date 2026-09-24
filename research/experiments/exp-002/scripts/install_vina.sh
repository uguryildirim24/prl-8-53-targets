#!/bin/sh
# Project-local AutoDock Vina install. The binary is intentionally gitignored.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
OUT="$ROOT/.local-tools/vina_1.2.7_mac_aarch64"
URL=https://github.com/ccsb-scripps/AutoDock-Vina/releases/download/v1.2.7/vina_1.2.7_mac_aarch64
mkdir -p "$ROOT/.local-tools"
printf 'started_utc=%s\nurl=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$URL"
curl --fail --location --show-error --silent --user-agent 'prl-8-53-exp-002/1.0' "$URL" --output "$OUT"
chmod 755 "$OUT"
printf 'finished_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
shasum -a 256 "$OUT"
"$OUT" --version
