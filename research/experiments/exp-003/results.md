# 6VRH/paroxetine native-reference pilot

## Result in one sentence

Under the one frozen, stripped rigid-SERT preparation, both neutral and protonated paroxetine repeatedly placed their top-ranked Vina pose near the deposited geometry; this makes a later calculation in this **exact model** geometrically interpretable, but it is not evidence that PRL-8-53 binds SERT and it does not validate Vina scores as affinities.

## Preparation completed with one documented pre-search amendment

The dated protocol was preserved before any search. Its initial receptor-preparation preflight stopped because the general missing-residue rule refused to omit incomplete Asn145 near a box face. Before any docking result existed, the protocol was amended to omit exactly the two known incomplete residues, Asn145 and Lys201. Their nearest **observed** atoms are 15.656 and 36.647 A from deposited paroxetine; those distances say nothing about the positions of their absent side-chain atoms. The failed preflight is preserved. No atom was reconstructed and no other residue was silently deleted.

Git ancestry independently establishes that commit `38f42a0ee213d9d19d67f31a35db0bd51e6d56b9` contains the amended protocol, both failed and final preparation records, fixed inputs and no search outputs, while its child contains the six searches. The prose UTC values, file contents and commit dates are recorded timestamps, not an independently timestamped proof of the order of the initial draft, failed preflight and amendment within the pre-search commit. The preserved failure and changed option disclose the tuning that occurred; no receptor change after search output is present in repository history.

The sole receptor model uses resolved human SERT auth chain A, residues 77–617, with all retained heavy-atom coordinates unchanged. Meeko standard templates/Gasteiger charges were used; all five histidines were HIE and are at least 20.706 A from paroxetine. Missing termini 1–76 and 618–630 were not modeled. Deleting residues 145 and 201 produced breaks between 144/146 and 200/202. The written prepared receptor adds neither terminal capping residues nor `OXT` at those breaks; the flanking residues retain ordinary template backbone atoms and hydrogens. This uncapped local treatment is another model limitation even though the observed remnants of the deleted residues are outside the local pocket.

Fab chains, the two covalent NAGs, LMT detergent and chloride were removed. No sodium or water is modeled in 6VRH and none was grafted. Distance supports calling Fab/NAG remote from this box and LMT a nearby detergent, but it does not establish functional irrelevance or make this stripping choice uniquely correct. Chloride 9.103 A away may still matter to the physical receptor environment. Its omission changes model composition and biological electrostatics; it does not remove an explicit Coulomb term from the Vina score, because the selected Vina scoring function has no such term. No universal stripping, ion grafting or reconstruction rule follows. Maps were not inspected.

The full CCD graph check found 24 named heavy atoms and 27 heavy-heavy bonds and mapped the two graph automorphisms while requiring `CAW:S` and `CAX:R`. Exactly one ETKDGv3/MMFF94 starting conformer was independently embedded for each state after discarding all source coordinates; the neutral and protonated states used different conformer seeds as well as different docking seeds. Their aligned starting-coordinate RMSD is 1.6858 A over all heavy atoms and 0.3809 A over the six-membered piperidine ring. Thus this is a two-preparation comparison, not an isolation of charge alone or a fixed-conformer charge perturbation.

The two predeclared states were CCD-neutral paroxetine (formal charge 0) and protonated paroxetine (+1); their PDBQT Gasteiger charge sums were 0.001 and 1.001. The actual logs identify the default `vina` scoring function. Its terms are Gaussian steric/attraction, repulsion, hydrophobic, hydrogen-bonding and rotatable-bond terms; unlike the separately available AD4 score, it has no explicit partial-charge/Coulomb term. The charge sums therefore check preparation bookkeeping, not a directly scored electrostatic energy. Protonation can still change hydrogens, donor/acceptor atom typing, geometry and the independently generated conformer. The states are a narrow preparation uncertainty check, not inferred physiological populations.

## Six fixed searches

All searches used the unchanged receptor frame and fixed native-site box, Vina 1.2.7, two CPUs, exhaustiveness 8, 20 modes, 5 kcal/mol range, and the three preregistered seeds per state. All 120 modes are preserved and tabulated.

| state | seed | top score | top site-frame RMSD | deposited contacts retained | top contact Jaccard | closest saved mode |
|---|---:|---:|---:|---:|---:|---|
| neutral | 2301 | -10.409 | 0.5572 A | 15/15 | 0.9375 | rank 1 (0.5572 A) |
| neutral | 2302 | -10.437 | 0.5579 A | 15/15 | 0.9375 | rank 1 (0.5579 A) |
| neutral | 2303 | -10.547 | 0.6189 A | 14/15 | 0.8750 | rank 1 (0.6189 A) |
| protonated | 2401 | -10.458 | 1.6352 A | 14/15 | 0.8235 | rank 1 (1.6352 A) |
| protonated | 2402 | -10.451 | 1.6207 A | 14/15 | 0.8235 | rank 1 (1.6207 A) |
| protonated | 2403 | -10.448 | 1.6535 A | 14/15 | 0.8235 | rank 1 (1.6535 A) |

RMSD is the minimum over complete stereochemistry-preserving heavy-atom graph automorphisms, measured directly in the unchanged protein frame. Neither ligand nor protein was fitted. The 4.0 A contact cutoff is a descriptive inventory, not a biological gate.

The neutral top poses retained all deposited contact residues in two seeds; the third lost Thr497. All added Tyr176. The protonated top poses consistently lost Ala169 and added Leu337/Tyr176. The second-ranked neutral modes were 5.27–5.29 A from the reference; second-ranked protonated modes were 3.65–3.72 A. Thus the nearest saved mode was top-ranked in every run and the measured top geometry was consistent across three stochastic docking seeds **for the one starting conformer in each state**. It is not a robustness result over other ligand conformers, ring states, receptor states or physiological populations. Cross-state pose differences cannot be assigned to charge alone. No numerical success threshold was set, so this is reported as observed ranking and limited reproducibility rather than a pass/fail claim.

Vina scores are empirical model values, not measured free energies or affinities. Their similarity across states does not rank physiological protonation or binding strength, and the recorded Gasteiger charge sums do not supply a mechanistic decomposition of those scores.

## What this permits—and does not

A later, separately preregistered PRL-8-53 calculation could be interpreted only as this question: how does a specified PRL charge/conformer behave in this same static, paroxetine-centered SERT pocket relative to the now coherent native geometry? It could report pose families and model scores as model behavior. **No PRL-8-53 docking was run here.**

Such a later result would still not establish SERT binding, affinity, efficacy, selectivity, safety or a probability of binding. Exact uncertainties that remain are:

- PRL-8-53's compound-specific protonation populations are not established in the bounded evidence;
- 6VRH lacks modeled sodium and water, while this model also removes chloride and detergent;
- the receptor is rigid, stripped of Fab/NAG, missing termini and two incomplete residues, with template protonation and no pKa calculation;
- the deposited paroxetine geometry has only summary map validation; density was not inspected;
- the box is conditioned on the known paroxetine site and says nothing about other SERT sites or other targets;
- no experimentally established negative control or calibrated scoring/affinity relationship exists.

Accordingly, native recovery increases confidence only in the internal geometry of this exact setup. It does not strengthen the SwissTargetPrediction SERT suggestion as compound-specific evidence.

## Resources and audit trail

The six jobs ran sequentially under `nice -n 19`, each with Vina `--cpu 2`, OMP limited to two and numerical-library variables limited to one. Sampled child-tree peak RSS was 478,052,352–486,440,960 bytes; observed child nice values were 19. The wrapper's 3 GiB sampled-RSS and 1,200-second stop controls did not fire. These are sampled per-run observations, not hard memory enforcement or project-wide aggregate measurements; macOS shell memory limits were observed as unlimited.

`protocol-prerun.md`, `commands.md`, `environment.txt`, `inputs/source_manifest.json`, every raw pose/log/monitor record, `tables/all_poses.csv`, `derived/results_summary.json`, `derived/validation.json`, `manifest.md` and `SHA256SUMS` provide the audit trail. Validation checks source bytes, graph/stereochemistry, charges, exact receptor omissions/coordinate preservation, the six-run matrix, resources and all 120 saved modes. The archived `logs/checksums.*` records preserve an earlier failed self-referential check caused by redirecting verification output into a file covered by the checksum list; running `shasum -a 256 -c SHA256SUMS` without changing a covered file verifies the package.

The recorded runtime path still existed during review and the Vina binary still matched its declared hash. It is nevertheless a local working-copy path that may disappear. Exp-003 records versions and the binary hash but does not vendor the binary, virtual environment or a complete dependency lock, so a future turnkey rerun requires independently rebuilding an equivalent environment and is not guaranteed by the archived path alone. The preserved raw outputs and their independent replay do not depend on that path remaining available.
