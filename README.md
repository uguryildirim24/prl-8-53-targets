# What does PRL-8-53 actually bind?

An evidence audit and a set of limited docking checks on the molecular-target hypotheses for PRL-8-53, a 1970s experimental nootropic with behavioural reports but no established mechanism.

**The honest answer, in three lines:**

1. **No binding target is established.** Nothing in the retained literature, patents, or public bioactivity databases contains a measured PRL-8-53 Ki, Kd, IC50, EC50, or binding pose — and that absence is a bounded search result, not proof that no measurement exists anywhere.
2. **ACC2 was the leading computational prediction, and the ACC2 work stopped before PRL-8-53 was ever docked** — the native-ligand redocking control failed, so there is no PRL-8-53/ACC2 score to report.
3. **SERT passed its control and produced PRL-8-53 poses, but those poses are uncalibrated model output** — they are preparation-sensitive, they sit in a rigid stripped receptor, and they are not evidence that PRL-8-53 binds SERT.

The useful product of this work is an auditable shortlist of hypotheses with the reason each one is unresolved, plus explicit failure evidence. That is a negative result, and it is reported as one.

> PRL-8-53 is an experimental compound. Nothing here is medical advice, and nothing here is a claim about efficacy, potency, selectivity, or safety. Docking scores are model behaviour, not affinity.

---

## The controls decided the outcome

![Native-ligand redocking controls](figures/fig1-redocking-controls.png)

Before docking PRL-8-53 anywhere, each receptor setup had to reproduce its own deposited ligand. The ACC2 pocket in **3TDC** failed: across three seeds, the top-ranked pose landed ~9.0 Å from the crystal geometry, reproducibly — the search found the *same wrong answer* every time, which is worse than a noisy one. The planned PRL-8-53 stage was cancelled. The SERT pocket in **6VRH** passed: in all six paroxetine searches, the pose closest to the deposit was also rank 1, at 0.56–0.62 Å (neutral) and 1.62–1.65 Å (protonated).

![Why the ACC2 pilot stopped](figures/fig4-acc2-site-and-poses.png)

The reason ACC2 failed is structural, and it is visible: the `0EU` site in 3TDC straddles a crystallographic symmetry interface. Fourteen of the twenty residues within 4.5 Å of the deposited ligand belong to the symmetry mate, not to chain A. That is a property of that particular pocket preparation — it neither tests nor excludes PRL-8-53 binding to ACC2.

![Top-ranked Vina scores in the shared SERT setup](figures/fig2-vina-scores.png)

In the one setup that passed its control, PRL-8-53 scored worse than the native ligand. That is not a potency comparison and it is not evidence of anything about SERT — it is two molecules' model output in one identical box, shown because it is the only place in this project where a PRL-8-53 score and a reference score exist side by side at all.

A fourth figure, [`figures/fig3-prl-pose-variability.png`](figures/fig3-prl-pose-variability.png), shows how far apart the exploratory PRL-8-53 top poses landed across seeds and starting conformers.

---

## Method

| Stage | What was done | Outcome |
|---|---|---|
| **Identity control** | Reconciled PRL-8-53 across PubChem records and US Patent 3,870,715. Free base (CID 39989) and the two salt records were kept distinct, since a disconnected salt record is not a covalent species. | [`research/identity-and-evidence.md`](research/identity-and-evidence.md) |
| **Bounded evidence audit** | ChEMBL 37, PubChem BioAssay, PubMed, Europe PMC, plus bounded checks of BindingDB, DrugBank, and the IUPHAR/BPS Guide to PHARMACOLOGY. Endpoint behaviour and zero-result queries were recorded rather than read as universal absence. | [`research/evidence-sources.md`](research/evidence-sources.md) |
| **Target shortlist** | Ligand-based prediction from the SwissTargetPrediction web server, then an independent trace of every named source compound back to its ChEMBL activity, assay, target, and document records. Shared compounds and shared publications were treated as *dependence*, not corroboration. | [`docs/target-shortlist.md`](docs/target-shortlist.md), [`research/alternative-target-audit.md`](research/alternative-target-audit.md) |
| **Structural triage** | Audited RCSB, wwPDB, UniProt, and Chemical Component Dictionary records for ACC2, SERT, and μ-opioid receptor structures; inventoried assemblies, modelled sequence, ligand copies, occupancy, contacts, and missing atoms. Experimental maps were *not* inspected. | [`research/alternative-coordinate-evidence/`](research/alternative-coordinate-evidence/), [`research/alternative-structure-evidence/`](research/alternative-structure-evidence/) |
| **Docking with validation** | AutoDock Vina 1.2.7, rigid receptor, default `vina` scoring function. Every receptor had to redock its own deposited ligand first. RMSD measured in the unchanged deposited frame over stereochemistry-preserving graph automorphisms, with no ligand fitting. | [`exp-002`](research/experiments/exp-002/), [`exp-003`](research/experiments/exp-003/), [`exp-004`](research/experiments/exp-004/) |

The four experiments in order:

- **[exp-001](research/experiments/exp-001/)** — target prediction and the ACC2 source-compound trace. ACC2/ACACB ranked first; its nearest source compound is a tetrahydroisoquinoline whose single ACC2 record is a *coupled-enzyme* IC50 with no counterscreen, which is inhibition, not binding.
- **[exp-002](research/experiments/exp-002/)** — ACC2 native-ligand redocking pilot in 3TDC. **Stopped by design** when the control failed. No PRL-8-53 score exists.
- **[exp-003](research/experiments/exp-003/)** — SERT reference pilot in 6VRH. Six paroxetine searches; the control passed.
- **[exp-004](research/experiments/exp-004/)** — exploratory PRL-8-53 docking in the byte-identical exp-003 receptor and box: 2 charge states × 2 starting conformers × 3 seeds = 12 fixed searches, 240 retained modes, 14,280 within-state pairwise RMSDs.

The full manuscript draft is [`manuscript/draft.md`](manuscript/draft.md), and every numbered claim in it is traced to a specific file and field in [`manuscript/claim-ledger.md`](manuscript/claim-ledger.md).

---

## Repository map

```
README.md                    you are here
CITATION.cff                 how to cite this work
DATA-SOURCES.md              third-party data and their licenses
LICENSE / LICENSE-docs       MIT for code, CC BY 4.0 for text and figures
pyproject.toml               environment for the figure script

figures/                     every figure, PNG + SVG, regenerated by script
scripts/make_figures.py      builds figures/ from data already in this repo

manuscript/
  draft.md                   draft preprint (not peer reviewed)
  claim-ledger.md            claim -> file -> field -> limitation, for every claim
  readiness.md               what would still need to happen before submission

docs/
  target-shortlist.md        the six candidate targets and why each is unresolved
  process/                   planning and feasibility memos kept for provenance

research/
  identity-and-evidence.md   compound identity reconciliation
  evidence-sources.md        bounded literature and database search log
  target-methods.md          methods review and uncertainty assessment
  alternative-target-audit.md   evidence appraisal for prediction ranks 2-6
  acc2-evidence/                ChEMBL, RCSB and patent records for ACC2
  alternative-target-evidence/  ChEMBL and UniProt records for ranks 2-6
  alternative-structure-evidence/  RCSB entry and polymer records
  alternative-coordinate-evidence/ deposited coordinates and contact analysis
  experiments/exp-001 .. exp-004   scripts, inputs, logs, poses, tables, manifests
```

Every experiment folder carries the same layout: `scripts/` (what ran), `inputs/` (what went in, with source hashes), `derived/` (prepared receptors, ligands, summaries), `poses/` (every saved docking mode), `logs/` (raw stdout/stderr and resource monitors), `tables/` (CSV results), `manifest.md`, `results.md`, and `SHA256SUMS`.

---

## Reproducing this

### The figures

Everything in `figures/` is generated from data already committed here — no network, no docking rerun.

```sh
git clone https://github.com/uguryildirim24/prl-8-53-targets.git
cd prl-8-53-targets
uv run scripts/make_figures.py
```

That needs only `matplotlib`; `uv` resolves it from [`pyproject.toml`](pyproject.toml) on first run.

### The docking

The docking runs themselves need the full stack recorded in each experiment's `environment.txt`: **AutoDock Vina 1.2.7** (macOS arm64 release binary, SHA-256 `823c2bba…d623f1`), **RDKit 2026.03.6**, **Meeko 0.8.0**, **gemmi 0.7.5**, **numpy 2.5.3**, **scipy 1.18.1**, Python 3.13. The Vina binary is not vendored here, and there is no complete dependency lock — versions and the binary hash are recorded instead, so an equivalent environment has to be rebuilt to rerun the searches. The exact command lines are in each experiment's `commands.md` and in the per-run `logs/docking/*/*.monitor.json`.

Every search used fixed seeds, so a matching environment should reproduce the saved poses. The saved poses, logs, tables, and checksums are all committed, so the *analysis* can be re-derived without rerunning Vina at all.

---

## Limitations

These are the ones that matter most; the full list is in the [manuscript's discussion](manuscript/draft.md) and in [`manuscript/claim-ledger.md`](manuscript/claim-ledger.md).

- **No PRL-8-53 measurement exists in the retained evidence.** Every number in this repository describes either a *different* compound or a *model*.
- **The literature review was bounded.** The 1978 human study was read as an abstract only; the 1974 preclinical report was available as citation metadata only and its contents are not characterised here. Database zero-results do not prove global absence.
- **Docking scores are not affinities.** Vina's default function has no explicit Coulomb term, no numerical pass threshold was declared in any protocol, and no cross-target ranking can be built from these numbers — prediction scores, source-compound IC50 values, redocking geometry, and PRL-8-53 docking scores are not commensurate quantities.
- **The receptor models are simplified.** Rigid receptor, stripped waters, no sodium, removed chloride, template histidine protonation, missing termini, and two incomplete residues deleted with uncapped gaps. Experimental density maps were never inspected.
- **Chemical state is unresolved.** No compound-specific pKa was found, so neutral and protonated were both modelled and neither is claimed to be physiological. The two preparations also differ in starting geometry, so the lower variability of the protonated sample cannot be attributed to charge.
- **Native-pose recovery validates a setup, not a ligand.** A passing control means the geometry of that one model is self-consistent. It says nothing about an unknown ligand in that pocket.
- **`SHA256SUMS` files were regenerated for this public release**, after material that is not redistributed here was removed. They verify the files in *this* repository, not the internal working copy.

---

## How this was built

I did this work with AI coding assistants (Claude Code) under my direction: they ran the searches, wrote the analysis scripts, and drafted text, while the protocols, the validation gates, and the decision to stop the ACC2 pilot were mine. Every retained claim is traced to a specific file and field in the [claim ledger](manuscript/claim-ledger.md), each docking stage had a native-ligand control that had to pass before the next stage ran, and a set of files that turned out to be AI-generated summaries rather than primary literature were found during review, withdrawn, and removed. I am responsible for the scientific content.

---

## Citation

If you use this work, please cite it via [`CITATION.cff`](CITATION.cff):

> Yildirim, H. U. (2026). *PRL-8-53 target hypotheses: a bounded evidence audit and limited docking checks.* https://github.com/uguryildirim24/prl-8-53-targets

The manuscript in `manuscript/` is a **draft preprint and has not been peer reviewed**.

---

## License

- **Code** (`scripts/`, every `*.py` and `*.sh` under `research/`): MIT — see [`LICENSE`](LICENSE).
- **Text and figures** (`README.md`, `manuscript/`, `docs/`, `figures/`, and the `*.md` documentation under `research/`): CC BY 4.0 — see [`LICENSE-docs`](LICENSE-docs).
- **Third-party data** retained under `research/` keeps its own license. See [`DATA-SOURCES.md`](DATA-SOURCES.md).

---

**Hasan Ugur (Rolf) Yildirim** · BS Biochemistry, Lasell University, Newton MA · expected May 2027
