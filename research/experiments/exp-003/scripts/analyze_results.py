#!/usr/bin/env python3
"""Measure every saved paroxetine pose in the unchanged 6VRH protein frame."""
from __future__ import annotations

import csv
import glob
import json
import math
import pathlib
import re

import gemmi
from rdkit import Chem, rdBase

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
RAW_CIF = REPO / "research/alternative-coordinate-evidence/raw/6VRH.cif"
STATES = {"paroxetine_neutral": [2301, 2302, 2303],
          "paroxetine_protonated": [2401, 2402, 2403]}
CUTOFF = 4.0


def coords(mol):
    conf = mol.GetConformer()
    return [(conf.GetAtomPosition(i).x, conf.GetAtomPosition(i).y, conf.GetAtomPosition(i).z)
            for i in range(mol.GetNumAtoms())]


def direct_rmsd(reference, pose, mapping):
    r = reference.GetConformer(); p = pose.GetConformer()
    total = 0.0
    for ref_idx, pose_idx in enumerate(mapping):
        a = r.GetAtomPosition(ref_idx); b = p.GetAtomPosition(pose_idx)
        total += (a.x-b.x)**2 + (a.y-b.y)**2 + (a.z-b.z)**2
    return math.sqrt(total / len(mapping))


def protein_atoms():
    structure = gemmi.read_structure(str(RAW_CIF))
    records = []
    for residue in structure[0]["A"]:
        if residue.het_flag != "A":
            continue
        for atom in residue:
            if atom.element.name != "H":
                records.append((f"A:{residue.name}{residue.seqid.num}",
                                (atom.pos.x, atom.pos.y, atom.pos.z)))
    return records


def contacts(ligand_coords, receptor_atoms, cutoff=CUTOFF):
    cutoff2 = cutoff * cutoff; found = set()
    for residue, xyz in receptor_atoms:
        for lig in ligand_coords:
            if sum((xyz[i] - lig[i])**2 for i in range(3)) <= cutoff2:
                found.add(residue); break
    return found


def load_reference(state):
    source = next(m for m in Chem.SDMolSupplier(str(ROOT / f"derived/{state}.sdf"), removeHs=False) if m)
    ref = Chem.RemoveHs(source)
    reference_json = json.loads((ROOT / "derived/native_reference.json").read_text())
    if ref.GetNumAtoms() != 24 or len(reference_json["atoms"]) != 24:
        raise RuntimeError("reference heavy-atom count mismatch")
    conf = ref.GetConformer()
    seen = set()
    for atom in reference_json["atoms"]:
        idx = atom["molecule_atom_index"]
        if ref.GetAtomWithIdx(idx).GetSymbol() != atom["element"]:
            raise RuntimeError(f"reference element mapping mismatch at {idx}")
        conf.SetAtomPosition(idx, atom["coord_A"]); seen.add(idx)
    if seen != set(range(ref.GetNumAtoms())):
        raise RuntimeError("reference map does not cover every heavy atom")
    Chem.AssignStereochemistry(ref, cleanIt=True, force=True)
    return ref


def score_from_pose(mol):
    if not mol.HasProp("meeko"):
        raise RuntimeError("exported pose lacks Meeko score metadata")
    return json.loads(mol.GetProp("meeko"))["free_energy"]


def main():
    receptor = protein_atoms()
    rows = []; run_rows = []
    for state, seeds in STATES.items():
        reference = load_reference(state)
        expected_charge = Chem.GetFormalCharge(reference)
        ref_contacts = contacts(coords(reference), receptor)
        for seed in seeds:
            sdf = ROOT / f"poses/{state}/seed-{seed}.sdf"
            pdbqt = ROOT / f"poses/{state}/seed-{seed}.pdbqt"
            monitor_path = ROOT / f"logs/docking/{state}/seed-{seed}.monitor.json"
            if not (sdf.is_file() and pdbqt.is_file() and monitor_path.is_file()):
                raise RuntimeError(f"missing preserved output for {state}/{seed}")
            monitor = json.loads(monitor_path.read_text())
            if monitor["returncode"] != 0 or monitor["stop_reason"] is not None:
                raise RuntimeError(f"stopped/failed output for {state}/{seed}")
            molecules = list(Chem.SDMolSupplier(str(sdf), removeHs=False))
            if not molecules or any(m is None for m in molecules):
                raise RuntimeError(f"unreadable mode in {sdf}")
            pdbqt_models = pdbqt.read_text().count("MODEL ")
            if pdbqt_models != len(molecules):
                raise RuntimeError(f"PDBQT/SDF mode mismatch for {state}/{seed}")
            current = []
            for rank, pose_h in enumerate(molecules, start=1):
                pose = Chem.RemoveHs(pose_h)
                Chem.AssignStereochemistry(pose, cleanIt=True, force=True)
                if Chem.GetFormalCharge(pose) != expected_charge:
                    raise RuntimeError(f"formal charge changed for {state}/{seed}/{rank}")
                mappings = pose.GetSubstructMatches(reference, uniquify=False, useChirality=True,
                                                    maxMatches=10000)
                mappings = [m for m in mappings if len(m) == pose.GetNumAtoms() == reference.GetNumAtoms()]
                if not mappings:
                    raise RuntimeError(f"no complete stereo-preserving graph map for {state}/{seed}/{rank}")
                rmsd = min(direct_rmsd(reference, pose, mapping) for mapping in mappings)
                pose_contacts = contacts(coords(pose), receptor)
                union = ref_contacts | pose_contacts
                row = {
                    "state": state, "formal_charge": expected_charge, "seed": seed, "rank": rank,
                    "vina_score_kcal_per_mol": score_from_pose(pose_h),
                    "site_frame_symmetry_aware_heavy_atom_RMSD_A": round(rmsd, 4),
                    "graph_automorphisms_considered": len(mappings),
                    "reference_contact_count": len(ref_contacts), "pose_contact_count": len(pose_contacts),
                    "contacts_retained": len(ref_contacts & pose_contacts),
                    "contacts_lost": ";".join(sorted(ref_contacts - pose_contacts)),
                    "contacts_gained": ";".join(sorted(pose_contacts - ref_contacts)),
                    "contact_jaccard": round(len(ref_contacts & pose_contacts) / len(union), 4),
                }
                rows.append(row); current.append(row)
            top = current[0]
            closest = min(current, key=lambda r: r["site_frame_symmetry_aware_heavy_atom_RMSD_A"])
            run_rows.append({
                "state": state, "formal_charge": expected_charge, "seed": seed,
                "saved_modes": len(current), "top_score": top["vina_score_kcal_per_mol"],
                "top_pose_RMSD_A": top["site_frame_symmetry_aware_heavy_atom_RMSD_A"],
                "top_contacts_retained": top["contacts_retained"],
                "top_contact_jaccard": top["contact_jaccard"],
                "closest_mode_rank": closest["rank"],
                "closest_mode_RMSD_A": closest["site_frame_symmetry_aware_heavy_atom_RMSD_A"],
                "closest_mode_score": closest["vina_score_kcal_per_mol"],
                "closest_contacts_retained": closest["contacts_retained"],
                "elapsed_seconds": monitor["elapsed_seconds"],
                "sampled_peak_tree_RSS_bytes": monitor["sampled_peak_process_tree_rss_bytes"],
                "observed_nice_values": ";".join(map(str, monitor["observed_process_tree_nice_values"])),
            })
    (ROOT / "tables").mkdir(exist_ok=True)
    with (ROOT / "tables/all_poses.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    with (ROOT / "tables/runs.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(run_rows[0])); writer.writeheader(); writer.writerows(run_rows)
    summary = {
        "method": {"reference": "deposited auth-A 8PR heavy atoms in unchanged 6VRH frame",
                   "alignment": "none; neither protein nor ligand was fitted during evaluation",
                   "mapping": "minimum direct RMSD over complete stereochemistry-preserving heavy-atom graph automorphisms",
                   "contact_cutoff_A": CUTOFF, "contact_cutoff_role": "descriptive inventory, not a success threshold",
                   "rdkit_version": rdBase.rdkitVersion},
        "reference_contacts": sorted(contacts(coords(load_reference("paroxetine_neutral")), receptor)),
        "run_summaries": run_rows,
        "no_threshold": "No numerical pass/fail or biological threshold was declared or inferred.",
    }
    (ROOT / "derived/results_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"searches": len(run_rows), "saved_modes": len(rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
