# Methods Review: Computational Target Deconvolution and Uncertainty Estimation

**Compound:** PRL-8-53 (methyl 3-[2-[benzyl(methyl)amino]ethyl]benzoate; free base CAS 51352-88-6 / HCl salt CAS 51352-87-5)
**Date of Access Checks:** 2026-09-22 (approx. 22:18–22:21 EDT / 2026-09-23 02:18–02:21 UTC)
**Status:** Exploratory Methods Review & Uncertainty Assessment
**Author:** Hasan Ugur (Rolf) Yildirim

---

## 1. Executive Summary & Problem Formulation

The goal of this project is to identify candidate macromolecular targets of PRL-8-53 using computational methods only, without wet-laboratory assays, and to report the outcome honestly whatever it turns out to be. The primary hazard in computational target deconvolution is confirmation bias: adopting an appealing receptor hypothesis from informal literature or speculative preprint titles and interpreting computational scores as confirmation.

This review evaluates:
1. The operational access, data sources, inputs, outputs, and terms of service for accessible target-prediction tools and databases.
2. The extent to which multi-tool concordance reflects shared training datasets (pseudoreplication) rather than independent evidence.
3. The statistical meaning of prediction scores, differentiating conditional target rankings from physical probabilities of binding.
4. The biophysical limits of molecular docking, explaining why docking cannot establish binding, why raw scores cannot be compared across different proteins, and why static docking cannot determine agonism versus antagonism.
5. Literature-derived calibration conventions (such as property-matched decoy distributions and control ligands), treating them as exploratory benchmarks rather than hard scientific pass/fail criteria.
6. Physicochemical uncertainties regarding ligand protonation and receptor conformational state.

---

## 2. Verified Tool and Resource Assessment

Each tool below was directly probed on 2026-09-22 between 22:18 and 22:21 EDT (2026-09-23 02:18–02:21 UTC). Web reachability (HTTP 200 on an index page) is strictly distinguished from verified execution of prediction jobs.

### 2.1 SwissTargetPrediction

*   **URL:** `https://www.swisstargetprediction.ch/` (redirects from `http://www.swisstargetprediction.ch/`).
*   **Reachability Checked:** HTTP/1.1 200 OK verified on 2026-09-22 at 22:18:57 EDT (2026-09-23 02:18:57 UTC; server: Apache/2.4.58 on Ubuntu).
*   **Methodology & Underlying Data:**
    *   *Algorithm:* Hybrid 2D and 3D similarity matching. 2D similarity uses path-based fingerprints (FP2 via Open Babel) and Tanimoto coefficients. 3D similarity uses Electroshape 5D (ES5D), evaluating shape, charge, and lipophilicity centroids across up to 20 conformers generated via Marvin.
    *   *Calibration:* Combines 2D and 3D scores using a logistic regression model trained to estimate the probability that a target is correct, *conditional on the premise that the compound is active against at least one target in the reference set*.
    *   *Data Source:* Curated bioactivity data from ChEMBL covering *Homo sapiens*, *Mus musculus*, and *Rattus norvegicus*.
*   **Inputs & Outputs:**
    *   *Input:* SMILES string or molecular sketcher (MarvinJS).
    *   *Output:* Table of ranked targets with common name, UniProt ID, ChEMBL ID, target class, known active ligand counts, and 2D/3D similarity scores to the nearest known active.
*   **Exportability & Access:** Interactive browser interface with CSV and PDF export options. No public programmatic REST API is documented. Query submissions post to backend scripts (`predict.php`).
*   **Terms of Use & Licensing:** SIB Terms of Use (last updated November 28, 2023) make licensed materials available under CC-BY 4.0 International, and restrict how the service may be accessed and how much of the licensed material may be collected. Only ordinary interactive use of the web form is in scope for this project, and the service's result material is not redistributed here; see [`docs/target-shortlist.md`](../docs/target-shortlist.md).
*   **Key Literature:**
    *   Daina A, Michielin O, Zoete V. *SwissTargetPrediction: updated data and new features for efficient prediction of protein targets of small molecules.* Nucleic Acids Res. 2019;47(W1):W357-W364. DOI: [10.1093/nar/gkz382](https://doi.org/10.1093/nar/gkz382).
    *   Daina A, Zoete V. *Testing the predictive power of reverse screening to infer drug targets, with the help of machine learning.* Commun Chem. 2024;7:105. DOI: [10.1038/s42004-024-01179-2](https://doi.org/10.1038/s42004-024-01179-2).
    *   Gfeller D, Michielin O, Zoete V. *Shaping the interaction landscape of bioactive molecules.* Bioinformatics. 2013;29(23):3073-3079. DOI: [10.1093/bioinformatics/btt536](https://doi.org/10.1093/bioinformatics/btt536).
*   **Core Methodological Limitation:** The service documentation (`about.php`) explicitly notes that the algorithm operates on small molecules "assumed as bioactive". If an inactive or non-binding compound is submitted, the platform still outputs a ranked list of targets with assigned probabilities. It cannot assess whether a compound is inert.

---

### 2.2 SEA (Similarity Ensemble Approach)

*   **URL:** `https://sea.bkslab.org/` (and `http://sea.bkslab.org/`).
*   **Reachability Checked:** HTTP/2 200 OK verified on 2026-09-22 at 22:19:33 EDT (2026-09-23 02:19:33 UTC; server: uvicorn).
*   **Methodology & Underlying Data:**
    *   *Algorithm:* Set-wise chemical similarity. Rather than evaluating only the single nearest neighbor, SEA calculates pairwise Tanimoto coefficients (using topological circular fingerprints such as ECFP4) between the query molecule and all annotated ligands for each target in ChEMBL.
    *   *Statistical Formulation:* The sum of pairwise similarities above a threshold is compared against an empirical model of random chemical background similarity to calculate a Z-score, which is converted to an Expectation value ($E$-value) using an Extreme Value Distribution (EVD).
*   **Inputs & Outputs:**
    *   *Input:* SMILES string and compound identifier.
    *   *Output:* Ranked targets with raw similarity sums, Z-scores, and statistical $E$-values.
*   **Access & Operational Caveats:** While an OpenAPI 3.1 specification is reachable at `/openapi.json`, the web interface integrates an Altcha cryptographic proof-of-work challenge (`/api/captcha/challenge`). Headless automated POST requests without challenge tokens will fail. Interactive browser submission is the accessible route.
*   **Terms & Licensing:** Academic web tool supported by NIGMS (GM71896) and the University of California Regents (Shoichet and Irwin Labs). Free for research use.
*   **Key Literature:**
    *   Keiser MJ, Roth BL, Armbruster BN, Ernsberger P, Irwin JJ, Shoichet BK. *Relating protein pharmacology by ligand chemistry.* Nat Biotechnol. 2007;25(2):197-206. DOI: [10.1038/nbt1284](https://doi.org/10.1038/nbt1284).
    *   Keiser MJ, Setola V, Irwin JJ, et al. *Predicting new molecular targets for known drugs.* Nature. 2009;462(7270):175-181. DOI: [10.1038/nature08506](https://doi.org/10.1038/nature08506).

---

### 2.3 ChEMBL REST API & Registry Baseline

*   **URL:** `https://www.ebi.ac.uk/chembl/api/data/` (status endpoint: `https://www.ebi.ac.uk/chembl/api/data/status`).
*   **Reachability Checked:** HTTP/2 200 OK verified on 2026-09-22 at 22:20:37 EDT (2026-09-23 02:20:37 UTC).
*   **Database Version:** `ChEMBL_37` (release date: 2026-05-01; reporting 2,921,148 distinct compounds, 24,527,044 activities, and 18,552 targets).
*   **Role in Research:** ChEMBL is the primary public repository of curated medicinal chemistry literature that forms the training corpus for SwissTargetPrediction, SEA, and related tools. Querying ChEMBL directly allows inspection of the exact empirical data supporting any target prediction.
*   **License & Publication:** CC BY-SA 3.0. Citation:
    *   Zdrazil B, Felix E, Hunter F, et al. *The ChEMBL Database in 2024.* Nucleic Acids Res. 2024;52(D1):D1180-D1192. DOI: [10.1093/nar/gkad1004](https://doi.org/10.1093/nar/gkad1004).

#### Verified Empirical Queries for PRL-8-53 (Performed 2026-09-22 and reviewed 2026-09-23)
To establish the baseline presence of PRL-8-53 in ChEMBL and PubChem, specific API endpoints were queried using the identifiers confirmed in the integrated identity review:
1.  **ChEMBL InChIKey Structure Lookups:**
    *   Query: `https://www.ebi.ac.uk/chembl/api/data/molecule.json?molecule_structures__standard_inchi_key=IGJQEMHBYKNIQR-UHFFFAOYSA-N` (free base).
        *   *Result:* HTTP 200 OK; `page_meta.total_count: 0`; `molecules: []`.
    *   Query: `https://www.ebi.ac.uk/chembl/api/data/molecule.json?molecule_structures__standard_inchi_key=HLBBSWSJLPLPRU-UHFFFAOYSA-N` (HCl salt).
        *   *Result:* HTTP 200 OK; `page_meta.total_count: 0`; `molecules: []`.
2.  **PubChem BioAssay Lookups:**
    *   Query: `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/39989/assaysummary/JSON` (free base CID 39989).
        *   *Result:* HTTP 404 with JSON payload: `{"Fault": {"Code": "PUGREST.NotFound", "Message": "No assay data found for the given ID(s)"}}`.
    *   Query: `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/70700868/assaysummary/JSON` (HCl salt CID 70700868).
        *   *Result:* HTTP 404 with JSON payload: `{"Fault": {"Code": "PUGREST.NotFound", "Message": "No assay data found for the given ID(s)"}}`.
3.  **ChEMBL Similarity Search (free-base SMILES: `CN(CCc1cccc(c1)C(=O)OC)Cc2ccccc2`):**
    *   At 70% threshold (`.../similarity/{smiles}/70.json`): `total_count: 0`.
    *   At 60% threshold (`.../similarity/{smiles}/60.json`): `total_count: 1` (`CHEMBL5941544`, similarity 60.98%).
    *   At 50% threshold (`.../similarity/{smiles}/50.json`): `total_count: 30` (page limit 20; retrieved 20 records on page 1).
4.  **Inspection of the sole 60% result (2026-09-23T02:34:45Z):**
    *   Molecule query: `https://www.ebi.ac.uk/chembl/api/data/molecule/CHEMBL5941544.json`.
    *   Activity query: `https://www.ebi.ac.uk/chembl/api/data/activity.json?molecule_chembl_id=CHEMBL5941544&limit=100`.
    *   CHEMBL5941544 is methyl 3-(2-hydroxyethyl)benzoate (`COC(=O)c1cccc(CCO)c1`), a 180.20 Da molecule lacking PRL-8-53's tertiary amine and benzyl group.
    *   Its six ChEMBL activity rows reduce to two standard IC50 results from document CHEMBL5729164: 69 nM at CYP4F2 and 210 nM at CYP4A11; the other four rows are non-standard empty kinetic fields.
    *   These are measurements of CHEMBL5941544, not PRL-8-53, and do not support either enzyme as a PRL-8-53 target.

*Interpretation & Scope Note:* Under the confirmed identifiers tested, ChEMBL 37 has no exact molecule record and PubChem BioAssay returns no assay data. Near results are sparse under this ChEMBL similarity metric, and the sole 60% result loses the amine-containing half of PRL-8-53. This bounded result does not show that every representation or pharmacophore model is outside its domain, but it supplies no binding evidence for PRL-8-53.

---

### 2.4 Other Candidate Tools Checked

*   **PharmMapper (`http://lilab-ecust.cn/pharmmapper/`):**
    *   *Reachability:* HTTP 200 OK verified on 2026-09-22 at 22:20:30 EDT (2026-09-23 02:20:30 UTC).
    *   *Methodology:* Reverse pharmacophore mapping using 3D cavity models derived from PDB structures (Cavity 1.1 / Pocket 4.0).
    *   *Terms:* Strictly non-commercial academic use ("PharmMapper may NOT be used for commercial purposes").
    *   *Citations:* Liu et al. Nucleic Acids Res. 2010;38:W609-W614; Wang et al. Nucleic Acids Res. 2017;45:W356-W360.
*   **TargetNet (`http://targetnet.scbdd.com/` / `https://targetnet.scbdd.com/`):**
    *   *Reachability:* Plain HTTP (`http://targetnet.scbdd.com/`) verified HTTP 200 OK on 2026-09-22 at 22:20:24 EDT.
    *   *TLS Status:* HTTPS on port 443 **failed TLS certificate verification** (`curl: (60) SSL certificate problem: certificate has expired`). In accordance with policy, no certificate bypasses or insecure flags will be used. Only plain HTTP is reachable.
    *   *Methodology:* Ensemble Random Forest QSAR models across 623 human proteins. Citation: Yao et al. J Comput Aided Mol Des. 2016;30(5):413-424.
*   **SuperPred 3.0 (`https://prediction.charite.de/`):**
    *   *TLS Status:* Server responded, but **failed strict TLS verification** (`curl: (60) SSL certificate problem: certificate has expired`). Because security bypasses are excluded, SuperPred is currently classified as unavailable for automated access.
*   **Inaccessible / Inactive Services:**
    *   *PPB2* (`https://gdb.unibe.ch/tools/ppb2/`): Returned HTTP 404 Not Found on 2026-09-22 at 22:20:10 EDT.
    *   *MolTarPred* (`https://moltarpred.ncats.io/`): Failed DNS resolution on 2026-09-22 at 22:20:10 EDT.

---

### 2.5 Structure-Based Docking Engine: AutoDock Vina

*   **Software & License:** AutoDock Vina (v1.2.x), Apache License 2.0 (open source).
*   **Local Tooling Status:** On the Mac research environment, `/opt/homebrew/bin/obabel` (Open Babel 3.2.1) is present. AutoDock Vina itself was not found in PATH and must be acquired or compiled if docking is later conducted.
*   **Scoring Function Overview:** Evaluates an empirical free-energy fitness function summing steric interactions (piecewise linear dispersion terms), directional hydrogen bonding, hydrophobic contact terms, and a conformational torsional penalty proportional to the number of active rotatable bonds.
*   **Resource Management:** Multi-threaded using OpenMP. CPU usage must be capped explicitly (e.g., `--cpu 4` with a single active job) to conform to the project resource ceiling (4 cores, 16 GB RAM under `nice -n 19`).
*   **Key Literature:**
    *   Trott O, Olson AJ. *AutoDock Vina: improving the speed and accuracy of docking with a new scoring function, efficient optimization, and multithreading.* J Comput Chem. 2010;31(2):455-461. DOI: [10.1002/jcc.21334](https://doi.org/10.1002/jcc.21334).
    *   Eberhardt J, Santos-Martins D, Tillack AF, Forli S. *AutoDock Vina 1.2.0: New Docking Methods, Expanded Force Field, and Python Bindings.* J Chem Inf Model. 2021;61(8):3891-3898. DOI: [10.1021/acs.jcim.1c00203](https://doi.org/10.1021/acs.jcim.1c00203).

---

### 2.6 Verified Tool Summary

| Tool | Primary Method | Operational URL | Reachability Checked (2026-09-22) | Inputs | Key Outputs | Terms / License |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SwissTargetPrediction** | 2D (FP2) + 3D (ES5D) similarity | `https://www.swisstargetprediction.ch/` | HTTP 200 OK | SMILES, 2D sketch | Target rank, probability, 2D/3D scores | CC-BY 4.0 licensed materials; see the service's terms for access and collection limits |
| **SEA** | Set-wise circular similarity | `https://sea.bkslab.org/` | HTTP 200 OK | SMILES + ID | Raw score, Z-score, $E$-value | Academic free; Altcha challenge active |
| **ChEMBL REST API** | Exact, substructure, circular similarity | `https://www.ebi.ac.uk/chembl/api/data/` | HTTP 200 OK (`ChEMBL_37`) | Identifiers, SMILES | Bioactivities, assay types, metadata | CC BY-SA 3.0; Open |
| **PharmMapper** | 3D cavity pharmacophore matching | `http://lilab-ecust.cn/pharmmapper/` | HTTP 200 OK | 3D Mol2 / SDF | Fit score, normalized score, Z-score | Academic non-commercial only |
| **TargetNet** | Random Forest QSAR | `http://targetnet.scbdd.com/` | HTTP 200 OK (HTTP only) | SMILES, SDF | Probability across 623 models | Academic free; HTTPS cert expired |
| **AutoDock Vina** | Empirical molecular docking | Local binary / open source | Not in PATH on Mac | PDBQT files | Docking score ($\Delta G$, kcal/mol), poses | Apache 2.0; Open source |

---

## 3. Theoretical Foundations and Uncertainty Estimation

### 3.1 Applicability Domain Considerations

The **applicability domain (AD)** of a cheminformatics model describes the chemical space where its predictive performance has been validated (OECD Principle 3).
*   Target-prediction algorithms rely on structural similarity to known ligands in training databases.
*   When a query compound shares low overall similarity with the reference active set, predictions are driven by isolated substructures (such as an unadorned benzene ring or a generic tertiary amine) rather than a coherent 3D pharmacophore.
*   This can lead to promiscuous scoring across common drug target classes (e.g., biogenic amine GPCRs, esterases, or cytochromes) simply because those classes frequently bind compounds containing similar common fragments.

### 3.2 Correlated Training Data and Pseudoreplication

A frequent pitfall in computational target prediction is treating agreement among multiple web servers as independent validation:
*   SwissTargetPrediction, SEA, TargetNet, and SuperPred all draw active-molecule bioactivity data from ChEMBL and BindingDB.
*   If multiple tools predict the same target, it is frequently because all of them encountered the same underlying set of ChEMBL assay records.
*   **Concordance across these platforms represents correlated observations from a shared literature corpus, not independent biological confirmation.**
*   Structure-based docking provides a *complementary* physical model, but is also not an independent experimental measurement.

### 3.3 Statistical Interpretation of Prediction Scores

#### 1. Conditional Probability vs. Absolute Probability
*   SwissTargetPrediction's probability score reflects the likelihood of a target being correct *given the assumption that the molecule is active against at least one target in the database*. It does not estimate the probability that the molecule is biologically active in absolute terms.
*   SEA's $E$-value represents the expected number of random target sets that would yield an equal or greater similarity sum by chance; it does not measure binding free energy.

#### 2. Base-Rate Considerations
A ranked prediction is not evidence that the compound binds the listed target. Interpreting a score requires calibration on compounds representative of the query and the intended target set. No such calibration has been established here, so this review does not assign a binding probability.

---

### 3.4 Biophysical Limits of Molecular Docking

Molecular docking algorithms provide useful spatial hypotheses, but have significant biophysical limitations:

1.  **Docking Scores Do Not Prove Binding:**
    *   AutoDock Vina evaluates an empirical scoring function approximating binding free energy ($\Delta G_{\text{bind}}$), but omits rigorous solvent thermodynamics.
    *   Desolvation penalties (the free-energy cost of removing water from polar/charged groups on the ligand and pocket) are heavily approximated.
    *   Solvent entropy changes (hydrophobic effect) and protein conformational entropy losses are simplified.
    *   Standard docking assumes a rigid receptor backbone, neglecting induced-fit adjustments.
    *   A favorable docking score can occur simply from extensive van der Waals contact in a deep cavity, even if the compound is inactive in solution. Conversely, poor docking scores can result from minor steric clashes with static side chains that would adjust in reality.
2.  **Raw Scores Cannot Be Compared Across Different Proteins:**
    *   Binding cavities vary substantially in volume, shape, and hydrophobicity. Deep, lipophilic pockets yield larger negative scores for almost any drug-sized aromatic molecule than shallow, solvent-exposed pockets.
    *   Comparing raw Vina energy scores across different proteins to rank target preferences is physically invalid.
3.  **Docking Cannot Determine Agonism vs. Antagonism:**
    *   Pharmacological efficacy (agonist, antagonist, or inverse agonist) depends on stabilizing specific dynamic receptor conformations (e.g., the outward tilt of transmembrane helix 6 in active GPCRs).
    *   Docking into a single static structure (often an inactive-state crystal structure) evaluates only steric and electrostatic compatibility with that specific snapshot. It cannot infer downstream signaling effects.

---

## 4. Calibration Conventions from Published Literature

To avoid subjective interpretation of raw docking scores, literature benchmarks use comparative control sets. These conventions serve as exploratory frameworks, not rigid project rules.

### 4.1 Property-Matched Decoys (DUD-E Framework)
*   **Concept:** The Directory of Useful Decoys - Enhanced (DUD-E; Mysinger et al. J Med Chem 2012) generates decoys that match the physical properties of active ligands (molecular weight, $\log P$, charge, rotatable bonds) while having dissimilar 2D topological fingerprints.
*   **Crucial Distinction:** Decoys are **presumed negatives**, not experimentally confirmed non-binders. They provide an empirical reference distribution of scores for property-matched compounds in that specific pocket.
*   **Decoy-Referenced Z-Scores:**
    $$Z = \frac{\text{Score}(\text{Compound}) - \mu_{\text{decoys}}}{\sigma_{\text{decoys}}}$$
    *   A Z-score contextualizes how a compound's score compares with the chosen decoy distribution in one modeled pocket.
    *   **Z-scores do not isolate physical specificity, calculate binding probabilities, or make scores comparable across targets.** Their meaning depends on the selected decoys and that specific model.

### 4.2 Control Ligands & Literature Evaluation Metrics
*   **Positive Controls:** In published virtual screening evaluations, co-crystallized native ligands and known active compounds are docked to establish whether the model can recognize characterized binders. No arbitrary affinity cutoff (e.g., $K_i < 50\ \text{nM}$) should exclude other informative active ligands.
*   **Literature Metrics (ROC-AUC, Enrichment Factors):** In benchmark studies, Area Under the ROC Curve (ROC-AUC) and Early Enrichment Factors ($\text{EF}$) are used to measure a model's ability to rank known actives ahead of presumed decoys. These metrics describe historical benchmark performance and are not hard pass/fail gates for exploratory single-compound studies.

---

## 5. Ligand and Receptor Preparation Considerations

### 5.1 Protonation and pKa Uncertainty

*   **Structure:** PRL-8-53 contains an aliphatic tertiary amine linked to a benzyl group and an ethyl(methylbenzoate) moiety.
*   **pKa Status:** No compound-specific experimental value was identified in the bounded literature review.
*   **Sensitivity treatment:** Submit neutral and protonated representations and record how the selected service canonicalizes them. If it normalizes both to the same input, their identical output is one result, not corroboration. This checks representation sensitivity without inventing a protonation fraction.
*   If a later target hypothesis involves a biogenic-amine GPCR, protonation can affect a possible interaction with the conserved Aspartate 3.32 ($\text{Asp}^{3.32}$); that general motif is not evidence that PRL-8-53 binds such a receptor.

### 5.2 Receptor Structure Selection & Co-Crystal Redocking

*   **Structure Quality:** High-resolution experimental structures (e.g., solved by X-ray crystallography or Cryo-EM) with clear active-site electron density are preferred over unrefined homology models. Holo structures (solved with a bound ligand) preserve binding pocket conformations that are often collapsed in apo structures.
*   **Co-Crystal Redocking:**
    *   *Purpose:* Redocking the co-crystallized native ligand back into its prepared pocket is a standard sanity check to verify that the grid definition, partial charge assignment, and scoring parameterization can recover the crystallographic pose.
    *   *Limited Epistemological Meaning:* Successful redocking demonstrates that the known crystal pose is near a local energy minimum of the scoring function. **It does not prove that the scoring function will accurately rank novel chemotypes or discriminate inactive molecules.**

---

## 6. Guarding Against Confirmation Bias

*   **Avoid Hypothesis Cherry-Picking:** Receptor families should not be selected solely based on speculative claims in informal forums or historical preprint titles.
*   **Transparent Uncertainty Reporting:** If target-prediction tools produce low similarity scores and docking shows no separation from property-matched decoys, this should be reported candidly as an inconclusive or negative finding. Documenting the boundaries of computational deconvolution for an orphan compound is an honest, valuable scientific contribution.
