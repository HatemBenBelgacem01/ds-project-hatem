from datetime import datetime
from pathlib import Path

import polars as pl

from ds_project_hatem.load import parse_counts

FIXTURE = Path(__file__).parent / "fixtures" / "counts_small.csv"


def test_parse_counts_turns_datum_into_a_timestamp():
    counts = parse_counts(pl.read_csv(FIXTURE))

    assert counts.height == 8
    assert isinstance(counts.schema["DATUM"], pl.Datetime)
    assert counts["DATUM"][0] == datetime(2019, 3, 1, 8, 0)
