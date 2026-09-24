# Exploratory First-Experiment Plan: Registry Baseline, Target Prediction & Conditional Docking Rationale

**Compound:** PRL-8-53 (methyl 3-[2-[benzyl(methyl)amino]ethyl]benzoate)
**Date:** 2026-09-22 / 2026-09-23
**Status:** Registry pilot and first target-prediction run completed; no docking run executed
**Author:** Hasan Ugur (Rolf) Yildirim

---

## 1. Plan Purpose and Scope

This document specifies a bounded, exploratory computational workflow to investigate potential targets for PRL-8-53 and map empirical uncertainty. 

Rather than committing immediately to a broad docking campaign, the first experiment has two focused stages:
1.  **Completed registry pilot:** Confirm the structure, check exact records and bioassays in ChEMBL and PubChem, and inspect the nearest ChEMBL result rather than treating a similarity count as target evidence.
2.  **Completed target-prediction experiment:** SwissTargetPrediction was run for neutral and protonated representations and the exports were preserved. The completed bounded analysis traced the top-ranked target rather than every non-zero prediction; see `experiments/exp-001/` for the result and deviations from this initial plan.

The completed pilot found no exact ChEMBL molecule or PubChem BioAssay record under the checked identifiers. Its sole ChEMBL result at the 60% threshold is too structurally incomplete to support a target hypothesis. A conditional docking rationale follows; no docking batch has been run.

---

## 2. Chemical Identifiers & Sensitivity Representations

The integrated identity review confirms the following registry representations:

*   **Chemical Name:** Methyl 3-[2-[benzyl(methyl)amino]ethyl]benzoate
*   **Free-base SMILES:** `CN(CCc1cccc(c1)C(=O)OC)Cc2ccccc2`
*   **Free-base InChIKey:** `IGJQEMHBYKNIQR-UHFFFAOYSA-N` (PubChem CID 39989)
*   **HCl-salt InChIKey:** `HLBBSWSJLPLPRU-UHFFFAOYSA-N` (PubChem CIDs 70700868 and 39988 use different component/ionic representations)

### Ionization Sensitivity Representations
No compound-specific experimental pKa was identified in the bounded review. The target-prediction experiment should therefore record whether the service accepts and distinguishes these two representations:
*   **Neutral:** `CN(CCc1cccc(c1)C(=O)OC)Cc2ccccc2`
*   **Protonated monocation:** `C[NH+](CCc1cccc(c1)C(=O)OC)Cc2ccccc2`

If the service normalizes both inputs to the same structure, that is the result; the two submissions must not be described as independent evidence.

---

## 3. Stage 1: Completed Registry Pilot (ChEMBL & PubChem)

### 3.1 Queries and Results
The exact URLs, timestamps, statuses, and key payloads are recorded in `evidence-sources.md` and `target-methods.md`.

1.  **Exact records:** ChEMBL 37 InChIKey filters returned `total_count: 0` for the free base and HCl salt. PubChem's BioAssay endpoint returned `PUGREST.NotFound: No assay data found` for CIDs 39989, 70700868, and 39988.
2.  **Similarity search:** ChEMBL returned 0 molecules at 70%, 1 at 60%, and 30 at 50% for the free-base SMILES.
3.  **Nearest-result inspection (checked 2026-09-23T02:34:45Z):** The sole 60% result, CHEMBL5941544 (reported similarity 60.98%), is methyl 3-(2-hydroxyethyl)benzoate (`COC(=O)c1cccc(CCO)c1`). It lacks PRL-8-53's tertiary amine and benzyl group. ChEMBL lists IC50 values of 69 nM for CYP4F2 and 210 nM for CYP4A11 from document CHEMBL5729164.

### 3.2 Pilot Interpretation
The CYP activities belong to a smaller fragment-like molecule, not PRL-8-53. They do not justify CYP4F2 or CYP4A11 as candidate targets for PRL-8-53. The practical outcome of the pilot is that similarity percentages must be followed by structure and assay inspection; the registry results supply no direct binding evidence for PRL-8-53.

---

## 4. Stage 2: Completed Target-Prediction Experiment (SwissTargetPrediction)

### 4.1 Tool Selection & Terms Caveat
SwissTargetPrediction (`https://www.swisstargetprediction.ch/`) was verified reachable (HTTP 200 OK) on 2026-09-22. Its terms restrict how the service may be accessed and how much of the licensed material may be collected; two single-molecule queries through the ordinary web form were within the intended scope, and the result material is not redistributed with this project. SEA was protected by an Altcha proof-of-work challenge, and SuperPred/TargetNet exhibited TLS certificate issues.

### 4.2 Original Query Execution Protocol

The following was the prospective protocol. Actual artifacts, paths, scope, and deviations are recorded in `experiments/exp-001/`.
1.  **Interactive Browser Submission:**
    *   Submit **Scenario A** (neutral SMILES) for *Homo sapiens*.
    *   Submit **Scenario B** (protonated SMILES) for *Homo sapiens*.
2.  **Output Preservation:**
    *   Download and preserve the raw CSV export for each run:
        *   `research/experiments/exp-001/raw_data/swisstarget/neutral_export.csv`
        *   `research/experiments/exp-001/raw_data/swisstarget/protonated_export.csv`
    *   Save the complete browser result HTML pages and note the query timestamp and server version notes.
3.  **Provenance & Training Data Audit:**
    *   Preserve the complete export. For every target discussed in the report:
        *   Record the UniProt ID, ChEMBL target ID, target name, rank, probability, and 2D/3D similarity fields supplied by the export.
        *   Identify and inspect the nearest active reference compounds that drive the score when the service exposes them.
        *   State whether each prediction rests on a coherent analog or only on common fragments.
4.  **Uncertainty Assessment:**
    *   Document differences in target rankings between the neutral and protonated queries to quantify sensitivity to ionization state.
    *   Explicitly note that reported probabilities represent conditional rankings among known database targets (assuming bioactivity), not absolute binding probabilities.

---

## 5. Conditional Docking Rationale (Future Exploration)

Downstream molecular docking is not preordained as an automatic batch. It is considered only if Stage 1 and Stage 2 provide justifiable rationale.

### 5.1 Gating Conditions for Downstream Docking
Docking should be pursued only if:
1.  The confirmed structure and explicit neutral/protonated representations are used consistently.
2.  Stage 1 and Stage 2 identify a small set of candidate targets that exhibit biologically plausible binding sites and non-trivial similarity to known active chemotypes.
3.  High-resolution, experimentally determined 3D structures (holo crystal or Cryo-EM structures) are available in the RCSB PDB for those candidate targets.

### 5.2 Provisional Controlled Docking Framework
If the gating conditions above are satisfied, docking should be conducted provisionally with rigorous comparative controls:
*   **Target Selection:** Focus on a small, manageable set of candidate receptors (e.g., 1 to 3 targets) rather than a large, unverified screen.
*   **Controls Design (Exploratory Benchmarks):**
    *   *Positive Controls:* Co-crystallized native ligand and known active ligands with experimental affinities documented in ChEMBL or primary literature.
    *   *Presumed Negatives (Decoys):* A provisional set of property-matched decoys (e.g., extracted from DUD-E matching molecular weight, $\log P$, charge, and rotatable bonds with topological dissimilarity). Decoys are recognized as *presumed negatives*, not proven non-binders.
    *   *Sanity Check:* Redock the co-crystallized native ligand to evaluate whether the scoring function and grid box reproduce the crystallographic pose (using literature convention, e.g., $\text{RMSD} \le 2.0\ \text{Å}$, as an exploratory sanity check, recognizing that this does not prove predictive accuracy for novel compounds).
*   **Exploratory Score Analysis:**
    *   Calculate mean and standard deviation of decoy scores to compute a decoy-referenced Z-score:
        $$Z = \frac{\Delta G_{\text{PRL}} - \mu_{\text{decoys}}}{\sigma_{\text{decoys}}}$$
    *   Examine where PRL-8-53 ranks relative to positive controls and the decoy distribution.
    *   *Limitation:* A low Z-score does not prove physical binding or specificity; it merely indicates that the compound scores well relative to property-matched presumed negatives under that specific rigid-receptor model.

---

## 6. Resource Ceilings & Execution Boundaries

For any future computational runs (whether on the Mac or on a remote machine):

1.  **Project Ceilings (Hard Limits):**
    *   Maximum **4 CPU cores** in aggregate.
    *   Maximum **16 GB RAM** in aggregate.
    *   All processes must execute under **`nice -n 19`**.
2.  **Thread & Process Capping:**
    *   When running multi-threaded tools such as AutoDock Vina, CPU threads must be explicitly capped (e.g., `--cpu 4` with only a single job executing at a time).
    *   Memory consumption must be bounded and monitored before launching large batch runs.
    *   Timings and memory scaling have not been empirically benchmarked on the remote box; no assumptions of zero overhead or instant execution may be made.
3.  **Host and Environment Boundaries:**
    *   No remote machine logins, file modifications, or process inspections are in scope. Remote paths and environments remain separate verification tasks.
    *   If remote jobs share a machine with other studies (such as `flyonenomics`), strict process and path isolation must be maintained: never access, read, write, or interfere with external folders or processes.
4.  **Local Tooling Status:**
    *   Open Babel 3.2.1 is available locally at `/opt/homebrew/bin/obabel`.
    *   AutoDock Vina is not currently in PATH on the local Mac and must be verified or installed when docking is formally scheduled.

---

## 7. Deliverables and Decision Points

After the interactive prediction experiment:
*   Add the two raw exports, accepted/canonicalized input structures, timestamps, and a concise provenance table.
*   Report weak similarities or representation sensitivity as limitations, not as binding results.
*   Decide whether any candidate has enough traceable analog support to justify a controlled docking exercise. Otherwise stop with the bounded conclusion that these computational searches did not resolve a target.
