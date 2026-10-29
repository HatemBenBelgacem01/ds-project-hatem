"""Entry point of `uv run build`: runs the pipeline steps in order."""

import argparse

from ds_project_hatem.download import RAW_DIR, URL, download


def main() -> None:
    parser = argparse.ArgumentParser(prog="build", description="Build this project's data from nothing.")
    parser.add_argument("--force", action="store_true", help="rebuild every step, including the download")
    args = parser.parse_args()

    download(URL, RAW_DIR, force=args.force)
