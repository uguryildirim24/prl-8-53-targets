#!/bin/sh
# Prepare the one predeclared rigid receptor and both fixed ligand conformers.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
: "${EXP003_RUNTIME:?set EXP003_RUNTIME to the exact-version project-local exp-002 runtime}"
PY="$EXP003_RUNTIME/.venv/bin/python"
RECEPTOR="$EXP003_RUNTIME/.venv/bin/mk_prepare_receptor.py"
LIGAND="$EXP003_RUNTIME/.venv/bin/mk_prepare_ligand.py"
[ -x "$PY" ] && [ -x "$RECEPTOR" ] && [ -x "$LIGAND" ]
mkdir -p "$ROOT/derived/pdbqt" "$ROOT/logs/ligand-preparation"

"$RECEPTOR" \
  --read_pdb "$ROOT/derived/receptor_6vrh_chainA_resolved_protein.pdb" \
  -o "$ROOT/derived/receptor_6vrh_primary" \
  -p "$ROOT/derived/receptor_6vrh_primary.pdbqt" \
  --write_pdb "$ROOT/derived/receptor_6vrh_primary_prepared.pdb" \
  --default_altloc A \
  --set_template "A:143,223,235,240,456=HIE" \
  --delete_residues "A:145,201" \
  --compute_charges --charge_model gasteiger \
  --box_center 135.153 124.0665 121.356 \
  --box_size 16.752 19.255 21.052 \
  -v "$ROOT/derived/vina_box.txt"

for state in paroxetine_neutral paroxetine_protonated; do
  "$LIGAND" \
    -i "$ROOT/derived/$state.sdf" \
    -o "$ROOT/derived/pdbqt/$state.pdbqt" \
    --charge_model gasteiger --add_index_map \
    > "$ROOT/logs/ligand-preparation/$state.stdout.txt" \
    2> "$ROOT/logs/ligand-preparation/$state.stderr.txt"
done
