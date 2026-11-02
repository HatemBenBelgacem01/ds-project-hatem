from datetime import date, datetime
from pathlib import Path

import polars as pl
import pytest

from ds_project_hatem.answer_dry import dry_answer_table, dry_city_sentence, dry_values

FIXTURE = Path(__file__).parent / "fixtures" / "place_year_dry_small.csv"


def test_each_place_gets_its_status():
    table = dry_answer_table(pl.read_csv(FIXTURE))

    statuses = {(row["OST"], row["NORD"]): row["status"] for row in table.iter_rows(named=True)}
    assert statuses == {
        (1000, 2000): "gewachsen",
        (3000, 4000): "geschrumpft",
        (5000, 6000): "unverändert",
        (7000, 8000): "gewachsen",
        (9000, 1000): "gewachsen",
    }


def test_change_percent_on_dry_weekdays():
    table = dry_answer_table(pl.read_csv(FIXTURE))
    row = table.filter((pl.col("OST") == 1000) & (pl.col("NORD") == 2000)).row(0, named=True)

    assert row["change_percent"] == pytest.approx(20.0)


def test_city_sentence_on_fixture_says_yes():
    table = dry_answer_table(pl.read_csv(FIXTURE))

    assert dry_city_sentence(table) == (
        "Für die Stadt bei trockenen Werktagen: ja. 3 von 5 vergleichbaren Orten sind gewachsen, "
        "1 geschrumpft, 1 unverändert."
    )


def test_place_without_dry_data_in_one_year_stops_with_an_error():
    dry = pl.DataFrame(
        {
            "OST": [1000, 1000],
            "NORD": [2000, 2000],
            "year": [2019, 2025],
            "dry_days": [150, 0],
            "dry_bikes_per_day": [100.0, None],
        }
    )

    with pytest.raises(ValueError):
        dry_answer_table(dry)


def test_dry_values_count_dry_days_with_bike_data_only():
    counts = pl.DataFrame(
        {
            "OST": [1000, 1000, 1000],
            "NORD": [2000, 2000, 2000],
            "DATUM": [datetime(2019, 3, 4, 8, 0), datetime(2019, 3, 4, 8, 15), datetime(2019, 3, 5, 8, 0)],
            "VELO_IN": [3, 2, 4],
            "VELO_OUT": [1, None, 0],
        }
    )
    days = pl.DataFrame({"date": [date(2019, 3, 4), date(2019, 3, 5)], "dry_weekday": [True, False]})

    row = dry_values(counts, days).row(0, named=True)

    assert row["year"] == 2019
    assert row["dry_days"] == 1
    assert row["dry_bikes_per_day"] == pytest.approx(6.0)
