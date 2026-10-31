"""Entry point of `uv run build`: runs the pipeline steps in order."""

import argparse
from pathlib import Path

from ds_project_hatem.derive import derive
from ds_project_hatem.download import RAW_DIR, URL, download
from ds_project_hatem.load import load

DERIVED_DIR = Path("data/derived")


def main() -> None:
    parser = argparse.ArgumentParser(prog="build", description="Build this project's data from nothing.")
    parser.add_argument("--force", action="store_true", help="rebuild every step, including the download")
    args = parser.parse_args()

    raw = download(URL, RAW_DIR, force=args.force)
    counts = load(raw, DERIVED_DIR / "counts.parquet", force=args.force)
    derive(counts, DERIVED_DIR / "place_year.parquet", force=args.force)
