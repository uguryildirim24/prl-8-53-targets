#!/usr/bin/env python3
"""Run one fixed exp-004 Vina search with sampled child-tree stop controls."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import signal
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
ALLOWED = {name: {5301, 5302, 5303} for name in
           ["prl_neutral_c1", "prl_neutral_c2", "prl_protonated_c1", "prl_protonated_c2"]}
RSS_STOP_BYTES = 3 * 1024**3
TIME_STOP_SECONDS = 20 * 60
POLL_SECONDS = 0.1

def utc_now(): return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
def sha256(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def snapshot(root_pid):
    result = subprocess.run(["ps", "-axo", "pid=,ppid=,rss=,ni=,comm="], capture_output=True, text=True, check=True)
    rows = []
    for line in result.stdout.splitlines():
        fields = line.strip().split(None, 4)
        if len(fields) != 5: continue
        try: rows.append({"pid": int(fields[0]), "ppid": int(fields[1]), "rss_kib": int(fields[2]),
                          "nice": int(fields[3]), "command": fields[4]})
        except ValueError: continue
    wanted = {root_pid}; changed = True
    while changed:
        changed = False
        for row in rows:
            if row["ppid"] in wanted and row["pid"] not in wanted:
                wanted.add(row["pid"]); changed = True
    return [r for r in rows if r["pid"] in wanted]

def main():
    parser = argparse.ArgumentParser(); parser.add_argument("ligand", choices=sorted(ALLOWED)); parser.add_argument("seed", type=int)
    args = parser.parse_args()
    if args.seed not in ALLOWED[args.ligand]: raise SystemExit("ligand/seed pair is not predeclared")
    runtime = pathlib.Path(os.environ.get("EXP004_RUNTIME", "")); vina = runtime / ".local-tools/vina_1.2.7_mac_aarch64"
    if not vina.is_file() or sha256(vina) != "823c2bbacf26d72183861322345f0a89736aca66c8e81054c66f93af5ad623f1":
        raise SystemExit("exact Vina 1.2.7 binary not found")
    receptor = REPO / "research/experiments/exp-003/derived/receptor_6vrh_primary.pdbqt"
    if sha256(receptor) != "01ec06e6bfb7708c389bcfc884c929547114b4a9318f8a1f6861c43ab793a5cc":
        raise SystemExit("reviewed exp-003 receptor hash mismatch")
    pose_dir = ROOT / "poses" / args.ligand; log_dir = ROOT / "logs/docking" / args.ligand
    pose_dir.mkdir(parents=True, exist_ok=True); log_dir.mkdir(parents=True, exist_ok=True)
    out = pose_dir / f"seed-{args.seed}.pdbqt"; monitor_file = log_dir / f"seed-{args.seed}.monitor.json"
    if out.exists() or monitor_file.exists(): raise SystemExit("refusing to overwrite an existing run")
    stdout_path = log_dir / f"seed-{args.seed}.stdout.txt"; stderr_path = log_dir / f"seed-{args.seed}.stderr.txt"
    command = [str(vina), "--receptor", str(receptor), "--ligand", str(ROOT / f"derived/pdbqt/{args.ligand}.pdbqt"),
               "--center_x", "135.153", "--center_y", "124.0665", "--center_z", "121.356",
               "--size_x", "16.752", "--size_y", "19.255", "--size_z", "21.052",
               "--cpu", "2", "--seed", str(args.seed), "--exhaustiveness", "8", "--num_modes", "20",
               "--energy_range", "5", "--out", str(out)]
    env = os.environ.copy(); env.update({"OMP_NUM_THREADS": "2", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
                                         "VECLIB_MAXIMUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1"})
    started_utc = utc_now(); start = time.monotonic(); samples = []; stop_reason = None; peak_rss = 0; observed_nice = set()
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        proc = subprocess.Popen(command, stdout=stdout, stderr=stderr, env=env, start_new_session=True)
        while proc.poll() is None:
            elapsed = time.monotonic() - start
            try: tree = snapshot(proc.pid)
            except Exception as exc:
                stop_reason = f"resource_monitor_failed:{type(exc).__name__}:{exc}"; os.killpg(proc.pid, signal.SIGTERM); break
            rss = sum(r["rss_kib"] * 1024 for r in tree); peak_rss = max(peak_rss, rss)
            observed_nice.update(r["nice"] for r in tree)
            samples.append({"elapsed_seconds": round(elapsed, 3), "aggregate_tree_rss_bytes": rss, "processes": tree})
            if rss >= RSS_STOP_BYTES:
                stop_reason = "sampled_process_tree_rss_reached_3_GiB"; os.killpg(proc.pid, signal.SIGTERM); break
            if elapsed >= TIME_STOP_SECONDS:
                stop_reason = "elapsed_time_reached_1200_seconds"; os.killpg(proc.pid, signal.SIGTERM); break
            time.sleep(POLL_SECONDS)
        try: returncode = proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL); returncode = proc.wait(); stop_reason = (stop_reason or "termination_timeout") + ";SIGKILL"
    record = {"ligand": args.ligand, "state": "protonated" if "protonated" in args.ligand else "neutral",
              "conformer": args.ligand.rsplit("_", 1)[-1], "seed": args.seed, "command": command,
              "environment_controls": {k: env[k] for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]},
              "started_utc": started_utc, "completed_utc": utc_now(), "elapsed_seconds": round(time.monotonic()-start, 3),
              "returncode": returncode, "stop_reason": stop_reason, "rss_stop_bytes": RSS_STOP_BYTES,
              "time_stop_seconds": TIME_STOP_SECONDS, "poll_seconds": POLL_SECONDS,
              "sampled_peak_process_tree_rss_bytes": peak_rss, "observed_process_tree_nice_values": sorted(observed_nice),
              "samples": samples,
              "limits_note": "RSS is sampled for this child tree only; not a hard kernel limit or aggregate-project measurement.",
              "stdout": str(stdout_path.relative_to(ROOT)), "stderr": str(stderr_path.relative_to(ROOT)), "output": str(out.relative_to(ROOT))}
    monitor_file.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: record[k] for k in ["ligand", "seed", "returncode", "stop_reason", "elapsed_seconds", "sampled_peak_process_tree_rss_bytes", "observed_process_tree_nice_values"]}, sort_keys=True))
    if returncode != 0 or stop_reason is not None: raise SystemExit(f"Vina failed/stopped: {returncode}, {stop_reason}")

if __name__ == "__main__": main()
