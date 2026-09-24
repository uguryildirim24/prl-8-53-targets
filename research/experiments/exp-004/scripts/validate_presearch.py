#!/usr/bin/env python3
"""Inspect prepared ligand graph, coordinates, charges and N geometry before searches."""
from __future__ import annotations
import csv
import json
import pathlib

import numpy as np
from rdkit import Chem

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIGANDS = ["prl_neutral_c1", "prl_neutral_c2", "prl_protonated_c1", "prl_protonated_c2"]


def parse_pdbqt(path):
    text = path.read_text(); smiles = None; atoms = []
    for line in text.splitlines():
        if line.startswith("REMARK SMILES ") and not line.startswith("REMARK SMILES IDX"):
            smiles = line.split(None, 2)[2]
        if line.startswith(("ATOM", "HETATM")):
            atoms.append({"serial": int(line[6:11]), "element": line[12:16].strip()[0],
                          "coord": np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])]),
                          "charge": float(line.split()[-2])})
    if smiles is None or not atoms:
        raise RuntimeError(f"could not parse {path}")
    return text, smiles, atoms


def full_maps(query, target):
    hits = target.GetSubstructMatches(query, uniquify=False, useChirality=False, maxMatches=10000)
    return [m for m in hits if len(m) == query.GetNumAtoms() == target.GetNumAtoms()]


def classify_n(mol):
    n = [a for a in mol.GetAtoms() if a.GetSymbol() == "N"][0]; out = {"nitrogen": n.GetIdx()}
    for atom in n.GetNeighbors():
        if atom.GetSymbol() == "H": out["hydrogen"] = atom.GetIdx(); continue
        h_count = sum(x.GetSymbol() == "H" for x in atom.GetNeighbors())
        if h_count == 3: out["methyl"] = atom.GetIdx(); continue
        other = [x for x in atom.GetNeighbors() if x.GetIdx() != n.GetIdx() and x.GetSymbol() != "H"]
        out["benzyl" if other[0].GetIsAromatic() else "phenethyl"] = atom.GetIdx()
    return out


def main():
    audit = json.loads((ROOT / "derived/identity_graph_and_conformers.json").read_text())
    expected_by_name = {r["id"]: r for r in audit["conformers"]}
    rows = []; details = []
    for name in LIGANDS:
        sdf = next(m for m in Chem.SDMolSupplier(str(ROOT / f"derived/{name}.sdf"), removeHs=False) if m)
        text, smiles, p_atoms = parse_pdbqt(ROOT / f"derived/pdbqt/{name}.pdbqt")
        pdb_graph = Chem.MolFromSmiles(smiles)
        heavy = Chem.RemoveHs(sdf)
        maps = full_maps(heavy, pdb_graph)
        if not maps:
            raise RuntimeError(f"PDBQT REMARK graph mismatch for {name}: {smiles}")
        conf = sdf.GetConformer(); source_to_pdb = {}; max_delta = 0.0
        for atom in sdf.GetAtoms():
            if atom.GetSymbol() == "H" and atom.GetIdx() not in classify_n(sdf).values():
                continue
            source = np.array(conf.GetAtomPosition(atom.GetIdx()), dtype=float)
            candidates = [(float(np.linalg.norm(source - p["coord"])), j) for j, p in enumerate(p_atoms)
                          if p["element"] == atom.GetSymbol() and j not in source_to_pdb.values()]
            if not candidates:
                if atom.GetSymbol() == "H": continue
                raise RuntimeError(f"no PDBQT coordinate candidate for {name} atom {atom.GetIdx()}")
            delta, j = min(candidates)
            if atom.GetSymbol() == "H" and delta > 0.002:
                continue
            source_to_pdb[atom.GetIdx()] = j; max_delta = max(max_delta, delta)
        heavy_indices = {a.GetIdx() for a in sdf.GetAtoms() if a.GetSymbol() != "H"}
        if not heavy_indices <= set(source_to_pdb) or max_delta > 0.001:
            raise RuntimeError(f"source/PDBQT coordinate mismatch for {name}: {max_delta}")
        idx = classify_n(sdf)
        n = p_atoms[source_to_pdb[idx["nitrogen"]]]["coord"]
        vectors = [p_atoms[source_to_pdb[idx[x]]]["coord"] - n for x in ("methyl", "benzyl", "phenethyl")]
        determinant = float(np.linalg.det(np.stack(vectors))); sign = 1 if determinant > 0 else -1
        expected = expected_by_name[name]
        if sign != expected["nitrogen_geometry"]["sign"]:
            raise RuntimeError(f"nitrogen sign changed in PDBQT for {name}")
        charge_sum = sum(a["charge"] for a in p_atoms)
        expected_charge = expected["formal_charge"]
        row = {"ligand": name, "state": expected["state"], "formal_charge": expected_charge,
               "pdbqt_atoms_including_polar_H": len(p_atoms), "gasteiger_charge_sum": round(charge_sum, 4),
               "charge_sum_within_0.01": abs(charge_sum - expected_charge) < 0.01,
               "source_pdbqt_max_coordinate_delta_A": round(max_delta, 6),
               "pdbqt_nitrogen_sign": sign, "pdbqt_nitrogen_determinant_A3": round(determinant, 6),
               "pdbqt_remark_smiles": smiles, "complete_heavy_graph_maps": len(maps)}
        rows.append(row)
        details.append({"ligand": name, "source_to_pdbqt_atom_serial": {
            str(i): p_atoms[j]["serial"] for i, j in sorted(source_to_pdb.items())},
            "graph_and_formal_charge_verified_from_pdbqt_remark": True})
    if not all(r["charge_sum_within_0.01"] for r in rows):
        raise RuntimeError(f"charge check failed: {rows}")
    (ROOT / "tables").mkdir(exist_ok=True)
    with (ROOT / "tables/presearch_ligand_checks.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    result = {"ligands": rows, "coordinate_maps": details,
              "receptor_reused_not_regenerated": "research/experiments/exp-003/derived/receptor_6vrh_primary.pdbqt",
              "receptor_sha256": "01ec06e6bfb7708c389bcfc884c929547114b4a9318f8a1f6861c43ab793a5cc",
              "passed": True}
    (ROOT / "derived/presearch_validation.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"passed": True, "ligands": len(rows), "charge_sums": [r["gasteiger_charge_sum"] for r in rows],
                      "nitrogen_signs": [r["pdbqt_nitrogen_sign"] for r in rows]}, sort_keys=True))

if __name__ == "__main__": main()
