# Pre-run protocol: 6VRH/paroxetine native-reference pilot

**Frozen before any docking search:** initially written 2026-09-23T05:08:04Z and amended after receptor-preparation preflight at 2026-09-23T05:18:36Z, at repository commit `5826daebcd5189105a9e39c7e42da4bd40e807fe`. No docking search for exp-003 had been run at either time. The deposited ligand coordinates may define the fixed box and held-out evaluation reference, but never a starting conformer.

The first Meeko preflight stopped as intended: the original generic rule would not remove an unmatched residue within 12 A of a box face. Its stdout/stderr are preserved as `logs/prepare_docking_inputs.*.txt`. Inspection then established that the only unmatched residues are the two already known incomplete residues: retained atoms of Asn145 and Lys201 are respectively 15.656 and 36.647 A from deposited 8PR. Before any search, the final preparation below replaced that arbitrary box-face rule with explicit omission of exactly these measured, unresolved residues. This amendment is driven by input tractability, not a docking answer.

## Question and stopping rule

This pilot asks whether one fixed, deliberately small 6VRH SERT preparation can recover the deposited paroxetine geometry under two explicit ligand charge assumptions. It is a setup-geometry check only. It cannot establish that PRL-8-53 binds SERT, estimate affinity or free energy, validate a target prediction, or determine pharmacology. **Only native paroxetine will be searched.** PRL-8-53, background ligands, other proteins and prediction services are out of scope.

Run exactly three fixed seeds for each of two paroxetine states, six searches total, sequentially. Preserve every returned mode and every failure. Do not change the receptor, box, search parameters, state definitions or seeds after results. No numerical biological or RMSD pass threshold is declared. Report rank, unchanged-site-frame graph/symmetry-aware heavy-atom RMSD and contacts for every mode. Stop after these six searches even if recovery is poor or inconsistent; do not tune toward the deposited answer and do not proceed to PRL-8-53 in this experiment.

## Immutable source bytes

No new source request is required. The pilot reuses the official records already preserved under `research/alternative-coordinate-evidence/raw/`; their retrieval transport records are in the adjacent `retrieval/` directory and published manifest. Inputs used or cited here are:

| source | SHA-256 |
|---|---|
| `6VRH.cif` (deposited coordinates; preparation and reference) | `15523af08c4701aa9cce327b41987c121702cedddf1840ceab2558c9c3eb7b61` |
| `6VRH-assembly1.cif` (assembly identity cross-check) | `501a2f048936dc4f88521b09c4f9035eafb6ee2a23f3571a0083baaa98181bda` |
| `ccd-8PR.cif` (full graph, atom names, formal charge and stereochemistry) | `e0c0df63947282ab7ef9f4dc48fc6637d0c8ce32157cb01835f4ece29d64e8c4` |
| `rcsb-chemcomp-8PR.json` (independent CCD API record) | `868233b46bee7107caf5611e43c8f63facfeeb4e6761397d693e3b80a419a116` |
| `rcsb-entry-6VRH.json` (entry metadata) | `14af22a5d384687a865fe9f7bf23fe0fe22900321dce33ca7eb41363a754013e` |
| `wwpdb-6vrh-validation.xml.gz` (official validation summary; no map) | `77eb5ce87c3c4d426f5e5baa86ff3f11fb46976ec0658ed5388f42dad6d126f7` |

The deposited and assembly-1 files were already shown to have identical 6,142-atom auth-coordinate signatures. Maps remain uninspected.

## Ligand graph, stereochemistry and states

The CCD record is the authority for the 8PR heavy-atom graph: 24 heavy atoms (C19 F N O3), 27 heavy-heavy bonds, neutral formal charge, and configured atoms `CAW:S` and `CAX:R`. The preparation script must reconstruct the complete molecule from the CCD CACTVS canonical isomeric SMILES, independently parse the CCD atom/bond tables, and require a full heavy-atom graph isomorphism. Through that verified map it must require CAW/CAX to resolve as S/R. It must also verify formula, all named heavy atoms, all heavy-heavy edges/bond types, and the InChIKey recorded by the CCD. Atom order or matching labels alone are not accepted.

Two states are predeclared because the neutral CCD representation does not establish physiological protonation:

1. `paroxetine_neutral`: the exact CCD-neutral graph (formal charge 0; secondary amine N-H).
2. `paroxetine_protonated`: the same heavy-atom graph with the piperidine nitrogen protonated (formal charge +1; N-H2+). Heavy-atom stereochemistry remains CAW:S/CAX:R.

This is a narrow charge sensitivity, not a claim about populations or a compound-specific pKa. For each state, remove every source conformer, add hydrogens according to that state, generate one independent RDKit ETKDGv3 conformer with `useRandomCoords=True`, one thread and seed 2201 (neutral) or 2202 (protonated), then MMFF94-optimize it. No deposited or CCD model/ideal coordinate enters either conformer. Meeko will assign Gasteiger partial charges when converting each fixed conformer to PDBQT; formal molecular charge and the PDBQT charge sum must be checked.

## One receptor preparation (no alternative)

The sole preparation is rigid resolved SERT chain auth A from deposited 6VRH in its unchanged coordinate frame.

- Retain every resolved standard-protein heavy atom that Meeko can template. Use Meeko 0.8.0 standard residue templates and Gasteiger charges. Standard acidic/basic templates therefore supply their usual charged forms. Assign all five histidines HIE; the nearest histidine is 20.706 A from 8PR, so this uncalculated tautomer choice is not a direct pocket-contact assignment. No pKa calculation is claimed.
- Keep the experimentally modeled sequence as-is: residues 77 to 617. Do not build missing termini 1 to 76 or 618 to 630, restore mutations (none are reported), or graft atoms/ions from another structure.
- Asn145 lacks CG/OD1/ND2 and Lys201 lacks CG/CD/CE/NZ in the deposit. Their nearest retained atoms are 15.656 and 36.647 A from 8PR, respectively; neither belongs to the audited 4 A contact set or its complete ±2-residue context. Explicitly omit exactly these two incomplete residues (`--delete_residues A:145,201`) rather than invent side-chain coordinates or let software delete an unspecified residue. This creates two local sequence gaps and remains a model limitation.
- Remove Fab chains B/C. Their nearest resolved ligand distances are 30.849/29.792 A and they make no resolved 4 A pocket contact. This is a receptor-model operation, not evidence that Fab or unresolved segments have no conformational influence.
- Remove both covalent NAGs (nearest 34.755 and 48.394 A), chloride (9.103 A) and LMT detergent (8.731 A). NAG and Fab are remote from this local box; LMT is a purification detergent outside the observed pocket. Chloride is potentially functionally relevant, so removing it is an important electrostatic limitation, not a universal stripping rule. Retaining a single chloride while both sodium sites and all waters are unmodeled would not restore a native ion environment. No sodium or water appears in 6VRH, and none will be grafted. There is no alternative preparation in this pilot.
- Rigid-receptor coordinates and all retained protein heavy-atom positions must remain unchanged. Added hydrogens and charge assignment are modeling operations.

The site is the deposited 8PR heavy-atom bounding box plus 6.0 A on each face: center `(135.153, 124.0665, 121.356)` A and size `(16.752, 19.255, 21.052)` A. It is fixed for all six runs.

## Search matrix and fixed settings

| state | conformer seed | docking seeds |
|---|---:|---|
| neutral | 2201 | 2301, 2302, 2303 |
| protonated | 2202 | 2401, 2402, 2403 |

AutoDock Vina 1.2.7: rigid receptor, `--cpu 2`, `--exhaustiveness 8`, `--num_modes 20`, `--energy_range 5`, and the fixed box above. Runs are sequential. These are bounded sampling settings, not statistical calibration. Vina scores are empirical model scores, not measured affinities or free energies.

## Evaluation fixed before results

Use the deposited auth-A 8PR heavy atoms as the reference in the unchanged protein frame. Establish CCD-name/element-to-coordinate mapping explicitly. For each pose, require the expected formal charge and a stereochemistry-preserving complete heavy-atom graph match. Calculate RMSD with no protein or ligand fitting: minimize direct coordinate RMSD over all heavy-atom graph automorphisms that preserve the specified stereochemistry. Report all modes, score rank, score, automorphism count, and protein-residue contact overlap at the previously descriptive 4.0 A cutoff. That cutoff is an inventory device, not a biological pass gate.

## Software and resource controls

Host is the local arm64 Mac (`Darwin 27.0.0`, 18 logical CPUs, 25,769,803,776 physical bytes). Reuse the existing project-local exp-002 environment; do not install globally or download another tool. Exact pre-run provenance:

- Python 3.13.15; RDKit 2026.03.6; gemmi 0.7.5; Meeko 0.8.0; NumPy 2.5.3; SciPy 1.18.1.
- Vina official macOS arm64 1.2.7 binary SHA-256 `823c2bbacf26d72183861322345f0a89736aca66c8e81054c66f93af5ad623f1`.
- Runtime currently resides at `<repo>/research/experiments/exp-002/`; this path is provenance, not an experiment input. Reproduction may point `EXP003_RUNTIME` at an equivalent environment with the exact versions/binary hash.

Every computational subprocess runs under `nice -n 19`. Set Vina `--cpu 2`, `OMP_NUM_THREADS=2`, and numerical-library variables `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `VECLIB_MAXIMUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`. Preparation/analysis uses `OMP_NUM_THREADS=1` as well. A wrapper monitors only its own child process tree via `ps` every 0.1 seconds, records observed RSS/nice values, and terminates the tree if aggregate RSS reaches 3 GiB or elapsed time reaches 20 minutes. This leaves headroom below the 4 GB calculation allocation. Runs are strictly serial.

macOS reports shell virtual-memory limits as unlimited, so no hard 4 GB enforcement is claimed. The 3 GiB stop is a sampled stop control, not a kernel memory limit; short peaks between samples and project-wide aggregate memory remain unmeasured. Any resource-control failure, nonzero run, incomplete modes or preparation ambiguity is preserved and reported, not replaced by another host or setup.
