#!/bin/sh
# Convert fixed ligand conformers to PDBQT with Meeko's Gasteiger model.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
mkdir -p "$ROOT/derived/pdbqt" "$ROOT/logs/ligand-preparation"
for sdf in "$ROOT"/derived/ligands/*.sdf; do
  name=$(basename "$sdf" .sdf)
  echo "preparing $name"
  "$ROOT/.venv/bin/mk_prepare_ligand.py" \
    -i "$sdf" -o "$ROOT/derived/pdbqt/$name.pdbqt" \
    --charge_model gasteiger --add_index_map \
    > "$ROOT/logs/ligand-preparation/$name.log" 2>&1
done
