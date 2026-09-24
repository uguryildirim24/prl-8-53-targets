# Exploratory PRL-8-53 poses in the reviewed 6VRH model

## Result in one sentence

The fixed calculations returned repeatable top-ranked model poses for several of the sampled preparations, but neutral results changed sharply with one starting geometry/seed combination while the protonated top poses varied less; these are behaviors of this exact stripped, rigid, paroxetine-centered model and **not evidence that PRL-8-53 binds SERT**.

## Pre-search record and verified chemistry

Git commit `06790a651d082e0fc18f40f44440a358979a494d` contains the protocol, retained-source hashes, prepared-input hashes, four starting conformers/PDBQTs and no pose or docking-log directory. Commit `a1e26101df0cca61ab177147877ecd9ce2152418` adds the fixed runner, still with no search output. The first monitor records a start at `2026-09-23T06:03:34.073Z`, after both commits in repository order. This is the retained pre-search-freezing record; neither repository ordering nor recorded timestamps are independent wall-clock attestation.

The full graph audit parsed three retained neutral representations and two protonated-moiety representations. Every complete map agreed on 21 heavy atoms, 22 heavy-heavy bonds, every element/bond order and the same connectivity. Neutral was C18H21NO2/formal charge 0; protonated was C18H22NO2+/formal charge +1. The disconnected chloride in hydrochloride records was not docked. PDBQT REMARK graphs independently matched the source heavy graphs. Gasteiger sums were 0.000 (reported as `-0.0` after rounding) for each neutral conformer and 1.002 for each protonated conformer. These sums check preparation bookkeeping; Vina's default score has no explicit partial-charge/Coulomb term.

The two states are assumptions, not measured populations. The retained bounded sources provide no compound-specific pKa. There are no specified carbon stereocenters in the modeled graph. Nitrogen geometry was measured from coordinates rather than inherited labels:

| state | c1 seed / N sign | c2 seed / N sign | symmetry-aware aligned starting RMSD |
|---|---|---|---:|
| neutral | 5101 / + | 5104 / - | 1.9818 A |
| protonated | 5201 / - | 5202 / + | 0.8572 A |

Thus both pairs were geometrically distinct and sampled opposite tertiary-nitrogen pyramidal coordinates. For protonated PRL the signs are opposite modeled N-H handedness assumptions. They are not asserted to be stable, isolable or experimentally present enantiomers; neutral tertiary-amine inversion is likewise not a permanent identity. All 240 exported poses retained their assigned sign, with minimum absolute heavy-neighbor determinant 2.1007 A3. Raw PDBQT and exported SDF heavy coordinates agreed exactly at the stored precision (maximum delta 0.0 A). Complete graph automorphisms preserved the chemically distinct methyl, benzyl and phenethyl N branches; none swapped those substituents. Across opposite signs, the resulting RMSDs are geometric correspondences under explicit local-handedness assumptions, not proof that different N models are identical stable stereoisomers or chirality-preserving equivalents.

The committed generator deterministically reproduces the four retained conformers from their chosen seeds without using receptor, paroxetine or score coordinates in conformer construction. However, the earlier graph-only seed-selection preflight is not fully retained: there is no selector script, candidate-seed list or raw record of the initial conformer trials used to choose 5101/5104/5201/5202. Deterministic regeneration therefore verifies the committed conformers and opposite signs, not the provenance of the unretained selection trials. Those trials are not raw observations and cannot be reconstructed as such. Different starting conformers necessarily differ in torsions and nitrogen geometry, so neither cross-conformer nor cross-state differences isolate one causal variable.

## Twelve fixed searches

All searches used the byte-identical reviewed receptor (SHA-256 `01ec06e6bfb7708c389bcfc884c929547114b4a9318f8a1f6861c43ab793a5cc`), fixed box, Vina 1.2.7/default `vina` score, two CPUs, exhaustiveness 8, 20 modes and energy range 5. Every run returned 20 modes without a Vina error or sampled resource stop; all 240 are preserved.

| state / conformer (start N sign) | seed | top score | nearest receptor heavy atoms | 4 A contacts | deposited-paroxetine contacts also present |
|---|---:|---:|---:|---:|---:|
| neutral c1 (+) | 5301 | -7.301 | 3.3322 A | 11 | 9/15 |
| neutral c1 (+) | 5302 | -7.328 | 3.3525 A | 11 | 9/15 |
| neutral c1 (+) | 5303 | -7.298 | 3.2508 A | 11 | 9/15 |
| neutral c2 (-) | 5301 | -8.717 | 2.7966 A | 13 | 11/15 |
| neutral c2 (-) | 5302 | -8.729 | 2.7610 A | 13 | 11/15 |
| neutral c2 (-) | 5303 | -7.263 | 2.9486 A | 12 | 10/15 |
| protonated c1 (-) | 5301 | -7.277 | 3.0900 A | 12 | 10/15 |
| protonated c1 (-) | 5302 | -7.601 | 3.3100 A | 13 | 11/15 |
| protonated c1 (-) | 5303 | -7.318 | 3.0704 A | 12 | 10/15 |
| protonated c2 (+) | 5301 | -7.388 | 3.3266 A | 11 | 9/15 |
| protonated c2 (+) | 5302 | -7.329 | 3.3696 A | 11 | 9/15 |
| protonated c2 (+) | 5303 | -7.363 | 3.2306 A | 11 | 9/15 |

Scores are empirical model outputs in the program's displayed kcal/mol units, not measured energies or affinities. Across all saved modes, neutral scores ranged -8.729 to -5.734 and protonated scores -7.601 to -5.860. The lower neutral-c2 scores in two runs are not evidence of stronger binding, a physiological state or an optimized pose. No calculation was extended because of them.

The complete residue strings, minimum distances, contact overlap and scores for every mode are in `tables/all_poses.csv`. Contacts use the actual prepared receptor heavy atoms. The 4 A cutoff is an inventory convention, not a biological gate. Overlap with the deposited-paroxetine contacts is descriptive: the retained evidence has no experimental PRL reference pose, so these values are not native-pose recovery.

For context only, exp-003's already reviewed paroxetine top scores were around -10.4 in this setup. Comparing those empirical scores across different molecules does not estimate relative affinity, potency or binding probability.

## Pose variability without fitting or thresholds

`tables/pose_pairs.csv` contains all 14,280 within-state pose pairs. RMSDs are direct in the unchanged protein frame, with no protein or ligand fit, minimized only over complete heavy-atom graph automorphisms. Cross-state pairs were not pooled because formal charge, donor/acceptor typing, hydrogen, independently generated geometry and N-handedness assumptions differ.

All-mode distributions are broad because each run deliberately retains ranks 1–20:

| state | comparison | pair count | minimum | median | maximum |
|---|---|---:|---:|---:|---:|
| neutral | within one run | 1,140 | 0.8834 A | 5.6279 A | 8.9071 A |
| neutral | across seeds, same start | 2,400 | 0.0849 A | 5.6243 A | 9.3907 A |
| neutral | across starts | 3,600 | 0.4236 A | 5.6277 A | 9.3059 A |
| protonated | within one run | 1,140 | 1.3891 A | 5.5768 A | 8.6285 A |
| protonated | across seeds, same start | 2,400 | 0.0564 A | 5.5884 A | 8.9325 A |
| protonated | across starts | 3,600 | 0.5123 A | 5.5761 A | 8.9840 A |

Top-ranked poses provide a narrower view, still without a declared success or clustering threshold:

- Neutral c1 top poses differed by 0.2058–0.8807 A across seeds. Neutral c2 seeds 5301/5302 differed by 0.0849 A, but seed 5303 differed from them by 6.0802–6.0825 A and had a substantially different top score. Across neutral starts, top-pose RMSDs ranged 0.8428–6.2508 A (median 6.1833 A). This is a clear negative/inconsistent observation for robustness to starting geometry and seed.
- Protonated top poses differed by 0.0927–1.1159 A across seeds within a start. Across the two opposite-N starts, top-pose RMSDs ranged 1.1642–1.4109 A (median 1.3107 A). This limited sample is more internally consistent than the neutral sample, but it does not establish physiological preference, binding or broader robustness.

No data-driven RMSD cutoff or cluster boundary was imposed. A reproducible model pose is still only a repeatable output of this setup. Conversely, inconsistency or absence of a visually favored pose would not establish nonbinding.

## Model and interpretation limits

The receptor remains exactly the reviewed exp-003 model: rigid resolved auth-A SERT, missing termini, incomplete Asn145/Lys201 deleted without caps, Fab/NAG/LMT/chloride removed, no modeled sodium or waters, template protonation and all five histidines HIE. Maps were not inspected. Chloride removal and absent ions/waters are physical/electrostatic model limitations even though the chosen Vina function lacks an explicit Coulomb term. The paroxetine-centered box conditions the question on one known-ligand site and cannot assess other SERT sites or other targets.

Only two starting conformers and two charge assumptions were sampled. Three stochastic seeds do not cover conformational, protonation, receptor-state or physiological uncertainty. The native-reference result supports only the internal geometry of this exact setup; it does not validate target prediction, score calibration or PRL-specific biology. The bounded sources retained in this repository contain no direct PRL-8-53 affinity measurement or experimental PRL pose; this is not an exhaustive global absence claim.

Therefore these outputs do not establish SERT binding, affinity, potency, efficacy, selectivity, safety, binding probability or target rank. They must not be used as a validated screen or biological pass/fail result.

## Resources, deviation and reproducibility

The actual host was the authorized local arm64 Mac (Darwin 27.0.0, 18 logical CPUs, 25,769,803,776 physical bytes). Runs were serial. Vina had `--cpu 2`, OMP two and numerical libraries one. Per-run elapsed times were 3.890–4.080 s; sampled child-tree peak RSS was 445,284,352–450,854,912 bytes, below the configured 3 GiB stop. No stop fired. Preparation and analysis were invoked with `nice -n 19` and one configured numerical thread; their `/usr/bin/time` records report maximum resident set sizes of 54,984,704–100,040,704 bytes, but do not independently record effective nice values or aggregate project use. Shell memory limits were unlimited, so neither hard 4 GB nor project-wide aggregate enforcement is claimed; sampling can miss short peaks.

One scheduling deviation is preserved rather than hidden: the sequential driver itself was invoked with `nice -n 19`, then each wrapper again invoked `nice -n 19`; macOS saturated the effective child nice value at 20 rather than the specified 19. This lowered scheduling priority further and did not grant extra resources. No run was retried. `derived/validation.json` therefore records data/resource integrity as passing but `effective_nice_exactly_19: false`.

The exact runtime path still existed for this run and its Vina hash matched. It is a local working-copy path and may disappear. Versions and binary hash are recorded, but the binary, environment and complete lock are not vendored, so turnkey reproduction then requires independently rebuilding an equivalent environment. `commands.md`, every raw mode/log/monitor, scripts, tables, manifest and checksums provide the preserved audit trail. No network request, prediction-service query, global install, or container use occurred.
