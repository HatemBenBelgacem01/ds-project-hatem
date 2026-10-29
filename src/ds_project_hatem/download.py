"""Download step: fetch the raw file and record each download in the manifest."""

import csv
import hashlib
import urllib.request
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path

URL = (
    "https://data.stadt-zuerich.ch/dataset/ted_taz_verkehrszaehlungen_werte_fussgaenger_velo"
    "/download/verkehrszaehlungen_werte_fussgaenger_velo_alle_jahre.parquet"
)
RAW_DIR = Path("data/raw")
MANIFEST_HEADER = ["url", "downloaded_at", "size_bytes", "sha256"]


def fetch_url(url: str, target: Path) -> None:
    """Stream the file at url into target."""
    with urllib.request.urlopen(url) as response, target.open("wb") as out:
        while chunk := response.read(1 << 20):
            out.write(chunk)


def sha256_of(path: Path) -> str:
    """Return the sha256 hex digest of a file, read in chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def download(
    url: str,
    raw_dir: Path,
    force: bool = False,
    fetch: Callable[[str, Path], None] = fetch_url,
) -> Path:
    """Fetch url into raw_dir, unless the file is already there, and log it in the manifest."""
    target = raw_dir / Path(url).name
    if target.exists() and not force:
        print(f"download: skipped, {target} already exists")
        return target

    raw_dir.mkdir(parents=True, exist_ok=True)
    # Write to a .part file first so an interrupted run never looks complete.
    part = target.with_name(target.name + ".part")
    fetch(url, part)
    part.replace(target)

    size = target.stat().st_size
    manifest = raw_dir / "manifest.csv"
    write_header = not manifest.exists()
    with manifest.open("a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(MANIFEST_HEADER)
        downloaded_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        writer.writerow([url, downloaded_at, size, sha256_of(target)])

    print(f"download: wrote {target} ({size} bytes)")
    return target
