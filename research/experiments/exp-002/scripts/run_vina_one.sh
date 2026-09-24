#!/bin/sh
# Usage: run_vina_one.sh ligand_id seed
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
LIGAND=$1
SEED=$2
OUTDIR="$ROOT/poses/$LIGAND"
LOGDIR="$ROOT/logs/docking/$LIGAND"
mkdir -p "$OUTDIR" "$LOGDIR"
exec "$ROOT/.local-tools/vina_1.2.7_mac_aarch64" \
  --receptor "$ROOT/derived/receptor_3tdc_assembly2.pdbqt" \
  --ligand "$ROOT/derived/pdbqt/$LIGAND.pdbqt" \
  --center_x 36.237 --center_y 63.819 --center_z 50.773 \
  --size_x 18.552 --size_y 22.095 --size_z 23.399 \
  --cpu 4 --seed "$SEED" --exhaustiveness 8 --num_modes 20 --energy_range 5 \
  --out "$OUTDIR/seed-${SEED}.pdbqt" \
  > "$LOGDIR/seed-${SEED}.log" 2>&1
