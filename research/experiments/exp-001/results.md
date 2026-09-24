# Experiment 001 — first PRL-8-53 target prediction

## Result in one paragraph

Target predictions were obtained from the SwissTargetPrediction web server for the verified neutral and protonated PRL-8-53 structures against *Homo sapiens*. The service accepted distinct canonical strings that retained the neutral tertiary amine or an explicit positive charge, but the two complete 100-target rankings were identical. They therefore show no representation sensitivity and are not independent support. The highest-ranked hypothesis was acetyl-CoA carboxylase 2 (ACACB; UniProt O00763; CHEMBL4829). The service's `Probability*` field, about 0.71, is explicitly conditional on the query being bioactive; it is not a measured or absolute binding probability. Inspection found one reasonably related source compound, but no evidence that PRL-8-53 itself binds ACACB. No absolute binding confidence can be assigned from this run.

## What ran

| Scenario | Submitted SMILES | Service-accepted/canonicalized SMILES |
|---|---|---|
| Neutral | `CN(CCc1cccc(c1)C(=O)OC)Cc2ccccc2` | `COC(=O)c1cccc(c1)CCN(Cc1ccccc1)C` |
| Protonated | `C[NH+](CCc1cccc(c1)C(=O)OC)Cc2ccccc2` | `COC(=O)c1cccc(c1)CC[NH+](Cc1ccccc1)C` |

Both queries used the site's standard one-molecule web form, selected `Homo_sapiens`, and returned a 100-target ranking. Parsing confirmed 100 rows rather than relying on the browser table's initial "15 of 100" display. The two rankings were byte-identical.

The service's result material is not redistributed here. The targets carried forward, with identifiers and the reason for each, are in [`docs/target-shortlist.md`](../../../docs/target-shortlist.md). The service terms were checked before the queries were run: they were last updated 2023-11-28, permit private study and internal research, and license result materials under CC BY 4.0. The About page states the model uses about 370,000 known actives over more than 3,000 proteins, and the service exposes no current training-database release identifier, so none is inferred here.

## The candidate examined: ACACB

The full ranking was read, but this bounded experiment interprets only the top-ranked target. The other 99 names are not treated as candidate evidence here because their nearest-actives and assays were not traced. (Ranks 2–6 were traced separately in [`research/alternative-target-audit.md`](../../alternative-target-audit.md).) The service reports ACACB as rank 1, UniProt O00763, CHEMBL4829, target class "Ligase," with 3,703 3D and 487 2D known actives in its pool. Its interface exposes at most 200 nearest actives per method. Because the service exposes no current training release, "source compound" below does not assert that a particular record or current ChEMBL row was in the trained model.

### Nearest 2D source compound

- **CHEMBL3928386**, InChIKey `QEUWJQXZXZICOI-UHFFFAOYSA-N`
- ChEMBL canonical SMILES: `COC(=O)c1ccc2c(c1)CCN(Cc1ccc(C(C)NC(C)=O)cc1)C2`
- Reported FP2 similarity to PRL-8-53: **0.764706**; also fourth on the 3D list at **0.787**.
- ChEMBL 37 has exactly one CHEMBL4829-filtered activity row (`page_meta.total_count: 1`, `next: null`): **IC50 = 524 nM**, relation `=`, standard units nM, activity 17768979. ChEMBL maps the row to its human ACACB target, but the assay's target assignment is **homologous single protein**, confidence score 8 — not a conclusive direct human-protein assignment.
- Assay CHEMBL3888444 labels its organism `Homo sapiens` and its description says `hACC2`, but `assay_tax_id` is absent and the captured record does not identify the enzyme preparation or sequence. It measures loss of NADH absorbance at 340 nm in a coupled system containing ACC2, pyruvate kinase, and lactate dehydrogenase. This is an indirect enzyme-inhibition readout, not a binding affinity (`Ki`/`Kd`) or evidence that the ligand physically binds ACC2. The captured controls are vehicle and omission of acetyl-CoA; no compound-interference or coupling-enzyme counterscreen was captured, so inhibition of a coupling enzyme or optical interference is not excluded by this record. The source is patent US-9340510-B2 (document CHEMBL3886715).

The ligand shares both aromatic regions, a methyl aromatic ester, a tertiary amine, and an N-benzyl-like connection with PRL-8-53. It is nevertheless a ring-constrained tetrahydroisoquinoline bearing an extra acetamidoethyl substituent, whereas PRL-8-53 has a flexible benzyl(methyl)aminoethyl chain. The similarity therefore reflects a recognizable but materially different chemotype, not a close identity.

### Nearest 3D source compound

- **CHEMBL1910396**, InChIKey `UMEWLRYFBAISSB-UHFFFAOYSA-N`
- ChEMBL canonical SMILES: `CC1(C)CC2(CCCN(C3CCN(C(=O)c4c(N)sc5ccccc45)CC3)C2)C(=O)O1`
- Reported 3D similarity to PRL-8-53: **0.830**.
- ChEMBL 37 again has exactly one CHEMBL4829-filtered activity row (`total_count: 1`, `next: null`): **IC50 = 750 nM**, relation `=`, for ChEMBL's human ACACB target, activity 7846231.
- This is an inhibition IC50, not an affinity measurement. Assay CHEMBL1912973 says "Inhibition of human ACC2," records `assay_tax_id: 9606`, uses a single-protein format, and has a direct protein target assignment (confidence score 9). The captured one-line assay description gives no protocol or counterscreen details and still does not demonstrate physical binding. The source is Yamashita et al., *Bioorg Med Chem Lett* 2011, DOI `10.1016/j.bmcl.2011.08.117` (document CHEMBL1909501).

This spirocyclic diamine/lactone/benzothiophene amide is topologically unlike PRL-8-53 and lacks its methyl-benzoate/flexible diaryl-amine architecture. Its high 3D score alone is not coherent structural support.

## Interpretation and uncertainty

SwissTargetPrediction explicitly assumes the query is bioactive. Its displayed `Probability*` is a conditional target-ranking output, not an absolute probability that PRL-8-53 binds ACACB. The neutral and protonated rankings being identical does not replicate the finding. The prediction and the ChEMBL trace are correlated through the ChEMBL literature corpus; the trace characterizes current records associated with two source ligands but is not independent validation. The service does not expose its current training release, so the current ChEMBL 37 rows cannot prove which database snapshot, assay rows, or ligands contributed to the model.

The experiment identifies **ACACB as a prediction to test**, not an empirically supported PRL-8-53 target. The best 2D source ligand preserves several structural features, but its sole target-filtered IC50 comes from the homologously assigned coupled assay described above. The experiment does not establish PRL-8-53 inhibition, binding, cellular activity, efficacy, mechanism, therapeutic effect, or safety. No PRL-8-53 `Ki`, `Kd`, `IC50`, or `EC50` was found.

## Docking decision

Structure selection and docking are outside this experiment. Before any separate pilot, the human ACC2 construct, pocket, and a genuinely site-resolved control ligand would need independent support; the captured coupled-assay IC50 does not identify a binding site. Docking could test pose compatibility within one chosen pocket but could not convert this prediction into binding evidence. No other ranked target is recommended from this bounded run because its nearest-active and assay evidence was not traced here.
