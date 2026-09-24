#!/usr/bin/env python3
"""Analyze every PRL mode and all within-state pose pairs without coordinate fitting."""
from __future__ import annotations
import csv
import itertools
import json
import math
import pathlib
import statistics

import gemmi
import numpy as np
from rdkit import Chem, rdBase

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
LIGANDS = ["prl_neutral_c1", "prl_neutral_c2", "prl_protonated_c1", "prl_protonated_c2"]
SEEDS = [5301, 5302, 5303]
CUTOFF = 4.0


def coords(mol):
    c = mol.GetConformer(); return [np.array(c.GetAtomPosition(i), dtype=float) for i in range(mol.GetNumAtoms())]

def direct_rmsd(a, b, mapping):
    ca, cb = a.GetConformer(), b.GetConformer(); total = 0.0
    for ai, bi in enumerate(mapping):
        x, y = ca.GetAtomPosition(ai), cb.GetAtomPosition(bi)
        total += (x.x-y.x)**2 + (x.y-y.y)**2 + (x.z-y.z)**2
    return math.sqrt(total / len(mapping))

def mappings(a, b):
    hits = b.GetSubstructMatches(a, uniquify=False, useChirality=False, maxMatches=10000)
    return [m for m in hits if len(m) == a.GetNumAtoms() == b.GetNumAtoms()]

def receptor_atoms():
    path = REPO / "research/experiments/exp-003/derived/receptor_6vrh_primary_prepared.pdb"
    structure = gemmi.read_structure(str(path)); out = []
    for chain in structure[0]:
        for residue in chain:
            if residue.het_flag != "A": continue
            for atom in residue:
                if atom.element.name == "H": continue
                out.append((f"{chain.name}:{residue.name}{residue.seqid.num}", np.array([atom.pos.x, atom.pos.y, atom.pos.z])))
    return out

def contacts_and_minimum(ligand_xyz, receptor):
    found = set(); minimum = float("inf")
    for residue, xyz in receptor:
        distances = [float(np.linalg.norm(xyz-lig)) for lig in ligand_xyz]
        d = min(distances); minimum = min(minimum, d)
        if d <= CUTOFF: found.add(residue)
    return found, minimum

def score(mol): return json.loads(mol.GetProp("meeko"))["free_energy"]

def classify_n(mol_h):
    n = [a for a in mol_h.GetAtoms() if a.GetSymbol() == "N"][0]; found = {"nitrogen": n.GetIdx()}
    for atom in n.GetNeighbors():
        if atom.GetSymbol() == "H": found["hydrogen"] = atom.GetIdx(); continue
        h_count = sum(x.GetSymbol() == "H" for x in atom.GetNeighbors())
        if h_count == 3: found["methyl"] = atom.GetIdx(); continue
        other = [x for x in atom.GetNeighbors() if x.GetIdx() != n.GetIdx() and x.GetSymbol() != "H"]
        found["benzyl" if other[0].GetIsAromatic() else "phenethyl"] = atom.GetIdx()
    return found

def nitrogen_geometry(mol_h):
    idx = classify_n(mol_h); xyz = coords(mol_h); n = xyz[idx["nitrogen"]]
    vectors = [xyz[idx[x]]-n for x in ("methyl", "benzyl", "phenethyl")]
    determinant = float(np.linalg.det(np.stack(vectors)))
    out = {"determinant": determinant, "sign": 1 if determinant > 0 else -1}
    if "hydrogen" in idx:
        h = xyz[idx["hydrogen"]]
        out["tetrahedral_determinant_H_origin"] = float(np.linalg.det(np.stack([xyz[idx[x]]-h for x in ("methyl", "benzyl", "phenethyl")])))
    return out

def raw_models(path):
    models = []; current = []
    for line in path.read_text().splitlines():
        if line.startswith("MODEL "): current = []
        elif line.startswith(("ATOM", "HETATM")):
            element = line[12:16].strip()[0]
            current.append((element, np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])))
        elif line.startswith("ENDMDL"):
            models.append(current); current = []
    return models

def raw_export_heavy_delta(raw, exported):
    heavy = [(a.GetSymbol(), xyz) for a, xyz in zip(exported.GetAtoms(), coords(exported)) if a.GetSymbol() != "H"]
    raw_heavy = [(e, xyz) for e, xyz in raw if e != "H"]; used = set(); maximum = 0.0
    if len(heavy) != len(raw_heavy): raise RuntimeError("raw/export heavy count mismatch")
    for element, xyz in heavy:
        candidates = [(float(np.linalg.norm(xyz-rxyz)), j) for j, (re, rxyz) in enumerate(raw_heavy) if re == element and j not in used]
        if not candidates: raise RuntimeError("raw/export element mismatch")
        delta, j = min(candidates); used.add(j); maximum = max(maximum, delta)
    return maximum

def stats(values):
    return {"count": len(values), "minimum_A": min(values), "median_A": statistics.median(values), "maximum_A": max(values)}

def main():
    receptor = receptor_atoms()
    native_contacts = set(json.loads((REPO / "research/experiments/exp-003/derived/results_summary.json").read_text())["reference_contacts"])
    prep = json.loads((ROOT / "derived/identity_graph_and_conformers.json").read_text())
    prep_by_name = {x["id"]: x for x in prep["conformers"]}
    records = []; all_rows = []; run_rows = []
    for ligand in LIGANDS:
        state = prep_by_name[ligand]["state"]; conformer = ligand.rsplit("_", 1)[-1]
        expected_charge = prep_by_name[ligand]["formal_charge"]; expected_sign = prep_by_name[ligand]["nitrogen_geometry"]["sign"]
        for seed in SEEDS:
            sdf_path = ROOT / f"poses/{ligand}/seed-{seed}.sdf"; pdbqt_path = ROOT / f"poses/{ligand}/seed-{seed}.pdbqt"
            poses_h = list(Chem.SDMolSupplier(str(sdf_path), removeHs=False)); raws = raw_models(pdbqt_path)
            if not poses_h or any(m is None for m in poses_h) or len(poses_h) != len(raws): raise RuntimeError(f"unreadable/mismatched modes: {ligand}/{seed}")
            current = []
            for rank, (pose_h, raw) in enumerate(zip(poses_h, raws), start=1):
                pose = Chem.RemoveHs(pose_h)
                if Chem.GetFormalCharge(pose) != expected_charge: raise RuntimeError("pose formal charge changed")
                reference = Chem.RemoveHs(next(m for m in Chem.SDMolSupplier(str(ROOT / f"derived/{ligand}.sdf"), removeHs=False) if m))
                autos = mappings(reference, pose)
                if not autos: raise RuntimeError("pose heavy graph mismatch")
                n_geom = nitrogen_geometry(pose_h)
                if n_geom["sign"] != expected_sign: raise RuntimeError(f"nitrogen sign changed: {ligand}/{seed}/{rank}")
                raw_delta = raw_export_heavy_delta(raw, pose_h)
                if raw_delta > 0.001: raise RuntimeError(f"raw/export coordinate mismatch: {raw_delta}")
                pose_contacts, minimum = contacts_and_minimum(coords(pose), receptor)
                retained = pose_contacts & native_contacts; union = pose_contacts | native_contacts
                rec = {"id": f"{ligand}:s{seed}:r{rank}", "ligand": ligand, "state": state, "conformer": conformer,
                       "start_n_sign": expected_sign, "formal_charge": expected_charge, "seed": seed, "rank": rank,
                       "vina_score_kcal_per_mol": score(pose_h), "minimum_receptor_heavy_atom_distance_A": round(minimum, 4),
                       "contact_count_4A": len(pose_contacts), "contacts_4A": ";".join(sorted(pose_contacts)),
                       "paroxetine_native_contacts_retained": len(retained),
                       "paroxetine_native_contact_jaccard": round(len(retained)/len(union), 4),
                       "paroxetine_native_contacts_lost": ";".join(sorted(native_contacts-pose_contacts)),
                       "paroxetine_native_contacts_gained": ";".join(sorted(pose_contacts-native_contacts)),
                       "graph_automorphisms": len(autos), "raw_export_max_heavy_coordinate_delta_A": round(raw_delta, 6),
                       "pose_n_determinant_A3": round(n_geom["determinant"], 6), "pose_n_sign": n_geom["sign"]}
                if "tetrahedral_determinant_H_origin" in n_geom:
                    rec["pose_n_tetrahedral_determinant_H_origin_A3"] = round(n_geom["tetrahedral_determinant_H_origin"], 6)
                else: rec["pose_n_tetrahedral_determinant_H_origin_A3"] = ""
                all_rows.append(rec); current.append(rec); records.append((rec, pose))
            run_rows.append({"ligand": ligand, "state": state, "conformer": conformer, "start_n_sign": expected_sign,
                             "seed": seed, "saved_modes": len(current), "top_score": current[0]["vina_score_kcal_per_mol"],
                             "top_minimum_receptor_distance_A": current[0]["minimum_receptor_heavy_atom_distance_A"],
                             "top_contacts_4A": current[0]["contacts_4A"],
                             "top_paroxetine_native_contacts_retained": current[0]["paroxetine_native_contacts_retained"]})
    pair_rows = []
    for (ra, a), (rb, b) in itertools.combinations(records, 2):
        if ra["state"] != rb["state"]: continue
        autos = mappings(a, b)
        if not autos: raise RuntimeError("pair graph mismatch")
        rmsd = min(direct_rmsd(a, b, m) for m in autos)
        pair_rows.append({"state": ra["state"], "pose1": ra["id"], "pose2": rb["id"],
                          "same_starting_conformer": ra["ligand"] == rb["ligand"], "same_docking_seed": ra["seed"] == rb["seed"],
                          "same_run": ra["ligand"] == rb["ligand"] and ra["seed"] == rb["seed"],
                          "same_start_n_sign": ra["start_n_sign"] == rb["start_n_sign"],
                          "graph_automorphisms": len(autos), "site_frame_symmetry_aware_heavy_atom_RMSD_A": round(rmsd, 4)})
    categories = {}
    for state in ("neutral", "protonated"):
        state_pairs = [r for r in pair_rows if r["state"] == state]
        selectors = {
            "within_same_run_all_modes": lambda r: r["same_run"],
            "across_seeds_same_starting_conformer_all_modes": lambda r: r["same_starting_conformer"] and not r["same_docking_seed"],
            "across_starting_conformers_all_modes": lambda r: not r["same_starting_conformer"],
        }
        categories[state] = {name: stats([float(r["site_frame_symmetry_aware_heavy_atom_RMSD_A"]) for r in state_pairs if f(r)]) for name, f in selectors.items()}
        top_ids = {r["id"] for r in all_rows if r["state"] == state and r["rank"] == 1}
        top_same = [float(r["site_frame_symmetry_aware_heavy_atom_RMSD_A"]) for r in state_pairs if r["pose1"] in top_ids and r["pose2"] in top_ids and r["same_starting_conformer"]]
        top_cross = [float(r["site_frame_symmetry_aware_heavy_atom_RMSD_A"]) for r in state_pairs if r["pose1"] in top_ids and r["pose2"] in top_ids and not r["same_starting_conformer"]]
        categories[state]["top_modes_across_seeds_same_starting_conformer"] = stats(top_same)
        categories[state]["top_modes_across_starting_conformers"] = stats(top_cross)
    (ROOT / "tables").mkdir(exist_ok=True)
    for name, rows in [("all_poses.csv", all_rows), ("runs.csv", run_rows), ("pose_pairs.csv", pair_rows)]:
        with (ROOT / "tables" / name).open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    summary = {"method": {"frame": "unchanged reviewed 6VRH protein frame", "coordinate_fitting": "none",
                          "pair_mapping": "minimum direct RMSD over complete heavy-atom graph automorphisms within formal state",
                          "cross_state_pairs": "not pooled", "contact_cutoff_A": CUTOFF,
                          "contact_cutoff_role": "descriptive inventory, not a biological threshold", "rdkit_version": rdBase.rdkitVersion},
               "native_paroxetine_contact_reference": sorted(native_contacts), "run_summaries": run_rows,
               "pairwise_variability": categories, "pose_rows": len(all_rows), "within_state_pair_rows": len(pair_rows),
               "interpretation": "continuous model variability only; no clustering, success or biological threshold"}
    (ROOT / "derived/results_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"searches": len(run_rows), "saved_modes": len(all_rows), "within_state_pairs": len(pair_rows), "variability": categories}, sort_keys=True))

if __name__ == "__main__": main()
