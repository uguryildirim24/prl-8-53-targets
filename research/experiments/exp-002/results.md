# Small ACC2 CT-pocket geometry pilot

## Result in one sentence

The inspected 3TDC pocket is a real, symmetry-spanning crystallographic site, but this fixed-receptor Vina model did not rank a reproducible native-like 0EU pose. The pilot therefore stopped before docking PRL-8-53 or the predeclared comparison set. It does not support an ACC2 binding claim.

## Structure was checked before docking

3TDC is a 2.41 Å X-ray structure of a human ACC2 carboxyltransferase construct. Current RCSB SIFTS maps the 756 construct residues to canonical human ACACB/ACC2 UniProt O00763 residues 1690–2445. The deposit instead calls it an “ACC2 variant,” uses the obsolete accession Q59GJ9, maps it to Q59GJ9 residues 921–1676, and numbers the same construct residues 1715–2470. Direct comparison with current O00763 found one difference: construct I at entity position 452/author residue 2166 versus canonical V2141. No current isoform identifier is assigned to the deposit. Six following histidines, author residues 2471–2476, are an expression tag.

The assembly metadata is not simply “a dimer.” Assembly 1 is the author-defined monomer. Assembly 2 is a PISA software-defined dimer made with the crystallographic operation `x,-y+1,-z+1`, Cartesian transform `x'=x`, `y'=-y+119.756`, `z'=-z+146.035`. For the chain-A 0EU site, 14 of 20 protein residues within 4.5 Å come from that symmetry mate. A monomer would therefore omit most observed pocket contacts. The receptor retained both chains of assembly 2, renamed A and B for PDB compatibility. This retains the actual crystallographic interface; it does not establish that the PISA dimer is the physiological oligomer.

Contact residue IDs below use deposited author numbering; current O00763 positions are 25 lower across the aligned segment (for example, author Gly2187/Glu2255 correspond to canonical Gly2162/Glu2230).

The observed ligand is CCD component 0EU, formal charge 0, with the specified S spiro center. Its 36 deposited heavy atoms have occupancy 1.00, no alternate location, and mean B factor 19.41 Å² (range 11.62–35.21 Å²). Two waters lie within 3.5 Å. No ions or other cofactors are present. Waters were removed because this small rigid-receptor model did not assign stable water roles; that is a model limitation, not evidence that they are irrelevant.

Missing author-numbered residues are 1715–1718, 2415–2427, and 2452–2476. They were not modeled. The resolved residues flanking those gaps are at least 41.99 Å from 0EU, so no resolved gap boundary is adjacent to the observed site. Those endpoint distances do not establish where a flexible missing segment could reach or prove that the omissions cannot influence the pocket. Alternate conformation A was selected for nine residues per chain because it has the higher occupancy, or is tied at 0.50; the nearest alternate residue is 8.88 Å from 0EU and none is a direct 4.5 Å contact. No map set was fetched and no electron-density claim is made. `derived/site_view.svg` is only a coordinate projection.

## Preparation and search

The protein-only PISA dimer retained every resolved standard protein atom and no ligand or water. Meeko 0.8.0 supplied standard residue templates and Gasteiger charges. This amounts to the usual charged Asp/Glu and Lys/Arg templates; all 34 histidines in the dimer were assigned HIE. There was no pKa calculation. Template padding handled unresolved chain ends without adding missing residues. This protonation choice, rigid protein, removed waters, and the software-defined assembly remain important sensitivities.

The search box is the observed 0EU heavy-atom bounds plus 6.0 Å on every face: center `(36.237, 63.819, 50.773)` Å and size `(18.552, 22.095, 23.399)` Å. Thus this is a site-directed CT-pocket test, not a blind whole-protein search.

For native redocking, the CCD 0EU chemical graph was loaded from `0EU_ideal.sdf`; all source coordinates were discarded. RDKit ETKDGv3 generated a new conformer with random coordinates and seed 1701, followed by MMFF94 optimization. The CCD S stereochemistry and neutral formal charge were preserved. Meeko then assigned Gasteiger charges. The crystal coordinates were used only as the fixed site-frame reference for measurement, never as a docking seed.

Vina 1.2.7 used a rigid receptor, four CPUs, exhaustiveness 8, 20 modes, a 5 kcal/mol output range, and seeds 1001, 1002, and 1003. These are initial sampling settings, not statistical calibration. RMSD is the minimum over four stereochemistry-preserving graph automorphisms using all 36 heavy atoms. No fit or independent ligand alignment was applied: both pose and reference stayed in the unchanged receptor coordinate frame.

## Native recovery measured

| Seed | top Vina score | top-pose site-frame RMSD | observed contacts retained | closest sampled mode | closest sampled RMSD | that mode's score |
|---:|---:|---:|---:|---:|---:|---:|
| 1001 | -10.316 | 9.0039 Å | 15/20 | 10 | 3.0195 Å | -7.978 |
| 1002 | -10.350 | 9.0082 Å | 15/20 | 5 | 5.4139 Å | -9.225 |
| 1003 | -10.332 | 9.0090 Å | 15/20 | 10 | 5.2461 Å | -8.580 |

The top-ranked pose was nearly identical across seeds, but it was about 9 Å from the deposited pose in the site frame. It lost the same five observed contacts—A:LYS1992, B:GLU2257, B:GLU2261, B:GLY2184 and B:ILE2262—and gained A:ALA2138, A:TYR1999 and B:VAL2253. Its contact-set Jaccard overlap with the observed pose was 0.6522. Seed 1001 sampled a 3.0195 Å pose only at rank 10; the other two searches did not reproduce that family closely. No numerical success threshold was set. The directly measured ranking and seed dependence are enough to say this setup lacks an interpretable native reference.

Vina values above are empirical model scores, not measured free energies or affinities. The more favorable score assigned to the wrong native orientation is specifically why PRL score comparisons would not be interpretable here.

## Conditional PRL comparison was not run

Before seeing any PRL docking score, four small background entries were fixed in `inputs/background_selection.json`. They span neutral/+1 charge, molecular weights 226–256, calculated cLogP 0.35–3.35, and four to six rotatable bonds. They are geometric/scoring comparisons only and are not known inactive controls. Neutral and protonated PRL graphs from the brief were independently embedded and converted to PDBQT to verify preparation. Their formal charges remained 0 and +1 (PDBQT Gasteiger sums 0.000 and 1.002). Neutral PRL has no stereocenter. Protonated PRL has an unspecified tetrahedral ammonium center; the input therefore does not assert one stable nitrogen stereoisomer. No nitrogen-inversion or proton-exchange kinetics were modeled or inferred.

Because native ranking was not interpretable, no Vina run was made for either PRL state or any background entry. There are therefore no PRL pose families or scores to overinterpret. CHEMBL3928386 was not used as a CT-site control because its binding site is unknown. No further SwissTargetPrediction request or resubmission was made.

## Scope and decision

This experiment probes one static model of the known 3TDC CT-pocket geometry. It does not test the nearer 2D analog's unknown site, establish PRL binding or nonbinding, rank ACC2 against another target, predict function, efficacy, safety, brain effects, selectivity, or a probability of binding. It also cannot support electrostatic specificity from Vina's score. Size, rigid-receptor bias, protonation, water removal, assembly choice and limited sampling remain limitations.

More PRL docking with this exact setup is not useful. A future experiment would first need a scientifically justified receptor/water/protonation treatment that improves the native ranking without tuning to an invented RMSD gate, then repeat independent native sampling. This pilot itself should end here.

## Resources and files

All three Vina jobs ran serially under `nice -n 19`, each configured with `--cpu 4`; BLAS thread counts were one. For each Vina process, `/usr/bin/time -lp` recorded 4.95–5.38 seconds wall time and 635,486,208–635,584,512 bytes maximum resident set size. These are per-process settings and observations, not a measurement of project-wide aggregate CPU or memory use, so they do not by themselves prove an aggregate peak below the project allocation. Raw logs and time records are in `logs/docking/native_0EU/`.

Exact source URLs, UTC retrieval times, byte counts and SHA-256 hashes are in `inputs/source_manifest.json`. Full pose measurements are in `tables/native_redocking_all_poses.csv`; the compact run table is `tables/native_redocking_runs.csv`; structure contacts and preparation checks are in the other tables and JSON under `derived/`. `environment.txt` records exact tool versions and the official Vina binary hash.
