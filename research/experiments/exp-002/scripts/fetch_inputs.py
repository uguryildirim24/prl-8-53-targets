#!/usr/bin/env python3
"""Retrieve the small immutable input set for exp-002 from official RCSB endpoints."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "inputs" / "raw"
SOURCES = {
    "3TDC.cif": "https://files.rcsb.org/download/3TDC.cif",
    "3TDC.pdb": "https://files.rcsb.org/download/3TDC.pdb",
    "3TDC-assembly1.cif.gz": "https://files.rcsb.org/download/3TDC-assembly1.cif.gz",
    "3TDC-assembly2.cif.gz": "https://files.rcsb.org/download/3TDC-assembly2.cif.gz",
    "rcsb-entry-3TDC.json": "https://data.rcsb.org/rest/v1/core/entry/3TDC",
    "rcsb-assembly-3TDC-1.json": "https://data.rcsb.org/rest/v1/core/assembly/3TDC/1",
    "rcsb-assembly-3TDC-2.json": "https://data.rcsb.org/rest/v1/core/assembly/3TDC/2",
    "rcsb-polymer-entity-3TDC-1.json": "https://data.rcsb.org/rest/v1/core/polymer_entity/3TDC/1",
    "rcsb-polymer-instance-3TDC-A.json": "https://data.rcsb.org/rest/v1/core/polymer_entity_instance/3TDC/A",
    "rcsb-chemcomp-0EU.json": "https://data.rcsb.org/rest/v1/core/chemcomp/0EU",
    "0EU.cif": "https://files.rcsb.org/ligands/download/0EU.cif",
    "0EU_ideal.sdf": "https://files.rcsb.org/ligands/download/0EU_ideal.sdf",
    "uniprot-O00763.json": "https://rest.uniprot.org/uniprotkb/O00763.json",
    "uniprot-O00763.fasta": "https://rest.uniprot.org/uniprotkb/O00763.fasta",
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for name, url in SOURCES.items():
        started = dt.datetime.now(dt.timezone.utc)
        request = urllib.request.Request(
            url, headers={"User-Agent": "prl-8-53-exp-002/1.0 (research archive)"}
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read()
                status = response.status
                final_url = response.url
                headers = dict(response.headers.items())
        except urllib.error.HTTPError as error:
            body = error.read()
            status = error.code
            final_url = error.url
            headers = dict(error.headers.items())
        finished = dt.datetime.now(dt.timezone.utc)
        if status != 200:
            raise RuntimeError(f"{url}: HTTP {status}")
        (OUT / name).write_bytes(body)
        (OUT / f"{name}.headers.json").write_text(
            json.dumps(headers, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        records.append(
            {
                "file": name,
                "url": url,
                "final_url": final_url,
                "http_status": status,
                "retrieved_utc": finished.isoformat().replace("+00:00", "Z"),
                "elapsed_seconds": round((finished - started).total_seconds(), 3),
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
                "response_headers_file": f"{name}.headers.json",
            }
        )
        print(f"{name}: {len(body)} bytes {records[-1]['sha256']}")
    (ROOT / "inputs" / "source_manifest.json").write_text(
        json.dumps(
            {
                "retrieval_tool": "Python urllib from Python "
                + __import__("platform").python_version(),
                "records": records,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
