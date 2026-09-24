#!/bin/sh
# Run the frozen six-search matrix serially, then export every mode to SDF.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
: "${EXP003_RUNTIME:?set EXP003_RUNTIME to the exact-version project-local exp-002 runtime}"
PY="$EXP003_RUNTIME/.venv/bin/python"
EXPORT="$EXP003_RUNTIME/.venv/bin/mk_export.py"

for item in \
  paroxetine_neutral:2301 paroxetine_neutral:2302 paroxetine_neutral:2303 \
  paroxetine_protonated:2401 paroxetine_protonated:2402 paroxetine_protonated:2403
do
  state=${item%:*}; seed=${item#*:}
  env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
    nice -n 19 "$PY" "$ROOT/scripts/run_vina_one.py" "$state" "$seed"
  env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
    nice -n 19 "$EXPORT" "$ROOT/poses/$state/seed-$seed.pdbqt" \
      -s "$ROOT/poses/$state/seed-$seed.sdf" \
      > "$ROOT/logs/docking/$state/seed-$seed-export.stdout.txt" \
      2> "$ROOT/logs/docking/$state/seed-$seed-export.stderr.txt"
done
