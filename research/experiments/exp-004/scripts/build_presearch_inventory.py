#!/usr/bin/env python3
"""Freeze hashes of every input before the first search."""
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
FILES = [
    "protocol-prerun.md", "environment.txt", "inputs/source_manifest.json",
    "derived/identity_graph_and_conformers.json", "derived/presearch_validation.json",
    "derived/prl_neutral_c1.sdf", "derived/prl_neutral_c2.sdf",
    "derived/prl_protonated_c1.sdf", "derived/prl_protonated_c2.sdf",
    "derived/pdbqt/prl_neutral_c1.pdbqt", "derived/pdbqt/prl_neutral_c2.pdbqt",
    "derived/pdbqt/prl_protonated_c1.pdbqt", "derived/pdbqt/prl_protonated_c2.pdbqt",
    "tables/presearch_ligand_checks.csv",
]
EXTERNAL = [
    "research/experiments/exp-003/derived/receptor_6vrh_primary.pdbqt",
    "research/experiments/exp-003/derived/receptor_6vrh_primary_prepared.pdb",
    "research/experiments/exp-003/derived/vina_box.txt",
]

def record(path, label):
    data = path.read_bytes()
    return {"path": label, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

items = [record(ROOT / rel, rel) for rel in FILES]
external = [record(REPO / rel, rel) for rel in EXTERNAL]
out = {"status": "frozen before any Vina search", "search_outputs_present_when_built": False,
       "prepared_inputs": items, "reused_exp003_inputs": external,
       "fixed_search_matrix": {name: [5301, 5302, 5303] for name in
         ["prl_neutral_c1", "prl_neutral_c2", "prl_protonated_c1", "prl_protonated_c2"]},
       "search_count": 12}
(ROOT / "inputs/presearch_inventory.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(f"prepared_inputs={len(items)} reused_inputs={len(external)} searches=12")
