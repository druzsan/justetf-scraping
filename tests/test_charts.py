"""
Tests for `justetf_scraping.charts` module.
"""

import pandas as pd
import pytest

import justetf_scraping.charts
import justetf_scraping.types

CHART_COLUMNS = {
    "quote",
    "relative",
    "dividends",
    "cumulative_dividends",
    "quote_with_dividends",
    "relative_with_dividends",
    "reinvested_dividends",
    "quote_with_reinvested_dividends",
    "relative_with_reinvested_dividends",
}


def _load_mocked_raw_chart(
    isin: str, currency: justetf_scraping.types.Currency = "EUR"
) -> justetf_scraping.charts.RawChart:
    """
    Mocked version of `justetf_scraping.charts.load_raw_chart`.

    Only takes predefined values as ISIN, completely ignores the currency.
    """
    if isin == "with_dividends":
        return {
            "latestQuote": {"raw": 110, "localized": "110"},
            "latestQuoteDate": "2026-01-20",
            "price": {"raw": 110, "localized": "110"},
            "performance": {"raw": 110, "localized": "110"},
            "prevDaySeries": [],
            "series": [
                {"date": "2026-01-15", "value": {"raw": 100, "localized": "100"}},
                {"date": "2026-01-16", "value": {"raw": 95, "localized": "95"}},
                {"date": "2026-01-17", "value": {"raw": 98, "localized": "98"}},
                {"date": "2026-01-18", "value": {"raw": 102, "localized": "102"}},
                {"date": "2026-01-19", "value": {"raw": 105, "localized": "105"}},
            ],
            "latestDate": "2026-01-19",
            "endOfDay": "2026-01-20T21:00:00Z",
            "features": {
                "DIVIDENDS": [
                    {"date": "2026-01-15", "value": {"raw": 1, "localized": "1"}},
                    {"date": "2026-01-18", "value": {"raw": 2, "localized": "2"}},
                ],
            },
        }
    if isin == "without_dividends":
        return {
            "latestQuote": {"raw": 55, "localized": "55"},
            "latestQuoteDate": "2026-01-20",
            "price": {"raw": 55, "localized": "55"},
            "performance": {"raw": 55, "localized": "55"},
            "prevDaySeries": [],
            "series": [
                {"date": "2026-01-10", "value": {"raw": 50, "localized": "50"}},
                {"date": "2026-01-11", "value": {"raw": 48, "localized": "40"}},
                {"date": "2026-01-12", "value": {"raw": 45, "localized": "45"}},
                {"date": "2026-01-13", "value": {"raw": 42, "localized": "42"}},
                {"date": "2026-01-14", "value": {"raw": 38, "localized": "38"}},
                {"date": "2026-01-15", "value": {"raw": 42, "localized": "42"}},
                {"date": "2026-01-16", "value": {"raw": 45, "localized": "45"}},
                {"date": "2026-01-17", "value": {"raw": 48, "localized": "48"}},
                {"date": "2026-01-18", "value": {"raw": 50, "localized": "50"}},
                {"date": "2026-01-19", "value": {"raw": 52, "localized": "52"}},
            ],
            "latestDate": "2026-01-19",
            "endOfDay": "2026-01-20T21:00:00Z",
            "features": {"DIVIDENDS": []},
        }
    raise ValueError(f"'{isin}' is not predefined for mocked data.")


def test_parse_series() -> None:
    """
    Test parsing a series of raw data.
    """
    raw_series: list[justetf_scraping.charts.RawSeriesItem] = [
        {"date": "2026-01-18", "value": {"raw": 102, "localized": "102"}},
        {"date": "2026-01-19", "value": {"raw": 105, "localized": "105"}},
    ]
    column_name = "quote"
    df = justetf_scraping.charts.parse_series(raw_series, value_name=column_name)

    assert set(df.columns.tolist()) == {column_name}
    assert len(df) == 2
    assert df.index[-1] == pd.to_datetime("2026-01-19")
    assert df[column_name].tolist() == [102, 105]


def test_load_chart_with_dividends(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test loading a mocked chart with dividends.
    """
    monkeypatch.setattr(
        "justetf_scraping.charts.load_raw_chart", _load_mocked_raw_chart
    )

    df = justetf_scraping.load_chart("with_dividends")

    assert set(df.columns.tolist()) == CHART_COLUMNS
    assert len(df) == 5
    last_date = pd.to_datetime("2026-01-19")
    assert df.index[-1] == last_date
    assert df.at[last_date, "quote"] == 105
    assert df.at[pd.to_datetime("2026-01-15"), "dividends"] == 1
    assert df.at[last_date, "cumulative_dividends"] == 3
    assert df.at[last_date, "reinvested_dividends"] > 0  # ty: ignore[unsupported-operator]
    assert df.at[last_date, "quote_with_dividends"] > df.at[last_date, "quote"]  # ty: ignore[unsupported-operator]
    assert df.at[last_date, "relative_with_dividends"] > df.at[last_date, "relative"]  # ty: ignore[unsupported-operator]
    assert (
        df.at[last_date, "quote_with_reinvested_dividends"]  # ty: ignore[unsupported-operator]
        > df.at[last_date, "quote_with_dividends"]
    )
    assert (
        df.at[last_date, "relative_with_reinvested_dividends"]  # ty: ignore[unsupported-operator]
        > df.at[last_date, "relative_with_dividends"]
    )


def test_load_chart_without_dividends(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test loading a mocked chart without dividends.
    """
    monkeypatch.setattr(
        "justetf_scraping.charts.load_raw_chart", _load_mocked_raw_chart
    )

    df = justetf_scraping.load_chart("without_dividends")

    assert set(df.columns.tolist()) == CHART_COLUMNS
    assert len(df) == 10
    assert df.index[-1] == pd.to_datetime("2026-01-19")
    assert df.at[pd.to_datetime("2026-01-19"), "quote"] == 52
    assert (df["dividends"] == 0).all()
    assert (df["cumulative_dividends"] == 0).all()
    assert (df["reinvested_dividends"] == 0).all()
    assert (df["quote_with_dividends"] == df["quote"]).all()
    assert (df["relative_with_dividends"] == df["relative"]).all()
    assert (df["quote_with_reinvested_dividends"] == df["quote"]).all()
    assert (df["relative_with_reinvested_dividends"] == df["relative"]).all()


def test_load_chart_with_unclosed(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test loading a mocked chart with unclosed day.
    """
    monkeypatch.setattr(
        "justetf_scraping.charts.load_raw_chart", _load_mocked_raw_chart
    )

    df = justetf_scraping.load_chart("with_dividends", unclosed=True)

    assert set(df.columns.tolist()) == CHART_COLUMNS
    assert len(df) == 6
    assert df.index[-1] == pd.to_datetime("2026-01-20")
    assert df.at[pd.to_datetime("2026-01-20"), "quote"] == 110
