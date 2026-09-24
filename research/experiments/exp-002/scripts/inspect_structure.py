#!/usr/bin/env python3
"""Inspect 3TDC assembly/site geometry and write the unfilled dimer receptor."""
from __future__ import annotations

import csv
import gzip
import json
import math
import pathlib
import statistics

import gemmi

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "inputs" / "raw"
DERIVED = ROOT / "derived"
TABLES = ROOT / "tables"


def distance(a: gemmi.Position, b: gemmi.Position) -> float:
    return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2 + (a.z-b.z)**2)


def heavy_atoms(residue):
    return [a for a in residue if a.element.name != "H"]


def main() -> None:
    DERIVED.mkdir(exist_ok=True)
    TABLES.mkdir(exist_ok=True)
    structure = gemmi.read_structure(str(RAW / "3TDC-assembly2.cif.gz"))
    model = structure[0]
    chain_a = model["A"]
    chain_b = model["A-2"]
    ligand = next(r for r in chain_a if r.name == "0EU")
    ligand_atoms = heavy_atoms(ligand)

    contacts = []
    for chain in (chain_a, chain_b):
        for residue in chain:
            if residue.het_flag != "A":
                continue
            best = None
            for pa in heavy_atoms(residue):
                for la in ligand_atoms:
                    d = distance(pa.pos, la.pos)
                    if best is None or d < best[0]:
                        best = (d, pa.name, la.name)
            if best and best[0] <= 6.0:
                contacts.append({
                    "chain": "A" if chain.name == "A" else "B(symmetry mate)",
                    "residue": residue.name,
                    "author_residue_number": residue.seqid.num,
                    "minimum_distance_A": round(best[0], 3),
                    "protein_atom": best[1],
                    "ligand_atom": best[2],
                    "within_4.5_A": best[0] <= 4.5,
                })
    contacts.sort(key=lambda x: x["minimum_distance_A"])
    with (TABLES / "native_site_contacts.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(contacts[0]))
        writer.writeheader()
        writer.writerows(contacts)

    water_contacts = []
    for chain in (chain_a, chain_b):
        for residue in chain:
            if residue.name != "HOH":
                continue
            d = min(distance(a.pos, la.pos) for a in heavy_atoms(residue) for la in ligand_atoms)
            if d <= 3.5:
                water_contacts.append({
                    "chain": "A" if chain.name == "A" else "B(symmetry mate)",
                    "author_residue_number": residue.seqid.num,
                    "minimum_distance_A": round(d, 3),
                })

    xs = [a.pos.x for a in ligand_atoms]
    ys = [a.pos.y for a in ligand_atoms]
    zs = [a.pos.z for a in ligand_atoms]
    bounds = {"x": [min(xs), max(xs)], "y": [min(ys), max(ys)], "z": [min(zs), max(zs)]}
    center = [(lo+hi)/2 for lo, hi in bounds.values()]
    size = [(hi-lo)+12.0 for lo, hi in bounds.values()]

    missing_ranges = [[1715, 1718], [2415, 2427], [2452, 2476]]
    flank_distances = []
    for seq in [1719, 2414, 2428, 2451]:
        found = next((r for r in chain_a if r.seqid.num == seq and r.het_flag == "A"), None)
        if found:
            flank_distances.append({
                "author_residue_number": seq,
                "residue": found.name,
                "minimum_distance_to_0EU_A": round(min(distance(a.pos, la.pos) for a in heavy_atoms(found) for la in ligand_atoms), 3),
            })

    occupancy = [a.occ for a in ligand_atoms]
    b_factors = [a.b_iso for a in ligand_atoms]
    altlocs = sorted({str(a.altloc) for a in ligand_atoms if str(a.altloc).strip("\x00 ")})
    uniprot = json.loads((RAW / "uniprot-O00763.json").read_text())
    api_entity = json.loads((RAW / "rcsb-polymer-entity-3TDC-1.json").read_text())
    entity_sequence = api_entity["entity_poly"]["pdbx_seq_one_letter_code"][:756]
    current_segment = uniprot["sequence"]["value"][1689:1689+756]
    sequence_differences = [
        {
            "entity_position": i + 1,
            "author_residue_number": i + 1715,
            "current_uniprot_position": i + 1690,
            "construct_residue": a,
            "current_uniprot_residue": b,
        }
        for i, (a, b) in enumerate(zip(entity_sequence, current_segment)) if a != b
    ]
    api_assembly1 = json.loads((RAW / "rcsb-assembly-3TDC-1.json").read_text())
    api_assembly2 = json.loads((RAW / "rcsb-assembly-3TDC-2.json").read_text())

    summary = {
        "entry": "3TDC",
        "resolution_A": 2.41,
        "current_identity": {
            "uniprot_accession": uniprot["primaryAccession"],
            "uniprot_entry": uniprot["uniProtkbId"],
            "protein_name": uniprot["proteinDescription"]["recommendedName"]["fullName"]["value"],
            "organism": uniprot["organism"]["scientificName"],
            "sequence_length": uniprot["sequence"]["length"],
            "rcsb_sifts_alignment": api_entity["rcsb_polymer_entity_align"],
            "direct_sequence_differences_from_current_O00763_1690_2445": sequence_differences,
            "isoform_note": "The deposit calls the molecule an ACC2 variant and assigns no current UniProt isoform identifier. Current RCSB SIFTS maps it to canonical O00763; direct comparison finds the single I/V difference recorded here.",
            "depositor_dbref_discrepancy": "Deposited mmCIF DBREF uses obsolete Q59GJ9 and maps entity 1-756 to database 921-1676, whereas current RCSB SIFTS maps it to O00763 residues 1690-2445. Author coordinate numbering is 1715-2470; six C-terminal histidines are tag residues 2471-2476.",
        },
        "assemblies": {
            "1": api_assembly1["pdbx_struct_assembly"],
            "2": api_assembly2["pdbx_struct_assembly"],
            "assembly2_generation": api_assembly2["pdbx_struct_assembly_gen"],
            "operator2": next(x for x in api_assembly2["pdbx_struct_oper_list"] if x["id"] == "2"),
            "selection": "software-defined PISA dimer assembly 2 retained because its symmetry-related chain contributes direct native-site contacts; author-defined assembly 1 is a monomer and omits those contacts",
        },
        "native_ligand": {
            "component": "0EU",
            "chain": "A",
            "author_residue_number": 3000,
            "heavy_atom_count": len(ligand_atoms),
            "heavy_atom_occupancy_min_max": [min(occupancy), max(occupancy)],
            "heavy_atom_b_factor_mean_range_A2": [round(statistics.mean(b_factors), 3), round(min(b_factors), 3), round(max(b_factors), 3)],
            "heavy_atom_altlocs": altlocs,
            "stereochemistry": "CCD specifies the spiro center as S (InChI /t27-/m0/s1; stereo SMILES retained in source record)",
            "bounding_box_A": bounds,
        },
        "site": {
            "protein_residue_contacts_within_4.5_A": sum(x["within_4.5_A"] for x in contacts),
            "symmetry_mate_contacts_within_4.5_A": sum(x["within_4.5_A"] and x["chain"].startswith("B") for x in contacts),
            "contact_table": "../tables/native_site_contacts.csv",
            "waters_within_3.5_A": water_contacts,
            "missing_author_residue_ranges": missing_ranges,
            "resolved_flank_distances": flank_distances,
            "interpretation": "No missing range is silently modeled. Resolved residues flanking all three missing ranges are at least 41.991 A from 0EU, so no resolved gap boundary is adjacent to the observed site. Endpoint distances do not establish where a flexible missing segment could reach or prove that the omissions cannot influence the pocket.",
        },
        "docking_box": {
            "definition": "axis-aligned native 0EU heavy-atom bounds plus 6.0 A padding on each face",
            "center_A": [round(x, 3) for x in center],
            "size_A": [round(x, 3) for x in size],
        },
        "preparation": {
            "assembly": "3TDC assembly 2, chains renamed A and B only for PDB compatibility",
            "retained": "all resolved standard protein atoms from both symmetry-related chains",
            "removed": "both 0EU copies and all crystallographic waters; no ions or other cofactors are present",
            "missing_residues": "left absent",
        },
    }
    (DERIVED / "structure_inspection.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    # Protein-only PDB for Meeko. Keep the PISA symmetry mate and do not fill gaps.
    receptor = gemmi.read_structure(str(RAW / "3TDC-assembly2.cif.gz"))
    receptor[0]["A-2"].name = "B"
    for chain in receptor[0]:
        for idx in range(len(chain) - 1, -1, -1):
            if chain[idx].het_flag != "A":
                del chain[idx]
    receptor.name = "3TDC_PISA_DIMER_PROTEIN_ONLY"
    receptor.write_pdb(str(DERIVED / "receptor_assembly2_protein_only.pdb"))

    # Bound reference PDB (heavy atoms) preserves deposited atom names and site frame.
    ref = gemmi.Structure()
    ref.name = "3TDC_BOUND_0EU_SITE_A"
    ref.add_model(gemmi.Model("1"))
    out_chain = gemmi.Chain("L")
    out_res = gemmi.Residue()
    out_res.name = "0EU"
    out_res.seqid = gemmi.SeqId(1, " ")
    out_res.het_flag = "H"
    for atom in ligand_atoms:
        out_res.add_atom(atom)
    out_chain.add_residue(out_res)
    ref[0].add_chain(out_chain)
    ref.write_pdb(str(DERIVED / "native_0EU_bound_reference.pdb"))


if __name__ == "__main__":
    main()
