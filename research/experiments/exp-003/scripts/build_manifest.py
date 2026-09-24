#!/usr/bin/env python3
"""Build exp-003 file manifest and SHA256SUMS."""
from __future__ import annotations
import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXCLUDED = {"manifest.md", "SHA256SUMS"}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def files(exclude_manifest=True):
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.name == "SHA256SUMS":
            continue
        if exclude_manifest and path.name == "manifest.md":
            continue
        yield path


def role(path):
    rel = path.relative_to(ROOT)
    if rel.parts[0] == "poses": return "raw search output/export"
    if rel.parts[0] == "logs": return "raw command/resource log"
    if rel.parts[0] == "tables": return "generated analysis table"
    if rel.parts[0] == "derived": return "prepared input/generated analysis"
    if rel.parts[0] == "inputs": return "source ledger"
    if rel.parts[0] == "scripts": return "reproduction script"
    return "protocol/report/provenance"


def main():
    rows = [(p.relative_to(ROOT).as_posix(), p.stat().st_size, digest(p), role(p)) for p in files()]
    lines = ["# exp-003 manifest", "", "Generated inventory of experiment files. Preserved official source bytes remain in `../../alternative-coordinate-evidence/raw/`; `inputs/source_manifest.json` records and verifies their hashes without duplicating them here. `manifest.md` excludes itself; `SHA256SUMS` covers it.", "", "| File | Bytes | SHA-256 | Role |", "|---|---:|---|---|"]
    for name, size, sha, item_role in rows:
        lines.append(f"| `{name}` | {size} | `{sha}` | {item_role} |")
    (ROOT / "manifest.md").write_text("\n".join(lines) + "\n")
    checksum_rows = []
    for path in files(exclude_manifest=False):
        checksum_rows.append(f"{digest(path)}  {path.relative_to(ROOT).as_posix()}")
    (ROOT / "SHA256SUMS").write_text("\n".join(checksum_rows) + "\n")
    print(f"manifest_files={len(rows)} checksum_files={len(checksum_rows)}")


if __name__ == "__main__":
    main()
