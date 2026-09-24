#!/usr/bin/env python3
"""Verify retained identity/model bytes and build four predeclared PRL conformers."""
from __future__ import annotations

import hashlib
import json
import math
import pathlib
from collections import Counter

import numpy as np
from rdkit import Chem, rdBase
from rdkit.Chem import AllChem, rdMolAlign, rdMolDescriptors

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
DERIVED = ROOT / "derived"
INPUTS = ROOT / "inputs"
EXPECTED = {
    "research/identity-and-evidence.md": "5c712d8f8d28dacbf6414806dafe58009f91b2d0e80574e445bf3b7c424b3493",
    "research/alternative-target-audit.md": "915378dd041d522280a8459983a034c5f3313ba12fd5aea09805693d6704b58f",
    "research/alternative-target-evidence/source-ligand-trace.json": "186979ce1c5d0ab11a54bbdb68d17d12658ca61797edc9a2909e058f7e0e0dee",
    "research/experiments/exp-003/derived/receptor_6vrh_primary.pdbqt": "01ec06e6bfb7708c389bcfc884c929547114b4a9318f8a1f6861c43ab793a5cc",
    "research/experiments/exp-003/derived/receptor_6vrh_primary_prepared.pdb": "de88b8085a444a92a9453d5b57908361c4c858db2834cdce3c7a564d366bf866",
    "research/experiments/exp-003/derived/vina_box.txt": "51039da260ded8df703a54880e09dd2707174408fc6ce29cbaffe6a9e01a53c7",
    "research/experiments/exp-003/derived/native_reference.json": "c7b58a8f5337d64869a1e692ce040683e1ca224031891a5d7a560a9dbab0ef1f",
    "research/experiments/exp-003/derived/results_summary.json": "f206f28683f32ae8b5784816f8f2b10133519fd842300ff3a8d688078dba14c8",
    "research/experiments/exp-003/derived/ligand_graph_and_conformers.json": "fa247811271a5c2b28badd5807005803f6e096e024ff61e9f406f768b422fa25",
    "research/experiments/exp-003/protocol-prerun.md": "7ca90b62215e78bca37fe44e61832d121e6713103fe7b041008d6820ac5e624f",
    "research/experiments/exp-003/results.md": "e35f4d9b8840c89285ea795135e6c94864043ab4d8ca9faefaf3ee4f20af2864",
}
NEUTRAL_REPRESENTATIONS = {
    "task_reference": "CN(CCc1cccc(c1)C(=O)OC)Cc2ccccc2",
    "retained_pubchem_connectivity": "CN(CCC1=CC(=CC=C1)C(=O)OC)CC2=CC=CC=C2",
    "canonical_prediction_query": "COC(=O)c1cccc(c1)CCN(Cc1ccccc1)C",
}
PROTONATED_REPRESENTATIONS = {
    "task_reference": "C[NH+](CCc1cccc(c1)C(=O)OC)Cc2ccccc2",
    "retained_pubchem_ion_pair_moiety_without_chloride": "C[NH+](CCC1=CC(=CC=C1)C(=O)OC)CC2=CC=CC=C2",
}
CONFORMERS = {
    "prl_neutral_c1": ("neutral", 5101),
    "prl_neutral_c2": ("neutral", 5104),
    "prl_protonated_c1": ("protonated", 5201),
    "prl_protonated_c2": ("protonated", 5202),
}


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bond_label(bond: Chem.Bond) -> str:
    if bond.GetIsAromatic():
        return "AROMATIC"
    return {Chem.BondType.SINGLE: "SINGLE", Chem.BondType.DOUBLE: "DOUBLE",
            Chem.BondType.TRIPLE: "TRIPLE"}[bond.GetBondType()]


def complete_maps(query: Chem.Mol, target: Chem.Mol):
    maps = target.GetSubstructMatches(query, uniquify=False, useChirality=False, maxMatches=10000)
    return [m for m in maps if len(m) == query.GetNumAtoms() == target.GetNumAtoms()]


def graph_record(mol: Chem.Mol):
    atoms = [{"index": a.GetIdx(), "element": a.GetSymbol(), "formal_charge": a.GetFormalCharge(),
              "aromatic": a.GetIsAromatic()} for a in mol.GetAtoms()]
    bonds = [{"atom1": min(b.GetBeginAtomIdx(), b.GetEndAtomIdx()),
              "atom2": max(b.GetBeginAtomIdx(), b.GetEndAtomIdx()),
              "order": bond_label(b)} for b in mol.GetBonds()]
    bonds.sort(key=lambda x: (x["atom1"], x["atom2"]))
    return {"atoms": atoms, "bonds": bonds, "heavy_atoms": mol.GetNumAtoms(),
            "heavy_heavy_bonds": mol.GetNumBonds(), "formal_charge": Chem.GetFormalCharge(mol),
            "formula": rdMolDescriptors.CalcMolFormula(mol),
            "canonical_isomeric_smiles": Chem.MolToSmiles(mol, isomericSmiles=True)}


def n_substituent_indices(mol_h: Chem.Mol):
    n_atoms = [a for a in mol_h.GetAtoms() if a.GetSymbol() == "N"]
    if len(n_atoms) != 1:
        raise RuntimeError("expected one nitrogen")
    n = n_atoms[0]; found = {"nitrogen": n.GetIdx()}
    for atom in n.GetNeighbors():
        if atom.GetSymbol() == "H":
            found["hydrogen"] = atom.GetIdx(); continue
        h_count = sum(x.GetSymbol() == "H" for x in atom.GetNeighbors())
        if h_count == 3:
            found["methyl"] = atom.GetIdx(); continue
        other = [x for x in atom.GetNeighbors() if x.GetIdx() != n.GetIdx() and x.GetSymbol() != "H"]
        if len(other) != 1:
            raise RuntimeError("ambiguous nitrogen substituent")
        found["benzyl" if other[0].GetIsAromatic() else "phenethyl"] = atom.GetIdx()
    required = {"nitrogen", "methyl", "benzyl", "phenethyl"}
    if not required <= set(found):
        raise RuntimeError(f"could not classify nitrogen substituents: {found}")
    return found


def n_geometry(mol_h: Chem.Mol):
    idx = n_substituent_indices(mol_h); conf = mol_h.GetConformer()
    xyz = lambda i: np.array(conf.GetAtomPosition(i), dtype=float)
    n = xyz(idx["nitrogen"])
    vectors = [xyz(idx[x]) - n for x in ("methyl", "benzyl", "phenethyl")]
    signed = float(np.linalg.det(np.stack(vectors)))
    lengths = {x: float(np.linalg.norm(xyz(idx[x]) - n)) for x in ("methyl", "benzyl", "phenethyl")}
    # Sum of the three C-N-C angles describes pyramidalization without assigning stable stereochemistry.
    angles = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        cosine = np.dot(vectors[i], vectors[j]) / (np.linalg.norm(vectors[i]) * np.linalg.norm(vectors[j]))
        angles.append(math.degrees(math.acos(float(np.clip(cosine, -1, 1)))))
    result = {"ordered_substituents": ["methyl", "benzyl", "phenethyl"],
              "signed_heavy_neighbor_determinant_A3": signed,
              "sign": 1 if signed > 0 else -1,
              "carbon_nitrogen_bond_lengths_A": lengths,
              "carbon_nitrogen_carbon_angles_deg": angles,
              "sum_CNC_angles_deg": sum(angles)}
    if "hydrogen" in idx:
        h = xyz(idx["hydrogen"])
        tetra = [xyz(idx[x]) - h for x in ("methyl", "benzyl", "phenethyl")]
        result["signed_tetrahedral_determinant_H_origin_A3"] = float(np.linalg.det(np.stack(tetra)))
        result["nitrogen_hydrogen_bond_length_A"] = float(np.linalg.norm(h - n))
    return result


def make_conformer(name: str, state: str, seed: int, graph: Chem.Mol):
    mol = Chem.AddHs(Chem.Mol(graph))
    params = AllChem.ETKDGv3(); params.randomSeed = seed; params.useRandomCoords = True; params.numThreads = 1
    embed = AllChem.EmbedMolecule(mol, params)
    if embed != 0:
        raise RuntimeError(f"ETKDG failed for {name}: {embed}")
    if not AllChem.MMFFHasAllMoleculeParams(mol):
        raise RuntimeError(f"MMFF94 parameters missing for {name}")
    optimize = AllChem.MMFFOptimizeMolecule(mol, maxIters=2000)
    mol.SetProp("_Name", name); mol.SetProp("modeled_state", state)
    mol.SetProp("source", "verified PRL-8-53 graph; no paroxetine or receptor coordinates")
    mol.SetProp("conformer_method", "RDKit ETKDGv3 useRandomCoords=True one thread; MMFF94 maxIters=2000")
    mol.SetIntProp("conformer_seed", seed)
    writer = Chem.SDWriter(str(DERIVED / f"{name}.sdf")); writer.write(mol); writer.close()
    return mol, {"id": name, "state": state, "conformer_seed": seed, "embed_status": embed,
                 "mmff_optimize_status": optimize, "formal_charge": Chem.GetFormalCharge(mol),
                 "formula": rdMolDescriptors.CalcMolFormula(mol), "heavy_atoms": Chem.RemoveHs(mol).GetNumAtoms(),
                 "nitrogen_geometry": n_geometry(mol)}


def main():
    DERIVED.mkdir(parents=True, exist_ok=True); INPUTS.mkdir(parents=True, exist_ok=True)
    sources = []
    for rel, expected in EXPECTED.items():
        path = REPO / rel; actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"source hash mismatch: {rel}: {actual}")
        sources.append({"path": rel, "bytes": path.stat().st_size, "sha256": actual, "verified": True})
    (INPUTS / "source_manifest.json").write_text(json.dumps({
        "baseline_commit": "e38554e47e232224ec1b9321bb80a98aaafb65b2",
        "new_network_requests": 0, "files": sources,
        "runtime_is_external_equivalent_requirement": True,
    }, indent=2, sort_keys=True) + "\n")

    neutral = {k: Chem.MolFromSmiles(v) for k, v in NEUTRAL_REPRESENTATIONS.items()}
    protonated = {k: Chem.MolFromSmiles(v) for k, v in PROTONATED_REPRESENTATIONS.items()}
    if any(m is None for m in [*neutral.values(), *protonated.values()]):
        raise RuntimeError("a retained representation did not parse")
    neutral_ref = neutral["task_reference"]; protonated_ref = protonated["task_reference"]
    for label, mol in neutral.items():
        if not complete_maps(neutral_ref, mol):
            raise RuntimeError(f"neutral full-graph mismatch: {label}")
    for label, mol in protonated.items():
        if not complete_maps(protonated_ref, mol):
            raise RuntimeError(f"protonated full-graph mismatch: {label}")
    if not complete_maps(Chem.Mol(neutral_ref), Chem.Mol(protonated_ref)):
        # Formal charges differ, so RDKit query matching may reject; compare after charge neutralization below.
        pass
    n0 = [a for a in neutral_ref.GetAtoms() if a.GetSymbol() == "N"][0]
    n1 = [a for a in protonated_ref.GetAtoms() if a.GetSymbol() == "N"][0]
    if (Chem.GetFormalCharge(neutral_ref), Chem.GetFormalCharge(protonated_ref)) != (0, 1):
        raise RuntimeError("unexpected state charges")
    # Explicitly verify the only heavy-graph atom-property change is N formal charge.
    protonated_copy = Chem.RWMol(protonated_ref); protonated_copy.GetAtomWithIdx(n1.GetIdx()).SetFormalCharge(0)
    protonated_copy.GetAtomWithIdx(n1.GetIdx()).SetNumExplicitHs(0); protonated_copy.GetAtomWithIdx(n1.GetIdx()).SetNoImplicit(False)
    neutralized = protonated_copy.GetMol(); Chem.SanitizeMol(neutralized)
    if not complete_maps(neutral_ref, neutralized):
        raise RuntimeError("neutral/protonated heavy connectivity differs beyond N protonation")

    molecules = {}; records = []
    for name, (state, seed) in CONFORMERS.items():
        graph = neutral_ref if state == "neutral" else protonated_ref
        molecules[name], record = make_conformer(name, state, seed, graph); records.append(record)
    comparisons = []
    for state in ("neutral", "protonated"):
        names = [n for n, (s, _) in CONFORMERS.items() if s == state]
        a = Chem.RemoveHs(Chem.Mol(molecules[names[0]])); b = Chem.RemoveHs(Chem.Mol(molecules[names[1]]))
        aligned = rdMolAlign.GetBestRMS(Chem.Mol(b), Chem.Mol(a), maxMatches=10000)
        comparisons.append({"state": state, "conformer1": names[0], "conformer2": names[1],
                            "symmetry_aware_aligned_heavy_atom_RMSD_A": aligned,
                            "geometrically_distinct_observation": aligned > 0.0,
                            "nitrogen_signs": [next(r for r in records if r["id"] == n)["nitrogen_geometry"]["sign"] for n in names]})
    if any(c["nitrogen_signs"] not in ([1, -1], [-1, 1]) for c in comparisons):
        raise RuntimeError(f"predeclared conformers did not cover opposite N signs: {comparisons}")

    audit = {
        "rdkit_version": rdBase.rdkitVersion,
        "identity_check": {
            "neutral_representations": NEUTRAL_REPRESENTATIONS,
            "protonated_representations": PROTONATED_REPRESENTATIONS,
            "neutral_complete_graph_map_counts": {k: len(complete_maps(neutral_ref, m)) for k, m in neutral.items()},
            "protonated_complete_graph_map_counts": {k: len(complete_maps(protonated_ref, m)) for k, m in protonated.items()},
            "neutral_graph": graph_record(neutral_ref), "protonated_graph": graph_record(protonated_ref),
            "neutral_nitrogen_index": n0.GetIdx(), "protonated_nitrogen_index": n1.GetIdx(),
            "chloride_docked": False,
            "stereochemistry": "no carbon stereocenters specified; nitrogen coordinate signs are explicit modeling assumptions, not permanent experimental enantiomers",
        },
        "conformers": records, "within_state_comparisons": comparisons,
        "coordinate_template_use": "none; no receptor, paroxetine, deposited-ligand or other ligand coordinates used",
    }
    (DERIVED / "identity_graph_and_conformers.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"sources_verified": len(sources), "conformers": len(records),
                      "neutral_heavy_atoms": neutral_ref.GetNumAtoms(), "neutral_bonds": neutral_ref.GetNumBonds(),
                      "within_state_comparisons": comparisons}, sort_keys=True))

if __name__ == "__main__":
    main()
