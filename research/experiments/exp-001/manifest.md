# Experiment 001 reproducibility manifest

## Scope

One bounded target-prediction step for PRL-8-53, run for two charge representations against *Homo sapiens*, followed by an independent ChEMBL trace of the source compounds the prediction named. The structured inputs are in `inputs.json`. Nothing in this folder is a wet-lab result.

## Prediction source

Target predictions were obtained from the [SwissTargetPrediction](https://www.swisstargetprediction.ch/) web server, operated by the SIB Swiss Institute of Bioinformatics. Method citations named by the service are Daina, Michielin & Zoete (2019), DOI `10.1093/nar/gkz382`; Daina & Zoete (2024), DOI `10.1038/s42004-024-01179-2`; and Gfeller, Michielin & Zoete (2013), DOI `10.1093/bioinformatics/btt536`.

**The service's result material is not redistributed in this repository.** What is retained is the query identity (`inputs.json`), the reading of the result (`results.md`), the list of targets carried forward ([`docs/target-shortlist.md`](../../../docs/target-shortlist.md)), and the independently retrieved ChEMBL records for the source compounds the service named (`raw_data/chembl/`). Anyone wanting the ranking itself should run the query at the service.

Environment versions are captured in `environment.txt`.

## ACACB source-compound evidence

Only the top-ranked target, ACACB, is interpreted in `results.md`. The two source compounds discussed there are structured in `source-ligand-trace.json` with identifiers, structures, assay endpoint type, relation, units, species labels, target-assignment confidence, readout limitations, and document provenance. A compound appearing on a nearest-actives list does not establish that it was in any particular training release of the model.

## ChEMBL validation evidence

All ChEMBL requests used the public JSON API and are preserved verbatim under `raw_data/chembl/`, with adjacent request timing and response headers:

- `status.json`: database status/version at collection time.
- `target-CHEMBL4829.json`: target identity and species.
- `molecule-CHEMBL1910396.json`, `molecule-CHEMBL3928386.json`: source structures and identifiers.
- `activities-*-CHEMBL4829.json`: target-filtered activities requested with `limit=1000`. Each response has `total_count: 1`, `next: null`; pagination is complete.
- `assay-CHEMBL1912973.json`, `assay-CHEMBL3888444.json`: assay format, organism, assignment, and description.
- `document-CHEMBL1909501.json`, `document-CHEMBL3886715.json`: publication/patent provenance.

No absent affinity or assay measurements were filled from inference. `source-ligand-trace.json` separates transcribed fields from explicit interpretation notes. In particular, CHEMBL3888444 has a `Homo sapiens` organism label and says `hACC2`, but has no assay taxon ID, no captured construct/sequence, and only a homologous target assignment (confidence 8). Its NADH readout is coupled through pyruvate kinase and lactate dehydrogenase; the captured record contains no counterscreen against the coupling enzymes or compound optical interference.

## Failure-mode checks

- **Wrong identity:** the submitted free-base identity is CID 39989 / InChIKey `IGJQEMHBYKNIQR-UHFFFAOYSA-N`; salt CIDs are explicitly marked not submitted in `inputs.json`.
- **Canonicalization:** the submitted and the service-accepted strings were both checked. Charge was preserved in the displayed accepted structures.
- **Charge sensitivity:** the neutral and protonated queries returned identical rankings; this is reported as *no observed sensitivity*, not as duplicate support.
- **Truncated ranking:** the complete 100-target ranking was read, not the initial 15-row browser view.
- **Truncated nearest-actives:** the service caps its nearest-actives tables at 200 rows per method; the numbers it reports for the full pools are larger, and no claim is made that the visible rows are the whole pool.
- **Units/relations:** ChEMBL's `IC50`, `=`, values, and `nM` units are retained. Neither source result is called `Ki` or `Kd`; enzyme inhibition is not direct binding.
- **Target assignment/readout:** the 524 nM row is not described as conclusively measured on a verified human ACACB construct. The ChEMBL target mapping, homologous confidence-8 assignment, missing assay taxon ID, coupled enzymes, captured controls, and absent counterscreens are kept distinct.
- **Shared provenance:** the prediction and the ChEMBL trace are treated as correlated use of the same literature corpus, not independent validation.

## Attribution

ChEMBL evidence is from ChEMBL 37; database citation: Zdrazil et al. (2024), DOI `10.1093/nar/gkad1004`. See [`DATA-SOURCES.md`](../../../DATA-SOURCES.md) for the full list of third-party sources and their licenses.

## Integrity

`SHA256SUMS` lists SHA-256 hashes for every file in the experiment except the checksum file itself. It was regenerated for this public release after the prediction-service material was removed, so it does not match the internal working copy. Regenerate after intentional changes with:

```sh
find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 shasum -a 256 > SHA256SUMS
```
