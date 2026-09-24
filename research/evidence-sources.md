# PRL-8-53: Evidence Sources and Bounded Search Log

This document records the bounded queries across pharmacological databases, primary literature records, and patent disclosures consulted for the evidence review of PRL-8-53.

---

## 1. Bounded Database Search Log

All searches were conducted between September 22 and September 23, 2026. Exact queries, timestamps, response codes, and raw excerpts are documented below.

### 1.1 ChEMBL Database
*   **Database Server Version:** `ChEMBL_37` (release date: `2026-05-01`; status: `UP`; 2,921,148 distinct compounds; 24,527,044 activities; 18,552 targets).
*   **Status Query URL:** `https://www.ebi.ac.uk/chembl/api/data/status.json`
*   **Timestamp:** `2026-09-23T02:27:28Z`
*   **Query 1 (Free Base InChIKey):**
    *   URL: `https://www.ebi.ac.uk/chembl/api/data/molecule.json?molecule_structures__standard_inchi_key=IGJQEMHBYKNIQR-UHFFFAOYSA-N`
    *   Result: `HTTP 200 OK` with `page_meta.total_count: 0` and `molecules: []`.
*   **Query 2 (Hydrochloride Salt InChIKey):**
    *   URL: `https://www.ebi.ac.uk/chembl/api/data/molecule.json?molecule_structures__standard_inchi_key=HLBBSWSJLPLPRU-UHFFFAOYSA-N`
    *   Result: `HTTP 200 OK` with `page_meta.total_count: 0` and `molecules: []`.
*   **Endpoint note:** A path such as `molecule/{identifier}.json` resolves a ChEMBL molecule ID, not an InChIKey filter. Its 404 response is therefore not evidence that an InChIKey is absent.
*   **Query 3 (Preferred Name Search):**
    *   URL: `https://www.ebi.ac.uk/chembl/api/data/molecule.json?pref_name__iexact=PRL-8-53`
    *   Result: `HTTP 200 OK` with payload:
        `{"molecules": [], "page_meta": {"limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 0}}`
*   **Query 4 (Synonym Search):**
    *   URL: `https://www.ebi.ac.uk/chembl/api/data/molecule.json?molecule_synonyms__molecule_synonym__iexact=PRL-8-53`
    *   Result: `HTTP 200 OK` with payload:
        `{"molecules": [], "page_meta": {"limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 0}}`
*   **Query 5 (Chemical Similarity Search):**
    *   URL: `https://www.ebi.ac.uk/chembl/api/data/similarity/CN(CCC1=CC(=CC=C1)C(=O)OC)CC2=CC=CC=C2/70.json`
    *   Result: `HTTP 200 OK` with 0 hits at $\ge 70\%$ Tanimoto similarity.

### 1.2 PubChem BioAssay
*   **Endpoint Behavior Verification:** The PUG REST `assaysummary` endpoint returns HTTP 200 with an assay table when bioassays exist (verified using Aspirin CID 2244, `2026-09-23T02:28:44Z`). When no assays exist, it returns HTTP 404 with code `PUGREST.NotFound`.
*   **Timestamp:** `2026-09-23T02:28:31Z`
*   **Query 1 (Free Base CID 39989):**
    *   URL: `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/39989/assaysummary/JSON`
    *   Result: `HTTP 404 PUGREST.NotFound`
    *   Raw Body:
        ```json
        {
          "Fault": {
            "Code": "PUGREST.NotFound",
            "Message": "No assay data found for the given ID(s)"
          }
        }
        ```
*   **Query 2 (Hydrochloride Salt CID 70700868):**
    *   URL: `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/70700868/assaysummary/JSON`
    *   Result: `HTTP 404 PUGREST.NotFound` (Message: `"No assay data found for the given ID(s)"`).
*   **Query 3 (Ionic Salt CID 39988):**
    *   URL: `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/39988/assaysummary/JSON`
    *   Result: `HTTP 404 PUGREST.NotFound` (Message: `"No assay data found for the given ID(s)"`).

### 1.3 PubMed (MEDLINE) Entrez Search
*   **Timestamp:** `2026-09-23T02:29:04Z`
*   **Query 1 (`"PRL-8-53"[All Fields]`):**
    *   URL: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%22PRL-8-53%22&retmode=json`
    *   Result: `HTTP 200 OK` with payload:
        `{"count": "1", "retmax": "1", "retstart": "0", "idlist": ["418433"]}`
*   **Query 2 (`Hansl N*[Author] AND benzoic`):**
    *   URL: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Hansl+N*[Author]+AND+benzoic&retmode=json`
    *   Timestamp: `2026-09-23T02:29:10Z`
    *   Result: `HTTP 200 OK` with payload:
        `{"count": "2", "retmax": "2", "retstart": "0", "idlist": ["418433", "4824605"]}`

### 1.4 Europe PMC
*   **Timestamp:** `2026-09-23T02:29:00Z`
*   **Query URL:** `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22PRL-8-53%22&format=json`
*   **Result:** `HTTP 200 OK`; `hitCount: 5`.
    1.  PMID 418433 (1978): Hansl & Mead primary clinical trial.
    2.  PMID 41048238 (2025): Survey on sports doping.
    3.  PMID 33024436 (2020): Survey on cognitive enhancers.
    4.  PMID 33909525 (2021): Survey on social media mentions of atypical drugs.
    5.  PMID 28692683 (2017): False-positive keyword match (prolactin/PRL abbreviation with percentage).

### 1.5 BindingDB
*   **Timestamp:** `2026-09-23T02:28:47Z`
*   **API Query:** `https://www.bindingdb.org/axis2/services/BDBService/getLigandsByInChIKey?inchiKey=IGJQEMHBYKNIQR-UHFFFAOYSA-N` returned `HTTP 404 Not Found`.
*   **Domain Search:** Web query `site:bindingdb.org "PRL-8-53" OR "IGJQEMHBYKNIQR"` (`2026-09-22T22:22:08-04:00`) yielded 0 indexed pages. Programmatic API access was unauthenticated; web index indicates no cataloged entry.

### 1.6 DrugBank Online
*   **Timestamp:** `2026-09-22T22:22:16-04:00`
*   **Search Method:** Domain query `site:go.drugbank.com "PRL-8-53"`.
*   **Result:** 0 matching pages. DrugBank Online does not provide a public unauthenticated REST search API.

### 1.7 IUPHAR / BPS Guide to PHARMACOLOGY
*   **Timestamp:** `2026-09-23T02:28:51Z`
*   **API Query:** `https://www.guidetopharmacology.org/services/ligands?name=PRL-8-53` returned `HTTP 401 Unauthorized` (endpoint requires API credentials).
*   **Domain Search:** Web query `site:guidetopharmacology.org "PRL-8-53"` (`2026-09-22T22:22:12-04:00`) yielded 0 indexed pages.

---

## 2. Primary Sources and Provenance Bibliography

### 2.1 Hansl & Mead (1978) — Primary Human Study
*   **Bibliographic Citation:** Hansl, N. R., & Mead, B. T. (1978). PRL-8-53: enhanced learning and subsequent retention in humans as a result of low oral doses of new psychotropic agent. *Psychopharmacology (Berl)*, 56(3), 249–253.
*   **Identifiers:** DOI: [10.1007/BF00432846](https://doi.org/10.1007/BF00432846) | PMID: [418433](https://pubmed.ncbi.nlm.nih.gov/418433/)
*   **Source Access Level:** Abstract and citation metadata verified via PubMed. Publisher full text is behind a Springer paywall; claims not exposed in the abstract are excluded below.
*   **Abstract Text (Verbatim Excerpt from PubMed):**
    > "The effect of 3-(2-benzylmethylaminoethyl) benzoic acid methyl ester hydrochloride (PRL-8-53) on learning and on retention of verbal information in human subjects was investigated. Using the serial anticipation method under double-blind conditions it was found that PRL-8-53 causes slight improvement of acquisition. Retinetion of verbal information was found improved to a statistically significant degree (most P values better than 0.01, some better than 0.001). No significant changes were found for either visual reaction time or motor control after drug when compared with placebo values."
*   **What the accessed abstract supports:** A double-blind serial-anticipation experiment in human subjects; slight improvement in acquisition; statistically significant improvement in retention; and no significant change in visual reaction time or motor control versus placebo. Participant count, dose, timing, word-list composition, and follow-up intervals require the inaccessible full text and are not treated here as independently verified. A non-significant result on the two controls does not prove an absence of sedation or stimulation.

### 2.2 Hansl (1974) — Primary Preclinical Animal Report
*   **Bibliographic Citation:** Hansl, N. R. (1974). A novel spasmolytic and CNS active agent: 3-(2-benzylmethylamino ethyl) benzoic acid methyl ester hydrochloride. *Experientia*, 30(3), 271–272.
*   **Identifiers:** DOI: [10.1007/BF01934822](https://doi.org/10.1007/BF01934822) | PMID: [4824605](https://pubmed.ncbi.nlm.nih.gov/4824605/)
*   **Source Access Level:** Citation and MEDLINE indexing verified via PubMed; PubMed supplies no abstract, and the publisher full text is behind a Springer/Birkhäuser paywall. The indexing includes animals, rats, dogs, avoidance learning, memory, motor activity, blood pressure, methamphetamine, and apomorphine, but does not expose the paper's numerical results.
*   **Access boundary:** Exact doses, effect sizes, and detailed claims attributed to this paper in later summaries were not independently checked against the full text and are not used as established results here. The patent separately supports inventor-reported rabbit-ileum, avoidance-learning, maze, and mouse-toxicity claims.

### 2.3 Hansl (1975) — US Patent 3,870,715
*   **Bibliographic Citation:** Hansl, N. R. (1975). *Substituted amino ethyl meta benzoic acid esters.* US Patent 3,870,715. Filed April 2, 1973; issued March 11, 1975; expired March 11, 1992.
*   **URL:** [Google Patents US3870715A](https://patents.google.com/patent/US3870715A/en)
*   **Source Access Level:** Complete scanned patent and Google Patents OCR transcription accessed from the URL above.
*   **Relevant Excerpts:**
    *   *Example 1 (OCR typography normalized):*
        > "The crude hydrochloride salt precipitated and was recrystallized from methyl alcohol/ether and then from isoamyl alcohol/ether mixtures. A total of 11.2 g. of white crystalline material consisting of m-[2-(benzylmethylamino)-ethyl]-benzoic acid methyl ester hydrochloride was obtained melting at 150–151°C."
    *   *Pharmacological evaluation:*
        > "Standard avoidance response tests using negative reinforcement (electric shock) as well as maze tests using positive reinforcement (water reward) were conducted using rats as the experimental animal. Using m-[2-(benzylmethylamino)-ethyl]-benzoic acid methyl ester as the test compound, it was found that a compound of this structure facilitates the rats acquisition and increases subsequent retention... a preferred species of the invention m-[2-(benzylmethylamino)-ethyl]-benzoic acid methyl ester was found to have an oral LD of about 500–700 mg/kg in mice."
    *   *Context Note:* Patent toxicology statements (e.g., tolerance in dogs and monkeys up to 50 mg/kg; lack of organ pathology) are inventor reports, not peer-reviewed clinical safety profiles.

---

## 3. Secondary Literature

The following modern publications were audited for bibliographic coherence (title, authors, year, PMID, and DOI):

1.  **Pietrzak, B., et al. (2025).** "Brain doping" substances: prohibited or not in sports? *Sport Sciences for Health*. PMID: [41048238](https://pubmed.ncbi.nlm.nih.gov/41048238/).
    *   *Coherence:* Survey article citing historical 1978 findings on cognitive enhancement in sport/academic doping context. Contains no new empirical pharmacology.
2.  **Schifano, F., et al. (2020).** The Psychonauts' World of Cognitive Enhancers. *Frontiers in Psychiatry*, 11:579145. DOI: [10.3389/fpsyt.2020.579145](https://doi.org/10.3389/fpsyt.2020.579145). PMID: [33024436](https://pubmed.ncbi.nlm.nih.gov/33024436/).
    *   *Coherence:* Review of internet gray-market nootropics. Mentions PRL-8-53 as an unapproved cognitive-enhancing agent discussed on web forums.
3.  **Orsolini, L., et al. (2021).** When an obscurity becomes trend: social-media descriptions of tianeptine use and associated atypical drug use. *Human Psychopharmacology: Clinical and Experimental*, 36(6):e2802. DOI: [10.1002/hup.2802](https://doi.org/10.1002/hup.2802). PMID: [33909525](https://pubmed.ncbi.nlm.nih.gov/33909525/).
    *   *Coherence:* Observational study of social media drug discussions; references PRL-8-53 within unprescribed cognitive enhancer discussions.
