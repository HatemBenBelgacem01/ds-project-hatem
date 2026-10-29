import csv
import hashlib
from pathlib import Path

from ds_project_hatem.download import MANIFEST_HEADER, download

URL = "https://example.test/data/file.parquet"
CONTENT = b"abc"
CONTENT_SHA256 = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def fake_fetch(url: str, target: Path) -> None:
    """Stand in for the network: write fixed bytes instead of downloading."""
    target.write_bytes(CONTENT)


def read_manifest(raw_dir: Path) -> list[list[str]]:
    with (raw_dir / "manifest.csv").open(newline="") as f:
        return list(csv.reader(f))


def test_first_run_writes_file_and_one_manifest_line(tmp_path, capsys):
    download(URL, tmp_path, fetch=fake_fetch)

    assert (tmp_path / "file.parquet").read_bytes() == CONTENT
    rows = read_manifest(tmp_path)
    assert rows[0] == MANIFEST_HEADER
    assert len(rows) == 2
    assert rows[1][0] == URL
    assert rows[1][2] == str(len(CONTENT))
    assert rows[1][3] == CONTENT_SHA256
    assert capsys.readouterr().out.startswith("download: wrote")


def test_sha256_in_manifest_matches_hashlib(tmp_path):
    download(URL, tmp_path, fetch=fake_fetch)

    assert read_manifest(tmp_path)[1][3] == hashlib.sha256(CONTENT).hexdigest()


def test_second_run_skips_and_adds_no_line(tmp_path, capsys):
    calls = []

    def counting_fetch(url: str, target: Path) -> None:
        calls.append(url)
        fake_fetch(url, target)

    download(URL, tmp_path, fetch=counting_fetch)
    download(URL, tmp_path, fetch=counting_fetch)

    assert len(calls) == 1
    assert len(read_manifest(tmp_path)) == 2
    assert "download: skipped" in capsys.readouterr().out


def test_force_fetches_again_and_appends_a_line(tmp_path):
    download(URL, tmp_path, fetch=fake_fetch)
    download(URL, tmp_path, force=True, fetch=fake_fetch)

    rows = read_manifest(tmp_path)
    assert len(rows) == 3
    assert rows[1][3] == rows[2][3]
