# Public data provenance and replay limits

## Published files and historical inventories

The published file manifests and `SHA256SUMS` describe the current tree. They are refreshed after documentation edits and log removal. They do not establish original presearch chronology.

The historical source manifests, exp-004 presearch inventory, and saved validation report remain unchanged. Some recorded document hashes and byte counts do not match the public files. In exp-004, the presearch inventory has stale hashes for `inputs/source_manifest.json` and `protocol-prerun.md`. It also has stale byte counts for those files and `environment.txt`. The protocol's host-boundary sentence now refers to unrelated projects without naming a private project. Only the published manifest and checksums were refreshed for that privacy edit. The historical inventories were not rewritten.

The original exp-004 validator exits with a data/resource integrity failure. Its failed frozen-input entries are `inputs/source_manifest.json` and `protocol-prerun.md`. The archived passing `derived/validation.json` is a historical report, not a reproducible passing check against the current tree. Running the validator replaces that report with its current output.

The original validator checks hashes but not inventory byte counts or the source manifest's document records. The recorded scheduling deviation is separate: child nice values were 20 rather than 19. The saved poses, scores, tables, and resource observations have not been changed to hide either issue.

Rolf needs to resolve provenance before claiming complete validation. Rebuilding an inventory now cannot prove that edited documents existed before the searches. The original inventory builder always labels its output as frozen before search, even when saved poses exist. The original preparation script also pins historical source hashes. These scripts remain unchanged. The command records are historical reconstruction notes, not portable rerun instructions.

## Removed captures

Seventy-nine log files were removed: 73 empty captures, five package-installation or timing files, and one duplicate exp-003 preparation capture. The duplicate matched the retained `prepare_inputs.final.stdout.txt` byte-for-byte. Meaningful preparation failures, docking stdout, timings, export diagnostics, environment records, and monitor JSON remain.

Small source snapshots and saved poses remain, including duplicates that belong to separate evidence packages. They support the reported result and offline analysis. They are not disposable build output.

## Scientific boundaries

The ACC2 symmetry-interface geometry is descriptive. Both receptor chains were retained. The cause of the failed native-ligand control is unresolved. No PRL-8-53/ACC2 score exists.

The claim ledger identifies unavailable SwissTargetPrediction exports and service pages. Withdrawn generated literature excerpts remain removed. A source hash establishes byte identity, not biological truth. Internal AI-assisted review is not external peer review.

## Replay check

The README commands were checked again on 2026-10-08 in the worktree with Python 3.13.15 and a fresh isolated environment. `uv sync --frozen` and figure generation completed. All four PNGs matched the retained files byte-for-byte. SVG bytes differed; the unchanged generator includes dates and unfixed element IDs.

All three saved-pose analyses completed. Their ten tables and summaries matched the retained files byte-for-byte. Exp-002 and exp-003 output validation passed. Exp-004 output validation failed on the stale protocol and source-manifest hashes as described above. Its analysis checks passed and its recorded nice values remained 20. Coordinate and structural-evidence checks passed. All seven published checksum inventories passed across 593 entries.

Regenerated tracked output was discarded after comparison. Environment and cache files remain ignored. No Vina searches or ligand preparation were rerun. No GPU, paid account, or multi-GB download was used. No history or new Gitleaks scan was performed in this scope review.
