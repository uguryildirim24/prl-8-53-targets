#!/usr/bin/env python3
"""Fetch the bounded official records used in the 6VRH/8EF5 coordinate audit.

Uses only Python's standard library. Response bodies are saved unchanged. A sidecar
JSON records request/final URLs, redirects, response headers, UTC times, byte count,
and SHA-256. Existing payloads are never overwritten unless --force is supplied.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

MAX_BYTES = 25 * 1024 * 1024
UA = "prl-8-53-coordinate-audit/1.0 (bounded academic reproducibility fetch)"

BASE_REQUESTS = [
    ("rcsb-entry-{pdb}.json", "https://data.rcsb.org/rest/v1/core/entry/{pdb}"),
    ("{pdb}.cif", "https://files.rcsb.org/download/{pdb}.cif"),
    ("{pdb}-assembly1.cif", "https://files.rcsb.org/download/{pdb}-assembly1.cif"),
    ("wwpdb-{pdb_lower}-validation.xml.gz", "https://files.rcsb.org/pub/pdb/validation_reports/{middle}/{pdb_lower}/{pdb_lower}_validation.xml.gz"),
]
STATIC_REQUESTS = [
    ("rcsb-chemcomp-8PR.json", "https://data.rcsb.org/rest/v1/core/chemcomp/8PR"),
    ("rcsb-chemcomp-7V7.json", "https://data.rcsb.org/rest/v1/core/chemcomp/7V7"),
    ("ccd-8PR.cif", "https://files.rcsb.org/ligands/download/8PR.cif"),
    ("ccd-7V7.cif", "https://files.rcsb.org/ligands/download/7V7.cif"),
    ("uniprot-P31645.json", "https://rest.uniprot.org/uniprotkb/P31645.json"),
    ("uniprot-P31645.fasta", "https://rest.uniprot.org/uniprotkb/P31645.fasta"),
    ("uniprot-P35372.json", "https://rest.uniprot.org/uniprotkb/P35372.json"),
    ("uniprot-P35372.fasta", "https://rest.uniprot.org/uniprotkb/P35372.fasta"),
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class RedirectRecorder(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        self.redirects: list[dict[str, object]] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        self.redirects.append({
            "status": code,
            "from_url": req.full_url,
            "to_url": newurl,
            "headers": list(headers.items()),
        })
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(raw_dir: Path, meta_dir: Path, filename: str, url: str, force: bool) -> dict[str, object]:
    payload_path = raw_dir / filename
    meta_path = meta_dir / f"{filename}.retrieval.json"
    if (payload_path.exists() or meta_path.exists()) and not force:
        raise FileExistsError(f"refusing to overwrite {payload_path} or {meta_path}")

    started = utc_now()
    redirect_handler = RedirectRecorder()
    opener = urllib.request.build_opener(redirect_handler)
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    try:
        with opener.open(request, timeout=90) as response:
            status = response.status
            final_url = response.url
            headers = list(response.headers.items())
            declared = response.headers.get("Content-Length")
            if declared and int(declared) > MAX_BYTES:
                raise RuntimeError(f"declared body exceeds {MAX_BYTES} bytes: {declared}")
            chunks: list[bytes] = []
            count = 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                count += len(chunk)
                if count > MAX_BYTES:
                    raise RuntimeError(f"response exceeds {MAX_BYTES} bytes")
                chunks.append(chunk)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} for {url}") from exc
    body = b"".join(chunks)
    completed = utc_now()
    digest = hashlib.sha256(body).hexdigest()
    payload_path.write_bytes(body)
    record: dict[str, object] = {
        "requested_url": url,
        "final_url": final_url,
        "redirects": redirect_handler.redirects,
        "http_status": status,
        "request_headers": {"User-Agent": UA, "Accept-Encoding": "identity"},
        "response_headers": headers,
        "started_utc": started,
        "completed_utc": completed,
        "bytes": len(body),
        "sha256": digest,
        "payload": f"raw/{filename}",
    }
    meta_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{status} {len(body):>8} {digest[:12]} {filename}")
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True, help="evidence directory")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    raw_dir = args.out / "raw"
    meta_dir = args.out / "retrieval"
    raw_dir.mkdir(parents=True, exist_ok=True)
    meta_dir.mkdir(parents=True, exist_ok=True)

    for pdb in ("6VRH", "8EF5"):
        values = {"pdb": pdb, "pdb_lower": pdb.lower(), "middle": pdb.lower()[1:3]}
        for filename, url in BASE_REQUESTS:
            fetch(raw_dir, meta_dir, filename.format(**values), url.format(**values), args.force)

    for filename, url in STATIC_REQUESTS:
        fetch(raw_dir, meta_dir, filename, url, args.force)

    # Entry records authoritatively enumerate entity and assembly IDs. Fetch only
    # those IDs, keeping this retrieval bounded to the two requested entries.
    for pdb in ("6VRH", "8EF5"):
        entry = json.loads((raw_dir / f"rcsb-entry-{pdb}.json").read_text(encoding="utf-8"))
        ids = entry["rcsb_entry_container_identifiers"]
        for entity_id in ids.get("polymer_entity_ids", []):
            fetch(raw_dir, meta_dir, f"rcsb-polymer-{pdb}-entity-{entity_id}.json",
                  f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb}/{entity_id}", args.force)
        for entity_id in ids.get("non_polymer_entity_ids", []):
            fetch(raw_dir, meta_dir, f"rcsb-nonpolymer-{pdb}-entity-{entity_id}.json",
                  f"https://data.rcsb.org/rest/v1/core/nonpolymer_entity/{pdb}/{entity_id}", args.force)
        for entity_id in ids.get("branched_entity_ids", []):
            fetch(raw_dir, meta_dir, f"rcsb-branched-{pdb}-entity-{entity_id}.json",
                  f"https://data.rcsb.org/rest/v1/core/branched_entity/{pdb}/{entity_id}", args.force)
        for assembly_id in ids.get("assembly_ids", []):
            fetch(raw_dir, meta_dir, f"rcsb-assembly-{pdb}-{assembly_id}.json",
                  f"https://data.rcsb.org/rest/v1/core/assembly/{pdb}/{assembly_id}", args.force)


if __name__ == "__main__":
    main()
