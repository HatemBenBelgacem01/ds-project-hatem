"""Answer step on dry weekdays: the same rules as answer.py, on the days that were dry."""

from pathlib import Path

import polars as pl

from ds_project_hatem.answer import BAND_PERCENT, FIRST_YEAR, LAST_YEAR


def dry_answer_table(dry: pl.DataFrame) -> pl.DataFrame:
    """Return one row per place with the dry-weekday values of both years, the change and a status."""
    first = dry.filter(pl.col("year") == FIRST_YEAR).select(
        "OST", "NORD", pl.col("dry_days").alias("dry_days_first"), pl.col("dry_bikes_per_day").alias("bikes_first")
    )
    last = dry.filter(pl.col("year") == LAST_YEAR).select(
        "OST", "NORD", pl.col("dry_days").alias("dry_days_last"), pl.col("dry_bikes_per_day").alias("bikes_last")
    )
    table = first.join(last, on=["OST", "NORD"], how="full", coalesce=True)
    if table.filter(pl.col("bikes_first").is_null() | pl.col("bikes_last").is_null()).height:
        bad = table.filter(pl.col("bikes_first").is_null() | pl.col("bikes_last").is_null())
        raise ValueError(f"no dry weekday with bike data for place {bad.row(0)[:2]}; decide before the answer")

    table = table.with_columns(
        ((pl.col("bikes_last") - pl.col("bikes_first")) / pl.col("bikes_first") * 100).alias("change_percent")
    )
    return table.with_columns(
        pl.when(pl.col("change_percent") > BAND_PERCENT)
        .then(pl.lit("gewachsen"))
        .when(pl.col("change_percent") < -BAND_PERCENT)
        .then(pl.lit("geschrumpft"))
        .otherwise(pl.lit("unverändert"))
        .alias("status")
    )


def dry_city_sentence(table: pl.DataFrame) -> str:
    """Return the second sentence for the city: yes when more than half of the places grew on dry weekdays."""
    statuses = table["status"]
    total = table.height
    grew = statuses.eq("gewachsen").sum()
    shrank = statuses.eq("geschrumpft").sum()
    unchanged = statuses.eq("unverändert").sum()
    answer = "ja" if grew * 2 > total else "nein"
    return (
        f"Für die Stadt bei trockenen Werktagen: {answer}. {grew} von {total} vergleichbaren Orten sind "
        f"gewachsen, {shrank} geschrumpft, {unchanged} unverändert."
    )


def dry_values(counts: pl.DataFrame, days: pl.DataFrame) -> pl.DataFrame:
    """Return per place and year the number of dry weekdays with bike data and the average bikes per day on them."""
    dry_dates = days.filter(pl.col("dry_weekday")).select("date")
    daily = (
        counts.filter(pl.col("VELO_IN").is_not_null() | pl.col("VELO_OUT").is_not_null())
        .with_columns(pl.col("DATUM").dt.date().alias("date"))
        .group_by("OST", "NORD", "date")
        .agg((pl.col("VELO_IN").fill_null(0) + pl.col("VELO_OUT").fill_null(0)).sum().alias("bikes_day"))
    )
    return (
        daily.join(dry_dates, on="date")
        .with_columns(pl.col("date").dt.year().alias("year"))
        .group_by("OST", "NORD", "year")
        .agg(pl.len().alias("dry_days"), pl.col("bikes_day").mean().alias("dry_bikes_per_day"))
    )


def answer_dry(counts_path: Path, days_path: Path, answer_path: Path, out_path: Path, force: bool = False) -> Path:
    """Write the dry-weekday answer to out_path, unless it is already there, and print the sentence."""
    if out_path.exists() and not force:
        print(f"answer_dry: skipped, {out_path} already exists")
        return out_path

    places = pl.read_parquet(answer_path).filter(pl.col("status") != "nicht vergleichbar").select("OST", "NORD")
    dry = dry_values(pl.read_parquet(counts_path), pl.read_parquet(days_path)).join(places, on=["OST", "NORD"])
    table = dry_answer_table(dry)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    part = out_path.with_name(out_path.name + ".part")
    table.write_parquet(part)
    part.replace(out_path)

    print(dry_city_sentence(table))
    return out_path
