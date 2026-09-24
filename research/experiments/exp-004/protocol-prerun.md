# Pre-run protocol: exploratory PRL-8-53 behavior in the reviewed 6VRH model

**Frozen before any docking search.** This experiment starts from reviewed repository commit `e38554e47e232224ec1b9321bb80a98aaafb65b2`. The prepared inputs, graph audit, hashes, fixed search matrix and this protocol will be committed together before Vina is run. Geometry-only conformer preflight did not use the receptor, paroxetine coordinates or Vina scores.

## Question and stopping rule

Does a small predeclared sampling of PRL-8-53 produce reproducible model poses in the **exact** exp-003 paroxetine-centered pocket, and how sensitive are those poses to selected initial geometry and formal-charge assumptions? Run exactly 12 searches: two graph-derived starting conformers for each of two charge states, with the same three docking seeds for every conformer. Preserve all modes and failures. Stop after the fixed matrix; do not tune preparation, box, seeds or settings toward a score or pose.

This is exploratory model behavior. There is no deposited or experimental PRL-8-53 pose. A predicted pose is not binding evidence. The calculation cannot establish that SERT is a biological target, nor affinity, potency, efficacy, selectivity, safety, binding probability, a biological threshold or a cross-target rank. Paroxetine is only the already reviewed setup reference.

## Identity and graph verification

The modeled moiety is PRL-8-53 without disconnected chloride. The retained identity review distinguishes free base CID 39989 from neutral-component and ion-pair hydrochloride records. Preparation must independently parse and graph-match all of these retained representations:

- neutral reference: `CN(CCc1cccc(c1)C(=O)OC)Cc2ccccc2`;
- retained PubChem neutral connectivity representation: `CN(CCC1=CC(=CC=C1)C(=O)OC)CC2=CC=CC=C2`;
- canonical representation used for the target prediction: `COC(=O)c1cccc(c1)CCN(Cc1ccccc1)C`;
- protonated reference: `C[NH+](CCc1cccc(c1)C(=O)OC)Cc2ccccc2`;
- protonated moiety from the retained PubChem ion-pair representation: `C[NH+](CCC1=CC(=CC=C1)C(=O)OC)CC2=CC=CC=C2`.

Require complete heavy-atom graph isomorphism, elements, every heavy-heavy edge, aromatic/bond orders and formal charges; strings alone are not accepted as the check. Require formula C18H21NO2/formal charge 0 for neutral and C18H22NO2+/formal charge +1 for protonated. Chloride is not covalently connected and will not be docked. No carbon stereocenter or permanent experimental enantiomer is specified.

The retained source files and the exact exp-003 receptor/reference files are inventoried by hash in `inputs/source_manifest.json`. No prediction-service request or network access is made in this experiment.

## Two state assumptions and four starting geometries

The two selected states are sensitivity assumptions, not measured physiological populations. A compound-specific pKa and state populations remain unestablished.

For each state, construct the molecule from its verified graph, discard any coordinates, add hydrogens, embed independently with RDKit ETKDGv3 (`useRandomCoords=True`, one thread), then MMFF94-minimize for at most 2,000 iterations:

| state | conformer | generation seed | docking seeds |
|---|---|---:|---|
| neutral (0) | c1 | 5101 | 5301, 5302, 5303 |
| neutral (0) | c2 | 5104 | 5301, 5302, 5303 |
| protonated (+1) | c1 | 5201 | 5301, 5302, 5303 |
| protonated (+1) | c2 | 5202 | 5301, 5302, 5303 |

The generation seeds were selected in a deterministic graph-only preflight to put the two initial structures on opposite signs of the tertiary-nitrogen pyramidal coordinate in each state; no protein, paroxetine geometry or docking result was consulted. The sign is measured from the ordered methyl, benzyl and phenethyl substituents. For protonated PRL the N-H supplies the fourth substituent, so opposite signs are explicit opposite modeled nitrogen handedness assumptions. They are not asserted to be isolable or permanent PRL enantiomers. Neutral tertiary-amine inversion is likewise a sampled coordinate assumption, not stable stereochemical identity. Record signed determinants, N bond geometry and pairwise symmetry-aware aligned heavy-atom RMSD after minimization; report whether each pair is geometrically distinct. Verify source SDF and prepared PDBQT coordinates and graphs independently of inherited stereochemical labels.

Meeko 0.8.0 assigns Gasteiger partial charges. Check PDBQT charge sums against 0/+1 as preparation bookkeeping only. The default Vina score has no explicit partial-charge/Coulomb term. State and conformer comparisons cannot be causally assigned to charge alone.

## Exact receptor, box and search

Reuse, byte-for-byte and without regeneration, `research/experiments/exp-003/derived/receptor_6vrh_primary.pdbqt` (SHA-256 `01ec06e6bfb7708c389bcfc884c929547114b4a9318f8a1f6861c43ab793a5cc`). Reuse center `(135.153, 124.0665, 121.356)` A and size `(16.752, 19.255, 21.052)` A. AutoDock Vina 1.2.7, default `vina` score, rigid receptor, `--cpu 2`, exhaustiveness 8, 20 modes, energy range 5. Runs are strictly sequential.

All exp-003 model limitations persist: resolved auth-A SERT only; incomplete Asn145/Lys201 deleted without caps; missing termini not built; Fab, NAG, LMT and chloride stripped; no modeled sodium or waters; template protonation with all five histidines HIE; rigid protein; no map inspection. The box is conditioned on known paroxetine and says nothing about other sites or targets.

## All-mode evaluation fixed before results

For every saved mode, report state/conformer/seed/rank, empirical Vina score, minimum ligand-to-prepared-receptor heavy-atom distance, 4.0 A residue-contact inventory and descriptive overlap with the deposited-paroxetine contact inventory. The cutoff is descriptive, not a biological gate.

For each state, compute every pairwise PRL heavy-atom RMSD across all saved poses directly in the unchanged protein frame, without protein or ligand fitting, minimizing only over complete graph automorphisms. Annotate whether a pair shares starting conformer, docking seed and nitrogen-sign assumption. Cross-state pairs are not pooled because formal charge, hydrogen/typing, independently generated geometry and protonated-N assumptions differ. Summarize continuous variability within runs, across docking seeds and across starting conformers without inventing a clustering or success threshold. Inspect PDBQT versus exported SDF coordinates and actual nitrogen geometry for every mode.

Any score/contact comparison to exp-003 paroxetine is descriptive only and cannot imply relative affinity, potency or binding probability. Lack of a visually or geometrically consistent pose would not establish nonbinding.

## Host, software and controls

Authorized host is this local arm64 Mac only. Preflight observed Darwin 27.0.0, 18 logical CPUs, 25,769,803,776 physical bytes and unlimited shell virtual-memory limits. No hard 4 GB shell enforcement is claimed. Do not use OCI, containers, helpers, global installs, network access or any flyonenomics path/process.

Reuse the existing project-local exact-version runtime at `<repo>/research/experiments/exp-002/` after verifying it exists: Python 3.13.15, RDKit 2026.03.6, gemmi 0.7.5, Meeko 0.8.0, NumPy 2.5.3, SciPy 1.18.1 and Vina arm64 1.2.7 SHA-256 `823c2bbacf26d72183861322345f0a89736aca66c8e81054c66f93af5ad623f1`. This worktree path may disappear; reproduction then requires an externally rebuilt equivalent environment because the binary/environment are not vendored.

Every computational subprocess runs under `nice -n 19`. Vina uses `--cpu 2`, `OMP_NUM_THREADS=2`; numerical-library variables are one. Preparation/analysis uses one thread. Each search wrapper samples only its own child tree every 0.1 s and terminates its process group at sampled 3 GiB RSS or 1,200 s, leaving headroom below the 4 GB calculation allocation. Runs are serial. These are configured/sample-based controls, not hard memory or aggregate-project enforcement; between-sample peaks and project-wide usage are not measured. Preserve and stop on preparation ambiguity, monitor failure, nonzero return or resource stop rather than retrying elsewhere.
