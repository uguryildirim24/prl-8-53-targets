# Structural Feasibility Audit for Alternative PRL-8-53 Binding Hypotheses

## Scope and evidence boundary

This audit asks whether human SERT (SLC6A4/P31645) and human μ-opioid receptor (OPRM1/P35372) have defensible experimental structures for later computational tests of the provisional hypotheses in `research/alternative-target-audit.md`. Structural tractability is not evidence that PRL-8-53 binds either protein.

The archived evidence is deliberately limited:

- RCSB core **entry** records establish titles, methods, nominal resolutions, citation metadata, and entry-level counts.
- RCSB **polymer-entity** records establish deposited construct sequences, source organisms, SIFTS accession mappings, and depositor mutation annotations for 4DKL, 5I6X, 6VRH, and 8EF5.
- RCSB chemical-component records establish the identities of paroxetine (`8PR`), fentanyl (`7V7`), and β-funaltrexamine (`BF0`).
- Two ChEMBL activity records and four molecule records preserve selected source-ligand annotations.

The archive does **not** contain coordinate/mmCIF files, map files, RCSB search requests or result sets, full UniProt records, or article full text. Four notes whose legacy names began `primary-excerpt-` and a contradictory `oprm1-human-mouse-alignment.txt` were investigator-written summaries rather than primary evidence; they have been withdrawn and removed, and none of their claims are used. `reviewed-evidence-check.py` and its captured output supersede only the bounded metadata and local-residue checks they actually reproduce.

Consequently this audit does not claim exhaustive structure counts, coordinate-measured distances, B factors, model continuity, or article-specific contacts. No new prediction-service query was made. This shortlist is a list of candidates to consider, not a decision to dock SERT or OPRM1 or to begin a broader alternative-target experiment.

## Candidate summary

| Target | Defensible primary candidate | What the archived records establish | Important limit |
|---|---|---|---|
| Human SERT | [6VRH](https://www.rcsb.org/structure/6VRH), paroxetine-bound | 3.3 Å cryo-EM; title identifies wild-type human SERT with paroxetine and 8B6 Fab; polymer entity is a 630-residue human SLC6A4 sequence, SIFTS-mapped over all 630 residues to P31645, with `rcsb_mutation_count = 0` | Coordinates were not archived, so pocket contacts, modeled residue span, ions, local density, and Fab-to-pocket separation remain unchecked |
| Human OPRM1 | [8EF5](https://www.rcsb.org/structure/8EF5), fentanyl-bound | 3.3 Å cryo-EM; title identifies a fentanyl-bound μ-opioid receptor-Gi complex; polymer entity is human OPRM1, SIFTS-mapped to P35372, with `rcsb_mutation_count = 0` | The deposited receptor entity maps to canonical residues 2 to 368, not the previously claimed 6 to 353; modeled residue span, contacts, partner proximity, and local density remain unchecked |

These are candidate starting structures, not prepared models. The zero-mutation statements are depositor/RCSB sequence metadata, not coordinate-by-coordinate validation.

## 1. Human SERT

### 1.1 Primary candidate: 6VRH

The archived 6VRH entry reports electron microscopy at 3.3 Å and gives the title “Cryo-EM structure of the wild-type human serotonin transporter complexed with paroxetine and 8B6 Fab.” The archived polymer entity:

- identifies *Homo sapiens* SLC6A4;
- contains 630 residues;
- maps by SIFTS to P31645 from residue 1 for a length of 630; and
- reports no sequence conflicts, deletions, insertions, or mutations.

This is enough to prefer 6VRH as a human, deposited-wild-type, ligand-bound SERT candidate. The entry title and the archived `8PR` component definition support paroxetine as the reference ligand. They do not by themselves prove a particular contact list or protonation state.

### 1.2 Comparison structure: 5I6X

The archived 5I6X entry reports a 3.14 Å X-ray structure of human SERT with paroxetine. SIFTS maps entity residues 3 to 545 to P31645 residues 76 to 618. A direct comparison of that mapped deposited sequence with the archived full-length 6VRH sequence finds **five** substitutions:

- Y110A
- I291A
- T439S
- C554A
- C580A

This corrects the earlier four-mutation account, which omitted Y110A. The RCSB fields themselves are inconsistent: `pdbx_mutation` names Y110A, I291A, and T439S, while mutation features flag the positions corresponding to I291A, T439S, C554A, and C580A. The deposited sequence comparison is therefore the clearest reproducible account available here.

T439S is a construct difference that must be tracked; its pocket location and practical effect were not independently verified from the archived metadata. 5I6X can be shortlisted as a comparison or possible ion reference, but it should not be treated as native human SERT. The core entry lists sodium among bound components, but the archive lacks coordinates; the number, locations, coordination geometry, chloride assignment, and transferable waters have not been checked.

### 1.3 Unresolved prerequisites if modeling is later authorized

No SERT modeling is authorized by this audit. A later, separately approved geometry probe would first need coordinate/map provenance; verification of modeled residues, local confidence, ligand identity and pose, ions, waters, lipids, pocket-facing mutations, and Fab proximity; and a documented preparation rationale. Any sodium transfer from 5I6X to 6VRH would be a model assumption requiring atom-level alignment, coordination checks, clash inspection, and sensitivity to the unmodified setup. Redocking could check setup behavior but could not validate PRL-8-53 binding or affinity.

The previously discussed 7LIA and 9VWS entries are not assessed here because no records for them were archived.

## 2. Human μ-opioid receptor

### 2.1 Primary candidate: 8EF5

The archived 8EF5 entry reports a 3.3 Å cryo-EM “Fentanyl-bound mu-opioid receptor-Gi complex.” The receptor polymer entity:

- identifies *Homo sapiens* OPRM1;
- has a deposited length of 367 residues;
- maps by SIFTS from entity residue 1 to P35372 residue 2 for all 367 residues, i.e. canonical residues 2 to 368; and
- reports no sequence conflicts, deletions, insertions, or mutations.

The archived `7V7` chemical-component record establishes the fentanyl component identity. Together these records make 8EF5 a defensible fentanyl-bound, Gi-coupled human OPRM1 candidate. Calling its receptor conformation “active state” is a structural interpretation that still requires coordinate or primary-source verification. The records do not establish which residues are actually modeled, atom-level contacts, or the reported mutations of every partner protein; those require coordinate and partner-entity records.

### 2.2 Conditional inactive comparator: 9PXU

The archived 9PXU core entry reports 3.4 Å cryo-EM and is titled “Inactive-state naloxone-mu opioid receptor nanobody6 complex.” It lists sodium (`NA`) among bound components. However, no receptor polymer entity, naloxone component record, or coordinates were archived for it. Thus 9PXU is a plausible inactive comparator, but its species/accession mapping, construct/fusion boundaries, receptor mutations, naloxone identity, sodium site, and local quality are not verified by this evidence package.

### 2.3 Why 4DKL is not a noncovalent human reference

The archived 4DKL records establish a 2.8 Å X-ray μ-opioid receptor/lysozyme chimera. SIFTS maps receptor portions to mouse P42866 and the inserted segment to T4 lysozyme P00720. The entry reports one intermolecular covalent bond, and the archived `BF0` component definition identifies BF0 as a covalent chemical modification that links its CAW atom to a lysine NZ atom. This is sufficient to reject 4DKL/β-funaltrexamine as an ordinary noncovalent redocking reference for human OPRM1.

The archive does not include the coordinate record needed to verify the previously quoted `LINK` line, exact 1.51 Å distance, or residue-level bond assignment. Those details have therefore been removed from the asserted evidence.

### 2.4 Human/mouse numbering that is actually supported

The archived polymer records support local residue mapping without assuming a universal offset:

- 8EF5 maps its deposited human sequence to P35372 residues 2 to 368.
- 4DKL maps receptor segments to P42866 residues 52 to 263 and 270 to 360.
- In the conserved TM3 window, human P35372 Asp149 and mouse P42866 Asp147 occupy the corresponding local sequence position.
- In the conserved TM5 window, human P35372 Lys235 corresponds locally to mouse P42866 Lys233.
- Human P35372 residue 233 is Leu.

`alternative-structure-evidence/reviewed-evidence-check.py` reproduces these local extractions from the archived JSON and `reviewed-evidence-check.txt` captures an actual run. The original purported global alignment is internally contradictory and is withdrawn. Its claim of a specific two-residue N-terminal indel is not reproducible from this package because the full canonical mouse sequence was not archived. No global “minus two” numbering rule should be used.

### 2.5 Unresolved prerequisites if modeling is later authorized

No OPRM1 modeling or dual-state experiment is authorized by this audit. A later, separately approved geometry probe would first need coordinate/map provenance and verification of modeled spans, chain IDs, missing pocket residues, alternate conformers, ligand identity and pose, local density, waters, ions, lipids, and partner contacts. Removing Gi would not convert 8EF5 into an inactive state. A verified inactive comparator would be a separate structural hypothesis, and relative docking scores could not classify an untested ligand as agonist or antagonist. Any future setup must use canonical human residue mapping rather than arithmetic transfer of mouse numbering.

## 3. Source-ligand provenance and limits

Only two retained activity records directly preserve numeric target annotations:

- ChEMBL activity 879137 records CHEMBL423726 at human OPRM1 with `Ki = 850 nM` and an assay description for displacement of `[3H]diprenorphine` from cloned human μ-opioid receptor.
- ChEMBL activity 1682463 records CHEMBL201666 at human SERT with `Ki = 3650 nM` and an assay description for displacement of `[125I]RTI-55` from human SERT expressed in HEK293 cells.

These are curated database records, not primary-paper text or structures of those compounds bound to the targets. The saved activity payloads do not contain a `confidence_score` field; confidence values from related assay/target records must not be silently attributed to these files. Similarity ranks and claims about additional functional assays come from the earlier target-prediction audit, not from these two payloads.

Paroxetine in 6VRH and fentanyl in 8EF5 define experimentally ligand-occupied candidate pockets at the entry level. Chemical resemblance between those ligands, ChEMBL source compounds, and PRL-8-53 is only analogy. It supplies no measured pose, affinity, efficacy, or selectivity for PRL-8-53.

## 4. PRL-8-53-specific modeling limits

- Its tertiary amine may have multiple relevant protonation microstates. No compound-specific experimental pKa is preserved here. If modeling were separately approved, alternative plausible states would be assumptions to document, not a mandated state.
- Its flexible open-chain linker creates conformational-entropy and sampling problems. Routine docking scores are not binding free energies and do not reliably price the solution-to-bound conformational penalty.
- Receptor/transporter state, ion placement, hydration, and construct engineering can change poses and scores. Any later comparison would be sensitivity analysis across model choices, not selection of one nominal “best” score.
- Docking could test geometric compatibility and prioritize hypotheses. It could not establish binding, non-binding, agonism, antagonism, or a human effect. Those conclusions require direct experiments.

## Conclusion

6VRH and 8EF5 form a compact provisional human shortlist, subject to coordinate-level verification. 5I6X is an engineered SERT comparison with five deposited-sequence substitutions; 9PXU remains only a conditional inactive OPRM1 comparator pending polymer and coordinate verification; and covalent mouse 4DKL is unsuitable as a noncovalent human benchmark. The unresolved gap is coordinate-level provenance. This audit authorizes no modeling and makes no biological claim about PRL-8-53.
