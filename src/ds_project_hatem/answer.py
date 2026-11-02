"""Answer step: which places are comparable, how they changed, and the sentence for the city."""

from pathlib import Path

import polars as pl

FIRST_YEAR = 2019
LAST_YEAR = 2025
MIN_DAYS = 300
BAND_PERCENT = 5.0


def answer_table(place_year: pl.DataFrame) -> pl.DataFrame:
    """Return one row per place with both years, the change in percent, a status and a reason."""
    places = place_year.select("OST", "NORD").unique()
    first = place_year.filter(pl.col("year") == FIRST_YEAR).select(
        "OST",
        "NORD",
        pl.col("days_with_bikes").alias("days_first"),
        pl.col("bikes_per_day").alias("bikes_first"),
    )
    last = place_year.filter(pl.col("year") == LAST_YEAR).select(
        "OST",
        "NORD",
        pl.col("days_with_bikes").alias("days_last"),
        pl.col("bikes_per_day").alias("bikes_last"),
    )
    table = places.join(first, on=["OST", "NORD"], how="left").join(last, on=["OST", "NORD"], how="left")

    comparable = (pl.col("days_first").fill_null(0) >= MIN_DAYS) & (pl.col("days_last").fill_null(0) >= MIN_DAYS)
    table = table.with_columns(
        pl.when(pl.col("bikes_first").is_null())
        .then(pl.lit(f"keine Daten {FIRST_YEAR}"))
        .when(pl.col("bikes_last").is_null())
        .then(pl.lit(f"keine Daten {LAST_YEAR}"))
        .when(pl.col("days_first") < MIN_DAYS)
        .then(pl.lit(f"weniger als {MIN_DAYS} Tage in {FIRST_YEAR}"))
        .when(pl.col("days_last") < MIN_DAYS)
        .then(pl.lit(f"weniger als {MIN_DAYS} Tage in {LAST_YEAR}"))
        .otherwise(pl.lit(None, dtype=pl.String))
        .alias("reason"),
        pl.when(comparable)
        .then((pl.col("bikes_last") - pl.col("bikes_first")) / pl.col("bikes_first") * 100)
        .otherwise(None)
        .alias("change_percent"),
    )
    return table.with_columns(
        pl.when(~comparable)
        .then(pl.lit("nicht vergleichbar"))
        .when(pl.col("change_percent") > BAND_PERCENT)
        .then(pl.lit("gewachsen"))
        .when(pl.col("change_percent") < -BAND_PERCENT)
        .then(pl.lit("geschrumpft"))
        .otherwise(pl.lit("unverändert"))
        .alias("status")
    )


def city_sentence(table: pl.DataFrame) -> str:
    """Return the one sentence for the city: yes when more than half of the comparable places grew."""
    statuses = table["status"]
    comparable = statuses.ne("nicht vergleichbar").sum()
    grew = statuses.eq("gewachsen").sum()
    shrank = statuses.eq("geschrumpft").sum()
    unchanged = statuses.eq("unverändert").sum()
    not_comparable = statuses.eq("nicht vergleichbar").sum()
    answer = "ja" if grew * 2 > comparable else "nein"
    return (
        f"Für die Stadt: {answer}. {grew} von {comparable} vergleichbaren Orten sind gewachsen, "
        f"{shrank} geschrumpft, {unchanged} unverändert. {not_comparable} Orte sind nicht vergleichbar."
    )


def answer(place_year_path: Path, out_path: Path, force: bool = False) -> Path:
    """Write the answer table to out_path, unless it is already there, and print the sentence."""
    if out_path.exists() and not force:
        print(f"answer: skipped, {out_path} already exists")
        return out_path

    table = answer_table(pl.read_parquet(place_year_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    part = out_path.with_name(out_path.name + ".part")
    table.write_parquet(part)
    part.replace(out_path)

    print(city_sentence(table))
    return out_path
