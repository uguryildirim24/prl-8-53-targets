# Third-party data and software

Everything under `research/` that was retrieved from someone else's database is listed here with its license and how it is used. Original text, figures, and generated analysis outputs are covered by [`LICENSE-docs`](LICENSE-docs) (CC BY 4.0). Code is covered by [`LICENSE`](LICENSE) (MIT). Generated CSV/TSV tables, JSON summaries, and poses use CC BY 4.0 only to the extent they are original contributions. Retrieved source records and adaptations keep their source terms, including ChEMBL share-alike requirements.

## Data

### RCSB PDB / wwPDB: CC0 1.0 Universal (public domain dedication)

Structure entries, polymer and non-polymer entity records, Chemical Component Dictionary definitions, deposited coordinates, and biological assemblies.

- Entries used: **3TDC**, **3FF6**, **5KKN** (ACC2 / ACACB); **6VRH**, **5I6X** (SERT / SLC6A4); **8EF5**, **4DKL**, **5C1M**, **9PXU** (μ-opioid receptor); chemical components **0EU**, **RCP**, **8PR**, **7V7**, **BF0**.
- Retained under: `research/acc2-evidence/`, `research/alternative-structure-evidence/`, `research/alternative-coordinate-evidence/raw/`, `research/experiments/exp-002/inputs/raw/`.
- Attribution: Berman, H.M. et al. (2000) *The Protein Data Bank.* Nucleic Acids Res. **28**:235 to 242. RCSB PDB data are released under CC0: <https://www.rcsb.org/pages/usage-policy>

### UniProt: CC BY 4.0

Canonical protein records and reference sequences.

- Accessions used: **O00763** (ACACB), **P31645** (SLC6A4/SERT), **P35372** (OPRM1), **P48048** (KCNJ1), **P06276** (BCHE), **Q12809** (KCNH2), **P42866** (mouse Oprm1, sequence comparison only).
- Retained under: `research/alternative-target-evidence/uniprot/`, `research/alternative-coordinate-evidence/raw/`, `research/experiments/exp-002/inputs/raw/`.
- Attribution: The UniProt Consortium (2025) *UniProt: the Universal Protein Knowledgebase.* Nucleic Acids Res. License: <https://www.uniprot.org/help/license>

### ChEMBL (EMBL-EBI), release 37: CC BY-SA 3.0

Molecule, activity, assay, target, and document records for the source compounds that drove each target prediction.

- Retained under: `research/experiments/exp-001/raw_data/chembl/`, `research/alternative-target-evidence/chembl/`, `research/acc2-evidence/`.
- **Share-alike note:** ChEMBL data are CC BY-SA 3.0. The retained JSON payloads in this repository are redistributed under that same license, not under CC BY 4.0. Adaptations of those specific records must be shared alike.
- Attribution: Zdrazil et al. (2024). Fuller bibliographic details are unverified in the retained source metadata, as noted in the manuscript claim ledger. DOI [`10.1093/nar/gkad1004`](https://doi.org/10.1093/nar/gkad1004). License: <https://chembl.gitbook.io/chembl-interface-documentation/about>

### PubChem (NCBI/NLM): public domain

Compound identity records used to reconcile PRL-8-53 across its free-base and salt forms. Used by identifier only; no PubChem record files are redistributed here.

- CIDs referenced: **39989** (free base, CAS 51352-88-6), **39988** and **70700868** (hydrochloride records, CAS 51352-87-5).
- Referenced in: `research/identity-and-evidence.md`, `research/experiments/exp-001/inputs.json`.
- Attribution: Kim, S. et al. (2025) *PubChem 2025 update.* Nucleic Acids Res. PubChem content is in the public domain, though individual depositor submissions may carry their own terms: <https://www.ncbi.nlm.nih.gov/home/about/policies/>

### US patent documents: public domain (US)

- **US 3,870,715** (Hansl, 1975): the PRL-8-53 inventor patent; used for compound identity and for the historical rabbit-ileum, rat-behaviour, and mouse LD50 observations.
- **US 9,340,510 B2** (Boehringer Ingelheim, 2016): biological-testing paragraphs [0224]-[0235] describing the coupled hACC2 assay behind the ACC2 source compound's reported IC50. Excerpt retained at `research/acc2-evidence/us9340510b2-primary-excerpt.txt`.
- Published US patent grants are not subject to US copyright. Retrieved via Google Patents; the URL and retrieval timestamp are recorded in the excerpt header and in `research/acc2-evidence/manifest.md`.

### SwissTargetPrediction (SIB Swiss Institute of Bioinformatics): cited, not redistributed

The ligand-based target prediction that produced the initial six-target shortlist came from this service. **Its result material is not included in this repository.** What is here is a hand-written summary of which targets were carried forward and why ([`docs/target-shortlist.md`](docs/target-shortlist.md)), plus the ChEMBL records for the source compounds, independently retrieved from the ChEMBL API.

- Attribution: Daina, A., Michielin, O. & Zoete, V. (2019) *SwissTargetPrediction: updated data and new features for efficient prediction of protein targets of small molecules.* Nucleic Acids Res. **47**:W357-W364. DOI [`10.1093/nar/gkz382`](https://doi.org/10.1093/nar/gkz382). Related methods: Gfeller, D., Michielin, O. & Zoete, V. (2013) DOI [`10.1093/bioinformatics/btt536`](https://doi.org/10.1093/bioinformatics/btt536); Daina, A. & Zoete, V. (2024) DOI [`10.1038/s42004-024-01179-2`](https://doi.org/10.1038/s42004-024-01179-2).
- Service: <https://www.swisstargetprediction.ch/>

## Software

None of the following is vendored in this repository.

| Tool | Version used | License |
|---|---|---|
| [AutoDock Vina](https://github.com/ccsb-scripps/AutoDock-Vina) | 1.2.7 | Apache-2.0 |
| [RDKit](https://www.rdkit.org/) | 2026.03.6 | BSD-3-Clause |
| [Meeko](https://github.com/forlilab/Meeko) | 0.8.0 | LGPL-2.1 |
| [gemmi](https://gemmi.readthedocs.io/) | 0.7.5 | MPL-2.0 |
| [NumPy](https://numpy.org/) | 2.5.3 | BSD-3-Clause |
| [SciPy](https://scipy.org/) | 1.18.1 | BSD-3-Clause |
| [Matplotlib](https://matplotlib.org/) | ≥3.9 (figures only) | PSF-based (matplotlib license) |

Vina citations: Eberhardt, J., Santos-Martins, D., Tillack, A.F. & Forli, S. (2021) *AutoDock Vina 1.2.0: New Docking Methods, Expanded Force Field, and Python Bindings.* J. Chem. Inf. Model. **61**:3891 to 3898. Trott, O. & Olson, A.J. (2010) *AutoDock Vina.* J. Comput. Chem. **31**:455 to 461.

## A note on checksums

The `SHA256SUMS` files in each evidence and experiment folder were regenerated for this public release, after material that is not redistributed here was removed. They verify the files as published in this repository. See [the release note](docs/release-review.md) for the unchanged historical inventory mismatch and removed captures.

## New downloads

Keep new datasets and downloads in ignored `data/`, `datasets/`, or `.local-tools/`. The small retained source snapshots and poses support the published result and offline analysis; do not replace them with fresh API responses. Source manifests and retrieval sidecars record the original endpoints, timestamps, and hashes.

To fetch a separate coordinate package without changing retained evidence:

```sh
uv run --frozen research/alternative-coordinate-evidence/scripts/fetch_official.py \
  --out .local-tools/coordinate-evidence
```

This fetch uses the official archives named in the script. It is not needed for the offline README commands. SwissTargetPrediction material is intentionally unavailable here. Do not automate service queries or add withdrawn generated summaries as evidence.
