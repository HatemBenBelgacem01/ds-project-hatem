from pathlib import Path

import polars as pl
from polars.testing import assert_frame_equal

from ds_project_hatem.derive import place_year_table
from ds_project_hatem.load import parse_counts

FIXTURE = Path(__file__).parent / "fixtures" / "counts_small.csv"


def test_place_year_table_on_fixture():
    table = place_year_table(parse_counts(pl.read_csv(FIXTURE)))

    expected = pl.DataFrame(
        {
            "OST": [1000, 1000, 3000],
            "NORD": [2000, 2000, 4000],
            "year": [2019, 2020, 2020],
            "days_with_bikes": [2, 1, 1],
            "bikes_per_day": [5.0, 6.0, 15.0],
        }
    )
    assert_frame_equal(table, expected, check_dtypes=False)


def test_place_year_table_on_empty_table_returns_empty_table():
    empty = parse_counts(pl.read_csv(FIXTURE).head(0))

    table = place_year_table(empty)

    assert table.height == 0
    assert table.columns == ["OST", "NORD", "year", "days_with_bikes", "bikes_per_day"]
