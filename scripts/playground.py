import logging
import time
from typing import Optional

import numpy as np
import pandas as pd
import requests

from justetf_scraping.chart_parsing import Chart, filter_charts, parse_xml
from justetf_scraping.chart_requests import HTML_HEADERS, Payload, URL, XML_HEADERS


def get_charts(isin: str) -> pd.DataFrame:
    """
    Get ETF charts as `pandas.DataFrame`. Columns are:
        market value since inception;
        dividends (always 0 in case of accumulating ETFs);
        volatility for the last year since 1 year after inception (including
            dividends in case of accumulating ETFs).
    """
    payload = Payload(isin)
    with requests.Session() as session:
        # Setup cookies.
        response = session.head(URL, params=payload.html(), headers=HTML_HEADERS)
        assert response.status_code == requests.codes.ok

        # Setup default chart
        response = session.head(URL, params=payload.default_chart(), headers=XML_HEADERS)
        assert response.status_code == requests.codes.ok

        volatility_chart: Optional[Chart] = None
        for _ in range(20):
            # After some time, we can receive the full period volatility chart
            # through the same endpoint.
            time.sleep(1)
            response = session.get(URL, params=payload.default_chart(), headers=XML_HEADERS)
            assert response.status_code == requests.codes.ok

            # Try to parse ETF volatility.
            charts = parse_xml(response.text, "charts")
            if charts:
                volatility_chart = filter_charts(charts, id=isin, name="Volatility", type="line")
                if volatility_chart is not None:
                    break
        else:
            logging.warning("Volatility chart not received.")

        # Set max time period and disable dividends.
        response = session.head(URL, params=payload.set_chart_period("max"), headers=XML_HEADERS)
        assert response.status_code == requests.codes.ok
        response = session.head(URL, params=payload.set_chart_dividends(False), headers=XML_HEADERS)
        assert response.status_code == requests.codes.ok

        # Parse ETF price (absolute and relative change can be derived from it).
        response = session.get(URL, params=payload.set_chart_value("market_value"), headers=XML_HEADERS)
        assert response.status_code == requests.codes.ok
        charts = parse_xml(response.text, "charts")
        price_chart = filter_charts(charts, id=isin, type="line")
        assert price_chart is not None
        df = price_chart.data.to_frame("price")

        # Parse ETF dividends in case of a distributing ETF.
        df["dividends"] = 0.0
        response = session.get(URL, params=payload.set_chart_dividends(True), headers=XML_HEADERS)
        assert response.status_code == requests.codes.ok
        dividends = parse_xml(response.text, "dividends")
        if dividends:
            df.loc[dividends[0].index, "dividends"] = dividends[0]

        # Append volatility if received.
        df["volatility"] = np.nan
        if volatility_chart is not None:
            df.loc[volatility_chart.data.index, "volatility"] = volatility_chart.data

        return df
        # df["change"] = 100 * df["price"] / df["price"][0] - 100


if __name__ == "__main__":
    df1 = get_charts("IE00B4L5Y983")
    df2 = get_charts("LU1737652237")
    print()
