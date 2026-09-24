# Commands and resource controls

Working directory: repository root on the local Mac. No helper, container, remote box, package installation, docking program, or SwissTargetPrediction request was used.

Every Python analysis/retrieval command used the standard library only, `nice -n 19`, and one-thread environment variables. The command record included an attempted shell virtual-memory limit of 4,194,304 KiB, shown below, but `runlogs/environment.txt` records the shell limit as `unlimited`; the package therefore does not claim that the 4 GB limit was successfully enforced:

```sh
ulimit -v 4194304
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1

/usr/bin/time -l nice -n 19 python3 \
  research/alternative-coordinate-evidence/scripts/fetch_official.py \
  --out research/alternative-coordinate-evidence \
  > research/alternative-coordinate-evidence/runlogs/fetch.stdout.txt \
  2> research/alternative-coordinate-evidence/runlogs/fetch.time.txt

/usr/bin/time -l nice -n 19 python3 \
  research/alternative-coordinate-evidence/scripts/analyze_coordinates.py \
  --evidence research/alternative-coordinate-evidence \
  > research/alternative-coordinate-evidence/runlogs/analyze.stdout.txt \
  2> research/alternative-coordinate-evidence/runlogs/analyze.time.txt

/usr/bin/time -l nice -n 19 python3 \
  research/alternative-coordinate-evidence/scripts/validate_evidence.py \
  --evidence research/alternative-coordinate-evidence \
  > research/alternative-coordinate-evidence/runlogs/validate.stdout.txt \
  2> research/alternative-coordinate-evidence/runlogs/validate.time.txt

nice -n 19 python3 \
  research/alternative-coordinate-evidence/scripts/build_manifest.py \
  --evidence research/alternative-coordinate-evidence

(cd research/alternative-coordinate-evidence && \
  nice -n 19 shasum -a 256 -c SHA256SUMS)
```

`/usr/bin/time -l` measured maximum resident-set sizes of 53,936,128 bytes for retrieval, 93,798,400 bytes for the final analysis run, and 25,411,584 bytes for validation. These are per-process observations from these runs, not a measured aggregate project peak. The one-thread environment variables are controls, not measured performance, and the low observed RSS does not retroactively prove a 4 GB enforced limit. The full time outputs and environment capture are in `runlogs/`.
