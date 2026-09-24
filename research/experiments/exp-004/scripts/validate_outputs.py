#!/usr/bin/env python3
"""Validate frozen inputs, exact run matrix, resources and all exp-004 outputs."""
from __future__ import annotations
import csv
import datetime as dt
import hashlib
import json
import pathlib

from rdkit import Chem

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
LIGANDS = ["prl_neutral_c1", "prl_neutral_c2", "prl_protonated_c1", "prl_protonated_c2"]
SEEDS = [5301, 5302, 5303]
EXPECTED = {(l, s) for l in LIGANDS for s in SEEDS}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def parse_time(text): return dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
def raw_scores(path):
    return [float(line.split()[3]) for line in path.read_text().splitlines() if line.startswith("REMARK VINA RESULT:")]

def main():
    inventory = json.loads((ROOT / "inputs/presearch_inventory.json").read_text())
    frozen = []
    for item in inventory["prepared_inputs"]:
        path = ROOT / item["path"]; frozen.append({"path": item["path"], "expected": item["sha256"], "actual": sha(path), "ok": sha(path) == item["sha256"]})
    external = []
    for item in inventory["reused_exp003_inputs"]:
        path = REPO / item["path"]; external.append({"path": item["path"], "expected": item["sha256"], "actual": sha(path), "ok": sha(path) == item["sha256"]})
    monitors = {}
    for path in sorted((ROOT / "logs/docking").glob("*/*.monitor.json")):
        x = json.loads(path.read_text()); monitors[(x["ligand"], x["seed"])] = x
    matrix_ok = set(monitors) == EXPECTED
    expected_controls = {"OMP_NUM_THREADS": "2", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "VECLIB_MAXIMUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1"}
    settings_ok = True; completions_ok = True; all_nice = set(); intervals = []
    for key, x in monitors.items():
        cmd = x["command"]; all_nice.update(x["observed_process_tree_nice_values"])
        settings_ok &= (x["environment_controls"] == expected_controls and
                        cmd[cmd.index("--cpu")+1] == "2" and cmd[cmd.index("--exhaustiveness")+1] == "8" and
                        cmd[cmd.index("--num_modes")+1] == "20" and cmd[cmd.index("--energy_range")+1] == "5" and
                        cmd[cmd.index("--center_x")+1:cmd.index("--center_x")+6:2] == ["135.153", "124.0665", "121.356"] and
                        cmd[cmd.index("--size_x")+1:cmd.index("--size_x")+6:2] == ["16.752", "19.255", "21.052"] and
                        cmd[cmd.index("--seed")+1] == str(key[1]) and
                        cmd[cmd.index("--ligand")+1].endswith(f"derived/pdbqt/{key[0]}.pdbqt") and
                        cmd[cmd.index("--receptor")+1].endswith("research/experiments/exp-003/derived/receptor_6vrh_primary.pdbqt"))
        completions_ok &= (x["returncode"] == 0 and x["stop_reason"] is None and
                           x["sampled_peak_process_tree_rss_bytes"] < x["rss_stop_bytes"] and
                           x["time_stop_seconds"] == 1200 and x["poll_seconds"] == 0.1)
        intervals.append((parse_time(x["started_utc"]), parse_time(x["completed_utc"]), key))
    intervals.sort(); serial = all(intervals[i][0] >= intervals[i-1][1] for i in range(1, len(intervals)))
    outputs = []; score_lookup = {}
    for ligand, seed in sorted(EXPECTED):
        pdbqt = ROOT / f"poses/{ligand}/seed-{seed}.pdbqt"; sdf = ROOT / f"poses/{ligand}/seed-{seed}.sdf"
        mols = list(Chem.SDMolSupplier(str(sdf), removeHs=False)); scores = raw_scores(pdbqt)
        outputs.append({"ligand": ligand, "seed": seed, "pdbqt_models": pdbqt.read_text().count("MODEL "),
                        "raw_scores": len(scores), "sdf_molecules": len(mols), "all_sdf_read": all(m is not None for m in mols)})
        for rank, value in enumerate(scores, 1): score_lookup[(ligand, seed, rank)] = value
    output_ok = all(x["pdbqt_models"] == x["raw_scores"] == x["sdf_molecules"] == 20 and x["all_sdf_read"] for x in outputs)
    pose_rows = list(csv.DictReader((ROOT / "tables/all_poses.csv").open())); run_rows = list(csv.DictReader((ROOT / "tables/runs.csv").open()))
    pair_rows = list(csv.DictReader((ROOT / "tables/pose_pairs.csv").open()))
    table_matrix = {(r["ligand"], int(r["seed"])) for r in run_rows}
    scores_ok = all(abs(float(r["vina_score_kcal_per_mol"])-score_lookup[(r["ligand"], int(r["seed"]), int(r["rank"]))]) < 1e-9 for r in pose_rows)
    pose_checks = (len(pose_rows) == 240 and len(run_rows) == 12 and table_matrix == EXPECTED and len(pair_rows) == 14280 and
                   all(int(r["graph_automorphisms"]) > 0 for r in pose_rows) and
                   all(float(r["raw_export_max_heavy_coordinate_delta_A"]) <= 0.001 for r in pose_rows) and
                   all(int(r["pose_n_sign"]) == int(r["start_n_sign"]) for r in pose_rows) and
                   all(int(r["graph_automorphisms"]) > 0 for r in pair_rows) and scores_ok)
    unexpected = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "poses").glob("**/*") if p.is_file() and
                        not any(p.name == f"seed-{seed}.{ext}" for seed in SEEDS for ext in ("pdbqt", "sdf")))
    effective_nice_exact_19 = all_nice == {19}
    integrity_passed = all([all(x["ok"] for x in frozen), all(x["ok"] for x in external), matrix_ok, settings_ok,
                            completions_ok, serial, output_ok, pose_checks, not unexpected])
    validation = {
        "frozen_presearch_inputs": frozen, "frozen_inputs_unchanged": all(x["ok"] for x in frozen),
        "reused_exp003_inputs": external, "reused_inputs_unchanged": all(x["ok"] for x in external),
        "run_matrix_exact": matrix_ok, "settings_exact": settings_ok, "successful_unstopped_runs": completions_ok,
        "runs_strictly_serial_by_recorded_intervals": serial, "observed_process_tree_nice_values": sorted(all_nice),
        "effective_nice_exactly_19": effective_nice_exact_19,
        "nice_deviation": "The outer sequential driver was also invoked with nice -n 19, so the wrapper's nested nice -n 19 saturated at effective nice 20. This is lower scheduling priority than specified, not extra resource use; no run was retried.",
        "output_checks": outputs, "all_outputs_complete": output_ok, "unexpected_pose_files": unexpected,
        "analysis_checks": pose_checks, "raw_scores_match_table": scores_ok, "pose_rows": len(pose_rows),
        "within_state_pair_rows": len(pair_rows), "data_and_resource_integrity_passed": integrity_passed,
        "protocol_deviations": [] if effective_nice_exact_19 else ["effective child nice was 20 rather than 19 because nice was nested"],
        "limits_note": "Vina cpu=2 and sampled per-child-tree stops were configured and observed; shell memory was unlimited and no hard/aggregate enforcement is claimed."
    }
    (ROOT / "derived/validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"data_and_resource_integrity_passed": integrity_passed, "effective_nice_exactly_19": effective_nice_exact_19,
                      "observed_nice": sorted(all_nice), "runs": len(monitors), "poses": len(pose_rows), "pairs": len(pair_rows)}, sort_keys=True))
    if not integrity_passed: raise SystemExit("data/resource integrity validation failed")

if __name__ == "__main__": main()
