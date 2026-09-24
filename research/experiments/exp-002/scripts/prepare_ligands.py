#!/usr/bin/env python3
"""Generate independent, seeded 3D ligand conformers and record graph properties."""
from __future__ import annotations

import csv
import json
import pathlib

from rdkit import Chem, rdBase
from rdkit.Chem import AllChem, Crippen, Descriptors, Lipinski

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "inputs" / "raw"
DERIVED = ROOT / "derived" / "ligands"
TABLES = ROOT / "tables"
PRL = {
    "prl_neutral": "CN(CCc1cccc(c1)C(=O)OC)Cc2ccccc2",
    "prl_protonated": "C[NH+](CCc1cccc(c1)C(=O)OC)Cc2ccccc2",
}
SEEDS = {
    "native_0EU": 1701,
    "prl_neutral": 1801,
    "prl_protonated": 1802,
    "diphenhydramine_neutral": 1901,
    "diphenhydramine_protonated": 1902,
    "procaine_protonated": 1903,
    "benzyl_phenylacetate": 1904,
}


def independent_conformer(mol: Chem.Mol, seed: int) -> tuple[Chem.Mol, int]:
    mol = Chem.RemoveHs(mol)
    mol.RemoveAllConformers()  # explicitly discard source/2D coordinates
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    params.useRandomCoords = True
    params.numThreads = 1
    result = AllChem.EmbedMolecule(mol, params)
    if result != 0:
        raise RuntimeError(f"ETKDG failed with status {result}")
    if AllChem.MMFFHasAllMoleculeParams(mol):
        optimization = AllChem.MMFFOptimizeMolecule(mol, maxIters=1000)
    else:
        optimization = AllChem.UFFOptimizeMolecule(mol, maxIters=1000)
    return mol, optimization


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(exist_ok=True)
    records = []

    native_source = next(x for x in Chem.SDMolSupplier(str(RAW / "0EU_ideal.sdf"), removeHs=False) if x)
    molecules = {"native_0EU": (native_source, "RCSB CCD 0EU graph; source coordinates discarded")}
    molecules.update({name: (Chem.MolFromSmiles(smiles), "brief-specified PRL graph") for name, smiles in PRL.items()})
    background = json.loads((ROOT / "inputs" / "background_selection.json").read_text())
    molecules.update({entry["id"]: (Chem.MolFromSmiles(entry["smiles"]), "preselected comparison graph") for entry in background["entries"]})

    for name, (source, provenance) in molecules.items():
        if source is None:
            raise RuntimeError(f"could not parse {name}")
        Chem.AssignStereochemistry(source, cleanIt=True, force=True)
        chiral_before = Chem.FindMolChiralCenters(source, includeUnassigned=True, useLegacyImplementation=False)
        prepared, optimization = independent_conformer(source, SEEDS[name])
        chiral_after = Chem.FindMolChiralCenters(prepared, includeUnassigned=True, useLegacyImplementation=False)
        prepared.SetProp("_Name", name)
        prepared.SetProp("conformer_method", "RDKit ETKDGv3 useRandomCoords=True then MMFF94 (UFF only if MMFF unavailable)")
        prepared.SetIntProp("random_seed", SEEDS[name])
        prepared.SetProp("source", provenance)
        writer = Chem.SDWriter(str(DERIVED / f"{name}.sdf"))
        writer.write(prepared)
        writer.close()
        no_h = Chem.RemoveHs(prepared)
        records.append({
            "id": name,
            "input_provenance": provenance,
            "canonical_isomeric_smiles": Chem.MolToSmiles(no_h, isomericSmiles=True),
            "formal_charge": Chem.GetFormalCharge(no_h),
            "heavy_atoms": no_h.GetNumHeavyAtoms(),
            "molecular_weight": round(Descriptors.MolWt(no_h), 3),
            "cLogP_RDKIT_Crippen": round(Crippen.MolLogP(no_h), 3),
            "rotatable_bonds_RDKIT": Lipinski.NumRotatableBonds(no_h),
            "H_bond_donors": Lipinski.NumHDonors(no_h),
            "H_bond_acceptors": Lipinski.NumHAcceptors(no_h),
            "chiral_centers_before": repr(chiral_before),
            "chiral_centers_after": repr(chiral_after),
            "seed": SEEDS[name],
            "optimizer_status": optimization,
        })
    with (TABLES / "ligand_properties.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    (DERIVED / "ligand_preparation.json").write_text(json.dumps({
        "rdkit_version": rdBase.rdkitVersion,
        "hydrogens": "explicit hydrogens added by RDKit after parsing each formal-charge graph",
        "conformer_generation": "All source conformers removed; one independent ETKDGv3 conformer generated with useRandomCoords=True and one thread, then MMFF94 optimized where parameterized",
        "charges_for_docking": "assigned later by Meeko Gasteiger model; formal molecular charge is checked here and after PDBQT conversion",
        "records": records,
    }, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
