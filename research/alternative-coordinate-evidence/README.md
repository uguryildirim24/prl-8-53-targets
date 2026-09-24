# 6VRH/8EF5 coordinate evidence

Bounded evidence for `research/alternative-coordinate-feasibility.md`.

- `raw/`: unchanged official response bodies (RCSB/wwPDB/UniProt), including deposited and biological-assembly mmCIFs. No map files.
- `retrieval/`: one JSON sidecar per response with requested/final URL, redirect chain, headers, actual UTC times, status, size and SHA-256.
- `scripts/`: standard-library retrieval, mmCIF parsing, analysis, validation and manifest scripts.
- `generated/`: deterministic coordinate/sequence/validation summaries. These include exact entity coverage, coordinate/unobserved-atom occupancy records, full local standard-residue heavy-atom checks, CCD atom/element matching and wwPDB ligand-copy identifiers. The 4.0 Å tables are descriptive geometry, not biological thresholds.
- `runlogs/`: actual command output, `/usr/bin/time -l` measurements and environment capture.
- `commands.md`: exact commands and resource controls.
- `manifest.md`: generated official-input inventory.
- `SHA256SUMS`: package integrity list (excluding itself).

The analysis does not dock, alter coordinates, inspect density maps, or contact SwissTargetPrediction.
