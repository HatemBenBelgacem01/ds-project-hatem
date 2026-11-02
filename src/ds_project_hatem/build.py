"""Entry point of `uv run build`: runs the pipeline steps in order."""

import argparse
from pathlib import Path

from ds_project_hatem.answer import answer
from ds_project_hatem.days import days
from ds_project_hatem.derive import derive
from ds_project_hatem.download import RAW_DIR, URL, download
from ds_project_hatem.load import load

DERIVED_DIR = Path("data/derived")
WEATHER_URLS = [
    f"https://data.stadt-zuerich.ch/dataset/ugz_meteodaten_tagesmittelwerte/download/ugz_ogd_meteo_d1_{year}.csv"
    for year in (2019, 2025)
]


def main() -> None:
    parser = argparse.ArgumentParser(prog="build", description="Build this project's data from nothing.")
    parser.add_argument("--force", action="store_true", help="rebuild every step, including the download")
    args = parser.parse_args()

    raw = download(URL, RAW_DIR, force=args.force)
    counts = load(raw, DERIVED_DIR / "counts.parquet", force=args.force)
    place_year = derive(counts, DERIVED_DIR / "place_year.parquet", force=args.force)
    answer(place_year, DERIVED_DIR / "answer.parquet", force=args.force)

    weather = [download(url, RAW_DIR, force=args.force) for url in WEATHER_URLS]
    days(weather, DERIVED_DIR / "days.parquet", force=args.force)
