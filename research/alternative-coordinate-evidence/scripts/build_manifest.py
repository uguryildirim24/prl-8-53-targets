#!/usr/bin/env python3
"""Build the retrieval manifest and package checksum list from preserved files."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    root = args.evidence
    records = []
    for metadata_path in sorted((root / "retrieval").glob("*.retrieval.json")):
        record = json.loads(metadata_path.read_text(encoding="utf-8"))
        record["metadata_file"] = metadata_path.relative_to(root).as_posix()
        records.append(record)

    lines = [
        "# Official-input retrieval manifest",
        "",
        "This table is generated from the per-response sidecars in `retrieval/`. Raw response bodies are preserved unchanged in `raw/`; generated analyses are separate in `generated/`. Redirect arrays are preserved even when empty.",
        "",
        "| Payload | Bytes | SHA-256 | HTTP | Completed UTC | Requested URL | Final URL | Redirects |",
        "|---|---:|---|---:|---|---|---|---:|",
    ]
    for record in records:
        payload = str(record["payload"])
        name = payload.split("/", 1)[1]
        lines.append(
            f"| [`{name}`]({payload}) | {record['bytes']} | `{record['sha256']}` | {record['http_status']} | "
            f"{record['completed_utc']} | <{record['requested_url']}> | <{record['final_url']}> | {len(record['redirects'])} |"
        )
    (root / "manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    excluded = {"SHA256SUMS"}
    files = sorted(path for path in root.rglob("*") if path.is_file() and path.name not in excluded)
    checksum_lines = [f"{digest(path)}  {path.relative_to(root).as_posix()}" for path in files]
    (root / "SHA256SUMS").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    print(f"wrote manifest for {len(records)} responses and checksums for {len(files)} files")


if __name__ == "__main__":
    main()
