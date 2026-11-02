from pathlib import Path

import polars as pl
import pytest

from ds_project_hatem.answer import answer_table, city_sentence

FIXTURE = Path(__file__).parent / "fixtures" / "place_year_small.csv"


def test_each_rule_gives_its_status():
    table = answer_table(pl.read_csv(FIXTURE))

    statuses = {(row["OST"], row["NORD"]): row["status"] for row in table.iter_rows(named=True)}
    assert statuses == {
        (1000, 2000): "gewachsen",
        (3000, 4000): "geschrumpft",
        (5000, 6000): "unverändert",
        (7000, 8000): "nicht vergleichbar",
        (9000, 1000): "nicht vergleichbar",
    }


def test_growth_percent_and_reasons():
    table = answer_table(pl.read_csv(FIXTURE))
    rows = {(row["OST"], row["NORD"]): row for row in table.iter_rows(named=True)}

    assert rows[(1000, 2000)]["change_percent"] == pytest.approx(20.0)
    assert rows[(7000, 8000)]["reason"] == "weniger als 300 Tage in 2019"
    assert rows[(9000, 1000)]["reason"] == "keine Daten 2019"


def test_city_sentence_on_fixture():
    table = answer_table(pl.read_csv(FIXTURE))

    assert city_sentence(table) == (
        "Für die Stadt: nein. 1 von 3 vergleichbaren Orten sind gewachsen, "
        "1 geschrumpft, 1 unverändert. 2 Orte sind nicht vergleichbar."
    )
