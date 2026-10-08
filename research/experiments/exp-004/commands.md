# exp-004 command record

This is historical search provenance, not the clean-clone run guide. Use the repository README for saved-pose replay. Empty captures were removed for release. Analysis and validation still overwrite retained tables and summaries. The original inventory builder always labels its output as frozen before search, even when poses already exist. Do not rerun it to repair historical provenance. The retained inventory mismatch is documented in `docs/release-review.md`.

Working directory is the repository root on the authorized local Mac. No network request, package installation, helper, container or other project path is used. The external runtime path is temporary provenance; a future rerun must supply an equivalent exact-version environment if it disappears.

```sh
export EXP004_RUNTIME=<repo>/research/experiments/exp-002
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1

/usr/bin/time -lp nice -n 19 "$EXP004_RUNTIME/.venv/bin/python" \
  research/experiments/exp-004/scripts/prepare_inputs.py \
  > research/experiments/exp-004/logs/prepare_inputs.stdout.txt \
  2> research/experiments/exp-004/logs/prepare_inputs.stderr.txt

/usr/bin/time -lp nice -n 19 \
  research/experiments/exp-004/scripts/prepare_ligands.sh \
  > research/experiments/exp-004/logs/prepare_ligands.stdout.txt \
  2> research/experiments/exp-004/logs/prepare_ligands.stderr.txt

/usr/bin/time -lp nice -n 19 "$EXP004_RUNTIME/.venv/bin/python" \
  research/experiments/exp-004/scripts/validate_presearch.py \
  > research/experiments/exp-004/logs/validate_presearch.stdout.txt \
  2> research/experiments/exp-004/logs/validate_presearch.stderr.txt

nice -n 19 "$EXP004_RUNTIME/.venv/bin/python" \
  research/experiments/exp-004/scripts/build_presearch_inventory.py
```

The original workflow recorded the protocol, prepared-input inventory and all four conformers/PDBQTs before the searches. That chronology statement is not an external timestamp attestation. The retained public inventory contains stale values and does not establish that edited records existed before docking. The fixed 12-run matrix was executed strictly serially:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /usr/bin/time -lp nice -n 19 \
  research/experiments/exp-004/scripts/run_all_searches.sh \
  > research/experiments/exp-004/logs/run_all_searches.stdout.txt \
  2> research/experiments/exp-004/logs/run_all_searches.stderr.txt
```

The driver was itself started with `nice -n 19`, and each per-run wrapper also used `nice -n 19`. The observed effective child nice value therefore saturated at 20 rather than 19. This exact scheduling deviation is preserved in monitor and validation records; no result was retried. Each monitor JSON also preserves the literal Vina command, environment controls, timestamps, sampled process-tree observations and stop settings. Export uses Meeko under the same nested nice/thread controls. Analysis, validation and manifest generation use:

```sh
/usr/bin/time -lp nice -n 19 "$EXP004_RUNTIME/.venv/bin/python" \
  research/experiments/exp-004/scripts/analyze_results.py \
  > research/experiments/exp-004/logs/analyze_results.stdout.txt \
  2> research/experiments/exp-004/logs/analyze_results.stderr.txt

/usr/bin/time -lp nice -n 19 "$EXP004_RUNTIME/.venv/bin/python" \
  research/experiments/exp-004/scripts/validate_outputs.py \
  > research/experiments/exp-004/logs/validate_outputs.stdout.txt \
  2> research/experiments/exp-004/logs/validate_outputs.stderr.txt

nice -n 19 "$EXP004_RUNTIME/.venv/bin/python" \
  research/experiments/exp-004/scripts/build_manifest.py
(cd research/experiments/exp-004 && shasum -a 256 -c SHA256SUMS)
```

`/usr/bin/time -lp` and monitor RSS values are process/sample observations, not hard memory or aggregate-project enforcement. Checksum verification is not redirected into a file covered by the checksum list.
