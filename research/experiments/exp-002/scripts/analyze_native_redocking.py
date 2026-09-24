#!/usr/bin/env python3
"""Measure site-frame native recovery without fitting docked poses to reference."""
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
TABLES = ROOT / "tables"
DERIVED = ROOT / "derived"


def atom_distance_sq(a, b) -> float:
    return (a.x-b.x)**2 + (a.y-b.y)**2 + (a.z-b.z)**2


def protein_contacts(coords, cutoff=4.5):
    structure = gemmi.read_structure(str(ROOT / "inputs/raw/3TDC-assembly2.cif.gz"))
    found = set()
    for chain in structure[0]:
        chain_name = "A" if chain.name == "A" else "B"
        for residue in chain:
            if residue.het_flag != "A":
                continue
            hit = False
            for atom in residue:
                if atom.element.name == "H":
                    continue
                for xyz in coords:
                    dx = atom.pos.x - xyz[0]
                    dy = atom.pos.y - xyz[1]
                    dz = atom.pos.z - xyz[2]
                    if dx*dx + dy*dy + dz*dz <= cutoff*cutoff:
                        hit = True
                        break
                if hit:
                    break
            if hit:
                found.add(f"{chain_name}:{residue.name}{residue.seqid.num}")
    return found


def parse_resources(path):
    text = pathlib.Path(path).read_text()
    def value(pattern, cast=float):
        match = re.search(pattern, text, re.MULTILINE)
        return cast(match.group(1)) if match else None
    return {
        "wall_seconds": value(r"^real ([0-9.]+)$"),
        "user_seconds": value(r"^user ([0-9.]+)$"),
        "sys_seconds": value(r"^sys ([0-9.]+)$"),
        "max_rss_bytes": value(r"^\s*([0-9]+)\s+maximum resident set size$", int),
    }


def main() -> None:
    # CCD atom order (first 36 heavy atoms) matches deposited 0EU atom order.
    reference = next(m for m in Chem.SDMolSupplier(str(ROOT / "inputs/raw/0EU_ideal.sdf"), removeHs=False) if m)
    reference = Chem.RemoveHs(reference)
    ref_conf = reference.GetConformer()
    bound = gemmi.read_structure(str(DERIVED / "native_0EU_bound_reference.pdb"))
    bound_atoms = [a for a in bound[0][0][0] if a.element.name != "H"]
    ccd_block = gemmi.cif.read_file(str(ROOT / "inputs/raw/0EU.cif")).sole_block()
    ccd_table = ccd_block.find(["_chem_comp_atom.atom_id", "_chem_comp_atom.type_symbol", "_chem_comp_atom.pdbx_ordinal"])
    ccd_heavy = sorted((row for row in ccd_table if row[1] != "H"), key=lambda row: int(row[2]))
    ccd_names = [row[0] for row in ccd_heavy]
    bound_names = [atom.name.strip() for atom in bound_atoms]
    if len(bound_atoms) != reference.GetNumAtoms() or ccd_names != bound_names:
        raise RuntimeError("CCD/deposited reference atom-name mapping mismatch")
    if [reference.GetAtomWithIdx(i).GetSymbol() for i in range(reference.GetNumAtoms())] != [row[1] for row in ccd_heavy]:
        raise RuntimeError("CCD/SDF reference element-order mismatch")
    for idx, atom in enumerate(bound_atoms):
        ref_conf.SetAtomPosition(idx, (atom.pos.x, atom.pos.y, atom.pos.z))
    ref_coords = [(a.pos.x, a.pos.y, a.pos.z) for a in bound_atoms]
    reference_contacts = protein_contacts(ref_coords)

    rows = []
    runs = []
    for sdf_path in sorted(glob.glob(str(ROOT / "poses/native_0EU/seed-*.sdf"))):
        seed = int(re.search(r"seed-(\d+)\.sdf$", sdf_path).group(1))
        resources = parse_resources(ROOT / f"logs/docking/native_0EU/seed-{seed}.time.txt")
        run_rows = []
        supplier = Chem.SDMolSupplier(sdf_path, removeHs=False)
        for mode, pose_with_h in enumerate(supplier, start=1):
            if pose_with_h is None:
                raise RuntimeError(f"failed to parse {sdf_path} mode {mode}")
            pose = Chem.RemoveHs(pose_with_h)
            if Chem.GetFormalCharge(pose) != Chem.GetFormalCharge(reference):
                raise RuntimeError("native ligand formal charge changed")
            mappings = pose.GetSubstructMatches(reference, uniquify=False, useChirality=True, maxMatches=10000)
            if not mappings:
                raise RuntimeError("no stereochemistry-preserving graph mapping")
            pose_conf = pose.GetConformer()
            rmsds = []
            for mapping in mappings:
                total = 0.0
                for ref_idx, pose_idx in enumerate(mapping):
                    total += atom_distance_sq(ref_conf.GetAtomPosition(ref_idx), pose_conf.GetAtomPosition(pose_idx))
                rmsds.append(math.sqrt(total / len(mapping)))
            rmsd = min(rmsds)
            coords = [(pose_conf.GetAtomPosition(i).x, pose_conf.GetAtomPosition(i).y, pose_conf.GetAtomPosition(i).z) for i in range(pose.GetNumAtoms())]
            contacts = protein_contacts(coords)
            score_data = json.loads(pose_with_h.GetProp("meeko"))
            row = {
                "seed": seed,
                "mode": mode,
                "vina_score_kcal_per_mol": score_data["free_energy"],
                "site_frame_symmetry_aware_heavy_atom_RMSD_A": round(rmsd, 4),
                "graph_automorphisms_considered": len(mappings),
                "reference_contact_count": len(reference_contacts),
                "pose_contact_count": len(contacts),
                "contacts_retained": len(reference_contacts & contacts),
                "contacts_lost": ";".join(sorted(reference_contacts - contacts)),
                "contacts_gained": ";".join(sorted(contacts - reference_contacts)),
                "contact_jaccard": round(len(reference_contacts & contacts) / len(reference_contacts | contacts), 4),
            }
            rows.append(row)
            run_rows.append(row)
        top = run_rows[0]
        closest = min(run_rows, key=lambda x: x["site_frame_symmetry_aware_heavy_atom_RMSD_A"])
        runs.append({
            "seed": seed,
            "top_score": top["vina_score_kcal_per_mol"],
            "top_pose_RMSD_A": top["site_frame_symmetry_aware_heavy_atom_RMSD_A"],
            "top_pose_contacts_retained": top["contacts_retained"],
            "closest_sampled_mode": closest["mode"],
            "closest_sampled_RMSD_A": closest["site_frame_symmetry_aware_heavy_atom_RMSD_A"],
            "closest_sampled_score": closest["vina_score_kcal_per_mol"],
            **resources,
        })
    with (TABLES / "native_redocking_all_poses.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with (TABLES / "native_redocking_runs.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(runs[0]))
        writer.writeheader()
        writer.writerows(runs)
    summary = {
        "method": {
            "reference": "deposited chain A 0EU heavy-atom coordinates in unchanged 3TDC assembly-2 frame",
            "mapping": "minimum over stereochemistry-preserving heavy-atom graph automorphisms",
            "alignment": "none; docked ligand was not independently fitted or aligned to the reference",
            "atom_mapping_check": "CCD CIF atom IDs/elements ordered by pdbx_ordinal exactly match deposited 0EU atom names and CCD SDF element order for all 36 heavy atoms",
            "contact_cutoff_A": 4.5,
            "rdkit_version": rdBase.rdkitVersion,
        },
        "reference_contacts": sorted(reference_contacts),
        "run_summaries": runs,
        "measured_interpretation": "The top-ranked pose repeated across seeds but occupied a different site-frame orientation from the observed ligand. A closer low-ranked pose occurred only in one seed; the other seeds did not reproduce it. This is not an interpretable native ranking reference, so the conditional PRL/background docking stage was not run.",
        "no_threshold": "No numerical pass gate was set or inferred; the measured pose/ranking behavior is reported directly.",
    }
    (DERIVED / "native_redocking_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
