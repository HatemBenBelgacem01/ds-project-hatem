from datetime import date
from pathlib import Path

import polars as pl
import pytest

from ds_project_hatem.days import STATION, weather_days

FIXTURE = Path(__file__).parent / "fixtures" / "weather_small.csv"


def read_fixture() -> pl.DataFrame:
    return pl.read_csv(FIXTURE, infer_schema=False)


def test_fixture_days_follow_the_rules():
    table = weather_days(read_fixture())
    rows = {row["date"]: row for row in table.iter_rows(named=True)}

    assert table.height == 6
    assert rows[date(2020, 3, 2)]["dry_weekday"] is True
    assert rows[date(2020, 3, 3)]["rain_min"] == 12.5
    assert rows[date(2020, 3, 3)]["dry_weekday"] is False
    assert rows[date(2020, 3, 4)]["rain_min"] is None
    assert rows[date(2020, 3, 4)]["dry_weekday"] is False
    assert rows[date(2020, 3, 5)]["rain_min"] is None
    assert rows[date(2020, 3, 5)]["dry_weekday"] is False
    assert rows[date(2020, 3, 6)]["rain_min"] is None
    assert rows[date(2020, 3, 6)]["dry_weekday"] is False
    assert rows[date(2020, 3, 7)]["rain_min"] == 0
    assert rows[date(2020, 3, 7)]["dry_weekday"] is False


def test_first_column_is_datum_despite_byte_order_mark():
    assert "Datum" in read_fixture().columns


def test_two_rain_values_on_one_day_stop_with_an_error():
    weather = pl.DataFrame(
        {
            "Datum": ["2020-03-02T00:00+0100", "2020-03-02T00:00+0100"],
            "Standort": [STATION, STATION],
            "Parameter": ["RainDur", "RainDur"],
            "Intervall": ["d1", "d1"],
            "Einheit": ["min", "min"],
            "Wert": ["0", "1"],
            "Status": ["bereinigt", "bereinigt"],
        },
        schema={name: pl.String for name in ["Datum", "Standort", "Parameter", "Intervall", "Einheit", "Wert", "Status"]},
    )

    with pytest.raises(ValueError):
        weather_days(weather)
