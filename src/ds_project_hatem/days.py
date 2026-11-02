"""Days step: one row per day with the rain at the station and the dry-weekday flag."""

from pathlib import Path

import polars as pl

STATION = "Zch_Stampfenbachstrasse"
PARAMETER = "RainDur"


def weather_days(weather: pl.DataFrame) -> pl.DataFrame:
    """Return one row per day in the weather data: the rain minutes at the station and whether it is a dry weekday."""
    dates = weather.select(pl.col("Datum").str.slice(0, 10).str.to_date("%Y-%m-%d").alias("date")).unique()
    station_rain = weather.filter((pl.col("Standort") == STATION) & (pl.col("Parameter") == PARAMETER)).select(
        pl.col("Datum").str.slice(0, 10).str.to_date("%Y-%m-%d").alias("date"),
        pl.when(pl.col("Wert").is_in(["", "NA"]))
        .then(pl.lit(None, dtype=pl.Float64))
        .otherwise(pl.col("Wert").cast(pl.Float64))
        .alias("rain_min"),
    )
    if station_rain.select("date").is_duplicated().any():
        day = station_rain.filter(pl.col("date").is_duplicated())["date"][0]
        raise ValueError(f"{STATION} has more than one {PARAMETER} value on {day}; decide which one counts")

    return (
        dates.join(station_rain, on="date", how="left")
        .with_columns(
            ((pl.col("date").dt.weekday() <= 5) & (pl.col("rain_min") == 0)).fill_null(False).alias("dry_weekday")
        )
        .sort("date")
    )


def days(weather_paths: list[Path], out_path: Path, force: bool = False) -> Path:
    """Write the day table to out_path, unless it is already there, and print one line."""
    if out_path.exists() and not force:
        print(f"days: skipped, {out_path} already exists")
        return out_path

    weather = pl.concat([pl.read_csv(path, infer_schema=False) for path in weather_paths])
    table = weather_days(weather)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    part = out_path.with_name(out_path.name + ".part")
    table.write_parquet(part)
    part.replace(out_path)

    print(f"days: wrote {out_path} ({table.height} days, {table['dry_weekday'].sum()} dry weekdays)")
    return out_path
