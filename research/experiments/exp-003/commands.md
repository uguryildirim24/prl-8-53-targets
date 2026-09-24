# exp-003 command record

Working directory was the repository root on the local Mac. `EXP003_RUNTIME` points to the already existing project-local exp-002 environment; no package or binary was installed or copied. Every command below used the preserved inputs whose hashes are in `inputs/source_manifest.json`. The recorded path is a local working copy and is not durable: it existed and its Vina binary matched the recorded hash during review, but exp-003 does not contain the virtual environment, binary or a complete dependency lock. Reproduction therefore requires supplying an independently rebuilt exact-version environment after that worktree disappears.

```sh
export EXP003_RUNTIME=<repo>/research/experiments/exp-002
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1

/usr/bin/time -lp nice -n 19 "$EXP003_RUNTIME/.venv/bin/python" \
  research/experiments/exp-003/scripts/prepare_inputs.py \
  > research/experiments/exp-003/logs/prepare_inputs.final.stdout.txt \
  2> research/experiments/exp-003/logs/prepare_inputs.final.stderr.txt

/usr/bin/time -lp nice -n 19 \
  research/experiments/exp-003/scripts/prepare_docking_inputs.sh \
  > research/experiments/exp-003/logs/prepare_docking_inputs.final.stdout.txt \
  2> research/experiments/exp-003/logs/prepare_docking_inputs.final.stderr.txt
```

The earlier receptor preflight used the same second command but the first protocol's `--delete_bad_res_from_box_radius 12` setting. It stopped without writing a search because incomplete Asn145 was 6.280 A outside a box face. Its original `logs/prepare_docking_inputs.stdout.txt` and `.stderr.txt` are retained. The dated pre-run protocol records the measured, pre-search amendment to explicit omission of only Asn145/Lys201.

The frozen six-search matrix is run sequentially by:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  research/experiments/exp-003/scripts/run_all_searches.sh \
  > research/experiments/exp-003/logs/run_all_searches.stdout.txt \
  2> research/experiments/exp-003/logs/run_all_searches.stderr.txt
```

For each fixed state/seed, that script executes `run_vina_one.py` under `nice -n 19`. The wrapper preserves its literal Vina argument array, start/end UTC times, return code, thread-control environment, sampled child-tree RSS/nice observations and stop settings in `logs/docking/<state>/seed-<seed>.monitor.json`. Vina stdout and stderr are separate adjacent files. It then exports every returned PDBQT model to SDF with Meeko `mk_export.py`, preserving export stdout/stderr.

Final analysis and validation commands:

```sh
/usr/bin/time -lp nice -n 19 "$EXP003_RUNTIME/.venv/bin/python" \
  research/experiments/exp-003/scripts/analyze_results.py \
  > research/experiments/exp-003/logs/analyze_results.stdout.txt \
  2> research/experiments/exp-003/logs/analyze_results.stderr.txt

/usr/bin/time -lp nice -n 19 "$EXP003_RUNTIME/.venv/bin/python" \
  research/experiments/exp-003/scripts/validate_outputs.py \
  > research/experiments/exp-003/logs/validate_outputs.stdout.txt \
  2> research/experiments/exp-003/logs/validate_outputs.stderr.txt

nice -n 19 "$EXP003_RUNTIME/.venv/bin/python" \
  research/experiments/exp-003/scripts/build_manifest.py
(cd research/experiments/exp-003 && nice -n 19 shasum -a 256 -c SHA256SUMS)
```

The preserved `logs/checksums.stdout.txt` and `.stderr.txt` came from an earlier attempt that redirected verification output into a file already covered by `SHA256SUMS`; it necessarily reports that changing file as failed. They remain unchanged as failed-attempt evidence. The command above succeeds when its output is not written into a covered file.

The `/usr/bin/time -lp` records are per-process observations, not aggregate-project accounting. Search monitor records are sampled observations and controls, not hard memory enforcement.
