#!/bin/sh
# Prepare the inspected PISA dimer as a rigid Vina receptor.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
exec "$ROOT/.venv/bin/mk_prepare_receptor.py" \
  --read_pdb "$ROOT/derived/receptor_assembly2_protein_only.pdb" \
  -o "$ROOT/derived/receptor_3tdc_assembly2" \
  -p "$ROOT/derived/receptor_3tdc_assembly2.pdbqt" \
  --write_pdb "$ROOT/derived/receptor_3tdc_assembly2_prepared.pdb" \
  --default_altloc A \
  --box_center 36.237 63.819 50.773 \
  --box_size 18.552 22.095 23.399 \
  -v "$ROOT/derived/vina_box.txt"
