# exp-002 manifest

> **Public release note.** Some files in this repository were edited before publication: local absolute paths were made repo-relative, a machine hostname was removed, and material that is not redistributed here was taken out. Every SHA-256 recorded in this folder, including `SHA256SUMS`, was recomputed against the published files, so the hashes verify what is here rather than the internal working copy. No scientific result, pose, score, or table value was changed. Empty captures and package-installation chatter were removed. Versions and binary provenance remain in `environment.txt` and `scripts/install_vina.sh`. Analysis and validation scripts still write to this experiment's retained output directories.


## Scope

This is a stopped native-redocking pilot for the human ACC2 3TDC CT pocket. The conditional PRL/background docking stage was not run because native pose ranking was not interpretable. No SwissTargetPrediction request was made.

## Inputs

`inputs/source_manifest.json` is the machine-readable source ledger. It records the exact official RCSB and UniProt URLs, redirects, response-header files, UTC retrieval timestamps, HTTP statuses, byte counts and SHA-256 hashes. Preserved records include:

- original 3TDC PDB and mmCIF;
- RCSB assembly 1 and assembly 2 coordinate mmCIFs and metadata;
- RCSB entry, polymer entity and polymer instance metadata;
- CCD 0EU JSON, component CIF and ideal SDF;
- current UniProt O00763 JSON and FASTA.

`inputs/background_selection.json` fixes the small comparison set and its selection reasoning before any PRL docking score. These are not established nonbinders.

## Derived preparation

- `derived/structure_inspection.json`: identity, sequence discrepancy, operators, ligand occupancy/stereochemistry, missing residues, contacts, water proximity and box definition.
- `derived/receptor_assembly2_protein_only.pdb`: unfilled PISA/crystallographic dimer, with the generated mate renamed B.
- `derived/receptor_3tdc_assembly2_prepared.pdb` and `.pdbqt`: Meeko-prepared receptor.
- `derived/native_0EU_bound_reference.pdb`: deposited heavy-atom reference in the unchanged site frame.
- `derived/ligands/`: independent seeded conformers. PRL/background entries were prepared only to verify their graph/stereochemistry/charge; they were not docked.
- `derived/pdbqt/`: Gasteiger-typed ligand files.
- `derived/site_view.svg`: simple coordinate schematic, not a density view.
- `derived/native_redocking_summary.json` and `validation.json`: interpretation and experiment-specific checks.

## Raw calculation outputs

- `poses/native_0EU/seed-{1001,1002,1003}.pdbqt`: raw Vina multi-model output.
- matching `.sdf`: Meeko export used for graph-aware measurement.
- `logs/docking/native_0EU/`: Vina stdout and `/usr/bin/time -lp` records.
- `tables/native_redocking_all_poses.csv`: all 60 score/RMSD/contact rows.
- `tables/native_redocking_runs.csv`: compact per-seed results.
- `tables/native_site_contacts.csv`, `ligand_properties.csv`, and `pdbqt_charge_check.csv`: preparation evidence.

## Reproduction order

The installed environment and binaries are intentionally excluded from git. The commands below are a reproduction order, not a timestamped transcript of the original command sequence. From this directory on arm64 macOS:

```sh
nice -n 19 python3 scripts/fetch_inputs.py
nice -n 19 python3 -m venv .venv
nice -n 19 env MAKEFLAGS=-j4 CMAKE_BUILD_PARALLEL_LEVEL=4 \
  .venv/bin/pip install gemmi==0.7.5 rdkit==2026.3.6 meeko==0.8.0 \
  numpy==2.5.3 scipy==1.18.1 pillow==12.3.0
nice -n 19 scripts/install_vina.sh
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  .venv/bin/python scripts/inspect_structure.py
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  .venv/bin/python scripts/prepare_ligands.py
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  scripts/prepare_receptor.sh
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  scripts/prepare_docking_inputs.sh
for seed in 1001 1002 1003; do
  /usr/bin/time -lp nice -n 19 env OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 \
    VECLIB_MAXIMUM_THREADS=1 scripts/run_vina_one.sh native_0EU "$seed" \
    2> "logs/docking/native_0EU/seed-${seed}.time.txt"
  nice -n 19 env OMP_NUM_THREADS=1 .venv/bin/mk_export.py \
    "poses/native_0EU/seed-${seed}.pdbqt" \
    -s "poses/native_0EU/seed-${seed}.sdf" \
    > "logs/docking/native_0EU/seed-${seed}-export.log" 2>&1
done
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  .venv/bin/python scripts/analyze_native_redocking.py
nice -n 19 .venv/bin/python scripts/make_site_view.py
nice -n 19 .venv/bin/python scripts/validate_outputs.py
```

The source fetch will naturally obtain a new timestamp and may obtain revised upstream records. The committed inputs are the immutable inputs to the reported run.

## Software and limits

`environment.txt` contains package versions, machine facts and the official Vina URL/SHA-256. Vina was the official v1.2.7 arm64 macOS release. Runs were serialized, configured with Vina `--cpu 4`, and each Vina process was monitored with `/usr/bin/time -lp`. Those per-process settings and records are not project-wide aggregate resource accounting. No environment, installed binary, map set, database bulk download or unrelated project file is committed.
