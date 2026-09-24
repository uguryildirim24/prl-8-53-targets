#!/usr/bin/env python3
"""Build exp-004 manifest and checksum list without self-reference."""
import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def files(include_manifest=False):
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.name == "SHA256SUMS": continue
        if not include_manifest and path.name == "manifest.md": continue
        yield path

def role(path):
    first = path.relative_to(ROOT).parts[0]
    return {"poses": "raw search output/export", "logs": "raw command/resource log",
            "tables": "generated analysis table", "derived": "prepared input/generated analysis",
            "inputs": "source/pre-search ledger", "scripts": "reproduction script"}.get(first, "protocol/report/provenance")

rows = [(p.relative_to(ROOT).as_posix(), p.stat().st_size, digest(p), role(p)) for p in files()]
lines = ["# exp-004 manifest", "", "Generated inventory of experiment files. Reused exp-003 and retained identity/source bytes are not duplicated; `inputs/source_manifest.json` and `inputs/presearch_inventory.json` pin them by hash. `manifest.md` excludes itself; `SHA256SUMS` includes it.", "", "| File | Bytes | SHA-256 | Role |", "|---|---:|---|---|"]
for name, size, sha, item_role in rows: lines.append(f"| `{name}` | {size} | `{sha}` | {item_role} |")
(ROOT / "manifest.md").write_text("\n".join(lines)+"\n")
checks = [f"{digest(p)}  {p.relative_to(ROOT).as_posix()}" for p in files(include_manifest=True)]
(ROOT / "SHA256SUMS").write_text("\n".join(checks)+"\n")
print(f"manifest_files={len(rows)} checksum_files={len(checks)}")
