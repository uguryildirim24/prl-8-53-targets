# Reproducibility and Provenance Manifest — Alternative Target Audit (Ranks 2–6)

## Scope

This manifest documents the provenance, retrieval parameters, and integrity of the raw evidence collected for the audit of the five targets immediately following rank-1 ACACB in the predictions obtained from the SwissTargetPrediction web server (`exp-001`). The evaluation scope is strictly bounded to the top 5 subsequent hypotheses in rank order (ranks 2 through 6).

**Retained in this repository:** ChEMBL and UniProt records only. The prediction-service output itself is not redistributed here; the target identities carried forward are listed in [`docs/target-shortlist.md`](../../docs/target-shortlist.md).

- **Query Compound:** PRL-8-53 (neutral free base)
- **Submitted SMILES:** `COC(=O)c1cccc(c1)CCN(Cc1ccccc1)C`
- **Prediction source:** SwissTargetPrediction web server (Daina, Michielin & Zoete, *Nucleic Acids Res.* 2019)
- **Evaluated Target Ranks:**
  1. Rank 2: OPRM1 (Mu-type opioid receptor; UniProt P35372; ChEMBL CHEMBL233)
  2. Rank 3: KCNJ1 (ATP-sensitive inward-rectifier potassium channel 1 / ROMK / Kir1.1; UniProt P48048; ChEMBL CHEMBL1293292)
  3. Rank 4: BCHE (Cholinesterase / Butyrylcholinesterase; UniProt P06276; ChEMBL CHEMBL1914)
  4. Rank 5: KCNH2 (Voltage-gated potassium channel Kv11.1 / hERG; UniProt Q12809; ChEMBL CHEMBL240)
  5. Rank 6: SLC6A4 (Sodium-dependent serotonin transporter / SERT; UniProt P31645; ChEMBL CHEMBL228)

Nothing in this folder constitutes a wet-lab measurement or direct experimental determination of PRL-8-53 binding.

---

## Retrieval Protocols and Tooling

The ChEMBL and UniProt records retained here were retrieved on 2026-09-23 using bounded, unauthenticated standard HTTP/1.1 requests through the Python 3.13 standard library (`urllib.request`), and remain subject to those services' ordinary terms. No account, access-control bypass, or bulk dataset download was used.

The target predictions that produced ranks 2–6 came from the SwissTargetPrediction web server. That service output is **not** redistributed in this repository. What was carried forward is the list of target identities and the nearest source compounds named by the service, which were then traced independently through the ChEMBL API; those ChEMBL records are the evidence retained here. See [`docs/target-shortlist.md`](../../docs/target-shortlist.md).

For every external query, three files are maintained:
1. The raw payload (`.json`, `.csv`, or `.raw.html`).
2. The HTTP response headers (`.headers.txt` or within `.json`).
3. The exact request metadata (`.request.txt` or within `.json`), recording query URL, HTTP status code, and millisecond UTC timestamps for start and completion.

---

## File Structure and Inventory

### 1. Prediction source (not redistributed)

The nearest-active ligand lists that SwissTargetPrediction exposes for each ranked target are not included in this repository. The compounds those lists named were looked up independently in ChEMBL, and it is the ChEMBL records below that carry the evidence used in the audit. The target shortlist, with UniProt and ChEMBL identifiers and the reason each target was or was not pursued, is in [`docs/target-shortlist.md`](../../docs/target-shortlist.md).

### 2. ChEMBL Records (`chembl/`)
Current live records retrieved from the European Bioinformatics Institute (EMBL-EBI) ChEMBL REST API (`https://www.ebi.ac.uk/chembl/api/data/`):
- **Database Status:** `status.json` verifies database version `ChEMBL_37` (release date: 2026-05-01).
- **Target Records:** `target-CHEMBL{233, 1293292, 1914, 240, 228}.json` (with adjacent headers and request files).
- **Molecule Records:**
  - `molecule-CHEMBL423726.json`: OPRM1 nearest 2D active
  - `molecule-CHEMBL138910.json`: OPRM1 nearest 3D active
  - `molecule-CHEMBL2146870.json`: KCNJ1 nearest 2D active / KCNH2 nearest 2D active (cross-target shared ligand)
  - `molecule-CHEMBL6050195.json`: KCNJ1 nearest 3D active
  - `molecule-CHEMBL5592832.json`: BCHE nearest 2D active
  - `molecule-CHEMBL5542214.json`: BCHE nearest 3D active
  - `molecule-CHEMBL1779004.json`: KCNH2 nearest 3D active
  - `molecule-CHEMBL379536.json`: SLC6A4 nearest 2D active
  - `molecule-CHEMBL579056.json`: SLC6A4 nearest 3D active
  - `molecule-CHEMBL201666.json`: SLC6A4 dual 2D/3D exposed active bearing an aromatic methyl ester
- **Target-Filtered Activity Records:** `activities-{molecule_id}-{target_id}.json` containing full activity objects and pagination metadata (`page_meta`).
- **Assay Records:** `assay-CHEMBL{753397, 754685, 2148625, 2148630, 4427467, 5735582, 5535548, 5535554, 2148626, 4427468, 1781193, 869834, 1040429, 859238, 859242}.json`.
- **Document Records:** `document-CHEMBL{1136497, 2146432, 4425169, 5727875, 5532688, 1777674, 1146859, 1154083, 1138144}.json`.

### 3. UniProt Canonical Records (`uniprot/`)
Direct REST JSON records from `https://rest.uniprot.org/uniprotkb/{accession}.json`:
- `uniprot-P35372.json` (OPRM1_HUMAN)
- `uniprot-P48048.json` (KCNJ1_HUMAN)
- `uniprot-P06276.json` (CHLE_HUMAN / BCHE)
- `uniprot-Q12809.json` (KCNH2_HUMAN)
- `uniprot-P31645.json` (SC6A4_HUMAN / SLC6A4)

### 4. Structured Synthesis
- `source-ligand-trace.json`: Machine-readable mapping compiling candidate targets, nearest 2D and 3D ligands, canonical SMILES, InChIKeys, quantitative endpoints, assay classifications, and primary publication metadata.
- `SHA256SUMS`: SHA-256 hashes covering every data and metadata file retained in this folder. Regenerated for the public release after the prediction-service files were removed, so it no longer matches the internal working copy.
