#!/usr/bin/env python3
"""Reproduce the bounded metadata and local-sequence checks used in r4 review."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT / name).read_text())


def sha256(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


json_files = sorted(path.name for path in ROOT.glob("*.json"))
for name in json_files:
    load(name)

# The five withdrawn notes (four `primary-excerpt-*` files and
# `oprm1-human-mouse-alignment.txt`) were removed from this package. Their
# recorded hashes stay in `manifest.md` so the provenance failure is still
# visible; nothing here depends on their contents.

entry_6vrh = load("rcsb-pdb-entry-6VRH.json")
entry_4dkl = load("rcsb-pdb-entry-4DKL.json")
poly_5i6x = load("rcsb-polymer-5I6X-entity-1.json")
poly_6vrh = load("rcsb-polymer-6VRH-entity-1.json")
poly_8ef5 = load("rcsb-polymer-8EF5-entity-1.json")
poly_4dkl = load("rcsb-polymer-4DKL-entity-1.json")

assert entry_6vrh["rcsb_primary_citation"]["pdbx_database_id_DOI"] == "10.7554/eLife.56427"
assert entry_4dkl["rcsb_primary_citation"]["pdbx_database_id_DOI"] == "10.1038/nature10954"

seq_5i6x = poly_5i6x["entity_poly"]["pdbx_seq_one_letter_code_can"]
seq_6vrh = poly_6vrh["entity_poly"]["pdbx_seq_one_letter_code_can"]
# Archived SIFTS mapping: 5I6X entity 3..545 -> P31645 76..618.
substitutions = [
    f"{reference}{position}{deposited}"
    for position, (deposited, reference) in enumerate(
        zip(seq_5i6x[2:545], seq_6vrh[75:618]), start=76
    )
    if deposited != reference
]
assert substitutions == ["Y110A", "I291A", "T439S", "C554A", "C580A"]

seq_human = poly_8ef5["entity_poly"]["pdbx_seq_one_letter_code_can"]
seq_mouse = poly_4dkl["entity_poly"]["pdbx_seq_one_letter_code_can"]
# Archived SIFTS mappings: 8EF5 entity 1 -> P35372 2; 4DKL entity 1 -> P42866 52.
def human_residue(canonical_position):
    return seq_human[canonical_position - 2]


def mouse_residue(canonical_position):
    return seq_mouse[canonical_position - 52]


human_tm3 = "".join(human_residue(i) for i in range(144, 155))
mouse_tm3 = "".join(mouse_residue(i) for i in range(142, 153))
human_tm5 = "".join(human_residue(i) for i in range(230, 241))
mouse_tm5 = "".join(mouse_residue(i) for i in range(228, 239))
assert human_tm3 == mouse_tm3 == "IVISIDYYNMF"
assert human_tm5 == mouse_tm5 == "WENLLKICVFI"
assert human_residue(149) == mouse_residue(147) == "D"
assert human_residue(233) == "L"
assert human_residue(235) == mouse_residue(233) == "K"

for activity_id in ("879137", "1682463"):
    assert "confidence_score" not in load(f"chembl-activity-{activity_id}.json")

print("R4 REVIEWED EVIDENCE CHECK")
print(f"JSON payloads parsed: {len(json_files)}")
print("Withdrawn generated files removed before publication: 5 (hashes recorded in manifest.md)")
print("6VRH citation DOI (RCSB): 10.7554/eLife.56427")
print("4DKL citation DOI (RCSB): 10.1038/nature10954")
print("5I6X mapped deposited-sequence substitutions: " + ", ".join(substitutions))
print("8EF5 SIFTS mapping used: entity 1..367 -> P35372 2..368")
print("4DKL SIFTS mapping used: entity 1..212 -> P42866 52..263")
print(f"TM3 local windows: human 144..154={human_tm3}; mouse 142..152={mouse_tm3}")
print(f"TM5 local windows: human 230..240={human_tm5}; mouse 228..238={mouse_tm5}")
print("Cited local residues: human D149/mouse D147; human L233; human K235/mouse K233")
print("No full-length human/mouse alignment was performed or inferred.")
print("ChEMBL activity payloads 879137 and 1682463 contain no confidence_score field.")
print("PASS")
