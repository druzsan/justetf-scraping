"""
Scrape and compare ETF chart data from justETF
(e.g. https://www.justetf.com/en/etf-profile.html?isin=IE00B4L5Y983#chart).
"""

from typing import Literal, Optional

import pandas as pd
import requests

from .helpers import USER_AGENT, assert_response_status_ok
from .types import Currency, RawChart, RawSeriesItem

BASE_URL = "https://www.justetf.com/api/etfs/{isin}/performance-chart"
BASE_PARAMS = {
    "locale": "en",
    "valuesType": "MARKET_VALUE",
    "reduceData": "false",
    "includeDividends": "false",
    "features": "DIVIDENDS",
}

# Supported `period` values accepted by the justETF performance-chart endpoint.
# "D1" returns the intraday (minute-by-minute) gettex series for the current
# trading day under the "series" field and for the previous day under
# "prevDaySeries". Other values (e.g. "MAX") behave like the default request.
Period = Literal["D1", "W1", "M1", "M3", "M6", "Y1", "Y3", "Y5", "MAX"]


def parse_series(
    raw_series: list[RawSeriesItem], value_name: str = "value"
) -> pd.DataFrame:
    """
    Parse data series as Pandas DataFrame from the received JSON format.
    """
    index = pd.to_datetime([sample["date"] for sample in raw_series], format="%Y-%m-%d")
    values = [sample["value"]["raw"] for sample in raw_series]
    return pd.DataFrame({value_name: values}, index=index)


def relative(series: pd.Series) -> pd.Series:
    """
    Convert a series to percentual values relative to its first value.
    """
    return 100 * (series / series.iloc[0] - 1)


def load_raw_chart(
    isin: str, currency: Currency = "EUR", period: Optional[str] = None
) -> RawChart:
    """
    Get a raw ETF chart for the whole time period.

    Args:
        isin: ISIN of an ETF.
        currency: Currency to get data in, see `Currency` for available options.
        period: Optional justETF chart period (see `Period`). When ``None``
            (default) the endpoint is queried without a ``period`` parameter,
            preserving the historical behaviour. Pass ``"D1"`` to obtain the
            intraday (minute-by-minute) gettex series for the current trading
            day (only populated for ``currency="EUR"``).

    Returns:
        Raw chart data as `RawChart`.
    """
    url = BASE_URL.format(isin=isin)
    params = {**BASE_PARAMS, "currency": currency}
    if period is not None:
        params["period"] = period
    response = requests.get(
        url,
        params=params,
        headers={"User-Agent": USER_AGENT},
    )
    assert_response_status_ok(response, "chart")
    data = response.json()
    return data


def load_raw_series(
    isin: str,
    currency: Currency = "EUR",
    period: str = "D1",
    series_field: str = "series",
) -> list[RawSeriesItem]:
    """
    Generic helper returning the raw list of series points of a chart query.

    This is a thin, reusable wrapper over `load_raw_chart` that extracts one of
    the list-valued fields of the response (e.g. ``"series"`` or
    ``"prevDaySeries"``). It performs no parsing or aggregation, so callers can
    process the raw points however they need.

    Args:
        isin: ISIN of an ETF.
        currency: Currency to get data in, see `Currency` for available options.
        period: justETF chart period (see `Period`). Defaults to ``"D1"``
            (intraday).
        series_field: Name of the list-valued field to extract from the raw
            response. Defaults to ``"series"`` (current day for ``period="D1"``);
            use ``"prevDaySeries"`` for the previous day.

    Returns:
        The raw list of series items (possibly empty, e.g. outside market hours
        or for currencies other than EUR where the intraday feed is not
        available).
    """
    data = load_raw_chart(isin, currency, period=period)
    return data.get(series_field) or []


def load_intraday_ohlc(isin: str, currency: Currency = "EUR") -> Optional[dict]:
    """
    Get the current-day intraday open/high/low/last from the gettex feed.

    Uses the ``period="D1"`` chart, whose ``series`` field holds the current
    trading day's minute-by-minute quotes. justETF only historizes the intraday
    gettex feed in EUR, so for other currencies (or outside market hours) the
    series is empty and this function returns ``None``.

    Args:
        isin: ISIN of an ETF.
        currency: Currency to get data in. Only ``"EUR"`` yields intraday data.

    Returns:
        A dict ``{open, high, low, last, date}`` where prices are floats and
        ``date`` is the ISO date string of the last intraday point, or ``None``
        if no intraday data is available.
    """
    series = load_raw_series(isin, currency, period="D1", series_field="series")
    if not series:
        return None
    values = [point["value"]["raw"] for point in series]
    last_date = series[-1]["date"][:10]
    return {
        "open": values[0],
        "high": max(values),
        "low": min(values),
        "last": values[-1],
        "date": last_date,
    }


def load_chart(
    isin: str, currency: Currency = "EUR", unclosed: bool = False
) -> pd.DataFrame:
    """
    Get and enrich an ETF chart for the whole time period.

    Args:
        isin: ISIN of an ETF.
        currency: Currency to get data in, see `Currency` for available options.
        unclosed: If True, include the current day's quote even if the day is
            not closed yet.

    Returns:
        Pandas DataFrame with dates as index and following columns:
            "quote": Daily quote of the ETF at the given date.
            "relative": Daily relative growth of quote compared to the first
                ever quote in percents.
            "dividends": For distributing ETFs, dividends payed out at the given
                date. 0 for all dates without dividends payouts.
            "cumulative_dividends": For distributing ETFs, sum of all dividends
                payed out until the given date.
            "quote_with_dividends": Sum of the daily quote and all dividends
                payed out until the given date.
            "relative_with_dividends": For distributing ETFs, daily relative
                growth of the sum of the daily quote and all dividends payed out
                until the given date compared to the first ever quote.
            "reinvested_dividends": For distributing ETFs, quote of all
                dividends payed out until the given date if they were reinvested
                immediately.
            "quote_with_reinvested_dividends": For distributing ETFs, sum of the
                daily quote and all dividends payed out until the given date if
                they were reinvested immediately.
            "relative_with_reinvested_dividends": For distributing ETFs, daily
                relative growth of the sum of the daily quote and all dividends
                payed out until the given date if they were reinvested
                immediately.
    """
    data = load_raw_chart(isin, currency)

    raw_series = data["series"]
    if unclosed:
        raw_series.append(
            {
                "date": data["latestQuoteDate"],
                "value": data["latestQuote"],
            }
        )

    df = parse_series(data["series"], "quote")
    df["relative"] = relative(df["quote"])

    dividends_df = parse_series(data["features"]["DIVIDENDS"], "dividends")
    df = df.join(dividends_df)
    df["dividends"] = df["dividends"].fillna(0)
    df["cumulative_dividends"] = df["dividends"].cumsum()
    df["quote_with_dividends"] = df["quote"] + df["cumulative_dividends"]
    df["relative_with_dividends"] = relative(df["quote_with_dividends"])
    reinvested_shares = pd.Series(1.0, index=df.index)
    for index, row in dividends_df.iterrows():
        reinvested_shares.loc[reinvested_shares.index >= index] += (
            reinvested_shares[index] * row["dividends"] / df.at[index, "quote"]  # ty: ignore[invalid-argument-type]
        )
    df["quote_with_reinvested_dividends"] = df["quote"] * reinvested_shares
    df["relative_with_reinvested_dividends"] = relative(
        df["quote_with_reinvested_dividends"]
    )
    df["reinvested_dividends"] = df["quote_with_reinvested_dividends"] - df["quote"]

    df.index.name = "date"
    return df


def compare_charts(
    charts: dict[str, pd.DataFrame],
    dates: Literal["shortest", "longest"] = "shortest",
    input_value: Literal[
        "quote", "quote_with_dividends", "quote_with_reinvested_dividends"
    ] = "quote_with_dividends",
    output_value: Literal["absolute", "relative", "percentage"] = "percentage",
) -> pd.DataFrame:
    """
    Compare charts of multiple ETFs.

    Args:
        charts: Dictionary of ISINs and their charts as `pd.DataFrame`.
        dates: If "shortest", include only the shortest common date range.
            If "longest", include all dates.
        input_value: Value to compare for each ISIN, one of "quote",
            "quote_with_dividends", "quote_with_reinvested_dividends".
        output_value: Value to return for each ISIN, one of "absolute",
            "relative", "percentage".

    Returns:
        Pandas DataFrame with dates as index and given ISINs as columns.
    """
    longest_chart = max(charts.values(), key=len)
    charts_df = pd.DataFrame(index=longest_chart.index)  # ty: ignore[unresolved-attribute]
    for isin, chart in charts.items():
        charts_df[isin] = chart[input_value]

    # First ever date when all values are available.
    min_common_date = charts_df.index[charts_df.notna().all(axis=1)].min()
    if dates == "shortest":
        charts_df = charts_df[charts_df.index >= min_common_date]
    elif dates != "longest":
        raise ValueError(
            f"`dates` argument must be one of 'shortest' or 'longest', but "
            f"value '{dates}' received."
        )

    if output_value == "absolute":
        return charts_df
    if output_value == "relative":
        return charts_df.div(charts_df.loc[min_common_date], axis="columns")
    if output_value == "percentage":
        return 100 * (charts_df.div(charts_df.loc[min_common_date], axis="columns") - 1)
    raise ValueError(
        f"`output_value` argument must be one of 'absolute', 'relative' or "
        f"'percentage', but value '{output_value}' received."
    )
