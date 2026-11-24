"""
Tests for `justetf_scraping.overview` module.

`tests/data/overview/search_rows_2026-11-24.json` holds a few raw rows of the
justETF search response captured on 2026-11-24, where `inceptionDate` is written
as `dd/mm/yyyy` (until the day before it was `dd.mm.yy`).
"""

import copy
import datetime
import json
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

import justetf_scraping.overview

DATA_FILE = Path(__file__).parent / "data" / "overview" / "search_rows_2026-11-24.json"

EXPECTED_INCEPTION_DATES = {
    "IE00B4L5Y983": datetime.datetime(2009, 9, 25),
    "IE000DHZXD61": datetime.datetime(2026, 4, 28),
    "GB00BNRRFY34": datetime.datetime(2022, 3, 23),
    "IE00077FRP95": datetime.datetime(2022, 2, 15),
}


@pytest.fixture(scope="module")
def raw_rows() -> list[dict[str, Any]]:
    """
    Raw search rows as justETF returns them today.
    """
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def _load_overview(
    monkeypatch: pytest.MonkeyPatch, rows: list[dict[str, Any]]
) -> pd.DataFrame:
    """
    Run `load_overview` on mocked raw rows instead of calling justETF.
    """
    monkeypatch.setattr(
        justetf_scraping.overview,
        "load_raw_overview",
        lambda *args, **kwargs: copy.deepcopy(rows),
    )
    return justetf_scraping.overview.load_overview(strategy="epg-longOnly")


def _with_inception_dates(
    rows: list[dict[str, Any]], dates: dict[str, str]
) -> list[dict[str, Any]]:
    """
    Copy of `rows` with `inceptionDate` replaced by `dates[isin]`.
    """
    rows = copy.deepcopy(rows)
    for row in rows:
        row["inceptionDate"] = dates[row["isin"]]
    return rows


def _assert_inception_dates(df: pd.DataFrame) -> None:
    assert {
        isin: date.to_pydatetime() for isin, date in df["inception_date"].items()
    } == EXPECTED_INCEPTION_DATES


def _assert_other_fields_parsed(df: pd.DataFrame) -> None:
    """
    Fields besides `inception_date` of the captured rows, a format change in
    any of them would show up here.
    """
    assert df.index.tolist() == list(EXPECTED_INCEPTION_DATES)

    world = df.loc["IE00B4L5Y983"]
    assert world["ter"] == pytest.approx(0.20)
    assert world["size"] == 121650
    assert world["number_of_holdings"] == 1249
    assert world["currency"] == "USD"
    assert not world["hedged"]
    assert world["securities_lending"]
    assert not world["is_sustainable"]
    assert world["replication"] == "Optimized sampling"
    assert world["dividends"] == "Accumulating"
    assert world["domicile_country"] == "Ireland"
    assert pd.isna(world["last_dividends"])

    # "-" placeholders become missing values, not errors.
    young = df.loc["IE000DHZXD61"]
    assert pd.isna(young["size"])
    assert pd.isna(young["number_of_holdings"])
    assert pd.isna(young["last_year"])

    # Thousands separator inside a percentage.
    assert df.loc["GB00BNRRFY34", str(pd.Timestamp("now").year - 3)] == pytest.approx(
        1017.39
    )
    distributing = df.loc["IE00077FRP95"]
    assert distributing["dividends"] == "Distributing"
    assert distributing["last_dividends"] == pytest.approx(10.21)
    assert distributing["last_year_dividends"] == pytest.approx(9.19)


def test_load_overview_legacy_date_format(
    monkeypatch: pytest.MonkeyPatch, raw_rows: list[dict[str, Any]]
) -> None:
    """
    Dates written as `dd.mm.yy` (the format used before 2026-11-24) still parse.
    """
    rows = _with_inception_dates(
        raw_rows,
        {
            "IE00B4L5Y983": "25.09.09",
            "IE000DHZXD61": "28.04.26",
            "GB00BNRRFY34": "23.03.22",
            "IE00077FRP95": "15.02.22",
        },
    )

    df = _load_overview(monkeypatch, rows)

    _assert_inception_dates(df)
    _assert_other_fields_parsed(df)


def test_load_overview_current_date_format(
    monkeypatch: pytest.MonkeyPatch, raw_rows: list[dict[str, Any]]
) -> None:
    """
    Dates written as `dd/mm/yyyy`, as returned since 2026-11-24, parse.
    """
    assert raw_rows[0]["inceptionDate"] == "25/09/2009"

    df = _load_overview(monkeypatch, raw_rows)

    _assert_inception_dates(df)
    _assert_other_fields_parsed(df)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("19.05.10", datetime.datetime(2010, 5, 19)),
        ("19.05.2010", datetime.datetime(2010, 5, 19)),
        ("19/05/2010", datetime.datetime(2010, 5, 19)),
        ("2010-05-19", datetime.datetime(2010, 5, 19)),
        # Day first, not month first.
        ("01/02/2011", datetime.datetime(2011, 2, 1)),
        ("01.02.11", datetime.datetime(2011, 2, 1)),
        # Single-digit day and month, surrounding whitespace.
        ("1.2.11", datetime.datetime(2011, 2, 1)),
        (" 19/05/2010 ", datetime.datetime(2010, 5, 19)),
        # Two-digit years follow `%y`: 69-99 are 19xx, 00-68 are 20xx.
        ("31.12.99", datetime.datetime(1999, 12, 31)),
        ("01.01.68", datetime.datetime(2068, 1, 1)),
        ("01.01.69", datetime.datetime(1969, 1, 1)),
        ("29/02/2024", datetime.datetime(2024, 2, 29)),
    ],
)
def test_parse_date(value: str, expected: datetime.datetime) -> None:
    """
    All known date formats parse to the same date.
    """
    assert justetf_scraping.overview._parse_date(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "",
        "-",
        "n/a",
        "19-05-2010",  # Not a known separator for this order.
        "19/05/10",  # Two-digit year only known with dots.
        "05/19/2010",  # Month first, month 19.
        "31/02/2010",  # Not a calendar date.
        "29/02/2023",  # Not a leap year.
        "00/05/2010",
        "2010/05/19",
        "19 May 2010",
        "19.05.2010 10:15",
    ],
)
def test_parse_date_rejects_unknown_format(value: str) -> None:
    """
    A value in none of the known formats is never turned into a (wrong) date.
    """
    assert justetf_scraping.overview._parse_date(value) is None


def test_parse_dates_missing_values_do_not_warn(
    recwarn: pytest.WarningsRecorder,
) -> None:
    """
    Placeholders ("-" cleaned up to NA) are missing dates, not unknown formats.
    """
    dates = pd.Series(["19/05/2010", pd.NA, "01.02.11"], name="inception_date")

    result = justetf_scraping.overview._parse_dates(dates)

    assert result.tolist()[0] == pd.Timestamp("2010-05-19")
    assert pd.isna(result.iloc[1])
    assert result.iloc[2] == pd.Timestamp("2011-02-01")
    assert result.dtype.kind == "M"
    assert not recwarn.list


def test_load_overview_unknown_date_format(
    monkeypatch: pytest.MonkeyPatch, raw_rows: list[dict[str, Any]]
) -> None:
    """
    An unknown date format makes only that date missing, with a warning, and
    doesn't affect the other rows and fields.
    """
    rows = _with_inception_dates(
        raw_rows,
        {
            "IE00B4L5Y983": "25/09/2009",
            "IE000DHZXD61": "28 Apr 2026",
            "GB00BNRRFY34": "31/02/2022",
            "IE00077FRP95": "15.02.22",
        },
    )

    with pytest.warns(UserWarning, match="inception_date") as record:
        df = _load_overview(monkeypatch, rows)

    assert "'28 Apr 2026'" in str(record[0].message)
    assert "'31/02/2022'" in str(record[0].message)
    assert df["inception_date"].isna().tolist() == [False, True, True, False]
    assert df.loc["IE00B4L5Y983", "inception_date"] == pd.Timestamp("2009-09-25")
    assert df.loc["IE00077FRP95", "inception_date"] == pd.Timestamp("2022-02-15")
    # Age is derived from the date, so it is missing too and nothing else breaks.
    assert df["age_in_days"].isna().tolist() == [False, True, True, False]
    _assert_other_fields_parsed(df)
