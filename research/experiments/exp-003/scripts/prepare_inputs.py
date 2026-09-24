#!/usr/bin/env python3
"""Verify preserved 6VRH/8PR inputs and create predeclared receptor/ligand inputs."""
from __future__ import annotations

import hashlib
import json
import math
import pathlib
import platform
import subprocess
from collections import Counter

import gemmi
from rdkit import Chem, rdBase
from rdkit.Chem import AllChem, rdMolDescriptors

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
RAW = REPO / "research/alternative-coordinate-evidence/raw"
DERIVED = ROOT / "derived"
INPUTS = ROOT / "inputs"
EXPECTED = {
    "6VRH.cif": "15523af08c4701aa9cce327b41987c121702cedddf1840ceab2558c9c3eb7b61",
    "6VRH-assembly1.cif": "501a2f048936dc4f88521b09c4f9035eafb6ee2a23f3571a0083baaa98181bda",
    "ccd-8PR.cif": "e0c0df63947282ab7ef9f4dc48fc6637d0c8ce32157cb01835f4ece29d64e8c4",
    "rcsb-chemcomp-8PR.json": "868233b46bee7107caf5611e43c8f63facfeeb4e6761397d693e3b80a419a116",
    "rcsb-entry-6VRH.json": "14af22a5d384687a865fe9f7bf23fe0fe22900321dce33ca7eb41363a754013e",
    "wwpdb-6vrh-validation.xml.gz": "77eb5ce87c3c4d426f5e5baa86ff3f11fb46976ec0658ed5388f42dad6d126f7",
}
STATES = {"paroxetine_neutral": 2201, "paroxetine_protonated": 2202}


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bond_type(order: str, aromatic: str):
    if aromatic == "Y":
        return Chem.BondType.AROMATIC
    return {"SING": Chem.BondType.SINGLE, "DOUB": Chem.BondType.DOUBLE,
            "TRIP": Chem.BondType.TRIPLE}[order]


def ccd_graph(block):
    atom_rows = list(block.find([
        "_chem_comp_atom.atom_id", "_chem_comp_atom.type_symbol",
        "_chem_comp_atom.charge", "_chem_comp_atom.pdbx_stereo_config",
        "_chem_comp_atom.pdbx_ordinal",
    ]))
    heavy = sorted((r for r in atom_rows if r[1] != "H"), key=lambda r: int(r[4]))
    rw = Chem.RWMol()
    by_name = {}
    expected_stereo = {}
    for row in heavy:
        atom = Chem.Atom(row[1])
        atom.SetFormalCharge(int(row[2]))
        atom.SetProp("ccd_name", row[0])
        idx = rw.AddAtom(atom)
        by_name[row[0]] = idx
        if row[3] in {"R", "S"}:
            expected_stereo[row[0]] = row[3]
    bond_rows = list(block.find([
        "_chem_comp_bond.atom_id_1", "_chem_comp_bond.atom_id_2",
        "_chem_comp_bond.value_order", "_chem_comp_bond.pdbx_aromatic_flag",
    ]))
    heavy_edges = []
    for row in bond_rows:
        if row[0] not in by_name or row[1] not in by_name:
            continue
        bt = bond_type(row[2], row[3])
        rw.AddBond(by_name[row[0]], by_name[row[1]], bt)
        if bt == Chem.BondType.AROMATIC:
            rw.GetAtomWithIdx(by_name[row[0]]).SetIsAromatic(True)
            rw.GetAtomWithIdx(by_name[row[1]]).SetIsAromatic(True)
        heavy_edges.append((row[0], row[1], row[2], row[3]))
    mol = rw.GetMol()
    Chem.SanitizeMol(mol)
    return mol, heavy, heavy_edges, expected_stereo


def descriptor_smiles(block) -> str:
    rows = block.find([
        "_pdbx_chem_comp_descriptor.type", "_pdbx_chem_comp_descriptor.program",
        "_pdbx_chem_comp_descriptor.descriptor",
    ])
    hits = [gemmi.cif.as_string(r[2]) for r in rows
            if gemmi.cif.as_string(r[0]) == "SMILES_CANONICAL"
            and gemmi.cif.as_string(r[1]) == "CACTVS"]
    if len(hits) != 1:
        raise RuntimeError(f"expected one CACTVS canonical SMILES, got {len(hits)}")
    return hits[0]


def verified_neutral(block):
    ccd, heavy_rows, edges, stereo = ccd_graph(block)
    smiles = descriptor_smiles(block)
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise RuntimeError("could not parse CCD canonical isomeric SMILES")
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    mappings = mol.GetSubstructMatches(ccd, uniquify=False, useChirality=False, maxMatches=10000)
    mappings = [m for m in mappings if len(m) == mol.GetNumAtoms() == ccd.GetNumAtoms()]
    valid = []
    for mapping in mappings:  # query CCD index -> target descriptor index
        observed = {}
        for ccd_idx, descriptor_idx in enumerate(mapping):
            name = ccd.GetAtomWithIdx(ccd_idx).GetProp("ccd_name")
            atom = mol.GetAtomWithIdx(descriptor_idx)
            if name in stereo:
                observed[name] = atom.GetProp("_CIPCode") if atom.HasProp("_CIPCode") else None
        if observed == stereo:
            valid.append(mapping)
    if not valid:
        raise RuntimeError(f"no complete graph map preserves CCD stereochemistry {stereo}")
    mapping = valid[0]
    index_to_name = {}
    for ccd_idx, descriptor_idx in enumerate(mapping):
        name = ccd.GetAtomWithIdx(ccd_idx).GetProp("ccd_name")
        mol.GetAtomWithIdx(descriptor_idx).SetProp("ccd_name", name)
        index_to_name[descriptor_idx] = name
    if rdMolDescriptors.CalcMolFormula(mol) != "C19H20FNO3":
        raise RuntimeError("neutral formula does not match CCD")
    return mol, index_to_name, {
        "canonical_isomeric_smiles_from_ccd": smiles,
        "rdkit_canonical_isomeric_smiles": Chem.MolToSmiles(mol, isomericSmiles=True),
        "heavy_atoms": mol.GetNumAtoms(),
        "heavy_heavy_bonds": mol.GetNumBonds(),
        "ccd_named_heavy_atoms": [r[0] for r in heavy_rows],
        "ccd_heavy_edges": edges,
        "graph_isomorphisms": len(mappings),
        "stereochemistry_preserving_name_maps": len(valid),
        "configured_atoms": stereo,
        "mapped_configured_atoms": stereo,
        "formula": rdMolDescriptors.CalcMolFormula(mol),
    }


def make_state(neutral, name: str, seed: int):
    mol = Chem.Mol(neutral)
    if name.endswith("protonated"):
        nitrogens = [a for a in mol.GetAtoms() if a.GetSymbol() == "N"]
        if len(nitrogens) != 1:
            raise RuntimeError("expected one paroxetine nitrogen")
        n = nitrogens[0]
        n.SetFormalCharge(1)
        n.SetNumExplicitHs(2)
        n.SetNoImplicit(True)
        Chem.SanitizeMol(mol)
    mol.RemoveAllConformers()
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    params.useRandomCoords = True
    params.numThreads = 1
    status = AllChem.EmbedMolecule(mol, params)
    if status != 0:
        raise RuntimeError(f"ETKDG failed for {name}: {status}")
    if not AllChem.MMFFHasAllMoleculeParams(mol):
        raise RuntimeError(f"MMFF94 not parameterized for {name}")
    optimization = AllChem.MMFFOptimizeMolecule(mol, maxIters=1000)
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True, useLegacyImplementation=False)
    mol.SetProp("_Name", name)
    mol.SetProp("source", "RCSB CCD 8PR graph and canonical stereochemistry; all source coordinates discarded")
    mol.SetProp("conformer_method", "RDKit ETKDGv3 useRandomCoords=True, one thread, then MMFF94")
    mol.SetIntProp("conformer_seed", seed)
    writer = Chem.SDWriter(str(DERIVED / f"{name}.sdf"))
    writer.write(mol)
    writer.close()
    heavy = Chem.RemoveHs(mol)
    return {
        "id": name,
        "conformer_seed": seed,
        "embed_status": status,
        "mmff_optimize_status": optimization,
        "formal_charge": Chem.GetFormalCharge(heavy),
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "heavy_atoms": heavy.GetNumAtoms(),
        "stereocenters": centers,
        "canonical_isomeric_smiles": Chem.MolToSmiles(heavy, isomericSmiles=True),
    }


def pdb_atom_line(record, serial, atom, residue, chain="A"):
    alt = atom.altloc if atom.altloc and atom.altloc != "\x00" else " "
    element = atom.element.name.rjust(2)
    icode = residue.seqid.icode if residue.seqid.icode and residue.seqid.icode != "\x00" else " "
    return (f"{record:<6}{serial:5d} {atom.name:<4}{alt:1}{residue.name:>3} {chain:1}"
            f"{residue.seqid.num:4d}{icode:1}   "
            f"{atom.pos.x:8.3f}{atom.pos.y:8.3f}{atom.pos.z:8.3f}"
            f"{atom.occ:6.2f}{atom.b_iso:6.2f}          {element:>2}\n")


def minimum_distance(atoms_a, atoms_b):
    return min(math.dist((a.pos.x, a.pos.y, a.pos.z), (b.pos.x, b.pos.y, b.pos.z))
               for a in atoms_a for b in atoms_b)


def main():
    DERIVED.mkdir(parents=True, exist_ok=True)
    INPUTS.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, expected in EXPECTED.items():
        path = RAW / name
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"source hash mismatch: {name} {actual}")
        manifest.append({"path": str(path.relative_to(REPO)), "bytes": path.stat().st_size,
                         "sha256": actual, "verified": True})
    (INPUTS / "source_manifest.json").write_text(json.dumps({
        "source_package": "research/alternative-coordinate-evidence",
        "retrieval_records": "research/alternative-coordinate-evidence/retrieval",
        "new_network_requests": 0,
        "files": manifest,
    }, indent=2, sort_keys=True) + "\n")

    doc = gemmi.cif.read_file(str(RAW / "ccd-8PR.cif"))
    neutral, index_to_name, graph_check = verified_neutral(doc.sole_block())
    state_records = [make_state(neutral, n, seed) for n, seed in STATES.items()]

    structure = gemmi.read_structure(str(RAW / "6VRH.cif"))
    chain = structure[0]["A"]
    proteins = [r for r in chain if r.het_flag == "A"]
    ligand_res = [r for r in chain if r.name == "8PR" and r.seqid.num == 702]
    if len(ligand_res) != 1:
        raise RuntimeError("expected one auth-A 8PR/702")
    ligand_res = ligand_res[0]
    ligand_atoms = [a for a in ligand_res if a.element.name != "H"]
    by_name = {a.name.strip(): a for a in ligand_atoms}
    if len(by_name) != 24 or set(by_name) != set(index_to_name.values()):
        raise RuntimeError("deposited/CCD ligand atom-name set mismatch")
    for idx, name in index_to_name.items():
        if neutral.GetAtomWithIdx(idx).GetSymbol() != by_name[name].element.name:
            raise RuntimeError(f"element mismatch for {name}")

    receptor_lines = []
    serial = 1
    for residue in proteins:
        for atom in residue:
            if atom.element.name == "H":
                continue
            receptor_lines.append(pdb_atom_line("ATOM", serial, atom, residue))
            serial += 1
    receptor_heavy_atom_count = serial - 1
    receptor_lines.extend([f"TER   {serial:5d}      {proteins[-1].name:>3} A{proteins[-1].seqid.num:4d}\n", "END\n"])
    (DERIVED / "receptor_6vrh_chainA_resolved_protein.pdb").write_text("".join(receptor_lines))

    ref_lines = []
    reference_atoms = []
    for serial, (idx, name) in enumerate(sorted(index_to_name.items()), start=1):
        atom = by_name[name]
        ref_lines.append(pdb_atom_line("HETATM", serial, atom, ligand_res))
        reference_atoms.append({"molecule_atom_index": idx, "ccd_atom_name": name,
                                "element": atom.element.name,
                                "coord_A": [atom.pos.x, atom.pos.y, atom.pos.z]})
    ref_lines.append("END\n")
    (DERIVED / "native_8PR_bound_reference.pdb").write_text("".join(ref_lines))

    xs = [a.pos.x for a in ligand_atoms]; ys = [a.pos.y for a in ligand_atoms]; zs = [a.pos.z for a in ligand_atoms]
    center = [(min(v) + max(v)) / 2 for v in (xs, ys, zs)]
    size = [max(v) - min(v) + 12.0 for v in (xs, ys, zs)]
    expected_center = [135.153, 124.0665, 121.356]
    expected_size = [16.752, 19.255, 21.052]
    if any(abs(a-b) > 1e-6 for a, b in zip(center + size, expected_center + expected_size)):
        raise RuntimeError(f"box differs from preregistration: {center}, {size}")

    het = {}
    for residue in chain:
        if residue.het_flag == "A" or residue is ligand_res:
            continue
        atoms = [a for a in residue if a.element.name != "H"]
        het[f"{residue.name}:{residue.seqid.num}"] = {
            "heavy_atoms": len(atoms), "minimum_distance_to_8PR_A": round(minimum_distance(atoms, ligand_atoms), 3)}
    histidine_distances = {}
    for residue in proteins:
        if residue.name == "HIS":
            histidine_distances[str(residue.seqid.num)] = round(minimum_distance(
                [a for a in residue if a.element.name != "H"], ligand_atoms), 3)

    reference = {
        "entry": "6VRH", "component": "8PR", "auth_chain": "A", "auth_residue": 702,
        "atoms": reference_atoms, "box_center_A": center, "box_size_A": size,
        "evaluation_frame": "unchanged deposited protein frame; no ligand fit or alignment",
    }
    (DERIVED / "native_reference.json").write_text(json.dumps(reference, indent=2, sort_keys=True) + "\n")
    audit = {
        "assembly": "deposited coordinates; assembly 1 has an identical auth-atom coordinate signature",
        "receptor": {"auth_chain": "A", "modeled_residue_range": [77, 617],
                     "protein_residues": len(proteins),
                     "resolved_protein_heavy_atoms_written": receptor_heavy_atom_count,
                     "missing_segments_not_built": [[1, 76], [618, 630]],
                     "incomplete_residues_not_reconstructed": {
                         "ASN145": {"missing_atoms": ["CG", "OD1", "ND2"],
                                    "nearest_retained_atom_to_8PR_A": 15.656,
                                    "preparation_action": "whole unresolved residue explicitly omitted"},
                         "LYS201": {"missing_atoms": ["CG", "CD", "CE", "NZ"],
                                    "nearest_retained_atom_to_8PR_A": 36.647,
                                    "preparation_action": "whole unresolved residue explicitly omitted"}},
                     "reported_mutations": 0,
                     "histidine_assignment": "HIE for residues 143,223,235,240,456",
                     "histidine_minimum_distances_to_8PR_A": histidine_distances,
                     "charge_model": "Meeko 0.8.0 standard templates and Gasteiger"},
        "removed_components": het,
        "modeled_waters": 0, "modeled_sodium_ions": 0,
        "ligand": {"heavy_atoms": len(ligand_atoms),
                   "occupancy_min_max": [min(a.occ for a in ligand_atoms), max(a.occ for a in ligand_atoms)],
                   "alternate_locations": sorted({a.altloc for a in ligand_atoms if a.altloc and a.altloc != "\x00"})},
        "box": {"definition": "8PR deposited heavy-atom bounds plus 6.0 A each face",
                "center_A": center, "size_A": size},
        "maps_inspected": False,
    }
    (DERIVED / "preparation_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    (DERIVED / "ligand_graph_and_conformers.json").write_text(json.dumps({
        "rdkit_version": rdBase.rdkitVersion,
        "graph_check": graph_check,
        "atom_index_to_ccd_name": index_to_name,
        "states": state_records,
        "source_coordinate_use": "none; CCD model/ideal and deposited 8PR coordinates excluded from conformer generation",
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"sources_verified": len(manifest), "states_prepared": len(state_records),
                      "receptor_heavy_atoms": receptor_heavy_atom_count, "box_center_A": center,
                      "box_size_A": size}, sort_keys=True))


if __name__ == "__main__":
    main()
