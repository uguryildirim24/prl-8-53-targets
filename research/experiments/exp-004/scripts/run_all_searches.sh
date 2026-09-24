#!/bin/sh
# Run exactly the frozen 12-search matrix serially and export every mode.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
: "${EXP004_RUNTIME:?set EXP004_RUNTIME to the verified exact-version project-local runtime}"
PY="$EXP004_RUNTIME/.venv/bin/python"
EXPORT="$EXP004_RUNTIME/.venv/bin/mk_export.py"
for ligand in prl_neutral_c1 prl_neutral_c2 prl_protonated_c1 prl_protonated_c2; do
  for seed in 5301 5302 5303; do
    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
      nice -n 19 "$PY" "$ROOT/scripts/run_vina_one.py" "$ligand" "$seed"
    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
      nice -n 19 "$EXPORT" "$ROOT/poses/$ligand/seed-$seed.pdbqt" \
        -s "$ROOT/poses/$ligand/seed-$seed.sdf" \
        > "$ROOT/logs/docking/$ligand/seed-$seed-export.stdout.txt" \
        2> "$ROOT/logs/docking/$ligand/seed-$seed-export.stderr.txt"
  done
done
