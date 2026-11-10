"""Download the knowledge-base documents from their official URLs into InputDocs/.

Each file is checked against the SHA-256 in sources.json. A file that is already
present and matches is skipped. Nothing is deleted.

    python fetch_sources.py [output_dir]      # default: InputDocs
"""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

TIMEOUT_SECONDS = 120
CHUNK = 1 << 20
HEADERS = {"User-Agent": "Mozilla/5.0 (knowledge-base fetch)"}


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response, target.open("wb") as out:
        for block in iter(lambda: response.read(CHUNK), b""):
            out.write(block)


def main() -> int:
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "InputDocs")
    sources = json.loads((Path(__file__).parent / "sources.json").read_text())
    failed = 0
    for source in sources:
        target = out_dir / source["path"]
        if target.exists() and sha256_of(target) == source["sha256"]:
            print(f"ok       {source['path']}")
            continue
        try:
            download(source["url"], target)
        except OSError as error:
            print(f"FAILED   {source['path']}: {error}")
            failed += 1
            continue
        if sha256_of(target) == source["sha256"]:
            print(f"fetched  {source['path']}")
        else:
            print(f"CHANGED  {source['path']}: the file at the URL differs from the one the report was written against")
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
