# Coordinate feasibility of 6VRH and 8EF5

## Scope and decision

This is a bounded inspection of the deposited coordinates for human SERT/paroxetine ([6VRH](https://www.rcsb.org/structure/6VRH)) and human OPRM1/fentanyl ([8EF5](https://www.rcsb.org/structure/8EF5)). It is not docking, a binding prediction, a target ranking, or evidence that PRL-8-53 binds either protein. No PRL pose or score was generated. The earlier source audit is context only; every coordinate statement below was independently derived from newly preserved official records.

**Recommendation:** if one native-reference recovery pilot is separately authorized next, use **6VRH/paroxetine**, conditionally and only with the controls below. Defer 8EF5. This preference is about simpler reference-copy selection and documented geometry, not a quantified cross-map quality ranking or presumed PRL binding. It does not authorize docking in this task.

All distances are Euclidean heavy-atom distances measured from deposited coordinates. The declared **4.0 Å cutoff is a descriptive contact inventory, not a biological or docking success threshold**. Exact contact atom pairs are in [`atom-pair-contacts-4A.tsv`](../../research/alternative-coordinate-evidence/generated/atom-pair-contacts-4A.tsv); [`component-nearest-distances.tsv`](../../research/alternative-coordinate-evidence/generated/component-nearest-distances.tsv) identifies the exact ligand and component atom pair for every other polymer chain and nonpolymer residue instance.

## What was obtained and checked

The evidence package preserves official PDBx/mmCIF deposited and assembly-1 coordinates, RCSB entry/assembly/all polymer and nonpolymer entity records, CCD JSON and CIF ligand definitions, canonical UniProt JSON/FASTA records, and small official wwPDB validation XML summaries. Per-response sidecars preserve requested and final URLs, redirect arrays, response headers, actual UTC start/completion times, byte counts, and hashes. Maps were deliberately neither downloaded nor inspected.

Both biological assemblies use operator `1` over all deposited asym IDs. Assembly-1 and deposited files have identical auth-atom coordinate signatures: 6VRH has 6,142 atoms and 8EF5 has 11,705. Thus no generated symmetry mate is needed for the reported pocket measurements. The entity IDs enumerated by each deposited mmCIF, entry API record and fetched entity-record set are identical; [`entity-inventory.tsv`](../../research/alternative-coordinate-evidence/generated/entity-inventory.tsv) records the comparison.

| Check | 6VRH | 8EF5 |
|---|---|---|
| Entry metadata | 3.3 Å cryo-EM; title names wild-type human SERT, paroxetine and 8B6 Fab | 3.3 Å cryo-EM; title names fentanyl-bound μ-opioid receptor-Gi complex; no independent “active-state” claim is made |
| Target identity | Human SLC6A4, P31645; deposited 630 aa maps 1 to 630 | Human OPRM1, P35372; deposited 367 aa maps to canonical 2 to 368 |
| Independent sequence comparison | No difference from canonical P31645 over 1 to 630 | No difference from canonical P35372 over 2 to 368 |
| Actually modeled target | label/auth/canonical A/A: 77 to 617 (541 residues) | label A/auth R/canonical: 65 to 351 / 66 to 352; label F/auth M/canonical: 65 to 352 / 66 to 353 |
| Reference ligand copies | one 8PR, label E/auth A/702 | two 7V7: label H/auth R/501 and label N/auth M/501 |
| Waters in deposited coordinates | none | none |

The full-length deposited SERT sequence therefore does **not** mean a complete coordinate model: residues 1 to 76 and 618 to 630 have no modeled atoms. Likewise, 8EF5 is not a 6 to 353 construct: its deposited receptor maps to P35372 2 to 368, while its two coordinate copies model canonical 66 to 352 and 66 to 353, respectively. RCSB reports zero target mutations, and direct comparison of deposited and canonical sequences found zero substitutions. Partner identities and modeled ranges are tabulated in [`entities.tsv`](../../research/alternative-coordinate-evidence/generated/entities.tsv); global missing segments are in [`missing-segments.tsv`](../../research/alternative-coordinate-evidence/generated/missing-segments.tsv).

## 6VRH: SERT/paroxetine

### Observed reference pocket

The one paroxetine has all 24 CCD heavy atoms under the CCD atom names with matching elements, occupancy 1.00, no alternate conformer, and a uniform deposited coordinate B factor of 90.23 Å². Its atom-site formal charges are unspecified. The CCD definition records net formal charge 0 and two named atom stereoconfigurations (`CAW:S`, `CAX:R`). This preserves the CCD atom/element mapping and declared stereochemistry; it does not independently reassign CIP configuration from the coordinates, infer the solution protonation state, or add unmodeled hydrogens.

At 4.0 Å, 66 atom pairs involve 15 SERT residues: Tyr95, Ala96, Asp98, Ala169, Ile172, Ala173, Phe335, Ser336, Gly338, Phe341, Ser438, Thr439, Gly442, Thr497 and Val501. The shortest observed pair is paroxetine `NAN`-Tyr95 `O`, 2.894 Å. All contact residues and every deposited sequence position within ±2 positions contain the full standard heavy-atom name set, with no zero/partial-occupancy coordinate or official unobserved-atom record in that local set. This local atom-completeness check does not prove that unresolved distant segments have no influence. Elsewhere in SERT, the official mmCIF reports absent side-chain atoms for Asn145 (`CG,OD1,ND2`) and Lys201 (`CG,CD,CE,NZ`); every coordinate atom in the entry has occupancy 1.00.

The deposited heteroatoms are one paroxetine, one chloride, two NAG residues and one LMT detergent. There are no modeled waters or sodium ions. Nearest distances to paroxetine are 8.731 Å for LMT, 9.103 Å for chloride, and 34.755/48.394 Å for the NAG residues. The mmCIF records the NAGs as N-glycosylations of SERT Asn208 and Asn217. These facts do not justify automatically stripping all heteroatoms or grafting sodium from another structure.

The 8B6 heavy and light chains are at least 29.792 and 30.849 Å from paroxetine; their nearest resolved atoms are 27.142 and 28.444 Å from the observed SERT contact atoms. This supports absence of a **resolved direct 4 Å pocket contact**, not absence of conformational or unresolved-segment influence.

### Local validation limit

The official wwPDB XML associates label asym E/auth A/702 with ligand Q-score 0.578 and residue inclusion 0.8750; the entry summary reports Q-score 0.454. Q-score and residue inclusion are map-dependent validation summaries, not experimental binding confidence and not, by themselves, a calibrated cross-map ranking. The deposited B factor is a model field, not an independent density metric. No map was downloaded or visually inspected, so the summary cannot establish atom-by-atom density support or resolve protonation.

### Preparation-feasibility recommendation

**Conditionally suitable and preferred for one later native-reference pilot.** It offers one full-occupancy ligand instance with named CCD stereochemistry, complete CCD heavy-atom/element mapping, intact observed immediate sequence context, and no assembly-copy choice. Preparation must still:

1. use SERT A/auth A and document missing termini 1 to 76 and 618 to 630 without filling them by default;
2. remove Fab only as an explicit receptor-model operation, not as a claim of no possible influence;
3. treat the absent sodium and absent waters as preparation uncertainty; this native-coordinate pilot should not add either from 5I6X or another structure unless a future protocol separately justifies and preregisters that modeling choice;
4. document rather than automatically apply removal of chloride, LMT and the covalent NAGs; and
5. document the chosen charge/protonation assumption. A narrowly justified alternate protonation check may be useful, but the CCD-neutral record neither establishes the physiological population nor mandates a broad sensitivity matrix.

## 8EF5: OPRM1/fentanyl

### Two observed reference pockets

The assembly contains two receptor copies and two fentanyl copies. Each ligand has all 25 CCD heavy atoms under CCD names with matching elements, occupancy 1.00, no alternate conformer, and no atom-site formal charge. The CCD records net formal charge 0 and no configured stereocenter. Coordinate B factors are uniform within each copy (76.18 Å² for H/auth R and 80.60 Å² for N/auth M). Again, this atom/element mapping and neutral CCD graph do not settle protonation.

The two copies are not interchangeable observations at the 4.0 Å inventory level:

- ligand H against receptor A/auth R contacts 46 atom pairs across 13 residues: Gln126, Asn129, Trp135, Asp149, Tyr150, Met153, Cys219, Trp295, Ile298, Val302, Ile324, Gly327 and Tyr328;
- ligand N against receptor F/auth M contacts 35 atom pairs across 10 residues: Gln126, Trp135, Val145, Ile146, Asp149, Tyr150, Met153, Cys219, Gly327 and Tyr328.

Eight residues are common; five occur only in the first inventory and two only in the second. The shortest pairs are fentanyl `N09`-Asp149 `OD2`, 3.235 and 2.981 Å. All contact positions and their ±2 sequence neighbors contain the full standard heavy-atom name set, with no zero/partial-occupancy coordinate or official unobserved-atom record. Every coordinate atom in 8EF5 has occupancy 1.00, and its mmCIF has no individual unobserved-atom category. The differing contact sets may reflect coordinate differences near a hard descriptive cutoff; they are not proof of different biological interactions.

The only deposited nonpolymer components are the two fentanyls and ten cholesterols. There are no modeled waters or ions. Cholesterol is no closer than 11.865/11.978 Å to the two fentanyls. The other receptor copy is 17.034/16.731 Å away. Gi alpha chains are at least 24.283 Å from a ligand and 21.345 Å from observed receptor contact atoms; beta, gamma and scFv are farther except that scFv is 25.753 Å from ligand N and 22.610 Å from its observed contact atoms. These are resolved-atom separations only. Removing the second receptor, Gi proteins, scFv or cholesterol remains a model operation; it cannot be said to have no possible influence.

### Local validation limit

The wwPDB XML associates label H/auth R/501 with ligand Q-score/residue-inclusion 0.523/0.5200 and label N/auth M/501 with 0.462/0.4800; entry Q-score is 0.39. No map was inspected. These are map-dependent summary measures, not binding confidence or a calibrated comparison with 6VRH. Together with the differing coordinate inventories they document copy dependence, but they do not independently validate every fentanyl atom.

### Preparation-feasibility recommendation

**Feasible for later study, but defer as the next native-reference pilot.** The reason is the extra reference-copy and preparation choice, not a quantified superiority claim for 6VRH. A defensible setup would have to predeclare whether both receptor/ligand copies are separate reference controls or justify one choice; preserve canonical numbering; document the one-residue modeled-span difference; and document partner/cholesterol handling. The structure title supports a fentanyl/Gi complex, but this analysis does not independently assign an activation state. A receptor-only extraction would not convert it to another state, and docking cannot determine efficacy.

## Proposed native-reference pilot prerequisites (not performed)

For the recommended 6VRH-only pilot:

- generate an independent paroxetine conformer from the preserved CCD graph and stereochemistry; do not initialize from the bound coordinates;
- define the site frame from retained SERT atoms and keep that frame fixed for evaluation;
- document the selected protonation and heteroatom treatment before the run; use only narrowly justified alternate preparations rather than treating a broad sensitivity matrix as a gate;
- compute graph- and symmetry-aware heavy-atom RMSD to the held-out bound pose **after protein-frame alignment and without aligning the ligand**; report pose-cluster alternatives rather than only a best score;
- record missing segments, retained ions/heteroatoms, charge assumptions, random seeds and software versions before the run.

No numerical RMSD cutoff is declared here. Native-pose recovery would check setup geometry only; it would not validate PRL-8-53 affinity or binding. PRL-8-53 still has no established compound-specific pKa in the bounded project evidence. No comparison of receptor conformations or docking score can determine agonism, antagonism, safety, selectivity or human effects.

## Reproducibility and unresolved limits

- [`alternative-coordinate-evidence/manifest.md`](../../research/alternative-coordinate-evidence/manifest.md) lists every official response and its transport evidence.
- [`commands.md`](../../research/alternative-coordinate-evidence/commands.md) records the one-thread, nice-19 commands, the unverified 4 GB limit attempt and measured per-process memory.
- [`ligand-instances.tsv`](../../research/alternative-coordinate-evidence/generated/ligand-instances.tsv), [`ligand-graph.tsv`](../../research/alternative-coordinate-evidence/generated/ligand-graph.tsv), [`hetero-inventory.tsv`](../../research/alternative-coordinate-evidence/generated/hetero-inventory.tsv), [`component-nearest-distances.tsv`](../../research/alternative-coordinate-evidence/generated/component-nearest-distances.tsv) and [`struct-connections.tsv`](../../research/alternative-coordinate-evidence/generated/struct-connections.tsv) separate coordinate facts from interpretation.
- [`pocket-sequence-context.tsv`](../../research/alternative-coordinate-evidence/generated/pocket-sequence-context.tsv) checks standard heavy-atom names and coordinate occupancy for every contact residue and ±2 sequence neighbor; [`atom-occupancy-summary.tsv`](../../research/alternative-coordinate-evidence/generated/atom-occupancy-summary.tsv) preserves entry-wide coordinate and official unobserved-atom counts.
- The official validation summaries are preserved, but maps were not acquired or visually inspected. Local density remains unresolved beyond those summary fields.
- A modeled coordinate is not an unengineered biological system; a missing coordinate is not evidence of no influence. No missing loops were filled, mutation was restored, ion was grafted, partner was deleted, or engineered model called experimentally observed.
