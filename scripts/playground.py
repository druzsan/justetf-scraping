import logging
import time
from typing import Optional

import numpy as np
import pandas as pd
import requests

from justetf_scraping.chart_parsing import Chart, filter_charts, parse_xml
from justetf_scraping.chart_requests import Headers, Payload, URL
from justetf_scraping import scrape_charts


def get_charts(isin: str) -> pd.DataFrame:
    """
    Get ETF charts as `pandas.DataFrame`. Columns are:
        "price": market value since inception;
        "dividends": dividends (always 0 in case of accumulating ETFs);
        "volatility": volatility for the last year since 1 year after inception
            (including dividends in case of accumulating ETFs).
    """
    headers = Headers(isin)
    payload = Payload(isin)
    with requests.Session() as session:
        # Setup cookies.
        # response = session.get(URL, params=payload.html(), headers=headers.html())
        # assert response.status_code == requests.codes.ok
        # print(response.text[:200])
        # print()

        # Setup default charts
        response = session.get(URL, params=payload.default_chart(), headers=headers.xml())
        assert response.status_code == requests.codes.ok
        print(response.text[:200])
        print()
        charts = parse_xml(response.text, "charts")

        volatility_chart: Optional[Chart] = None
        for _ in range(20):
            # After some time, we can receive the full period volatility charts
            # through the same endpoint.
            time.sleep(1)
            response = session.get(URL, params=payload.default_chart(), headers=headers.xml())
            assert response.status_code == requests.codes.ok
            print(response.text[:200])
            print()

            # Try to parse ETF volatility.
            charts = parse_xml(response.text, "charts")
            if charts:
                volatility_chart = filter_charts(charts, id=isin, name="Volatility", type="line")
                if volatility_chart is not None:
                    break
        else:
            logging.warning("Volatility charts not received.")

        # Set max time period and disable dividends.
        response = session.get(URL, params=payload.set_chart_period("max"), headers=headers.xml())
        assert response.status_code == requests.codes.ok
        print(response.text[:200])
        print()
        charts = parse_xml(response.text, "charts")
        response = session.get(URL, params=payload.set_chart_dividends(False), headers=headers.xml())
        assert response.status_code == requests.codes.ok
        print(response.text[:200])
        print()
        charts = parse_xml(response.text, "charts")

        # Parse ETF price (absolute and relative change can be derived from it).
        response = session.get(URL, params=payload.set_chart_value("market_value"), headers=headers.xml())
        assert response.status_code == requests.codes.ok
        print(response.text[:200])
        print()
        charts = parse_xml(response.text, "charts")
        price_chart = filter_charts(charts, id=isin, type="line")
        assert price_chart is not None
        df = price_chart.data.to_frame("price")

        # Parse ETF dividends in case of a distributing ETF.
        df["dividends"] = 0.0
        response = session.get(URL, params=payload.set_chart_dividends(True), headers=headers.xml())
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


def experiment(isin: str) -> None:
    headers = Headers(isin)
    payload = Payload(isin)
    with requests.Session() as session:
        response = session.get(URL, params=payload.html(), headers=headers.html())
        assert response.status_code == requests.codes.ok
        print(response.text[:200])
        print()
        with open("2-default.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        response = session.get(URL, params=payload.overview_panel(), headers=headers.xml())
        assert response.status_code == requests.codes.ok
        charts = parse_xml(response.text, "charts")
        dividends = parse_xml(response.text, "dividends")
        print(response.text[:200])
        print(len(charts), len(dividends))
        with open("2-overview-panel.xml", "w", encoding="utf-8") as f:
            f.write(response.text)

        response = session.get(URL, params=payload.returns_panel(), headers=headers.xml())
        assert response.status_code == requests.codes.ok
        charts = parse_xml(response.text, "charts")
        dividends = parse_xml(response.text, "dividends")
        print(response.text[:200])
        print(len(charts), len(dividends))
        with open("2-returns-panel.xml", "w", encoding="utf-8") as f:
            f.write(response.text)

        time.sleep(1.5)
        response = session.get(URL, params=payload.default_chart(), headers=headers.xml())
        assert response.status_code == requests.codes.ok
        charts = parse_xml(response.text, "charts")
        dividends = parse_xml(response.text, "dividends")
        print(response.text[:200])
        print(len(charts), len(dividends))
        with open("2-default.xml", "w", encoding="utf-8") as f:
            f.write(response.text)

        response = session.get(URL, params=payload.set_chart_period("max"), headers=headers.xml())
        assert response.status_code == requests.codes.ok
        charts = parse_xml(response.text, "charts")
        dividends = parse_xml(response.text, "dividends")
        print(response.text[:200])
        print(len(charts), len(dividends))
        with open("2-max.xml", "w", encoding="utf-8") as f:
            f.write(response.text)

        # response = session.get(URL, params=payload.set_chart_dividends(False), headers=headers.xml())
        response = session.post(URL, params=payload.set_chart_dividends(False), headers={**headers.xml(), "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Content-Length": "0"})
        assert response.status_code == requests.codes.ok
        print(response.text[:200])
        print()

        # response = session.get(URL, params=payload.set_chart_value("market_value"), headers=headers.xml())
        #response = session.post(URL, params=payload.set_chart_value("market_value"), headers={**headers.xml(), "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Content-Length": "187"}, timeout=5)
        #print(response.request.body)
        #assert response.status_code == requests.codes.ok
        #print(response.text[:200])
        #print()



if __name__ == "__main__":
    # experiment("IE00B4L5Y983")
    # experiment("LU1737652237")
    # df1 = get_charts("IE00B4L5Y983")
    # df2 = get_charts("LU1737652237")
    df3 = scrape_charts("IE00B4L5Y983")
    # df4 = scrape_charts("LU1737652237")
    print()
