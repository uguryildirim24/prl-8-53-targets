# Acetyl-CoA Carboxylase 2 (ACC2) Feasibility Note: Primary Source Assays and Structural Feasibility

**Target:** Human Acetyl-CoA Carboxylase 2 (ACACB / UniProt [O00763](https://www.uniprot.org/uniprotkb/O00763) / ChEMBL [CHEMBL4829](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4829/))  
**Investigated Molecule:** PRL-8-53 (methyl 3-[2-[benzyl(methyl)amino]ethyl]benzoate)  
**Date:** 2026-09-23  
**Status:** Feasibility review; no docking executed; no biological binding claim  
**Associated Evidence Archive:** [`acc2-evidence/`](../../research/acc2-evidence/)

---

## 1. Summary of Evidence and Scope

In SwissTargetPrediction experiment `exp-001` (source commit `18d4794177cf1c749b8c078e671a0f04492ad841`), acetyl-CoA carboxylase 2 (ACACB; UniProt [O00763](https://www.uniprot.org/uniprotkb/O00763); ChEMBL [CHEMBL4829](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4829/)) ranked highest among 100 predictions with a conditional score of 0.710. 

### Core Observations:

1. **Prediction Score Metric:** The SwissTargetPrediction score (0.710) is a conditional ranking score derived under the assumption that the input molecule is active within the curated target database. It does not measure physical binding affinity ($K_i$ or $K_d$) or an absolute probability of binding. Neutral and protonated queries yielded identical target exports, reflecting input normalization or scoring insensitivity rather than independent verification.
2. **Nearest 2D Active ([CHEMBL3928386](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL3928386/)):** The top 2D driver (FP2 similarity 0.765) is Example 1.2 (indexed as 1.002) from Boehringer Ingelheim patent [US-9340510-B2](../../research/acc2-evidence/us9340510b2-primary-excerpt.txt), with a reported $\text{IC}_{50}$ of 524 nM. The ChEMBL assay record labels the organism `Homo sapiens` and says `hACC2`, but has no assay taxon ID or captured construct sequence; ChEMBL assigned relationship `H` ("Homologous protein target assigned") with confidence score 8. Independently, the checked patent text describes testing a recombinant human ACC2 construct lacking the N-terminal 128 amino acids ($\Delta$1-128 hACC2) in a spectrophotometric coupled-enzyme assay. The ChEMBL record does not state why curators used `H`/8, so the database annotation and patent disclosure remain separate observations with an unexplained discrepancy. The checked patent text reports no ACC1 selectivity data, coupled-enzyme counterscreens, binding site, or structural domain mapping.
3. **Nearest 3D Active ([CHEMBL1910396](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL1910396/)):** The nearest 3D active (similarity 0.830) is compound 25c from Yamashita et al. (*Bioorg. Med. Chem. Lett.* 2011), reporting an ACC2 $\text{IC}_{50}$ of 750 nM and an ACC1 $\text{IC}_{50} > 10,000\ \text{nM}$. The series targets the Carboxyltransferase (CT) domain, and an optimized analogue (compound 31 / `0EU`) was co-crystallized with human ACC2 CT domain in PDB [3TDC](https://www.rcsb.org/structure/3TDC). Compound 25c itself has no deposited crystal structure, so its binding interactions are inferred from series SAR rather than directly measured. PRL-8-53 has a flexible acyclic aminoalkyl-ester structure, differing from the rigid spirocyclic lactone-piperidine and 2-aminobenzothiophene scaffold of compound 25c. The 3D similarity score reflects volumetric and electrostatic field overlap under the tool's conformer model, but fails to establish whether PRL-8-53 can satisfy critical CT pocket interactions or bind ACC2.
4. **Structural Biology Context:** An accession search of the RCSB PDB for UniProt O00763 (accessed 2026-09-23) returned 11 entries. Three representative entry payloads were retrieved: PDB [3TDC](https://www.rcsb.org/structure/3TDC) (CT domain with analogue 31 at 2.41 Å), PDB [3FF6](https://www.rcsb.org/structure/3FF6) (CT domain with CP-640186 at 3.19 Å), and PDB [5KKN](https://www.rcsb.org/structure/5KKN) (BC domain with ND-646 at 2.60 Å). In the retrieved records and checked literature, no experimental structure of ACC complexed with CHEMBL3928386 or any tetrahydroisoquinoline derivative was identified.
5. **Feasibility of Downstream Docking:** Docking against an arbitrary pocket to model CHEMBL3928386 is unsupported because its primary binding site is unknown. An exploratory docking probe against the CT catalytic site in PDB 3TDC is feasible if framed to test steric and electrostatic fit rather than binding affinity. Such a study should include native ligand redocking (`0EU`) as a benchmark, reference controls, neutral and protonated PRL-8-53 states, and property-matched decoys to calibrate background scoring. Coordinate assembly (including dimer symmetry operators, missing loops, and residue protonation) must be evaluated directly during preparation.

---

## 2. Primary-Source Trace: Nearest 2D Driver ([CHEMBL3928386](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL3928386/))

### 2.1 Compound Identification and Mapping

*   **ChEMBL Identifier:** [CHEMBL3928386](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL3928386/)
*   **InChIKey:** `QEUWJQXZXZICOI-UHFFFAOYSA-N`
*   **Canonical SMILES:** `COC(=O)c1ccc2c(c1)CCN(Cc1ccc(C(C)NC(C)=O)cc1)C2`
*   **Chemical Name:** methyl 2-(4-(1-acetamidoethyl)benzyl)-1,2,3,4-tetrahydroisoquinoline-6-carboxylate
*   **Molecular Formula:** $\text{C}_{22}\text{H}_{26}\text{N}_2\text{O}_3$ (MW 366.46 g/mol)
*   **SwissTargetPrediction Metrics:** 2D FP2 = **0.764706**; 3D = 0.787.
*   **Primary Source:** US Patent [9,340,510 B2](../../research/acc2-evidence/us9340510b2-primary-excerpt.txt) ("Tetrahydroisoquinoline derivatives, pharmaceutical compositions and uses thereof"), issued May 17, 2016, to Boehringer Ingelheim International GmbH (Inventors: Roth et al.).
*   **Document Mapping:**
    *   *Chemical Synthesis:* Table 14, Entry **1.2** (paragraph [0709]), prepared by reductive amination of 6-methoxycarbonyl-1,2,3,4-tetrahydroisoquinoline hydrochloride and *N*-(1-(4-formylphenyl)ethyl)acetamide.
    *   *Bioactivity Value:* Disclosed in biological data (paragraph [0235]) as **Example 1.002**, reporting an $\text{IC}_{50}$ of $0.524\ \mu\text{M}$ (524 nM).
    *   *Database Record:* Extracted into ChEMBL via BindingDB (`src_id: 37`, record 2880959, compound key `BDBM230398`; raw payload in [`chembl-compound-record-2880959.json`](../../research/acc2-evidence/chembl-compound-record-2880959.json)).

### 2.2 Construct Identity and ChEMBL Target Assignment

*   **Cloned Construct:** US Patent 9,340,510 B2 paragraph [0225] explicitly states:
    > "For biological testing, a human ACC2 construct which lacks the 128 amino acids at the N-terminus for increased solubility (nt 385–6966 in Genbank entry AJ575592) is cloned. The protein is then expressed in insect cells using a baculoviral expression system. Protein purification is performed by anion exchange."
*   **ChEMBL Target Assignment Discrepancy:** In ChEMBL activity row 17768979 (payload in [`chembl-activity-17768979-CHEMBL3928386.json`](../../research/acc2-evidence/chembl-activity-17768979-CHEMBL3928386.json)), the target is listed as [CHEMBL4829](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4829/) (Homo sapiens ACC2) with relationship `H` ("Homologous protein target assigned") and confidence score **8**, rather than `D` / confidence 9. Assay CHEMBL3888444 has an organism label of `Homo sapiens` and says `hACC2`, but its `assay_tax_id` is null and the captured record gives no construct sequence.
*   **Assessment:** The independently checked patent states that the cloned sequence is human ACC2 with an N-terminal 128-amino-acid deletion ($\Delta$1-128 hACC2). The specific rationale for ChEMBL's `H`/8 assignment is not documented. The patent disclosure does not erase the database caveats, and no curation rationale is inferred; the difference remains unexplained.

### 2.3 Assay Method and Stated Limitations

*   **Assay Scheme:** Spectrophotometric 384-well kinetic coupled-enzyme assay measuring the rate of NADH oxidation at 340 nm at 25 °C over 15 minutes.
    *   Target reaction: $\text{Acetyl-CoA} + \text{ATP} + \text{HCO}_3^- \xrightarrow{\text{ACC2}} \text{Malonyl-CoA} + \text{ADP} + \text{P}_i$
    *   Coupling reactions: $\text{ADP} + \text{PEP} \xrightarrow{\text{PK}} \text{ATP} + \text{Pyruvate}$; $\text{Pyruvate} + \text{NADH} + \text{H}^+ \xrightarrow{\text{LDH}} \text{Lactate} + \text{NAD}^+$
*   **Assay Composition:** 100 mM Tris (pH 7.5), 10 mM trisodium citrate, 25 mM $\text{KHCO}_3$, 10 mM $\text{MgCl}_2$, 0.5 mg/ml BSA, 3.75 mM reduced L-glutathione, 15 U/ml LDH, 0.5 mM PEP, 15 U/ml PK, and test compound in 1% DMSO. Reaction initiated by adding 2 mM acetyl-CoA, 2 mM NADH, and 500 $\mu$M ATP.
*   **Primary Uncertainties:**
    1.  *Endpoint Nature:* The 524 nM value is an enzymatic inhibition $\text{IC}_{50}$, not an equilibrium dissociation constant ($K_i$ or $K_d$).
    2.  *Coupled-Assay Vulnerability:* The assay relies on pyruvate kinase (PK) and lactate dehydrogenase (LDH) to link ADP production to NADH oxidation. Compounds that inhibit PK or LDH could decrease the rate of NADH consumption, producing a reduced slope that mimics ACC2 inhibition. The patent text contains no reported PK or LDH counterscreens to evaluate this possibility.
    3.  *Unreported ACC1 Selectivity:* US Patent 9,340,510 B2 contains no reported evaluation of human ACC1. Isoform selectivity is uncharacterized in the source text.
    4.  *Unknown Binding Site:* The patent reports no crystallographic, biophysical, or mutagenesis studies. The binding domain (BC domain, CT domain, or an allosteric pocket) remains unknown.

---

## 3. Primary-Source Trace: Nearest 3D Driver ([CHEMBL1910396](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL1910396/))

### 3.1 Compound Identification and Literature Mapping

*   **ChEMBL Identifier:** [CHEMBL1910396](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL1910396/)
*   **InChIKey:** `UMEWLRYFBAISSB-UHFFFAOYSA-N`
*   **Canonical SMILES:** `CC1(C)CC2(CCCN(C3CCN(C(=O)c4c(N)sc5ccccc45)CC3)C2)C(=O)O1`
*   **Chemical Name:** *rac*-7-{1-[(2-amino-1-benzothiophen-3-yl)carbonyl]piperidin-4-yl}-3,3-dimethyl-2-oxa-7-azaspiro[4.5]decan-1-one
*   **Molecular Formula:** $\text{C}_{25}\text{H}_{31}\text{N}_3\text{O}_3\text{S}$ (MW 453.60 g/mol)
*   **SwissTargetPrediction Metric:** 3D similarity = **0.830**.
*   **Primary Source:** Yamashita et al., *"Design, synthesis, and structure-activity relationships of spirolactones bearing 2-ureidobenzothiophene as acetyl-CoA carboxylases inhibitors,"* *Bioorg. Med. Chem. Lett.* 2011, **21**(21): 6314–6318 (DOI: [`10.1016/j.bmcl.2011.08.117`](https://doi.org/10.1016/j.bmcl.2011.08.117), PMID: [21944854](https://pubmed.ncbi.nlm.nih.gov/21944854/)).
*   **Compound Mapping:** Compound **25c** (payload in [`chembl-compound-record-1542641.json`](../../research/acc2-evidence/chembl-compound-record-1542641.json)).

### 3.2 Primary Assays and Activity Profile

In Yamashita et al. (2011), compound 25c was tested against recombinant human ACC1 and ACC2 (payload in [`chembl-activities-CHEMBL1910396.json`](../../research/acc2-evidence/chembl-activities-CHEMBL1910396.json)):

*   **Human ACC2:** $\text{IC}_{50} \mathbf{= 750\ \text{nM}}$ (relation `=`, activity ID 7846231, assay [CHEMBL1912973](https://www.ebi.ac.uk/chembl/assay_report_card/CHEMBL1912973/), confidence 9).
*   **Human ACC1:** $\text{IC}_{50} \mathbf{> 10,000\ \text{nM}}$ (relation `>`, activity ID 7846230, assay [CHEMBL1912972](https://www.ebi.ac.uk/chembl/assay_report_card/CHEMBL1912972/), confidence 9).
*   **Selectivity Interpretation:** Because ACC1 inhibition is reported with a `>` qualifier ($> 10\ \mu\text{M}$), compound 25c was inactive at the highest concentration assayed. This supports an apparent selectivity ratio of $> 13$-fold for ACC2 over ACC1, rather than an exact measured factor.
*   **Binding Domain and Co-Crystal Provenance:** Yamashita et al. targeted the Carboxyltransferase (CT) domain active site, building on interactions observed with CP-640186 (PDB [3FF6](https://www.rcsb.org/structure/3FF6)) with Gly2162 and Glu2230. An optimized derivative, compound 31 (`0EU`, with an *N*-ethylurea moiety), was co-crystallized with the human ACC2 CT domain in PDB [3TDC](https://www.rcsb.org/structure/3TDC) (2.41 Å). Compound 25c itself was not co-crystallized; its binding mode is an inference based on the shared scaffold with compound 31.

### 3.3 Chemotype Comparison with PRL-8-53

*   **Structural Differences:** PRL-8-53 contains an acyclic, flexible benzyl(methyl)aminoethyl-benzoate ester scaffold. Compound 25c incorporates a rigid spirocyclic lactone-piperidine system and a 2-aminobenzothiophene carboxamide.
*   **3D Score Meaning:** The high SwissTargetPrediction 3D similarity score (0.830) indicates that the algorithm identified substantial volumetric and electrostatic field overlap between generated conformations of the two molecules.
*   **What the Score Fails to Establish:** Structural divergence between the molecules remains significant. The 3D score does not establish whether PRL-8-53 can satisfy specific hydrogen-bonding or packing contacts in the CT active site, whether it adopts a compatible bioactive conformation, or whether it exhibits measurable affinity for ACC2. The internal scoring weights of the service are not documented in the export.

---

## 4. Structural Biology Feasibility and Search Results

### 4.1 PDB Query and Retrieved Structures

An accession query of the RCSB PDB for UniProt [O00763](https://www.uniprot.org/uniprotkb/O00763) (human ACC2) executed on 2026-09-23 returned 11 matching entry identifiers. Three representative entry payloads were retrieved and archived in [`acc2-evidence/`](../../research/acc2-evidence/):

1.  **PDB [3TDC](https://www.rcsb.org/structure/3TDC) (Archived payload: [`rcsb-pdb-entry-3TDC.json`](../../research/acc2-evidence/rcsb-pdb-entry-3TDC.json)):**
    *   *Method / Resolution:* X-ray diffraction, measured resolution **2.41 Å**.
    *   *Construct:* Human ACC2 Carboxyltransferase (CT) domain, residues 1690–2458 with a C-terminal His-tag.
    *   *Ligand:* `0EU` (compound 31 from Yamashita et al. 2011), bound in the CT catalytic pocket.
    *   *Asymmetric Unit:* Single monomer (Chain A).
2.  **PDB [3FF6](https://www.rcsb.org/structure/3FF6) (Archived payload: [`rcsb-pdb-entry-3FF6.json`](../../research/acc2-evidence/rcsb-pdb-entry-3FF6.json)):**
    *   *Method / Resolution:* X-ray diffraction, measured resolution **3.19 Å**.
    *   *Construct:* Human ACC2 CT domain, residues 1693–2458.
    *   *Ligand:* `RCP` (CP-640186), bound in the CT catalytic pocket.
    *   *Asymmetric Unit:* Four chains (A, B, C, D).
3.  **PDB [5KKN](https://www.rcsb.org/structure/5KKN) (Archived payload: [`rcsb-pdb-entry-5KKN.json`](../../research/acc2-evidence/rcsb-pdb-entry-5KKN.json)):**
    *   *Method / Resolution:* X-ray diffraction, measured resolution **2.60 Å**.
    *   *Construct:* Human ACC2 Biotin Carboxylase (BC) domain, residues 238–765.
    *   *Ligand:* `6U3` (ND-646, an allosteric inhibitor at the BC dimer interface).

**Absence of 2D Analog Structure:** In the retrieved records and examined literature, no structure of ACC complexed with CHEMBL3928386 or any tetrahydroisoquinoline derivative was identified.

### 4.2 Structural Assembly and Modeling Considerations

*   **Dimer Interface Assembly:** In PDB 3TDC, the asymmetric unit contains a monomer (Chain A), but published structural literature indicates that the active site is formed across the homodimer interface. An isolated Chain A coordinate file does not represent the intact binding pocket. Any modeling attempt must generate the physiological dimer using crystallographic symmetry operators (space group $C 2 2 2_1$).
*   **Unmodeled Regions:** The PDB 3TDC entry summary lists unmodeled segments (including residues 1–4, 701–713, and 738–762). Direct inspection of coordinate files is required to determine whether these loops impinge on the binding pocket.
*   **Residue Protonation and Charge:** Defining protonation states for active-site residues (such as Glu2230 and histidine residues) is a preparation variable that must be documented and tested as a parameter, rather than assumed as a known physical constant.

---

## 5. Feasibility and Protocol for a Downstream Docking Pilot

### 5.1 Docking Rationale

*   **CHEMBL3928386:** Docking the 2D driver is unsupported because its primary binding domain and binding pocket are unknown. Selecting an arbitrary cavity would not produce an interpretable result.
*   **CT Active Site (PDB 3TDC):** An exploratory docking probe against the CT pocket in PDB 3TDC is feasible. Although PRL-8-53 is chemically distinct from compound 25c and compound 31, a bounded calculation can evaluate whether PRL-8-53 can physically fit within the pocket.

### 5.2 Recommended Pilot Design

If a future experiment pursues an exploratory docking pilot, the following framework is recommended:

1.  **Receptor:** Human ACC2 CT domain from PDB [3TDC](https://www.rcsb.org/structure/3TDC) (2.41 Å).
2.  **Assembly Check:** Reconstitute the full crystallographic homodimer using symmetry operators prior to defining grid coordinates.
3.  **Benchmark Controls:**
    *   *Native Redocking:* Redock crystallographic ligand `0EU` to assess pose reproduction. Literature conventions (e.g., $\text{RMSD} \le 2.0\ \text{Å}$) provide standard reference context.
    *   *Secondary Reference:* Dock CP-640186 (`RCP`) as a cross-chemotype control.
    *   *Decoy Reference:* Dock a reference set of property-matched decoys (matching molecular weight, calculated $\log P$, charge, and rotatable bonds, with topological dissimilarity) to evaluate background scoring.
4.  **Test States:** Evaluate both neutral and protonated monocation forms of PRL-8-53.
5.  **Uncertainty Boundaries:**
    *   *Favorable Score:* Would establish only geometric and electrostatic complementarity to the static crystallographic pocket. It would not establish physical binding, affinity, or biological inhibition.
    *   *Unfavorable Score:* Would show poor fit to this specific static CT pocket, but would not exclude binding to other ACC domains or alternative conformations.

---

## 6. Archival Evidence Trail

Under [`acc2-evidence/`](../../research/acc2-evidence/), 12 raw data payloads and summary manifests are preserved:

*   [`us9340510b2-primary-excerpt.txt`](../../research/acc2-evidence/us9340510b2-primary-excerpt.txt): Primary excerpt of US Patent 9,340,510 B2 covering biological testing paragraphs [0224]–[0235] and Table 14 Ex. 1.2 synthesis.
*   [`chembl-activity-17768979-CHEMBL3928386.json`](../../research/acc2-evidence/chembl-activity-17768979-CHEMBL3928386.json): ChEMBL activity record for CHEMBL3928386 ($\text{IC}_{50} = 524\ \text{nM}$).
*   [`chembl-assay-CHEMBL3888444.json`](../../research/acc2-evidence/chembl-assay-CHEMBL3888444.json): ChEMBL assay record for CHEMBL3888444 (confidence score 8).
*   [`chembl-compound-record-2880959.json`](../../research/acc2-evidence/chembl-compound-record-2880959.json): ChEMBL compound record mapping CHEMBL3928386 to US9340510 Ex 1.002.
*   [`chembl-activities-CHEMBL1910396.json`](../../research/acc2-evidence/chembl-activities-CHEMBL1910396.json): ChEMBL activities for CHEMBL1910396 showing ACC1 ($\text{IC}_{50} > 10,000\ \text{nM}$) and ACC2 ($\text{IC}_{50} = 750\ \text{nM}$).
*   [`chembl-assay-CHEMBL1912973.json`](../../research/acc2-evidence/chembl-assay-CHEMBL1912973.json): ChEMBL assay record for human ACC2 inhibition.
*   [`chembl-compound-record-1542641.json`](../../research/acc2-evidence/chembl-compound-record-1542641.json): ChEMBL compound record for compound 25c.
*   [`rcsb-pdb-entry-3TDC.json`](../../research/acc2-evidence/rcsb-pdb-entry-3TDC.json): RCSB core entry metadata for PDB 3TDC (2.41 Å).
*   [`rcsb-pdb-entry-3FF6.json`](../../research/acc2-evidence/rcsb-pdb-entry-3FF6.json): RCSB core entry metadata for PDB 3FF6 (3.19 Å).
*   [`rcsb-pdb-entry-5KKN.json`](../../research/acc2-evidence/rcsb-pdb-entry-5KKN.json): RCSB core entry metadata for PDB 5KKN (2.60 Å).
*   [`rcsb-chemcomp-0EU.json`](../../research/acc2-evidence/rcsb-chemcomp-0EU.json): Chemical component dictionary record for ligand `0EU`.
*   [`rcsb-chemcomp-RCP.json`](../../research/acc2-evidence/rcsb-chemcomp-RCP.json): Chemical component dictionary record for ligand `RCP`.
*   [`manifest.md`](../../research/acc2-evidence/manifest.md) / [`manifest.json`](../../research/acc2-evidence/manifest.json): Full audit tables with SHA-256 checksums, byte counts, and retrieval timestamps.
