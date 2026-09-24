# PRL-8-53: Chemical Identity and Published Evidence Review

## 1. Chemical Identity and Authoritative Records

### 1.1 Verified Identifiers

| Parameter | Free Base | Hydrochloride Salt (Neutral Component) | Hydrochloride Salt (Ionic Form) |
| :--- | :--- | :--- | :--- |
| **Chemical Name** | methyl 3-[2-[benzyl(methyl)amino]ethyl]benzoate | methyl 3-[2-[benzyl(methyl)amino]ethyl]benzoate;hydrochloride | benzyl-[2-(3-methoxycarbonylphenyl)ethyl]-methylazanium chloride |
| **CAS Registry Number** | 51352-88-6 | 51352-87-5 | 51352-87-5 |
| **PubChem CID** | [39989](https://pubchem.ncbi.nlm.nih.gov/compound/39989) | [70700868](https://pubchem.ncbi.nlm.nih.gov/compound/70700868) | [39988](https://pubchem.ncbi.nlm.nih.gov/compound/39988) |
| **ChemSpider ID** | [36560](https://www.chemspider.com/Chemical-Structure.36560.html) | None (unindexed separate page) | None |
| **FDA UNII** | BM2TE2XHK6 | 2P77XL8HV7 | 2P77XL8HV7 |
| **EPA CompTox DTXSID** | DTXSID701045345 | DTXSID101350483 | DTXSID101350483 |
| **Molecular Formula** | $\text{C}_{18}\text{H}_{21}\text{NO}_2$ | $\text{C}_{18}\text{H}_{22}\text{ClNO}_2$ | $\text{C}_{18}\text{H}_{22}\text{ClNO}_2$ |
| **Molecular Weight** | 283.4 g/mol | 319.8 g/mol | 319.8 g/mol |
| **PubChem ConnectivitySMILES** | `CN(CCC1=CC(=CC=C1)C(=O)OC)CC2=CC=CC=C2` | `CN(CCC1=CC(=CC=C1)C(=O)OC)CC2=CC=CC=C2.Cl` | `C[NH+](CCC1=CC(=CC=C1)C(=O)OC)CC2=CC=CC=C2.[Cl-]` |
| **Standard InChIKey** | `IGJQEMHBYKNIQR-UHFFFAOYSA-N` | `HLBBSWSJLPLPRU-UHFFFAOYSA-N` | `HLBBSWSJLPLPRU-UHFFFAOYSA-N` |

### 1.2 Raw PubChem PUG REST Record Payload
*   **Query URL:** `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/39989,70700868,39988/property/IUPACName,ConnectivitySMILES,InChIKey,MolecularFormula,MolecularWeight/JSON`
*   **Retrieval Timestamp:** 2026-09-23T02:27:44Z
*   **Response Payload:**
```json
{
  "PropertyTable": {
    "Properties": [
      {
        "CID": 39989,
        "MolecularFormula": "C18H21NO2",
        "MolecularWeight": "283.4",
        "ConnectivitySMILES": "CN(CCC1=CC(=CC=C1)C(=O)OC)CC2=CC=CC=C2",
        "InChIKey": "IGJQEMHBYKNIQR-UHFFFAOYSA-N",
        "IUPACName": "methyl 3-[2-[benzyl(methyl)amino]ethyl]benzoate"
      },
      {
        "CID": 70700868,
        "MolecularFormula": "C18H22ClNO2",
        "MolecularWeight": "319.8",
        "ConnectivitySMILES": "CN(CCC1=CC(=CC=C1)C(=O)OC)CC2=CC=CC=C2.Cl",
        "InChIKey": "HLBBSWSJLPLPRU-UHFFFAOYSA-N",
        "IUPACName": "methyl 3-[2-[benzyl(methyl)amino]ethyl]benzoate;hydrochloride"
      },
      {
        "CID": 39988,
        "MolecularFormula": "C18H22ClNO2",
        "MolecularWeight": "319.8",
        "ConnectivitySMILES": "C[NH+](CCC1=CC(=CC=C1)C(=O)OC)CC2=CC=CC=C2.[Cl-]",
        "InChIKey": "HLBBSWSJLPLPRU-UHFFFAOYSA-N",
        "IUPACName": "benzyl-[2-(3-methoxycarbonylphenyl)ethyl]-methylazanium chloride"
      }
    ]
  }
}
```

### 1.3 Salt Standardization and Representation
*   **Disconnected Notation:** In PubChem ConnectivitySMILES for CID 70700868 (`...C(=O)OC)CC2=CC=CC=C2.Cl`), the period (`.`) denotes disconnected chemical components in the record, not a covalent nitrogen-chlorine bond.
*   **Standardization Duality:** PubChem provides two representations for the hydrochloride salt: uncharged disconnected components (`base.Cl`, CID 70700868) and an ionized salt pair (`base-H+.[Cl-]`, CID 39988). Both resolve to the identical InChIKey `HLBBSWSJLPLPRU-UHFFFAOYSA-N`.
*   **External Record Correction:** The English Wikipedia article for "PRL-8-53" cites CID 39988 in its infobox while displaying the free-base SMILES and free-base InChIKey `IGJQEMHBYKNIQR-UHFFFAOYSA-N`. CID 39989 is the correct record for the neutral free base.

### 1.4 Patent Corroboration
*   **Source:** US Patent 3,870,715 (Inventor: Nikolaus R. Hansl; issued March 11, 1975), checked in the scanned patent and Google Patents OCR transcription.
*   **Example 1 (OCR typography normalized):**
    > "The crude hydrochloride salt precipitated and was recrystallized from methyl alcohol/ether and then from isoamyl alcohol/ether mixtures. A total of 11.2 g. of white crystalline material consisting of m-[2-(benzylmethylamino)-ethyl]-benzoic acid methyl ester hydrochloride was obtained melting at 150–151°C."

The 153–155°C value elsewhere in the patent belongs to the different benzyl ester in Example 20. A later sentence about hydrolysis also describes the free acid, not isolation of the methyl ester hydrochloride.

---

## 2. Acid-Base State & Structural Hypotheses

### 2.1 Ionization State
*   **Measured $\text{p}K_a$:** No experimental value was identified in the bounded sources searched for this review.
*   **Modeling Implication:** The structure contains a tertiary aliphatic amine, but a class analogy is not a compound-specific measurement. Protonated (`[PRL-8-53-H]+`, charge $+1$) and neutral free-base (charge $0$) representations are useful sensitivity choices rather than evidence that either fraction has been measured.

### 2.2 Metabolic and Pharmacokinetic Hypotheses
*   **Ester Hydrolysis:** The molecule contains a methyl ester, but the bounded sources did not identify compound-specific pharmacokinetic measurements, responsible enzymes, clearance rates, or characterized metabolites.
*   **Blood-Brain Barrier:** The bounded sources did not identify direct permeability or brain-tissue measurements. Behavioral observations alone do not measure brain exposure.

---

## 3. Compact Evidence Table

| Stated Effect / Claim | Assay / Test System | Species / Subjects | Compound Form & Route / Dose | Observed Finding | Direct Binding Measured? | Evidence Type & Source Access Level |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Verbal acquisition and retention** | Serial anticipation | Human subjects | PRL-8-53 HCl; details not exposed in the accessed abstract | Slight improvement in acquisition and statistically significant improvement in retention; no significant change in visual reaction time or motor control versus placebo. | **No** | **Primary study abstract.** Hansl & Mead (1978), PMID 418433. The full text is paywalled; participant count, dose, timing, task materials, and follow-up intervals repeated by secondary sources were not independently checked. |
| **Spasmolytic activity** | Ileum stimulated by acetylcholine, $\text{BaCl}_2$, and histamine | Isolated rabbit ileum | Form and concentration not stated in the patent passage | The patent presents class-level activity relative to papaverine. | **No** | **Inventor patent disclosure.** US Patent 3,870,715. The 1974 paper's citation and indexing were verified, but its full text was not accessed. |
| **Avoidance and maze performance** | Avoidance response (electric shock) and maze (water reward) | Rats | Patent passage does not state form, route, or dose | Patent reports facilitated acquisition and increased subsequent retention for the methyl ester. | **No** | **Inventor patent disclosure.** US Patent 3,870,715. No quantitative result appears in the cited passage. |
| **Preclinical toxicity** | Acute oral lethal dose | Mice | Patent passage does not fully specify form | Patent reports oral $\text{LD}_{50}$ of about 500–700 mg/kg. | **No** | **Inventor patent disclosure.** US Patent 3,870,715; not a clinical safety profile. |

---

## 4. Analogs and Structure-Activity Provenance

*   **Patent Analog Scope:** US Patent 3,870,715 discloses preparation of over 20 derivatives (ethyl, propyl, and cresyl esters; morpholino, piperidino, and diethylamino alkyl variations). The patent provides only blanket statements of spasmolytic and learning-facilitating utility for the class; it contains no per-compound binding data, dissociation constants, or quantitative concentration-response comparisons.
*   **Close Analogs in Modern Databases:** In `ChEMBL_37`, zero compounds possess $\ge 70\%$ Tanimoto similarity to PRL-8-53.
*   **Status:** The bounded searches did not establish an experimentally characterized close analog with measured molecular-target affinity. Generic structural features alone cannot establish a target ranking.

---

## 5. Plain-Prose Conclusion

1. **Identity:** PRL-8-53 is verified as methyl 3-[2-[benzyl(methyl)amino]ethyl]benzoate hydrochloride (CAS 51352-87-5).
2. **Measured Findings:** The accessed record comprises a 1974 preclinical citation without accessible abstract or full text, a 1975 inventor patent disclosure, and the abstract of a 1978 double-blind human study reporting improved verbal retention. The abstract does not expose the often-repeated participant, dose, or follow-up details.
3. **Unmeasured Inferences:** The bounded literature and database searches found no direct affinity measurement ($K_i$, $K_d$, or $\text{IC}_{50}$) for PRL-8-53 at a molecular target. Historical labels such as "dopaminergic potentiation," "partial serotonin inhibition," and "cholinergic agent" are not established binding results.
