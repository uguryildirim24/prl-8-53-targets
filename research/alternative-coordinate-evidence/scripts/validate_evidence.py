#!/usr/bin/env python3
"""Lightweight integrity and internal-consistency checks for the evidence package."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", required=True, type=Path)
    args = parser.parse_args()
    evidence = args.evidence
    raw = evidence / "raw"
    generated = evidence / "generated"

    retrievals = sorted((evidence / "retrieval").glob("*.retrieval.json"))
    assert len(retrievals) == 32, len(retrievals)
    for path in retrievals:
        record = json.loads(path.read_text(encoding="utf-8"))
        payload = evidence / record["payload"]
        body = payload.read_bytes()
        assert record["http_status"] == 200, path
        assert record["bytes"] == len(body), path
        assert record["sha256"] == hashlib.sha256(body).hexdigest(), path
        assert record["started_utc"].endswith("Z") and record["completed_utc"].endswith("Z"), path
        started = dt.datetime.fromisoformat(record["started_utc"].replace("Z", "+00:00"))
        completed = dt.datetime.fromisoformat(record["completed_utc"].replace("Z", "+00:00"))
        assert started <= completed, path
        assert isinstance(record["redirects"], list), path

    summary = json.loads((generated / "structure-summary.json").read_text(encoding="utf-8"))
    assert summary["contact_cutoff_A"] == 4.0
    assert summary["structures"]["6VRH"]["independent_sequence_substitutions"] == []
    assert summary["structures"]["8EF5"]["independent_sequence_substitutions"] == []
    assert summary["structures"]["6VRH"]["ligand_instance_count"] == 1
    assert summary["structures"]["8EF5"]["ligand_instance_count"] == 2
    assert not summary["structures"]["6VRH"]["maps_downloaded_or_inspected"]
    assert not summary["structures"]["8EF5"]["maps_downloaded_or_inspected"]

    assemblies = rows(generated / "assembly-check.tsv")
    assert len(assemblies) == 2
    assert all(row["operator_expression"] == "1" for row in assemblies)
    assert all(row["deposited_atom_count"] == row["assembly_atom_count"] for row in assemblies)
    assert all(row["auth_atom_coordinate_signatures_identical"] == "True" for row in assemblies)

    inventories = rows(generated / "entity-inventory.tsv")
    assert len(inventories) == 2
    assert all(row["inventory_identical"] == "True" for row in inventories)

    targets = [row for row in rows(generated / "entities.tsv") if row["entity"] == "1"]
    expected = {
        ("6VRH", "A"): ("A", "77-617", "77-617"),
        ("8EF5", "A"): ("R", "65-351", "66-352"),
        ("8EF5", "F"): ("M", "65-352", "66-353"),
    }
    observed = {(r["pdb"], r["label_asym"]): (r["observed_auth_asym"], r["modeled_label_seq_ranges"], r["modeled_target_canonical_ranges"]) for r in targets}
    assert observed == expected, observed
    assert all(row["rcsb_mutation_count"] == "0" and row["independent_target_sequence_substitutions"] == "" for row in targets)

    ligands = rows(generated / "ligand-instances.tsv")
    assert len(ligands) == 3
    assert all(row["missing_ccd_heavy_atom_names"] == "" and row["extra_coordinate_atom_names"] == "" for row in ligands)
    assert all(row["ccd_coordinate_element_mismatches"] == "" for row in ligands)
    assert all(row["occupancy_min"] == "1.0" and row["occupancy_max"] == "1.0" and row["alt_ids"] == "" for row in ligands)
    assert all(row["ccd_formal_charge"] == "0" and row["atom_site_formal_charges"] == "" for row in ligands)
    expected_validation_ids = {
        ("6VRH", "E"): ("1", "E", "A", "702", "5", ".", "8PR"),
        ("8EF5", "H"): ("1", "H", "R", "501", "6", ".", "7V7"),
        ("8EF5", "N"): ("1", "N", "M", "501", "6", ".", "7V7"),
    }
    observed_validation_ids = {
        (row["pdb"], row["label_asym"]): (
            row["validation_model"], row["validation_label_asym_said"], row["validation_auth_asym_chain"],
            row["validation_auth_seq_resnum"], row["validation_entity"], row["validation_label_seq"],
            row["validation_resname"],
        )
        for row in ligands
    }
    assert observed_validation_ids == expected_validation_ids, observed_validation_ids

    atom_contacts = rows(generated / "atom-pair-contacts-4A.tsv")
    assert len(atom_contacts) == 147
    assert all(float(row["distance_A"]) <= 4.0 for row in atom_contacts)
    assert all(row["target_kind"] == "polymer" and row["target_entity"] == "1" for row in atom_contacts)
    residue_contacts = rows(generated / "contact-residues-4A.tsv")
    assert len(residue_contacts) == 38
    assert all(row["canonical_position"] for row in residue_contacts)
    context = rows(generated / "pocket-sequence-context.tsv")
    assert context and all(row["modeled"] == "True" for row in context)
    assert all(row["expected_standard_heavy_atom_count"] == row["observed_heavy_atom_count"] for row in context)
    assert all(
        row["missing_expected_heavy_atom_names"] == ""
        and row["official_unobserved_atom_names"] == ""
        and row["zero_occupancy_coordinate_atom_names"] == ""
        and row["partial_occupancy_coordinate_atom_names"] == ""
        for row in context
    )

    occupancy = {row["pdb"]: row for row in rows(generated / "atom-occupancy-summary.tsv")}
    assert occupancy["6VRH"]["atom_site_occupancy_values"] == "1.00"
    assert occupancy["8EF5"]["atom_site_occupancy_values"] == "1.00"
    assert all(row["zero_occupancy_coordinate_count"] == "0" and row["partial_occupancy_coordinate_count"] == "0" for row in occupancy.values())
    assert occupancy["6VRH"]["unobserved_atom_record_count"] == "7"
    assert occupancy["8EF5"]["unobserved_atom_record_count"] == "0"
    assert "A:ASN:145:CG:occupancy_flag=1" in occupancy["6VRH"]["target_unobserved_atom_records"]
    assert "A:LYS:201:NZ:occupancy_flag=1" in occupancy["6VRH"]["target_unobserved_atom_records"]

    components = rows(generated / "component-nearest-distances.tsv")
    assert len(components) == 43
    assert all(
        row["ligand_atom_at_min"] and row["ligand_element_at_min"]
        and row["component_label_asym_at_min"] and row["component_auth_asym_at_min"]
        and row["component_comp_at_min"] and row["component_auth_seq_at_min"]
        and row["component_atom_at_min"] and row["component_element_at_min"]
        and row["component_occupancy_at_min"]
        for row in components
    )

    hetero = rows(generated / "hetero-inventory.tsv")
    assert not any(row["comp"] in {"HOH", "DOD"} for row in hetero)
    assert {(row["pdb"], row["comp"]) for row in hetero} == {
        ("6VRH", "NAG"), ("6VRH", "8PR"), ("6VRH", "CL"), ("6VRH", "LMT"),
        ("8EF5", "7V7"), ("8EF5", "CLR"),
    }
    connections = rows(generated / "struct-connections.tsv")
    assert sum(row["role"] == "N-Glycosylation" for row in connections) == 2

    forbidden_map_suffixes = {".map", ".mrc", ".ccp4", ".map.gz", ".mrc.gz"}
    assert not any(any(path.name.lower().endswith(suffix) for suffix in forbidden_map_suffixes) for path in evidence.rglob("*"))
    print(f"PASS: {len(retrievals)} retrieved payloads verified")
    print("PASS: entity/target mappings, assemblies, ligand/XML identity, contacts, local atom completeness, occupancy, hetero inventory and map exclusion verified")


if __name__ == "__main__":
    main()
