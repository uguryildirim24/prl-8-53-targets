#!/bin/sh
# Convert only the four fixed PRL conformers; never regenerate the reviewed receptor.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
: "${EXP004_RUNTIME:?set EXP004_RUNTIME to the verified exact-version project-local runtime}"
LIGAND="$EXP004_RUNTIME/.venv/bin/mk_prepare_ligand.py"
[ -x "$LIGAND" ]
mkdir -p "$ROOT/derived/pdbqt" "$ROOT/logs/ligand-preparation"
for ligand in prl_neutral_c1 prl_neutral_c2 prl_protonated_c1 prl_protonated_c2; do
  "$LIGAND" \
    -i "$ROOT/derived/$ligand.sdf" \
    -o "$ROOT/derived/pdbqt/$ligand.pdbqt" \
    --charge_model gasteiger --add_index_map \
    > "$ROOT/logs/ligand-preparation/$ligand.stdout.txt" \
    2> "$ROOT/logs/ligand-preparation/$ligand.stderr.txt"
done
