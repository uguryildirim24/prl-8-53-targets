#!/usr/bin/env python3
"""Validate exp-003 scope, preparation, run matrix and preserved outputs."""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib

import gemmi
from rdkit import Chem

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
EXPECTED_RUNS = {("paroxetine_neutral", 2301), ("paroxetine_neutral", 2302),
                 ("paroxetine_neutral", 2303), ("paroxetine_protonated", 2401),
                 ("paroxetine_protonated", 2402), ("paroxetine_protonated", 2403)}


def sha256(path):
    h = hashlib.sha256(path.read_bytes()); return h.hexdigest()


def pdbqt_charge(path):
    charges = []
    for line in path.read_text().splitlines():
        if line.startswith(("ATOM", "HETATM")):
            charges.append(float(line.split()[-2]))
    return len(charges), sum(charges)


def residue_atom_map(path):
    structure = gemmi.read_structure(str(path)); result = {}
    for chain in structure[0]:
        for residue in chain:
            if residue.het_flag != "A":
                continue
            for atom in residue:
                if atom.element.name == "H":
                    continue
                result[(chain.name, residue.seqid.num, atom.name.strip())] = (
                    atom.element.name, atom.pos.x, atom.pos.y, atom.pos.z)
    return result


def main():
    source_manifest = json.loads((ROOT / "inputs/source_manifest.json").read_text())
    source_checks = []
    for item in source_manifest["files"]:
        path = REPO / item["path"]
        source_checks.append({"path": item["path"], "actual_sha256": sha256(path),
                              "expected_sha256": item["sha256"],
                              "ok": sha256(path) == item["sha256"]})

    graph = json.loads((ROOT / "derived/ligand_graph_and_conformers.json").read_text())
    graph_ok = (graph["graph_check"]["heavy_atoms"] == 24 and
                graph["graph_check"]["heavy_heavy_bonds"] == 27 and
                graph["graph_check"]["configured_atoms"] == {"CAW": "S", "CAX": "R"} and
                graph["graph_check"]["stereochemistry_preserving_name_maps"] > 0)
    state_expected = {"paroxetine_neutral": 0, "paroxetine_protonated": 1}
    charge_rows = []
    for state, charge in state_expected.items():
        count, observed = pdbqt_charge(ROOT / f"derived/pdbqt/{state}.pdbqt")
        charge_rows.append({"state": state, "expected_formal_charge": charge,
                            "pdbqt_atoms_including_polar_H": count,
                            "pdbqt_gasteiger_charge_sum": round(observed, 4),
                            "within_rounding_0.01": abs(observed - charge) < 0.01})
    with (ROOT / "tables/ligand_charge_check.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(charge_rows[0])); writer.writeheader(); writer.writerows(charge_rows)

    original = residue_atom_map(ROOT / "derived/receptor_6vrh_chainA_resolved_protein.pdb")
    prepared = residue_atom_map(ROOT / "derived/receptor_6vrh_primary_prepared.pdb")
    removed = sorted(set(original) - set(prepared))
    unexpected = sorted(set(prepared) - set(original))
    removed_residues = sorted({(x[0], x[1]) for x in removed})
    coordinate_deltas = []
    for key in sorted(set(original) & set(prepared)):
        a = original[key]; b = prepared[key]
        if a[0] != b[0]:
            raise RuntimeError(f"element changed at {key}")
        coordinate_deltas.append(max(abs(a[i] - b[i]) for i in range(1, 4)))
    histidine_h = {}
    structure = gemmi.read_structure(str(ROOT / "derived/receptor_6vrh_primary_prepared.pdb"))
    for residue in structure[0]["A"]:
        if residue.name == "HIS":
            histidine_h[str(residue.seqid.num)] = sorted(a.name.strip() for a in residue if a.element.name == "H")
    receptor_ok = (removed_residues == [("A", 145), ("A", 201)] and not unexpected and
                   max(coordinate_deltas, default=0) <= 0.001 and
                   all("HE2" in names and "HD1" not in names for names in histidine_h.values()))

    monitors = {}
    for path in sorted((ROOT / "logs/docking").glob("*/*.monitor.json")):
        record = json.loads(path.read_text()); key = (record["state"], record["seed"])
        monitors[key] = record
    monitor_ok = set(monitors) == EXPECTED_RUNS
    for record in monitors.values():
        monitor_ok &= (record["returncode"] == 0 and record["stop_reason"] is None and
                       record["observed_process_tree_nice_values"] == [19] and
                       record["sampled_peak_process_tree_rss_bytes"] < record["rss_stop_bytes"] and
                       record["environment_controls"] == {"OMP_NUM_THREADS": "2", "OPENBLAS_NUM_THREADS": "1",
                           "MKL_NUM_THREADS": "1", "VECLIB_MAXIMUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1"} and
                       "--cpu" in record["command"] and record["command"][record["command"].index("--cpu") + 1] == "2")

    output_rows = []
    for state, seed in sorted(EXPECTED_RUNS):
        pdbqt = ROOT / f"poses/{state}/seed-{seed}.pdbqt"
        sdf = ROOT / f"poses/{state}/seed-{seed}.sdf"
        mols = list(Chem.SDMolSupplier(str(sdf), removeHs=False))
        output_rows.append({"state": state, "seed": seed,
                            "pdbqt_models": pdbqt.read_text().count("MODEL "),
                            "sdf_molecules": len(mols), "all_sdf_molecules_read": all(m is not None for m in mols)})
    extra_pose_files = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "poses").glob("**/*")
                              if p.is_file() and not any(p.name == f"seed-{seed}.{ext}"
                              for _, seed in EXPECTED_RUNS for ext in ("pdbqt", "sdf")))
    pose_ok = all(r["pdbqt_models"] == r["sdf_molecules"] == 20 and r["all_sdf_molecules_read"]
                  for r in output_rows) and not extra_pose_files

    rows = list(csv.DictReader((ROOT / "tables/all_poses.csv").open()))
    run_rows = list(csv.DictReader((ROOT / "tables/runs.csv").open()))
    analysis_ok = (len(rows) == 120 and len(run_rows) == 6 and
                   {(r["state"], int(r["seed"])) for r in run_rows} == EXPECTED_RUNS and
                   all(int(r["graph_automorphisms_considered"]) > 0 for r in rows))

    validation = {
        "source_hash_checks": source_checks,
        "all_source_hashes_match": all(x["ok"] for x in source_checks),
        "graph_and_stereochemistry_check": graph_ok,
        "ligand_charge_checks": charge_rows,
        "all_ligand_charge_sums_match": all(x["within_rounding_0.01"] for x in charge_rows),
        "receptor_check": {"ok": receptor_ok, "prepared_heavy_atoms": len(prepared),
                           "removed_residues": removed_residues, "removed_heavy_atoms": len(removed),
                           "unexpected_heavy_atoms": len(unexpected),
                           "maximum_retained_heavy_atom_coordinate_delta_A": max(coordinate_deltas, default=0),
                           "histidine_hydrogen_names": histidine_h},
        "run_matrix_and_resource_check": monitor_ok,
        "run_count": len(monitors), "output_checks": output_rows,
        "all_pose_outputs_complete": pose_ok, "extra_pose_files": extra_pose_files,
        "analysis_check": analysis_ok, "all_pose_rows": len(rows),
        "scope_check": "six native-paroxetine searches only; no PRL/background/other-target pose paths or prediction-service inputs",
        "passed": all([all(x["ok"] for x in source_checks), graph_ok,
                       all(x["within_rounding_0.01"] for x in charge_rows), receptor_ok,
                       monitor_ok, pose_ok, analysis_ok]),
    }
    (ROOT / "derived/validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"passed": validation["passed"], "run_count": len(monitors),
                      "pose_rows": len(rows)}, sort_keys=True))
    if not validation["passed"]:
        raise SystemExit("validation failed")


if __name__ == "__main__":
    main()
