#!/usr/bin/env python3
"""Derive auditable coordinate tables for official 6VRH and 8EF5 records.

No docking, structure modification, density-map access, or biological scoring is
performed. Distances are direct Euclidean distances between deposited atom
coordinates. The 4.0 A contact cutoff is descriptive, not a success threshold.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

from cif_utils import read_cif

CONFIG = {
    "6VRH": {"ligand": "8PR", "accession": "P31645"},
    "8EF5": {"ligand": "7V7", "accession": "P35372"},
}
CUTOFF_A = 4.0
UNKNOWN = {".", "?", ""}
STANDARD_AMINO_ACID_HEAVY_ATOMS = {
    "ALA": {"N", "CA", "C", "O", "CB"},
    "ARG": {"N", "CA", "C", "O", "CB", "CG", "CD", "NE", "CZ", "NH1", "NH2"},
    "ASN": {"N", "CA", "C", "O", "CB", "CG", "OD1", "ND2"},
    "ASP": {"N", "CA", "C", "O", "CB", "CG", "OD1", "OD2"},
    "CYS": {"N", "CA", "C", "O", "CB", "SG"},
    "GLN": {"N", "CA", "C", "O", "CB", "CG", "CD", "OE1", "NE2"},
    "GLU": {"N", "CA", "C", "O", "CB", "CG", "CD", "OE1", "OE2"},
    "GLY": {"N", "CA", "C", "O"},
    "HIS": {"N", "CA", "C", "O", "CB", "CG", "ND1", "CD2", "CE1", "NE2"},
    "ILE": {"N", "CA", "C", "O", "CB", "CG1", "CG2", "CD1"},
    "LEU": {"N", "CA", "C", "O", "CB", "CG", "CD1", "CD2"},
    "LYS": {"N", "CA", "C", "O", "CB", "CG", "CD", "CE", "NZ"},
    "MET": {"N", "CA", "C", "O", "CB", "CG", "SD", "CE"},
    "PHE": {"N", "CA", "C", "O", "CB", "CG", "CD1", "CD2", "CE1", "CE2", "CZ"},
    "PRO": {"N", "CA", "C", "O", "CB", "CG", "CD"},
    "SER": {"N", "CA", "C", "O", "CB", "OG"},
    "THR": {"N", "CA", "C", "O", "CB", "OG1", "CG2"},
    "TRP": {"N", "CA", "C", "O", "CB", "CG", "CD1", "CD2", "NE1", "CE2", "CE3", "CZ2", "CZ3", "CH2"},
    "TYR": {"N", "CA", "C", "O", "CB", "CG", "CD1", "CD2", "CE1", "CE2", "CZ", "OH"},
    "VAL": {"N", "CA", "C", "O", "CB", "CG1", "CG2"},
}


def clean(value: str | None) -> str:
    return "" if value is None or value in UNKNOWN else value


def number(value: str) -> float:
    return float(value)


def distance(a: dict[str, str], b: dict[str, str]) -> float:
    return math.sqrt(sum((number(a[f"_atom_site.Cartn_{axis}"]) - number(b[f"_atom_site.Cartn_{axis}"])) ** 2 for axis in "xyz"))


def heavy(atom: dict[str, str]) -> bool:
    return atom["_atom_site.type_symbol"].upper() not in {"H", "D"}


def compress_ranges(values: set[int]) -> str:
    if not values:
        return ""
    ordered = sorted(values)
    ranges: list[str] = []
    start = previous = ordered[0]
    for value in ordered[1:]:
        if value == previous + 1:
            previous = value
            continue
        ranges.append(str(start) if start == previous else f"{start}-{previous}")
        start = previous = value
    ranges.append(str(start) if start == previous else f"{start}-{previous}")
    return ",".join(ranges)


def sequence(value: str) -> str:
    return "".join(value.split()).replace("(", "").replace(")", "")


def write_tsv(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, dialect="excel-tab", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def atom_id(atom: dict[str, str]) -> dict[str, object]:
    return {
        "label_asym": atom["_atom_site.label_asym_id"],
        "auth_asym": atom["_atom_site.auth_asym_id"],
        "entity": atom["_atom_site.label_entity_id"],
        "label_seq": clean(atom["_atom_site.label_seq_id"]),
        "auth_seq": clean(atom["_atom_site.auth_seq_id"]),
        "comp": atom["_atom_site.label_comp_id"],
        "atom": atom["_atom_site.label_atom_id"],
        "element": atom["_atom_site.type_symbol"],
        "alt": clean(atom["_atom_site.label_alt_id"]),
        "occupancy": atom["_atom_site.occupancy"],
        "b_iso_A2": atom["_atom_site.B_iso_or_equiv"],
        "atom_site_formal_charge": clean(atom["_atom_site.pdbx_formal_charge"]),
    }


def min_pair(left: list[dict[str, str]], right: list[dict[str, str]]) -> tuple[float, dict[str, str], dict[str, str]]:
    best: tuple[float, dict[str, str], dict[str, str]] | None = None
    for a in left:
        if not heavy(a):
            continue
        for b in right:
            if not heavy(b):
                continue
            d = distance(a, b)
            if best is None or d < best[0]:
                best = (d, a, b)
    if best is None:
        raise ValueError("empty heavy-atom group")
    return best


def parse_entities(raw: Path, pdb: str) -> dict[str, dict[str, object]]:
    entities: dict[str, dict[str, object]] = {}
    for path in sorted(raw.glob(f"rcsb-polymer-{pdb}-entity-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        identifiers = record["rcsb_polymer_entity_container_identifiers"]
        entity_id = str(identifiers["entity_id"])
        sources = record.get("rcsb_entity_source_organism", [])
        entities[entity_id] = {
            "kind": "polymer",
            "description": record.get("rcsb_polymer_entity", {}).get("pdbx_description", ""),
            "species": ";".join(sorted({str(x.get("ncbi_scientific_name", "")) for x in sources})),
            "taxonomy_ids": ";".join(sorted({str(x.get("ncbi_taxonomy_id", "")) for x in sources})),
            "label_asym_ids": identifiers.get("asym_ids", []),
            "auth_asym_ids": identifiers.get("auth_asym_ids", []),
            "record": record,
        }
    for path in sorted(raw.glob(f"rcsb-nonpolymer-{pdb}-entity-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        identifiers = record["rcsb_nonpolymer_entity_container_identifiers"]
        entity_id = str(identifiers["entity_id"])
        nonpoly = record.get("pdbx_entity_nonpoly", {})
        entities[entity_id] = {
            "kind": "nonpolymer",
            "description": nonpoly.get("name", ""),
            "species": "",
            "taxonomy_ids": "",
            "label_asym_ids": identifiers.get("asym_ids", []),
            "auth_asym_ids": identifiers.get("auth_asym_ids", []),
            "record": record,
        }
    return entities


def validation_records(raw: Path, pdb: str) -> tuple[dict[str, str], dict[tuple[str, str, str], dict[str, str]]]:
    with gzip.open(raw / f"wwpdb-{pdb.lower()}-validation.xml.gz", "rb") as handle:
        root = ET.parse(handle).getroot()
    entry_element = root.find("Entry")
    if entry_element is None:
        raise ValueError(f"no Entry in {pdb} validation XML")
    records: dict[tuple[str, str, str], dict[str, str]] = {}
    for node in root.findall("ModelledSubgroup"):
        key = (node.attrib.get("said", ""), node.attrib.get("seq", ""), node.attrib.get("resname", ""))
        records[key] = dict(node.attrib)
    return dict(entry_element.attrib), records


def ccd_data(raw: Path, comp: str) -> tuple[dict[str, str], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    scalars, categories = read_cif(raw / f"ccd-{comp}.cif")
    atoms = categories.get("_chem_comp_atom", [])
    bonds = categories.get("_chem_comp_bond", [])
    descriptors = categories.get("_pdbx_chem_comp_descriptor", [])
    return scalars, atoms, bonds, descriptors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    raw = args.evidence / "raw"
    generated = args.evidence / "generated"
    generated.mkdir(parents=True, exist_ok=True)

    structure_summary: dict[str, object] = {
        "analysis": "direct deposited-coordinate geometry",
        "contact_cutoff_A": CUTOFF_A,
        "contact_cutoff_interpretation": "descriptive inventory only; not a biological or docking success threshold",
        "structures": {},
    }
    entity_rows: list[dict[str, object]] = []
    assembly_rows: list[dict[str, object]] = []
    ligand_rows: list[dict[str, object]] = []
    ligand_graph_rows: list[dict[str, object]] = []
    contact_rows: list[dict[str, object]] = []
    residue_rows: list[dict[str, object]] = []
    nearby_rows: list[dict[str, object]] = []
    missing_rows: list[dict[str, object]] = []
    context_rows: list[dict[str, object]] = []
    hetero_rows: list[dict[str, object]] = []
    validation_rows: list[dict[str, object]] = []
    connection_rows: list[dict[str, object]] = []
    entity_inventory_rows: list[dict[str, object]] = []
    occupancy_rows: list[dict[str, object]] = []

    for pdb, config in CONFIG.items():
        ligand = config["ligand"]
        accession = config["accession"]
        scalars, categories = read_cif(raw / f"{pdb}.cif")
        assembly_scalars, assembly_categories = read_cif(raw / f"{pdb}-assembly1.cif")
        atoms = categories["_atom_site"]
        assembly_atoms = assembly_categories["_atom_site"]
        entities = parse_entities(raw, pdb)
        entry_validation, residue_validation = validation_records(raw, pdb)
        entry = json.loads((raw / f"rcsb-entry-{pdb}.json").read_text(encoding="utf-8"))

        # Confirm that the fetched API entity records exhaust the IDs enumerated
        # by both the entry API and the deposited mmCIF.
        entry_ids = entry["rcsb_entry_container_identifiers"]
        api_entity_ids = {
            str(value)
            for key in ("polymer_entity_ids", "non_polymer_entity_ids", "branched_entity_ids")
            for value in entry_ids.get(key, [])
        }
        mmcif_entity_ids = {row["_entity.id"] for row in categories.get("_entity", [])}
        fetched_entity_ids = set(entities)
        entity_inventory_rows.append({
            "pdb": pdb,
            "mmcif_entity_ids": ",".join(sorted(mmcif_entity_ids, key=int)),
            "entry_api_entity_ids": ",".join(sorted(api_entity_ids, key=int)),
            "fetched_entity_ids": ",".join(sorted(fetched_entity_ids, key=int)),
            "inventory_identical": mmcif_entity_ids == api_entity_ids == fetched_entity_ids,
        })

        unobserved_atoms = categories.get("_pdbx_unobs_or_zero_occ_atoms", [])
        unobserved_residues = categories.get("_pdbx_unobs_or_zero_occ_residues", [])
        zero_occupancy_atoms = [atom for atom in atoms if number(atom["_atom_site.occupancy"]) == 0.0]
        partial_occupancy_atoms = [atom for atom in atoms if 0.0 < number(atom["_atom_site.occupancy"]) < 1.0]
        target_unobserved_atoms = [
            row for row in unobserved_atoms
            if row.get("_pdbx_unobs_or_zero_occ_atoms.label_asym_id") in entities["1"]["label_asym_ids"]
        ]
        occupancy_rows.append({
            "pdb": pdb,
            "atom_site_count": len(atoms),
            "atom_site_occupancy_values": ",".join(sorted({atom["_atom_site.occupancy"] for atom in atoms})),
            "zero_occupancy_coordinate_count": len(zero_occupancy_atoms),
            "partial_occupancy_coordinate_count": len(partial_occupancy_atoms),
            "unobserved_atom_category_present": bool(unobserved_atoms),
            "unobserved_atom_record_count": len(unobserved_atoms),
            "target_unobserved_atom_records": ",".join(
                f"{row['_pdbx_unobs_or_zero_occ_atoms.label_asym_id']}:{row['_pdbx_unobs_or_zero_occ_atoms.label_comp_id']}:"
                f"{row['_pdbx_unobs_or_zero_occ_atoms.label_seq_id']}:{row['_pdbx_unobs_or_zero_occ_atoms.label_atom_id']}:"
                f"occupancy_flag={row['_pdbx_unobs_or_zero_occ_atoms.occupancy_flag']}"
                for row in target_unobserved_atoms
            ),
            "unobserved_residue_record_count": len(unobserved_residues),
        })

        # Assembly operators and a coordinate-level deposited/assembly comparison.
        assembly_gen = categories.get("_pdbx_struct_assembly_gen", [])
        if not assembly_gen:
            scalar_gen = {key: value for key, value in scalars.items() if key.startswith("_pdbx_struct_assembly_gen.")}
            assembly_gen = [scalar_gen] if scalar_gen else []
        operators = categories.get("_pdbx_struct_oper_list", [])
        if not operators:
            scalar_operator = {key: value for key, value in scalars.items() if key.startswith("_pdbx_struct_oper_list.")}
            operators = [scalar_operator] if scalar_operator else []
        original_signature = sorted((a["_atom_site.auth_asym_id"], a["_atom_site.auth_seq_id"], a["_atom_site.auth_comp_id"],
                                     a["_atom_site.auth_atom_id"], a["_atom_site.Cartn_x"], a["_atom_site.Cartn_y"], a["_atom_site.Cartn_z"])
                                    for a in atoms)
        assembly_signature = sorted((a["_atom_site.auth_asym_id"], a["_atom_site.auth_seq_id"], a["_atom_site.auth_comp_id"],
                                     a["_atom_site.auth_atom_id"], a["_atom_site.Cartn_x"], a["_atom_site.Cartn_y"], a["_atom_site.Cartn_z"])
                                    for a in assembly_atoms)
        for row in assembly_gen:
            assembly_rows.append({
                "pdb": pdb,
                "assembly_id": row.get("_pdbx_struct_assembly_gen.assembly_id", ""),
                "operator_expression": row.get("_pdbx_struct_assembly_gen.oper_expression", ""),
                "label_asym_id_list": row.get("_pdbx_struct_assembly_gen.asym_id_list", ""),
                "operator_count_in_cif": len(operators),
                "deposited_atom_count": len(atoms),
                "assembly_atom_count": len(assembly_atoms),
                "auth_atom_coordinate_signatures_identical": original_signature == assembly_signature,
            })

        # Entity/construct, canonical mapping, modeled spans, and substitutions.
        target_entity = entities["1"]["record"]
        deposited = sequence(target_entity["entity_poly"]["pdbx_seq_one_letter_code_can"])
        uniprot = json.loads((raw / f"uniprot-{accession}.json").read_text(encoding="utf-8"))
        canonical = uniprot["sequence"]["value"]
        align = target_entity["rcsb_polymer_entity_align"][0]["aligned_regions"][0]
        entity_beg = int(align["entity_beg_seq_id"])
        ref_beg = int(align["ref_beg_seq_id"])
        align_length = int(align["length"])
        compared_reference = canonical[ref_beg - 1:ref_beg - 1 + align_length]
        substitutions = [f"{compared_reference[i]}{ref_beg+i}{deposited[i]}" for i in range(align_length)
                         if deposited[i] != compared_reference[i]]
        if len(deposited) != align_length or len(compared_reference) != align_length:
            raise ValueError(f"unexpected alignment length for {pdb}")

        modeled_by_asym: dict[str, set[int]] = defaultdict(set)
        auth_seq_by_asym: dict[str, set[int]] = defaultdict(set)
        auth_chains_by_asym: dict[str, set[str]] = defaultdict(set)
        residue_names: dict[tuple[str, int], str] = {}
        residue_atoms: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
        official_unobserved_atom_names: dict[tuple[str, int], set[str]] = defaultdict(set)
        for row in unobserved_atoms:
            seq_value = row.get("_pdbx_unobs_or_zero_occ_atoms.label_seq_id", "")
            if seq_value not in UNKNOWN:
                official_unobserved_atom_names[(row["_pdbx_unobs_or_zero_occ_atoms.label_asym_id"], int(seq_value))].add(
                    row["_pdbx_unobs_or_zero_occ_atoms.label_atom_id"]
                )
        for atom in atoms:
            if atom["_atom_site.group_PDB"] == "ATOM" and atom["_atom_site.label_seq_id"] not in UNKNOWN:
                seq_id = int(atom["_atom_site.label_seq_id"])
                asym = atom["_atom_site.label_asym_id"]
                modeled_by_asym[asym].add(seq_id)
                residue_atoms[(asym, seq_id)].append(atom)
                auth_chains_by_asym[asym].add(atom["_atom_site.auth_asym_id"])
                if atom["_atom_site.auth_seq_id"] not in UNKNOWN:
                    try:
                        auth_seq_by_asym[asym].add(int(atom["_atom_site.auth_seq_id"]))
                    except ValueError:
                        pass
                residue_names[(asym, seq_id)] = atom["_atom_site.label_comp_id"]

        for entity_id, entity in sorted(entities.items(), key=lambda item: int(item[0])):
            record = entity["record"]
            sample_length = ""
            mutation_count = ""
            align_text = ""
            if entity["kind"] == "polymer":
                sample_length = record.get("entity_poly", {}).get("rcsb_sample_sequence_length", "")
                mutation_count = record.get("entity_poly", {}).get("rcsb_mutation_count", "")
                aligns = record.get("rcsb_polymer_entity_align", [])
                align_text = json.dumps(aligns, sort_keys=True, separators=(",", ":")) if aligns else ""
            for asym in entity["label_asym_ids"] or [""]:
                modeled = modeled_by_asym.get(asym, set())
                entity_rows.append({
                    "pdb": pdb, "entity": entity_id, "kind": entity["kind"], "description": entity["description"],
                    "species": entity["species"], "taxonomy_ids": entity["taxonomy_ids"], "label_asym": asym,
                    "auth_asym_ids_entity_record": ",".join(entity["auth_asym_ids"]),
                    "observed_auth_asym": ",".join(sorted(auth_chains_by_asym.get(asym, set()))),
                    "deposited_sequence_length": sample_length,
                    "modeled_residue_count": len(modeled), "modeled_label_seq_ranges": compress_ranges(modeled),
                    "modeled_auth_seq_ranges": compress_ranges(auth_seq_by_asym.get(asym, set())),
                    "modeled_target_canonical_ranges": compress_ranges({ref_beg + value - entity_beg for value in modeled}) if entity_id == "1" else "",
                    "rcsb_mutation_count": mutation_count, "reference_alignment": align_text,
                    "independent_target_sequence_substitutions": ",".join(substitutions) if entity_id == "1" else "",
                })
                if entity["kind"] == "polymer" and sample_length and asym:
                    all_ids = set(range(1, int(sample_length) + 1))
                    missing = all_ids - modeled
                    missing_rows.append({"pdb": pdb, "entity": entity_id, "label_asym": asym,
                                         "deposited_sequence_length": sample_length, "modeled_count": len(modeled),
                                         "missing_label_seq_ranges": compress_ranges(missing)})

        for connection in categories.get("_struct_conn", []):
            connection_rows.append({
                "pdb": pdb,
                "id": connection.get("_struct_conn.id", ""),
                "type": connection.get("_struct_conn.conn_type_id", ""),
                "partner1": f"{connection.get('_struct_conn.ptnr1_label_asym_id', '')}:{connection.get('_struct_conn.ptnr1_label_comp_id', '')}:{connection.get('_struct_conn.ptnr1_label_seq_id', '')}:{connection.get('_struct_conn.ptnr1_label_atom_id', '')}",
                "partner2": f"{connection.get('_struct_conn.ptnr2_label_asym_id', '')}:{connection.get('_struct_conn.ptnr2_label_comp_id', '')}:{connection.get('_struct_conn.ptnr2_label_seq_id', '')}:{connection.get('_struct_conn.ptnr2_label_atom_id', '')}",
                "reported_distance_A": clean(connection.get("_struct_conn.pdbx_dist_value")),
                "role": clean(connection.get("_struct_conn.pdbx_role")),
            })

        ccd_scalars, ccd_atoms, ccd_bonds, descriptors = ccd_data(raw, ligand)
        ccd_heavy_names = {a["_chem_comp_atom.atom_id"] for a in ccd_atoms if a["_chem_comp_atom.type_symbol"].upper() not in {"H", "D"}}
        ccd_all_names = {a["_chem_comp_atom.atom_id"] for a in ccd_atoms}
        ccd_elements = {a["_chem_comp_atom.atom_id"]: a["_chem_comp_atom.type_symbol"].upper() for a in ccd_atoms}
        stereo_atoms = sorted(f"{a['_chem_comp_atom.atom_id']}:{a['_chem_comp_atom.pdbx_stereo_config']}"
                              for a in ccd_atoms if clean(a.get("_chem_comp_atom.pdbx_stereo_config")) not in {"", "N"})
        smiles = [d["_pdbx_chem_comp_descriptor.descriptor"] for d in descriptors
                  if d.get("_pdbx_chem_comp_descriptor.type") in {"SMILES_CANONICAL", "SMILES"}]
        for bond in ccd_bonds:
            ligand_graph_rows.append({
                "pdb": pdb, "comp": ligand, "atom_1": bond["_chem_comp_bond.atom_id_1"],
                "atom_2": bond["_chem_comp_bond.atom_id_2"], "value_order": bond["_chem_comp_bond.value_order"],
                "aromatic": bond["_chem_comp_bond.pdbx_aromatic_flag"],
                "stereo": clean(bond.get("_chem_comp_bond.pdbx_stereo_config")),
            })

        ligand_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
        for atom in atoms:
            if atom["_atom_site.label_comp_id"] == ligand:
                ligand_groups[atom["_atom_site.label_asym_id"]].append(atom)
        if not ligand_groups:
            raise ValueError(f"no {ligand} atoms in {pdb}")

        # Hetero inventory is residue-instance exact; not an inferred solvent model.
        hetero_groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
        for atom in atoms:
            if atom["_atom_site.group_PDB"] == "HETATM":
                key = (atom["_atom_site.label_asym_id"], atom["_atom_site.auth_asym_id"],
                       atom["_atom_site.label_comp_id"], atom["_atom_site.auth_seq_id"])
                hetero_groups[key].append(atom)
        for key, group in sorted(hetero_groups.items()):
            hetero_rows.append({"pdb": pdb, "label_asym": key[0], "auth_asym": key[1], "comp": key[2],
                                "auth_seq": key[3], "atom_count": len(group), "heavy_atom_count": sum(heavy(x) for x in group),
                                "occupancies": ",".join(sorted({x["_atom_site.occupancy"] for x in group})),
                                "alt_ids": ",".join(sorted({clean(x["_atom_site.label_alt_id"]) for x in group if clean(x["_atom_site.label_alt_id"])}))})

        receptor_contact_atoms_by_ligand: dict[str, list[dict[str, str]]] = {}
        for ligand_asym, ligand_atoms in sorted(ligand_groups.items()):
            coord_names = {a["_atom_site.label_atom_id"] for a in ligand_atoms}
            coord_heavy_names = {a["_atom_site.label_atom_id"] for a in ligand_atoms if heavy(a)}
            coordinate_elements = {a["_atom_site.label_atom_id"]: a["_atom_site.type_symbol"].upper() for a in ligand_atoms}
            element_mismatches = sorted(
                f"{name}:CCD={ccd_elements[name]}:coordinate={coordinate_elements[name]}"
                for name in coord_names & ccd_all_names
                if ccd_elements[name] != coordinate_elements[name]
            )
            ligand_validation = residue_validation.get((ligand_asym, ".", ligand), {})
            ligand_rows.append({
                "pdb": pdb, "comp": ligand, "label_asym": ligand_asym,
                "auth_asym": ligand_atoms[0]["_atom_site.auth_asym_id"], "auth_seq": ligand_atoms[0]["_atom_site.auth_seq_id"],
                "coordinate_atom_count": len(ligand_atoms), "coordinate_heavy_atom_count": len(coord_heavy_names),
                "ccd_atom_count_including_H": len(ccd_all_names), "ccd_heavy_atom_count": len(ccd_heavy_names),
                "missing_ccd_heavy_atom_names": ",".join(sorted(ccd_heavy_names - coord_heavy_names)),
                "extra_coordinate_atom_names": ",".join(sorted(coord_names - ccd_all_names)),
                "ccd_coordinate_element_mismatches": ",".join(element_mismatches),
                "occupancy_min": min(number(a["_atom_site.occupancy"]) for a in ligand_atoms),
                "occupancy_max": max(number(a["_atom_site.occupancy"]) for a in ligand_atoms),
                "b_iso_A2_min": min(number(a["_atom_site.B_iso_or_equiv"]) for a in ligand_atoms),
                "b_iso_A2_max": max(number(a["_atom_site.B_iso_or_equiv"]) for a in ligand_atoms),
                "b_iso_A2_mean": round(sum(number(a["_atom_site.B_iso_or_equiv"]) for a in ligand_atoms) / len(ligand_atoms), 3),
                "alt_ids": ",".join(sorted({clean(a["_atom_site.label_alt_id"]) for a in ligand_atoms if clean(a["_atom_site.label_alt_id"])})),
                "atom_site_formal_charges": ",".join(sorted({clean(a["_atom_site.pdbx_formal_charge"]) for a in ligand_atoms if clean(a["_atom_site.pdbx_formal_charge"])})),
                "ccd_formal_charge": ccd_scalars.get("_chem_comp.pdbx_formal_charge", ""),
                "ccd_formula": ccd_scalars.get("_chem_comp.formula", ""), "ccd_stereo_atoms": ",".join(stereo_atoms),
                "ccd_smiles": " | ".join(smiles),
                "validation_model": ligand_validation.get("model", ""),
                "validation_label_asym_said": ligand_validation.get("said", ""),
                "validation_auth_asym_chain": ligand_validation.get("chain", ""),
                "validation_auth_seq_resnum": ligand_validation.get("resnum", ""),
                "validation_entity": ligand_validation.get("ent", ""),
                "validation_label_seq": ligand_validation.get("seq", ""),
                "validation_resname": ligand_validation.get("resname", ""),
                "validation_Q_score": ligand_validation.get("Q_score", ""),
                "validation_residue_inclusion": ligand_validation.get("residue_inclusion", ""),
                "validation_mogul_bonds_rmsz": ligand_validation.get("mogul_bonds_rmsz", ""),
                "validation_mogul_angles_rmsz": ligand_validation.get("mogul_angles_rmsz", ""),
            })

            receptor_contact_atoms: list[dict[str, str]] = []
            per_residue: dict[tuple[str, str, str, str], list[tuple[float, dict[str, str], dict[str, str]]]] = defaultdict(list)
            for ligand_atom in ligand_atoms:
                if not heavy(ligand_atom):
                    continue
                for target_atom in atoms:
                    if target_atom in ligand_atoms or not heavy(target_atom):
                        continue
                    d = distance(ligand_atom, target_atom)
                    if d <= CUTOFF_A:
                        target_info = atom_id(target_atom)
                        entity = entities[target_atom["_atom_site.label_entity_id"]]
                        contact_rows.append({
                            "pdb": pdb, "ligand_comp": ligand, "ligand_label_asym": ligand_asym,
                            "ligand_auth_asym": ligand_atom["_atom_site.auth_asym_id"],
                            "ligand_auth_seq": ligand_atom["_atom_site.auth_seq_id"],
                            "ligand_atom": ligand_atom["_atom_site.label_atom_id"],
                            "target_kind": entity["kind"], "target_entity": target_info["entity"],
                            "target_description": entity["description"], "target_label_asym": target_info["label_asym"],
                            "target_auth_asym": target_info["auth_asym"], "target_comp": target_info["comp"],
                            "target_label_seq": target_info["label_seq"], "target_auth_seq": target_info["auth_seq"],
                            "target_atom": target_info["atom"], "distance_A": f"{d:.3f}",
                            "target_occupancy": target_info["occupancy"], "target_b_iso_A2": target_info["b_iso_A2"],
                        })
                        residue_key = (target_atom["_atom_site.label_entity_id"], target_atom["_atom_site.label_asym_id"],
                                       target_atom["_atom_site.label_comp_id"], target_atom["_atom_site.label_seq_id"])
                        per_residue[residue_key].append((d, ligand_atom, target_atom))
                        if target_atom["_atom_site.label_entity_id"] == "1":
                            receptor_contact_atoms.append(target_atom)
            receptor_contact_atoms_by_ligand[ligand_asym] = receptor_contact_atoms
            for key, pairs in sorted(per_residue.items()):
                best = min(pairs, key=lambda x: x[0])
                canonical_position = ""
                if key[0] == "1" and key[3] not in UNKNOWN:
                    canonical_position = ref_beg + int(key[3]) - entity_beg
                validation = residue_validation.get((key[1], key[3], key[2]), {})
                residue_rows.append({
                    "pdb": pdb, "ligand_label_asym": ligand_asym, "target_entity": key[0],
                    "target_kind": entities[key[0]]["kind"], "target_description": entities[key[0]]["description"],
                    "target_label_asym": key[1], "target_comp": key[2], "target_label_seq": clean(key[3]),
                    "canonical_accession": accession if key[0] == "1" else "", "canonical_position": canonical_position,
                    "minimum_distance_A": f"{best[0]:.3f}", "ligand_atom_at_min": best[1]["_atom_site.label_atom_id"],
                    "target_atom_at_min": best[2]["_atom_site.label_atom_id"], "atom_pair_count_within_4A": len(pairs),
                    "validation_Q_score": validation.get("Q_score", ""),
                    "validation_residue_inclusion": validation.get("residue_inclusion", ""),
                })

            # Every component/chain gets an exact nearest pair to the ligand.
            component_groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
            for atom in atoms:
                if atom in ligand_atoms:
                    continue
                entity = entities[atom["_atom_site.label_entity_id"]]
                if entity["kind"] == "polymer":
                    key = ("polymer_chain", atom["_atom_site.label_entity_id"], atom["_atom_site.label_asym_id"], "")
                else:
                    key = ("nonpolymer_residue", atom["_atom_site.label_entity_id"], atom["_atom_site.label_asym_id"], atom["_atom_site.auth_seq_id"])
                component_groups[key].append(atom)
            unique_receptor_contact_atoms = list({a["_atom_site.id"]: a for a in receptor_contact_atoms}.values())
            for key, group in sorted(component_groups.items()):
                d, lig_atom, other_atom = min_pair(ligand_atoms, group)
                pocket_distance = ""
                pocket_atom = ""
                component_atom = ""
                if key[0] == "polymer_chain" and key[1] != "1" and unique_receptor_contact_atoms:
                    p_d, p_atom, c_atom = min_pair(unique_receptor_contact_atoms, group)
                    pocket_distance = f"{p_d:.3f}"
                    pocket_atom = f"{p_atom['_atom_site.label_asym_id']}:{p_atom['_atom_site.label_comp_id']}:{p_atom['_atom_site.label_seq_id']}:{p_atom['_atom_site.label_atom_id']}"
                    component_atom = f"{c_atom['_atom_site.label_asym_id']}:{c_atom['_atom_site.label_comp_id']}:{c_atom['_atom_site.label_seq_id']}:{c_atom['_atom_site.label_atom_id']}"
                nearby_rows.append({
                    "pdb": pdb, "ligand_label_asym": ligand_asym, "component_group": key[0], "entity": key[1],
                    "description": entities[key[1]]["description"], "component_label_asym": key[2],
                    "component_auth_seq": key[3], "minimum_ligand_distance_A": f"{d:.3f}",
                    "ligand_atom_at_min": lig_atom["_atom_site.label_atom_id"],
                    "ligand_element_at_min": lig_atom["_atom_site.type_symbol"],
                    "component_label_asym_at_min": other_atom["_atom_site.label_asym_id"],
                    "component_auth_asym_at_min": other_atom["_atom_site.auth_asym_id"],
                    "component_comp_at_min": other_atom["_atom_site.label_comp_id"],
                    "component_label_seq_at_min": clean(other_atom["_atom_site.label_seq_id"]),
                    "component_auth_seq_at_min": clean(other_atom["_atom_site.auth_seq_id"]),
                    "component_atom_at_min": other_atom["_atom_site.label_atom_id"],
                    "component_element_at_min": other_atom["_atom_site.type_symbol"],
                    "component_occupancy_at_min": other_atom["_atom_site.occupancy"],
                    "minimum_distance_to_observed_receptor_contact_atoms_A": pocket_distance,
                    "receptor_pocket_atom_at_min": pocket_atom, "accessory_atom_at_min": component_atom,
                })

            # Sequence-neighbor check around every observed receptor contact residue.
            contact_seq = {int(a["_atom_site.label_seq_id"]) for a in receptor_contact_atoms if a["_atom_site.label_seq_id"] not in UNKNOWN}
            receptor_asym = {a["_atom_site.label_asym_id"] for a in receptor_contact_atoms}
            for asym in sorted(receptor_asym):
                modeled = modeled_by_asym[asym]
                for contact_seq_id in sorted(contact_seq):
                    for offset in (-2, -1, 0, 1, 2):
                        seq_id = contact_seq_id + offset
                        if 1 <= seq_id <= len(deposited):
                            local_atoms = residue_atoms.get((asym, seq_id), [])
                            modeled_comp = residue_names.get((asym, seq_id), "")
                            observed_heavy_names = {atom["_atom_site.label_atom_id"] for atom in local_atoms if heavy(atom)}
                            expected_heavy_names = STANDARD_AMINO_ACID_HEAVY_ATOMS.get(modeled_comp, set())
                            zero_names = sorted({
                                atom["_atom_site.label_atom_id"] for atom in local_atoms
                                if number(atom["_atom_site.occupancy"]) == 0.0
                            })
                            partial_names = sorted({
                                atom["_atom_site.label_atom_id"] for atom in local_atoms
                                if 0.0 < number(atom["_atom_site.occupancy"]) < 1.0
                            })
                            context_rows.append({
                                "pdb": pdb, "ligand_label_asym": ligand_asym, "receptor_label_asym": asym,
                                "contact_label_seq": contact_seq_id, "offset": offset, "context_label_seq": seq_id,
                                "canonical_position": ref_beg + seq_id - entity_beg,
                                "deposited_one_letter": deposited[seq_id - 1], "modeled": seq_id in modeled,
                                "modeled_comp": modeled_comp,
                                "expected_standard_heavy_atom_count": len(expected_heavy_names),
                                "observed_heavy_atom_count": len(observed_heavy_names),
                                "missing_expected_heavy_atom_names": ",".join(sorted(expected_heavy_names - observed_heavy_names)),
                                "official_unobserved_atom_names": ",".join(sorted(official_unobserved_atom_names.get((asym, seq_id), set()))),
                                "zero_occupancy_coordinate_atom_names": ",".join(zero_names),
                                "partial_occupancy_coordinate_atom_names": ",".join(partial_names),
                            })

        validation_rows.append({
            "pdb": pdb, "reported_resolution_A": entry_validation.get("PDB-resolution", ""),
            "emdb_id": entry_validation.get("emdb_id", ""), "entry_Q_score": entry_validation.get("Q_score", ""),
            "atom_inclusion_backbone": entry_validation.get("atom_inclusion_backbone", ""),
            "atom_inclusion_all_atoms": entry_validation.get("atom_inclusion_all_atoms", ""),
            "calculated_FSC_0.143_A": entry_validation.get("calculated_fsc_resolution_by_cutoff_0.143", ""),
            "author_FSC_0.143_A": entry_validation.get("author_provided_fsc_resolution_by_cutoff_0.143", ""),
            "validation_xml_creation": entry_validation.get("XMLcreationDate", ""),
            "note": "official wwPDB summary parsed; maps were not downloaded or inspected",
        })
        structure_summary["structures"][pdb] = {
            "title": entry.get("struct", {}).get("title", ""),
            "method": entry.get("exptl", [{}])[0].get("method", ""),
            "nominal_resolution_A": entry.get("rcsb_entry_info", {}).get("resolution_combined", []),
            "deposited_atom_count": len(atoms), "assembly1_atom_count": len(assembly_atoms),
            "assembly_coordinate_signature_identical_to_deposited": original_signature == assembly_signature,
            "target_entity": 1, "target_accession": accession, "target_taxonomy": 9606,
            "deposited_target_sequence_length": len(deposited),
            "canonical_target_sequence_length": len(canonical), "sifts_ref_begin": ref_beg,
            "sifts_aligned_length": align_length, "independent_sequence_substitutions": substitutions,
            "ligand": ligand, "ligand_instance_count": len(ligand_groups),
            "maps_downloaded_or_inspected": False,
        }

    # Stable output ordering.
    contact_rows.sort(key=lambda r: (r["pdb"], r["ligand_label_asym"], float(r["distance_A"]), r["target_label_asym"], r["target_auth_seq"], r["target_atom"]))
    residue_rows.sort(key=lambda r: (r["pdb"], r["ligand_label_asym"], float(r["minimum_distance_A"]), r["target_label_asym"], str(r["target_label_seq"])))
    nearby_rows.sort(key=lambda r: (r["pdb"], r["ligand_label_asym"], float(r["minimum_ligand_distance_A"]), r["component_label_asym"]))
    context_rows = list({tuple(row.items()): row for row in context_rows}.values())
    context_rows.sort(key=lambda r: (r["pdb"], r["ligand_label_asym"], r["receptor_label_asym"], r["contact_label_seq"], r["offset"]))

    (generated / "structure-summary.json").write_text(json.dumps(structure_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_tsv(generated / "entities.tsv", entity_rows, ["pdb", "entity", "kind", "description", "species", "taxonomy_ids", "label_asym", "auth_asym_ids_entity_record", "observed_auth_asym", "deposited_sequence_length", "modeled_residue_count", "modeled_label_seq_ranges", "modeled_auth_seq_ranges", "modeled_target_canonical_ranges", "rcsb_mutation_count", "reference_alignment", "independent_target_sequence_substitutions"])
    write_tsv(generated / "assembly-check.tsv", assembly_rows, ["pdb", "assembly_id", "operator_expression", "label_asym_id_list", "operator_count_in_cif", "deposited_atom_count", "assembly_atom_count", "auth_atom_coordinate_signatures_identical"])
    write_tsv(generated / "ligand-instances.tsv", ligand_rows, ["pdb", "comp", "label_asym", "auth_asym", "auth_seq", "coordinate_atom_count", "coordinate_heavy_atom_count", "ccd_atom_count_including_H", "ccd_heavy_atom_count", "missing_ccd_heavy_atom_names", "extra_coordinate_atom_names", "ccd_coordinate_element_mismatches", "occupancy_min", "occupancy_max", "b_iso_A2_min", "b_iso_A2_max", "b_iso_A2_mean", "alt_ids", "atom_site_formal_charges", "ccd_formal_charge", "ccd_formula", "ccd_stereo_atoms", "ccd_smiles", "validation_model", "validation_label_asym_said", "validation_auth_asym_chain", "validation_auth_seq_resnum", "validation_entity", "validation_label_seq", "validation_resname", "validation_Q_score", "validation_residue_inclusion", "validation_mogul_bonds_rmsz", "validation_mogul_angles_rmsz"])
    write_tsv(generated / "ligand-graph.tsv", ligand_graph_rows, ["pdb", "comp", "atom_1", "atom_2", "value_order", "aromatic", "stereo"])
    write_tsv(generated / "atom-pair-contacts-4A.tsv", contact_rows, ["pdb", "ligand_comp", "ligand_label_asym", "ligand_auth_asym", "ligand_auth_seq", "ligand_atom", "target_kind", "target_entity", "target_description", "target_label_asym", "target_auth_asym", "target_comp", "target_label_seq", "target_auth_seq", "target_atom", "distance_A", "target_occupancy", "target_b_iso_A2"])
    write_tsv(generated / "contact-residues-4A.tsv", residue_rows, ["pdb", "ligand_label_asym", "target_entity", "target_kind", "target_description", "target_label_asym", "target_comp", "target_label_seq", "canonical_accession", "canonical_position", "minimum_distance_A", "ligand_atom_at_min", "target_atom_at_min", "atom_pair_count_within_4A", "validation_Q_score", "validation_residue_inclusion"])
    write_tsv(generated / "component-nearest-distances.tsv", nearby_rows, ["pdb", "ligand_label_asym", "component_group", "entity", "description", "component_label_asym", "component_auth_seq", "minimum_ligand_distance_A", "ligand_atom_at_min", "ligand_element_at_min", "component_label_asym_at_min", "component_auth_asym_at_min", "component_comp_at_min", "component_label_seq_at_min", "component_auth_seq_at_min", "component_atom_at_min", "component_element_at_min", "component_occupancy_at_min", "minimum_distance_to_observed_receptor_contact_atoms_A", "receptor_pocket_atom_at_min", "accessory_atom_at_min"])
    write_tsv(generated / "missing-segments.tsv", missing_rows, ["pdb", "entity", "label_asym", "deposited_sequence_length", "modeled_count", "missing_label_seq_ranges"])
    write_tsv(generated / "pocket-sequence-context.tsv", context_rows, ["pdb", "ligand_label_asym", "receptor_label_asym", "contact_label_seq", "offset", "context_label_seq", "canonical_position", "deposited_one_letter", "modeled", "modeled_comp", "expected_standard_heavy_atom_count", "observed_heavy_atom_count", "missing_expected_heavy_atom_names", "official_unobserved_atom_names", "zero_occupancy_coordinate_atom_names", "partial_occupancy_coordinate_atom_names"])
    write_tsv(generated / "hetero-inventory.tsv", hetero_rows, ["pdb", "label_asym", "auth_asym", "comp", "auth_seq", "atom_count", "heavy_atom_count", "occupancies", "alt_ids"])
    write_tsv(generated / "validation-summary.tsv", validation_rows, ["pdb", "reported_resolution_A", "emdb_id", "entry_Q_score", "atom_inclusion_backbone", "atom_inclusion_all_atoms", "calculated_FSC_0.143_A", "author_FSC_0.143_A", "validation_xml_creation", "note"])
    write_tsv(generated / "struct-connections.tsv", connection_rows, ["pdb", "id", "type", "partner1", "partner2", "reported_distance_A", "role"])
    write_tsv(generated / "entity-inventory.tsv", entity_inventory_rows, ["pdb", "mmcif_entity_ids", "entry_api_entity_ids", "fetched_entity_ids", "inventory_identical"])
    write_tsv(generated / "atom-occupancy-summary.tsv", occupancy_rows, ["pdb", "atom_site_count", "atom_site_occupancy_values", "zero_occupancy_coordinate_count", "partial_occupancy_coordinate_count", "unobserved_atom_category_present", "unobserved_atom_record_count", "target_unobserved_atom_records", "unobserved_residue_record_count"])


if __name__ == "__main__":
    main()
