"""
Scrape ETF chart data from justETF
(e.g. https://www.justetf.com/en/etf-profile.html?isin=IE00B4L5Y983).
"""

from typing import Dict, Literal

import pandas as pd
import requests

from justetf_scraping.types import Currency

BASE_URL = "https://www.justetf.com/api/etfs/{isin}/performance-chart"
BASE_PARAMS = {
    "locale": "en",
    "valuesType": "MARKET_VALUE",
    "reduceData": "false",
    "includeDividends": "false",
    "features": "DIVIDENDS",
}


def parse_series(raw_series: Dict, value_name: str = "value") -> pd.DataFrame:
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


def load_chart(isin: str, currency: Currency = "EUR") -> pd.DataFrame:
    """
    Get and enrich an ETF chart for the whole time period.

    Args:
        isin: ISIN of an ETF.
        currency: Currency to get data in, see `Currency`.

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
    url = BASE_URL.format(isin=isin)
    response = requests.get(url, params={**BASE_PARAMS, "currency": currency})
    assert response.status_code == requests.codes.ok
    data = response.json()

    df = parse_series(data["series"], "quote")
    df["relative"] = relative(df["quote"])

    dividends_df = parse_series(data["features"]["DIVIDENDS"], "dividends")
    df = df.join(dividends_df)
    df["dividends"] = df["dividends"].fillna(0)
    df["cumulative_dividends"] = df["dividends"].cumsum()
    df["quote_with_dividends"] = df["quote"] + df["cumulative_dividends"]
    df["relative_with_dividends"] = relative(df["quote_with_dividends"])
    df["reinvested_dividends"] = 0
    for index, row in dividends_df.iterrows():
        df["reinvested_dividends"] += (
            df["quote"] * row["dividends"] / df.at[index, "quote"]
        ).mask(df.index < index, 0)
    df["quote_with_reinvested_dividends"] = df["quote"] + df["reinvested_dividends"]
    df["relative_with_reinvested_dividends"] = relative(
        df["quote_with_reinvested_dividends"]
    )

    df.index.name = "date"
    return df


def compare_charts(
    charts: Dict[str, pd.DataFrame],
    dates: Literal["shortest", "longest"] = "shortest",
    input_value: Literal[
        "quote", "quote_with_dividends", "quote_with_reinvested_dividends"
    ] = "quote_with_dividends",
    output_value: Literal["absolute", "relative", "percentage"] = "percentage",
) -> pd.DataFrame:
    longest_chart = max(charts.values(), key=len)
    charts_df = pd.DataFrame(index=longest_chart.index)
    for isin, chart in charts.items():
        charts_df[isin] = chart[input_value]

    # First ever date when all values are available.
    min_common_date = charts_df.index[charts_df.notna().all(axis=1)].min()
    if dates == "shortest":
        charts_df = charts_df[charts_df.index >= min_common_date]
    elif dates != "longest":
        raise ValueError(
            f"`dates` argument must be 'shortest' or 'longest', but value "
            f"'{dates}' received."
        )

    if output_value == "absolute":
        return charts_df
    if output_value == "relative":
        return charts_df.div(charts_df.loc[min_common_date], axis="columns")
    if output_value == "percentage":
        return 100 * (charts_df.div(charts_df.loc[min_common_date], axis="columns") - 1)
    raise ValueError(
        f"`output_value` argument must be 'absolute', 'relative' or "
        f"'percentage', but value '{dates}' received."
    )
