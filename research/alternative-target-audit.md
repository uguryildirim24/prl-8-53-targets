# Audit of Alternative Target Predictions (Ranks 2–6) for PRL-8-53

## 1. Scope and Analytical Framework

This audit evaluates the evidence supporting the five targets immediately following rank-1 ACACB in the target predictions obtained from the SwissTargetPrediction web server (`exp-001`). The scope covers ranks 2 through 6 in rank order:

1. **Rank 2: OPRM1** / P35372 / CHEMBL233 — Mu-type opioid receptor
2. **Rank 3: KCNJ1** / P48048 / CHEMBL1293292 — Inward-rectifier potassium channel (Kir1.1 / ROMK)
3. **Rank 4: BCHE** / P06276 / CHEMBL1914 — Cholinesterase (Butyrylcholinesterase)
4. **Rank 5: KCNH2** / Q12809 / CHEMBL240 — Voltage-gated potassium channel Kv11.1 (hERG)
5. **Rank 6: SLC6A4** / P31645 / CHEMBL228 — Sodium-dependent serotonin transporter (SERT)

### Methodological Principles
- **Reversible Work Budget:** The selection of these five targets reflects a sequential computational work budget based strictly on prediction rank. It does not reflect biological confidence, established therapeutic relevance, or target validation.
- **Preliminary Hypotheses:** SwissTargetPrediction scores are conditional probabilistic rankings assuming compound bioactivity against human targets. They are not measured affinities ($K_i$, $K_d$, or $\text{IC}_{50}$) for PRL-8-53.
- **Strict Separation of Evidence:** ChEMBL annotations, curated activity endpoints, and primary literature records are explicitly distinguished.
- **Non-Inference of Biological Safety or Use:** No inference of compound safety, toxicity, behavioral effect, or human drug utility is made from these predictive hypotheses.
- **Bounded Search Record:** To date in the literature and database searches performed for this project, zero direct binding assays ($K_i$, $K_d$), enzyme inhibition values ($\text{IC}_{50}$), or functional responses ($\text{EC}_{50}$) have been identified for PRL-8-53 at any molecular target. The absence of a recorded assay does not establish non-binding.
- **Distinguishing Observation from Inference:** Structural descriptions report observed 2D and 3D chemical representations from database records. Explanations of why the algorithm ranked a compound, or whether structural features align, are explicitly hypothetical interpretations, not verified model attributions or binding pose analyses.
- **Provenance Limitation:** The target predictions were obtained from the SwissTargetPrediction web server (Daina, Michielin & Zoete, *Nucleic Acids Res.* 2019). The service output is not redistributed in this repository; only the target identities carried forward and the reasoning about them are recorded here (see [`docs/target-shortlist.md`](../docs/target-shortlist.md)). The ChEMBL and UniProt evidence has separate provenance under those services' ordinary terms and is retained in full.

---

## 2. Canonical Target Verification and Training Set Parameters

The five targets were verified against official UniProtKB (2026-09 release) and ChEMBL 37 (2026-05-01 release) records.

| Rank | Prediction Export Label | Canonical UniProt Recommended Name | Gene Symbol | UniProt ID | ChEMBL Target ID | Canonical Target Class | Server-Reported Actives (3D / 2D) | Exposed Rows Captured |
|:---:|:---|:---|:---:|:---:|:---:|:---|:---:|:---:|
| **2** | Mu-type opioid receptor | Mu-type opioid receptor | `OPRM1` | `P35372` | `CHEMBL233` | Family A GPCR | 4,157 / 870 | 200 / 200 |
| **3** | ATP-sensitive inward rectifier potassium channel 1 | ATP-sensitive inward rectifier potassium channel 1 (Kir1.1 / ROMK) | `KCNJ1` | `P48048` | `CHEMBL1293292` | Inward-rectifier potassium channel | 1,362 / 580 | 200 / 200 |
| **4** | Cholinesterase | Cholinesterase (Butyrylcholinesterase) | `BCHE` | `P06276` | `CHEMBL1914` | Hydrolase (Esterase) | 2,083 / 345 | 200 / 200 |
| **5** | Voltage-gated inwardly rectifying potassium channel KCNH2 | Potassium voltage-gated channel subfamily H member 2 (Kv11.1 / hERG) | `KCNH2` | `Q12809` | `CHEMBL240` | Voltage-gated potassium channel | 5,638 / 464 | 200 / 200 |
| **6** | Sodium-dependent serotonin transporter | Sodium-dependent serotonin transporter (SERT / 5-HTT) | `SLC6A4` | `P31645` | `CHEMBL228` | Electrochemical transporter | 4,929 / 663 | 200 / 200 |

### Naming and Classification Notes
1. **KCNJ1 Classification:** The SwissTargetPrediction export classifies KCNJ1 as a "Voltage-gated ion channel." Canonical nomenclature in UniProtKB and IUPHAR classifies KCNJ1 (Kir1.1 / ROMK) as an **inward-rectifier potassium channel** regulated by intracellular ATP and phosphorylation, not by transmembrane voltage sensors.
2. **KCNH2 Nomenclature:** The SwissTargetPrediction export applies the label "Voltage-gated inwardly rectifying potassium channel KCNH2." While UniProt records this historical full name, the protein is standardly designated **Kv11.1** or **hERG** (*human Ether-à-go-go-Related Gene*). It is functionally a voltage-gated potassium channel that exhibits rapid C-type inactivation producing apparent inward rectification at depolarized potentials.
3. **Training Library Size vs. Exposed Table Interface:** The SwissTargetPrediction web interface exposes at most 200 nearest active compounds per method (200 for 2D FP2 and 200 for 3D electroshape). As shown above, the underlying training pools contain between 345 and 5,638 compounds per target. All analyses here are based on the nearest actives the service reported for this query, and the ChEMBL records those compounds were then traced to.

---

## 3. Reference Structure: PRL-8-53

To evaluate whether source ligands actually preserve the architecture of PRL-8-53, its verified structural features are defined:
- **Systematic Chemical Name:** Methyl 3-[2-[benzyl(methyl)amino]ethyl]benzoate
- **Molecular Formula & Weight:** $\text{C}_{18}\text{H}_{21}\text{NO}_2$ (283.4 g/mol)
- **Canonical SMILES:** `COC(=O)c1cccc(c1)CCN(Cc1ccccc1)C`
- **Standard InChIKey:** `IGJQEMHBYKNIQR-UHFFFAOYSA-N`
- **Core Structural Components:**
  1. *Methyl 3-benzoate ester:* An aromatic methyl ester at the *meta*-position of a benzene ring (`3-MeOOC-C6H4-`).
  2. *Flexible ethylene linker:* A saturated two-carbon chain (`-CH2-CH2-`) linking the benzoate ring to the basic amine.
  3. *Acyclic tertiary methylamine:* An open-chain basic nitrogen bearing a methyl group (`-N(CH3)-`).
  4. *N-benzyl moiety:* A simple phenylmethylene unit attached to the tertiary nitrogen (`-CH2-Ph`).

---

## 4. Source Ligand Trace and Pharmacology per Target

### 4.1 Target Rank 2: OPRM1 (Mu-Type Opioid Receptor)
- **UniProt:** `P35372` | **ChEMBL:** `CHEMBL233`
- **Reported Server Probability:** `0.4058`
- **Known Actives in Server Pool:** 4,157 (3D) / 870 (2D)

#### Nearest 2D Source Active: CHEMBL423726
- **Tool Metric:** FP2 2D Tanimoto similarity = **0.666667** (Rank 1 of 200 exposed 2D rows).
- **Structure:**
  - InChIKey: `MFOJFLGOVDOOCY-FDDCHVKYSA-N`
  - Canonical SMILES: `COC(=O)c1cccc([C@]2(C)CCN(CCc3ccccc3)C[C@@H]2C)c1`
- **Measured Activity:**
  - Activity ID: `879137`
  - Endpoint: $K_i = 850.0\text{ nM}$ ($p\text{ChEMBL} = 6.07$), relation `=`
  - Target: Cloned human mu opioid receptor (`Homo sapiens`)
  - Assay ID: `CHEMBL753397` (Assay type: B)
  - BAO Format: `BAO_0000357` (Single protein format)
  - Assay Description: *Inhibition of binding of the non-selective opioid antagonist, [3H]diprenorphine, to cloned human mu opioid receptor.*
  - Target Assignment Confidence: `8` (Homologous protein target assigned). *Caveat:* ChEMBL confidence 8 indicates an unresolved homologous protein target assignment in the database curation; species/construct mapping is taken from curated database fields rather than verified full-text validation of the cloned cell line.
  - Activity Pagination: Total target-filtered records in ChEMBL 37 = 2 (`total_count: 2`, `next: null`). The second record (Activity ID `879140`) is a functional $[^{35}\text{S}]\text{GTP}\gamma\text{S}$ assay (`CHEMBL754685`) showing no reported agonism.
- **Primary Source:**
  - Publication: Le Bourdonnec et al., *Bioorg Med Chem Lett* 2003, 13(24), 4459–4462.
  - Title: *trans-3,4-dimethyl-4-(3-carboxamidophenyl)piperidines: a novel class of $\mu$-selective opioid antagonists.*
  - Identifiers: DOI `10.1016/j.bmcl.2003.09.012` | PubMed `14643346` | ChEMBL Document `CHEMBL1136497`.
  - Evidence Level: Curated ChEMBL record and publication abstract inspected.
- **Structural Comparison with PRL-8-53:**
  - *Observed Overlap:* CHEMBL423726 contains an authentic **methyl 3-benzoate ester** (`meta`-methoxycarbonyl phenyl ring), matching that of PRL-8-53. It also possesses two aromatic rings and a basic tertiary nitrogen.
  - *Observed Differences:* The nitrogen is part of a rigid *trans*-3,4-dimethylpiperidine ring bearing a quaternary stereocenter at C4. The connection between the aromatic ring and nitrogen is constrained within the piperidine ring rather than an open ethylene chain. The other N-substituent is a phenethyl group (`-CH2-CH2-Ph`) rather than a benzyl group (`-CH2-Ph`).

#### Nearest 3D Source Active: CHEMBL138910
- **Tool Metric:** 3D electroshape/spectrophore similarity = **0.885** (Rank 1 of 200 exposed 3D rows).
- **Structure:**
  - InChIKey: `ZNBUYPLGEXQQGG-QMHKHESXSA-N`
  - Canonical SMILES: `C[C@H]1CN(Cc2cc3ccccc3o2)CC[C@@]1(C)c1cccc(C(N)=O)c1`
- **Measured Activity:**
  - Activity ID: `879141`
  - Endpoint: $K_i = 6.2\text{ nM}$ ($p\text{ChEMBL} = 8.21$), relation `=`
  - Assay ID: `CHEMBL753397` (Radioligand displacement of $[^3\text{H}]\text{diprenorphine}$, confidence 8)
  - Source: Le Bourdonnec et al., 2003 (Document `CHEMBL1136497`).
  - Total Target Activities in ChEMBL 37: 1 (`total_count: 1`, `next: null`).
- **Structural Comparison with PRL-8-53:**
  - *Observed Overlap:* Tertiary basic amine, *meta*-substituted aromatic ring.
  - *Observed Differences:* Substituent is a primary carboxamide (`-C(=O)NH2`), not a methyl ester. Nitrogen is constrained in the *trans*-3,4-dimethylpiperidine core. The pendant group is a benzofuran-2-ylmethyl moiety, not a benzyl group.
- **Synthesis:** Both nearest 2D and 3D ligands for OPRM1 originate from the same 2003 publication (`CHEMBL1136497`). CHEMBL423726 shares an authentic methyl 3-benzoate ester, while the opioid antagonist scaffold is a rigid piperidine.

---

### 4.2 Target Rank 3: KCNJ1 (Inward-Rectifier Potassium Channel Kir1.1 / ROMK)
- **UniProt:** `P48048` | **ChEMBL:** `CHEMBL1293292`
- **Reported Server Probability:** `0.3039`
- **Known Actives in Server Pool:** 1,362 (3D) / 580 (2D)

#### Nearest 2D Source Active: CHEMBL2146870
- **Tool Metric:** FP2 2D Tanimoto similarity = **0.638554** (Rank 1 of 200 exposed 2D rows).
- **Structure:**
  - InChIKey: `PYUXNNYRCHVGKZ-UHFFFAOYSA-N`
  - Canonical SMILES: `O=C1OCc2cc(CCN3CCN(CCc4ccc5c(c4)COC5=O)CC3)ccc21`
- **Measured Activity:**
  - Activity ID: `12040500`
  - Endpoint: $\text{IC}_{50} = 89.0\text{ nM}$ ($p\text{ChEMBL} = 7.05$), relation `=`
  - Target: Human ROMK1 channel expressed in CHO cells (`Homo sapiens`)
  - Assay ID: `CHEMBL2148625` (Assay type: B; BAO Format `BAO_0000219`, cell-based format)
  - Assay Description: *Inhibition of human ROMK1 channel expressed in CHO cells coexpressing DHFR assessed as inhibition of 86Rb+ efflux after 35 mins by TopCount method.*
  - Target Assignment Confidence: `9` (Direct protein target assigned)
  - Additional Activity ID: `12041141`, whole-cell patch-clamp electrophysiology $\text{IC}_{50} = 26.0\text{ nM}$ (`CHEMBL2148630`, confidence 8).
  - Total Target Activities in ChEMBL 37: 3 (`total_count: 3`, `next: null`).
  - *Format Clarification:* Although ChEMBL assigns assay type code `B`, these assays measure cellular rubidium efflux and electrophysiological current inhibition, not direct equilibrium binding affinities ($K_i / K_d$).
- **Primary Source:**
  - Publication: Tang et al., *ACS Med Chem Lett* 2012, 3(5), 367–372.
  - Title: *Discovery of Selective Small Molecule ROMK Inhibitors as Potential New Mechanism Diuretics.*
  - Identifiers: DOI `10.1021/ml3000066` | PubMed `24900480` | ChEMBL Document `CHEMBL2146432`.
- **Structural Comparison with PRL-8-53:**
  - *Observed Overlap:* Two aromatic systems, basic nitrogen atoms, saturated two-carbon chains (`-CH2-CH2-`).
  - *Observed Differences:* Symmetrical **bis-isobenzofuranone (bis-phthalide) piperazine**. It possesses two cyclic lactone rings (isobenzofuran-1-ones) rather than an acyclic methyl ester. The amine core is a 1,4-piperazine ring, not an acyclic benzyl(methyl)amino group.

#### Nearest 3D Source Active: CHEMBL6050195
- **Tool Metric:** 3D electroshape/spectrophore similarity = **0.886** (Rank 1 of 200 exposed 3D rows).
- **Structure:**
  - InChIKey: `IQIUGONRJBMMDL-UHFFFAOYSA-N`
  - Canonical SMILES: `CN(Cc1ccc(-c2ccc(C#N)c(F)c2)cc1)Cc1ccc2c(c1)COC2=O`
- **Measured Activity:**
  - Activity ID: `28069241`
  - Endpoint: $\text{IC}_{50} = 3300.0\text{ nM}$ ($3.3\ \mu\text{M}$; $p\text{ChEMBL} = 5.48$), relation `=`
  - Assay ID: `CHEMBL5735582` (Assay type: B; BAO Format `BAO_0000019`, cell-based format)
  - Assay Description: *Thallium flux assay in CHO T-Rex hROMK (human Kir1.1) stable cell line using FluxOR dye.*
  - Target Assignment Confidence: `9` (Direct protein target assigned)
  - Total Target Activities in ChEMBL 37: 3 (`total_count: 3`, `next: null`).
  - *Format Clarification:* This endpoint reflects fluorometric cellular ion flux inhibition, not direct receptor binding.
- **Primary Source:**
  - Patent: US Patent 10,723,723-B2 (issued July 28, 2020; ChEMBL Document `CHEMBL5727875`).
  - Title: *Substituted bicycle heterocyclic derivatives useful as ROMK channel inhibitors.*
- **Structural Comparison with PRL-8-53:**
  - *Observed Overlap:* Contains an acyclic tertiary methylamine (`-N(CH3)-`) and an N-benzyl-like group attached to the nitrogen (`-CH2-c1ccc(-c2ccc(C#N)c(F)c2)cc1`).
  - *Observed Differences:* One aromatic arm is a phthalide lactone rather than an aromatic methyl ester. The benzyl-like arm carries a 4-(4-cyano-3-fluorophenyl) substituent. Both aromatic rings are connected to nitrogen via single methylene spacers (`-CH2-N(Me)-CH2-`), lacking PRL-8-53's two-carbon ethylene linker.

---

### 4.3 Target Rank 4: BCHE (Cholinesterase / Butyrylcholinesterase)
- **UniProt:** `P06276` | **ChEMBL:** `CHEMBL1914`
- **Reported Server Probability:** `0.3010`
- **Known Actives in Server Pool:** 2,083 (3D) / 345 (2D)

#### Nearest 2D Source Active: CHEMBL5592832
- **Tool Metric:** FP2 2D Tanimoto similarity = **0.64557** (Rank 1 of 200 exposed 2D rows).
- **Structure:**
  - InChIKey: `WMFDQTBZMDBZMV-UHFFFAOYSA-N`
  - Canonical SMILES: `c1ccc(CCNCc2ccc(OCc3ccccc3)cc2)cc1`
  - Systematic Chemical Identity: N-(4-(benzyloxy)benzyl)-2-phenylethan-1-amine (secondary monoamine)
- **Measured Activity:**
  - Activity ID: `25945381`
  - Endpoint: $\text{IC}_{50} = 2000.0\text{ nM}$ ($2.0\ \mu\text{M}$; $p\text{ChEMBL} = 5.70$), relation `=`
  - Additional Endpoint: Activity ID `25945328`, $81.0\%$ inhibition at $10\ \mu\text{M}$ (`CHEMBL5535548`).
  - Target: Human butyrylcholinesterase (`Homo sapiens`)
  - Assay ID: `CHEMBL5535554` (Assay type: B; BAO Format `BAO_0000357`, single protein format)
  - Assay Description: *Inhibition of human BChE using butyrylthiocholine iodide as substrate incubated for 1 mins by spectrophotometric Ellman's method.*
  - Target Assignment Confidence: `9` (Direct protein target assigned)
  - Total Target Activities in ChEMBL 37: 2 (`total_count: 2`, `next: null`).
  - *Format Clarification:* The endpoint is a spectrophotometric substrate-turnover enzyme-inhibition $\text{IC}_{50}$, not a binding dissociation constant.
- **Primary Source:**
  - Publication: Pidany et al., *RSC Med Chem* 2024, 15(7), 2378–2388.
  - Title: *Carltonine-derived compounds for targeted butyrylcholinesterase inhibition.*
  - Identifiers: DOI `10.1039/d4md00060a` | PubMed `38784455` | ChEMBL Document `CHEMBL5532688`.
- **Structural Comparison with PRL-8-53:**
  - *Observed Overlap:* Phenethyl group (`PhCH2CH2-`), basic nitrogen, aromatic benzyl-like unit.
  - *Observed Differences:* **Secondary monoamine** (`-NH-`) containing exactly one nitrogen atom, not a tertiary methylamine. It carries a **benzyloxy ether** (`-O-CH2Ph`) and completely lacks an ester carbonyl group.

#### Nearest 3D Source Active: CHEMBL5542214
- **Tool Metric:** 3D electroshape/spectrophore similarity = **0.863** (Rank 1 of 200 exposed 3D rows).
- **Structure:**
  - InChIKey: `PITGQRKFJHYWAE-UHFFFAOYSA-N`
  - Canonical SMILES: `c1ccc(CNCc2cccc(OCc3ccccc3)c2)cc1`
  - Systematic Chemical Identity: N-benzyl-1-(3-(benzyloxy)phenyl)methanamine (secondary monoamine)
- **Measured Activity:**
  - Activity ID: `25945359`
  - Endpoint: $\text{IC}_{50} = 500.0\text{ nM}$ ($p\text{ChEMBL} = 6.30$), relation `=`
  - Additional Endpoint: Activity ID `25945306`, $92.0\%$ inhibition at $10\ \mu\text{M}$ (`CHEMBL5535548`).
  - Source: Pidany et al., 2024 (Document `CHEMBL5532688`).
  - Total Target Activities in ChEMBL 37: 2 (`total_count: 2`, `next: null`).
- **Structural Comparison with PRL-8-53:**
  - *Observed Overlap:* Benzyl group (`PhCH2-NH-`), *meta*-substituted benzene ring.
  - *Observed Differences:* Secondary monoamine (`-NH-`) containing one nitrogen atom. The *meta*-substituent is a benzyloxy ether, not an ester, and the linker is a single methylene unit.
- **Synthesis:** Both top 2D and 3D actives for BCHE originate from the same 2024 publication on carltonine derivatives (`CHEMBL5532688`). Both compounds are secondary monoamine benzyl ethers that lack the ester carbonyl and tertiary methylamine of PRL-8-53.

---

### 4.4 Target Rank 5: KCNH2 (Voltage-Gated Potassium Channel Kv11.1 / hERG)
- **UniProt:** `Q12809` | **ChEMBL:** `CHEMBL240`
- **Reported Server Probability:** `0.3004`
- **Known Actives in Server Pool:** 5,638 (3D) / 464 (2D)

#### Nearest 2D Source Active: CHEMBL2146870 (Cross-Target Shared Compound)
- **Tool Metric:** FP2 2D Tanimoto similarity = **0.638554** (Rank 1 of 200 exposed 2D rows).
- **Structure:**
  - InChIKey: `PYUXNNYRCHVGKZ-UHFFFAOYSA-N`
  - Canonical SMILES: `O=C1OCc2cc(CCN3CCN(CCc4ccc5c(c4)COC5=O)CC3)ccc21`
- **Shared Compound Observation:** CHEMBL2146870 is the identical chemical compound identified as the rank-1 2D active for KCNJ1 (ROMK).
- **Measured Activity on KCNH2:**
  - Activity ID: `12041121`
  - Endpoint: $\text{IC}_{50} = 1900.0\text{ nM}$ ($1.9\ \mu\text{M}$; $p\text{ChEMBL} = 5.72$), relation `=`
  - Target: Human ERG (`Homo sapiens`)
  - Assay ID: `CHEMBL2148626` (Assay type: B; BAO Format `BAO_0000357`)
  - Assay Description: *Displacement of [35S]MK499 from human ERG.*
  - Target Assignment Confidence: `9` (Direct protein target assigned)
  - Secondary Activity: Activity ID `19410796`, $\text{IC}_{50} = 1900.0\text{ nM}$ (`CHEMBL4427468` in Tang et al., 2016, `CHEMBL4425169`).
  - Total Target Activities in ChEMBL 37: 2 (`total_count: 2`, `next: null`).
- **Primary Source:**
  - Source: Tang et al., *ACS Med Chem Lett* 2012 (ChEMBL Document `CHEMBL2146432`).
- **Context and Analytical Caveats:**
  - *Origin of Record:* In Tang et al. (2012), this compound was assayed against hERG as an off-target counterscreen during optimization of ROMK inhibitors.
  - *Endpoint Comparison:* The source study reported an $\text{IC}_{50}$ of $89\text{ nM}$ in a cell-based $^{86}\text{Rb}^+$ efflux assay for ROMK versus an $\text{IC}_{50}$ of $1,900\text{ nM}$ in a radioligand displacement binding assay for hERG. These two numbers reflect in vitro selectivity across two distinct assay formats within that medicinal chemistry program; they do not represent a clinical or human safety margin.
  - *Validity of Data:* A measured in vitro off-target interaction remains valid empirical data regardless of whether it was generated in a primary optimization or counterscreening setting.
  - *Ascertainment Consideration:* The frequent counterscreening of basic amine lead compounds against hERG in drug discovery creates a large volume of hERG activity records in ChEMBL. This library density is a possible ascertainment factor in target prediction ranking, but it does not invalidate individual measured endpoints or prove that the prediction is false. No inference regarding PRL-8-53 safety or toxicity is made.

#### Nearest 3D Source Active: CHEMBL1779004
- **Tool Metric:** 3D electroshape/spectrophore similarity = **0.883** (Rank 1 of 200 exposed 3D rows).
- **Structure:**
  - InChIKey: `KSYYFCDUINESKT-UHFFFAOYSA-N`
  - Canonical SMILES: `COc1cc(F)ccc1-c1cccc(CNC2CCCC2)c1`
- **Measured Activity on KCNH2:**
  - Activity ID: `6210365`
  - Endpoint: $\text{IC}_{50} = 2150.0\text{ nM}$ ($2.15\ \mu\text{M}$; $p\text{ChEMBL} = 5.67$), relation `=`
  - Target: Human ERG expressed in CHO-K1 cells (`Homo sapiens`)
  - Assay ID: `CHEMBL1781193` (Assay type: B; BAO Format `BAO_0000219`, cell-based format)
  - Assay Description: *Inhibition of human ERG expressed in CHOK1 cells electrophysiology study.*
  - Total Target Activities in ChEMBL 37: 1 (`total_count: 1`, `next: null`).
  - *Format Clarification:* The endpoint is whole-cell planar patch-clamp electrophysiology, not a radioligand binding affinity.
- **Primary Source:**
  - Publication: Brown et al., *Bioorg Med Chem Lett* 2011, 21(11), 3326–3330.
  - Title: *2,6-Disubstituted pyrazines and related analogs as NR2B site antagonists of the NMDA receptor with anti-depressant activity.*
  - Identifiers: DOI `10.1016/j.bmcl.2011.03.117` | PubMed `21524576` | ChEMBL Document `CHEMBL1777674`.
  - *Context:* Assayed as an in vitro cardiac liability counterscreen during optimization of NMDA receptor antagonists.
- **Structural Comparison with PRL-8-53:**
  - Secondary cyclopentylamine (`-CH2-NH-c-Pentyl`) on a fluoro/methoxy-substituted biphenyl core. Lacks an ester, tertiary methylamine, and benzyl groups.

---

### 4.5 Target Rank 6: SLC6A4 (Sodium-Dependent Serotonin Transporter / SERT)
- **UniProt:** `P31645` | **ChEMBL:** `CHEMBL228`
- **Reported Server Probability:** `0.2695`
- **Known Actives in Server Pool:** 4,929 (3D) / 663 (2D)

#### Nearest 2D Source Active: CHEMBL379536
- **Tool Metric:** FP2 2D Tanimoto similarity = **0.614458** (Rank 1 of 200 exposed 2D rows).
- **Structure:**
  - InChIKey: `AGCDRDCNYZHHKS-UHFFFAOYSA-N`
  - Canonical SMILES: `NC(=O)c1cccc(CC(c2ccccc2)N2CCNCC2)c1`
- **Measured Activity:**
  - Activity ID: `1755283`
  - Endpoint: $\text{IC}_{50} = 210.0\text{ nM}$ ($p\text{ChEMBL} = 6.68$), relation `=`
  - Target: Human serotonin transporter expressed in HEK293 cells (`Homo sapiens`)
  - Assay ID: `CHEMBL869834` (Assay type: B; BAO Format `BAO_0000219`, cell-based format)
  - Assay Description: *Inhibition of [3H]5-HT uptake at 5HT transporter expressed in HEK293 cells.*
  - Target Assignment Confidence: `9` (Direct protein target assigned)
  - Total Target Activities in ChEMBL 37: 1 (`total_count: 1`, `next: null`).
  - *Format Clarification:* The endpoint is cellular neurotransmitter uptake inhibition, not equilibrium binding.
- **Primary Source:**
  - Publication: Fray et al., *Bioorg Med Chem Lett* 2006, 16(16), 4420–4424.
  - Title: *N-(1,2-diphenylethyl)piperazines: a new class of dual serotonin/noradrenaline reuptake inhibitor.*
  - Identifiers: DOI `10.1016/j.bmcl.2006.05.051` | PubMed `16750359` | ChEMBL Document `CHEMBL1146859`.
- **Structural Comparison with PRL-8-53:**
  - 1,2-diphenylethyl piperazine bearing a primary *meta*-carboxamide (`-C(=O)NH2`). Lacks an ester and an open-chain tertiary methylamine.

#### Nearest 3D Source Active: CHEMBL579056
- **Tool Metric:** 3D electroshape/spectrophore similarity = **0.926** (Rank 1 of 200 exposed 3D rows).
- **Structure:**
  - InChIKey: `NGSZLOCYHZRIMB-UHDQLFAASA-N`
  - Canonical SMILES: `COC(=O)[C@@H]1C2CCC(C[C@@H]1c1ccc(SC)cc1)N2C`
  - Systematic Chemical Identity: Methyl (1R,2S,3S,5S)-3-(4-(methylthio)phenyl)-8-methyl-8-azabicyclo[3.2.1]octane-2-carboxylate ($3\beta$-phenyltropane)
- **Measured Activity:**
  - Activity ID: `2918210`
  - Endpoint: $K_i = 0.70\text{ nM}$ ($p\text{ChEMBL} = 9.15$), relation `=`
  - Target: Cloned human serotonin transporter (`Homo sapiens`)
  - Assay ID: `CHEMBL1040429` (Assay type: B; BAO Format `BAO_0000357`, single protein format)
  - Assay Description: *Displacement of [3H]paroxetine from 5-HTT.*
  - Target Assignment Confidence: `8` (Homologous protein target assigned). *Caveat:* Confidence 8 indicates an unresolved homologous protein target assignment in ChEMBL; species/construct details reflect database curation.
  - Total Target Activities in ChEMBL 37: 1 (`total_count: 1`, `next: null`).
- **Primary Source:**
  - Publication: Jin et al., *Bioorg Med Chem* 2009, 17(14), 5126–5135.
  - Title: *Synthesis and structure-activity relationship of $3\beta$-(4-alkylthio, -methylsulfinyl, and -methylsulfonylphenyl)tropane and $3\beta$-(4-alkylthiophenyl)nortropane derivatives for monoamine transporters.*
  - Identifiers: DOI `10.1016/j.bmc.2009.05.052` | PubMed `19523837` | ChEMBL Document `CHEMBL1154083`.
- **Structural Comparison with PRL-8-53:**
  - *Observed Overlap:* Possesses an aliphatic methyl ester (`-C(=O)OCH3`), an N-methyl basic nitrogen (`-N(CH3)-`), and a substituted phenyl ring.
  - *Observed Differences:* Scaffold is a rigid $3\beta$-phenyltropane (cocaine analog). The methyl ester is attached to the bicyclic alicyclic ring at C2, rather than an aromatic ring. The nitrogen is constrained in an 8-azabicyclo[3.2.1]octane bicycle. There is no benzyl substituent.
  - *Interpretation:* The 3D similarity score reflects spatial overlap computed by the electroshape algorithm; this metric is a geometric descriptor and does not demonstrate an identical binding pose or shared pharmacophore in the transporter.

#### Exposed Dual Active: CHEMBL201666 (Aromatic Methyl Ester Preserved)
- **Presence in Exposed Lists:** Rank 4 in exposed 2D list (FP2 = **0.539326**); Rank 3 in exposed 3D list (3D score = **0.919**).
- **Structure:**
  - InChIKey: `RUCXEVOCSDADAL-UHFFFAOYSA-N`
  - Canonical SMILES: `CCCC(C(=O)c1ccc(C(=O)OC)cc1)N1CCCC1`
  - Systematic Chemical Identity: Methyl 4-(2-(pyrrolidin-1-yl)pentanoyl)benzoate (pyrovalerone analog)
- **Measured Activities:**
  - Activity ID: `1682463`, $K_i = 3650.0\text{ nM}$ ($3.65\ \mu\text{M}$; $p\text{ChEMBL} = 5.44$), displacement of $[^{125}\text{I}]\text{RTI-55}$ from human SERT (`CHEMBL859238`, confidence 9).
  - Activity ID: `1682494`, $\text{IC}_{50} = 2350.0\text{ nM}$ ($2.35\ \mu\text{M}$; $p\text{ChEMBL} = 5.63$), inhibition of $[^3\text{H}]\text{5-HT}$ uptake (`CHEMBL859242`, confidence 9).
  - Total Target Activities in ChEMBL 37: 2 (`total_count: 2`, `next: null`).
- **Primary Source:**
  - Publication: Meltzer et al., *J Med Chem* 2006, 49(4), 1420–1432.
  - Identifiers: DOI `10.1021/jm050797a` | PubMed `16480278` | ChEMBL Document `CHEMBL1138144`.
- **Significance:** CHEMBL201666 confirms that a compound containing an **aromatic methyl ester** (`-c1ccc(C(=O)OC)cc1`) exhibits measured micromolar binding and uptake inhibition ($2.35$–$3.65\ \mu\text{M}$) against human SERT in vitro. This observation shows that aromatic esters can be accommodated in this chemotype, but it does not establish a causal rule regarding the effect of an ester in other scaffolds.

---

## 5. Comparative Synthesis: Evidence and Methodological Nuances

The following synthesis compares the structural and pharmacological observations across all five audited hypotheses.

| Target | Rank | Predicted Probability | Nearest 2D Active | FP2 Score | Nearest 3D Active | 3D Score | Methyl Benzoate Preserved? | Tertiary Amine Preserved? | Nature of Primary Evidence | Methodological Notes & Limitations |
|---|:---:|:---:|---|:---:|---|:---:|:---:|:---:|---|---|
| **OPRM1** | 2 | 0.4058 | CHEMBL423726 | 0.6667 | CHEMBL138910 | 0.885 | **Yes** (in 2D: *meta*-ester) | Constrained (piperidine) | Single 2003 publication (`CHEMBL1136497`) of *trans*-3,4-dimethylpiperidine opioid antagonists ($K_i = 850\text{ nM}$ for ester) | Nearest 2D ligand carries *meta*-ester; amine is embedded in rigid piperidine core with N-phenethyl group. |
| **KCNJ1** | 3 | 0.3039 | CHEMBL2146870 | 0.6386 | CHEMBL6050195 | 0.886 | **No** (phthalide lactones) | Symmetrical diamine / tertiary | ROMK diuretic program ($\text{IC}_{50} = 26$–$89\text{ nM}$ in efflux/patch-clamp) | Symmetrical bis-phthalide piperazine pore-blocker; 3D ligand contains N-methyl and benzyl-like group. |
| **BCHE** | 4 | 0.3010 | CHEMBL5592832 | 0.6456 | CHEMBL5542214 | 0.863 | **No** (benzyloxy ethers) | **No** (secondary monoamines) | Single 2024 publication (`CHEMBL5532688`) on carltonine derivatives ($\text{IC}_{50} = 0.5$–$2.0\ \mu\text{M}$) | Secondary monoamines with benzyloxy ether groups; lacks ester carbonyl. |
| **KCNH2** | 5 | 0.3004 | CHEMBL2146870 | 0.6386 | CHEMBL1779004 | 0.883 | **No** (phthalide lactone / biphenyl) | Piperazine / secondary | Measured in vitro counterscreens ($\text{IC}_{50} = 1.9$–$2.15\ \mu\text{M}$) from ROMK and NMDA receptor programs | **Shared ligand** with KCNJ1; off-target screens provide valid measured data, though training set density may reflect library ascertainment bias. |
| **SLC6A4** | 6 | 0.2695 | CHEMBL379536 | 0.6145 | CHEMBL579056 | 0.926 | Alicyclic ester in 3D; aromatic in CHEMBL201666 | Constrained (tropane / pyrrolidine) | $3\beta$-phenyltropanes ($K_i = 0.7\text{ nM}$) and pyrovalerones ($K_i = 3.65\ \mu\text{M}$) | High 3D score reflects shape overlap with cocaine analogs; pyrovalerone analog confirms aromatic ester accommodation in vitro. |

### Cross-Cutting Patterns
1. **Cross-Target Shared Compound:** CHEMBL2146870 is the top-ranked 2D active for **both KCNJ1 and KCNH2**. It is a symmetrical bis-phthalide piperazine evaluated for ROMK inhibition and counterscreened against hERG.
2. **Within-Target Shared Sources:**
   - Both OPRM1 top actives (CHEMBL423726 and CHEMBL138910) originate from the same 2003 publication (`CHEMBL1136497`).
   - Both BCHE top actives (CHEMBL5592832 and CHEMBL5542214) originate from the same 2024 publication (`CHEMBL5532688`).
3. **Ascertainment Bias vs. Empirical Validity:** The high representation of hERG (KCNH2) in pharmaceutical databases reflects routine cardiac safety counterscreening of basic amine lead series. This library bias is a possible contributing factor to the high predicted rank, but does not alter the empirical validity of the measured in vitro activity of the source ligands.
4. **Structural Differences:** Several high-ranking source ligands feature rigid scaffolds (*trans*-3,4-dimethylpiperidine, 8-azabicyclo[3.2.1]octane, bis-phthalide piperazine), whereas PRL-8-53 contains an open-chain, flexible benzyl(methyl)aminoethyl linker. These topological differences are observed structural facts; whether they permit or preclude productive pocket interactions remains an unmodeled question.

---

## 6. Provisional Evidence Assessment and Remaining Checks

This audit provides a provisional comparison of evidence and remaining checks, not a validated biological ranking.

### Provisional Assessment
1. **Candidates for Potential Structural Investigation:**
   - **SLC6A4 (SERT):** High 3D shape similarity to phenyltropanes and documented micromolar in vitro activity for an aromatic methyl ester analog (CHEMBL201666, $K_i = 3.65\ \mu\text{M}$).
   - **OPRM1:** Authentic presence of the *meta*-methoxycarbonyl phenyl group in nearest 2D active CHEMBL423726 ($K_i = 850\text{ nM}$).
2. **Unresolved Hypotheses:**
   - **KCNH2 (hERG):** Possesses measured micromolar activity in nearest source ligands, though identified through counterscreening contexts. It remains unresolved whether PRL-8-53 interacts with the hERG pore.
   - **KCNJ1 (ROMK):** Driven by bis-phthalide pore blockers. It remains unresolved whether compounds lacking phthalide lactones interact with this channel.
   - **BCHE:** Supported by lipophilic secondary monoamine benzyl ethers. It remains unresolved whether PRL-8-53 inhibits or binds cholinesterases.

### Remaining Checks and Immediate Structural Verification Steps
If computational structural modeling is pursued beyond ACACB, experimental structure verification is the necessary first step rather than assuming docking coordinates:
1. **Experimental Structure Validation:** High-resolution experimental structures (cryo-EM or X-ray crystallography) must be verified for the specific target species (human vs. rodent constructs). For example, rodent mu-opioid structures (such as mouse OPRM1 crystal structures) cannot be assumed to be identical to human OPRM1 without sequence alignment and residue numbering validation.
2. **State and Pocket Definition:** The receptor conformational state (active vs. inactive, agonist-bound vs. antagonist-bound) and specific coordinate definitions must be established before running docking pilots.
3. **Conformational Analysis:** Modeling must evaluate whether PRL-8-53's flexible chain can adopt favorable conformations within candidate pockets without excessive conformational strain.
4. **Direct Experimental Testing Required:** Algorithmic target prediction scores and similarity metrics cannot confirm binding, non-binding, or functional efficacy. Direct experimental binding assays remain required to determine whether PRL-8-53 interacts with any of these proteins.
