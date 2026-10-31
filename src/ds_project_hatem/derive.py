"""Derive step: one row per place and year, with days with bike data and bikes per day."""

from pathlib import Path

import polars as pl


def place_year_table(counts: pl.DataFrame) -> pl.DataFrame:
    """Return days with bike data and the average bikes per day, per place (OST, NORD) and year."""
    bikes = counts.filter(pl.col("VELO_IN").is_not_null() | pl.col("VELO_OUT").is_not_null()).with_columns(
        (pl.col("VELO_IN").fill_null(0) + pl.col("VELO_OUT").fill_null(0)).alias("bikes"),
        pl.col("DATUM").dt.date().alias("day"),
    )
    per_day = bikes.group_by("OST", "NORD", "day").agg(pl.col("bikes").sum().alias("bikes_day"))
    return (
        per_day.with_columns(pl.col("day").dt.year().alias("year"))
        .group_by("OST", "NORD", "year")
        .agg(
            pl.len().alias("days_with_bikes"),
            pl.col("bikes_day").mean().alias("bikes_per_day"),
        )
        .sort("OST", "NORD", "year")
    )


def derive(counts_path: Path, out_path: Path, force: bool = False) -> Path:
    """Write the place-year table to out_path, unless it is already there."""
    if out_path.exists() and not force:
        print(f"derive: skipped, {out_path} already exists")
        return out_path

    table = place_year_table(pl.read_parquet(counts_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    part = out_path.with_name(out_path.name + ".part")
    table.write_parquet(part)
    part.replace(out_path)

    places = table.select("OST", "NORD").unique().height
    print(f"derive: wrote {out_path} ({table.height} place-years, {places} places)")
    return out_path
