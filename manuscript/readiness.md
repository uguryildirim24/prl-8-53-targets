# Manuscript readiness checklist

This folder contains:

- [`draft.md`](draft.md): the unpublished manuscript draft. Not peer reviewed.
- [`claim-ledger.md`](claim-ledger.md): claim, result, citation, and limitation trace, with unavailable service material marked.

The draft is not submitted anywhere. The gaps below are what would need closing first.

## Publication-readiness gaps

- [x] Internal claim-by-claim and citation review of the draft and ledger, including direct checks of the ChEMBL payloads, structure-entry records, and experiment tables retained here. This is not external peer review.
- [ ] Independent human/external claim and citation review.
- [x] Rolf's name and affiliation are recorded. Funding “None” and competing interests “None declared” are existing declarations, not inferred by the release cleanup.
- [ ] Rolf should reconfirm funding, competing interests, contribution wording, and scientific responsibility before submission.
- [ ] Final sign-off from a faculty reader on wording and scientific responsibility. The AI-assistance disclosure is in the draft.
- [ ] Decide whether abstract-only and patent-supported historical claims are sufficient for the intended venue; full historical texts were not reviewed here.
- [x] Prediction-service result material is not redistributed with this work; the shortlist is described in Rolf's own words with the service cited as the prediction source.
- [ ] Verify the final bibliography against source records/full texts available to the authors. The internal review corrected three article page/issue ranges and filled details found in retained source records; it did not obtain missing full texts. Reference 15 retains only the author shorthand, year, and DOI supported by the reviewed experiment manifest because its fuller citation appears solely in an earlier generated methods synthesis, not retained official/source bibliographic metadata.
- [x] Figure dependencies are locked. Saved-pose replay commands use recorded package versions in the README.
- [ ] Resolve the stale exp-004 inventory without misrepresenting original presearch provenance. Its validator currently fails; see `docs/release-review.md`.
- [ ] Define a durable original search/preparation archive if turnkey docking reconstruction is required. Vina and the original preparation runtime are not vendored or fully locked.
- [ ] Select a venue and apply its formatting, data-policy, reporting, and declaration requirements only after the scientific draft is approved.
- [ ] Confirm that no ethics statement beyond “no new human or animal experiment” is required for the chosen venue.
- [ ] Obtain any required permissions for third-party database/service material and attribution.

## Scientific boundary to preserve during editing

No PRL-8-53 binding target or calibrated biological target order was established. ACC2 and SERT remain hypotheses for different reasons; other ranked targets remain unresolved rather than excluded. Docking outputs are model behavior, not affinity, efficacy, safety, or target confirmation.
