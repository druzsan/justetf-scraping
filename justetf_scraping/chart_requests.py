"""
Helpers for charts requests.

Unnecessary headers are removed.

Extra XML POST headers are:
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    Content-Length: 89
    Origin: https://www.justetf.com
but such POST requests hang so we use equivalent GET requests.
"""
from typing import Dict, Literal


URL = "https://www.justetf.com/en/etf-profile.html"

COMMON_HEADERS: Dict[str, str] = {
    "Host": "www.justetf.com",
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}
HTML_HEADERS: Dict[str, str] = {
    **COMMON_HEADERS,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}
XML_HEADERS: Dict[str, str] = {
    **COMMON_HEADERS,
    "Accept": "application/xml, text/xml, */*; q=0.01",
    "Wicket-Ajax": "true",
    "Wicket-Ajax-BaseURL": "en/etf-profile.html?isin=IE00B4L5Y983",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Referer": "https://www.justetf.com/en/etf-profile.html?isin=IE00B4L5Y983",
    "TE": "trailers",
}

"""
2: ?0-1.0-overviewPanel&isin=IE00B4L5Y983&_wicket=1&_=1654968616036
3: ?0-1.0-returnsPanel&isin=IE00B4L5Y983&_wicket=1&_=1654968616037
4: ?0-1.1-&isin=IE00B4L5Y983&_wicket=1&_=1654968616038
5: ?0-1.1-&isin=IE00B4L5Y983&_wicket=1&_=1654968616039
6: ?0-1.1-&isin=IE00B4L5Y983&_wicket=1&_=1654968616040
7: ?0-1.1-&isin=IE00B4L5Y983&_wicket=1&_=1654968616041
8: ?0-1.0-chartPanel-charts-content-dates-ptl_max&isin=IE00B4L5Y983&_wicket=1&_=1654972505831
Wicket-FocusedElementId: id285
9: ?0-1.0-chartPanel-charts-content-optionsPanel-selectContainer-valueType&isin=IE00B4L5Y983&_wicket=1
+
"chartPanel:charts:content:optionsPanel:selectContainer:valueType": "absolute_change"
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Content-Length: 89
Wicket-FocusedElementId: id286
Origin: https://www.justetf.com

"""

ChartPeriod = Literal["1m", "3m", "6m", "1y", "3y", "5y", "ytd", "max"]
ChartValue = Literal["market_value", "absolute_change", "relative_change"]
ChartCurrency = Literal["0", "1", "2", "3"]

CURRENCIES: Dict[str, ChartCurrency] = {
    "EUR": "0",
    "USD": "1",
    "CHF": "2",
    "GBP": "3",
}


class Payload:
    """
    Payload generator for getting charts data.
    """

    _isin: str

    def __init__(self, isin: str) -> None:
        self._isin = isin

    def html(self) -> Dict[str, str]:
        """
        Base HTML payload.
        """
        return {"isin": self._isin}

    def xml(self) -> Dict[str, str]:
        """
        Base XML payload.
        """
        return {**self.html(), "_wicket": "1"}

    def overview_panel(self) -> Dict[str, str]:
        """
        Payload for getting overview panel (no charts).
        """
        return {**self.xml(), "0-1.0-overviewPanel": ""}

    def returns_panel(self) -> Dict[str, str]:
        """
        Payload for getting returns panel (no charts).
        """
        return {**self.xml(), "0-1.0-returnsPanel": ""}

    def default_chart(self) -> Dict[str, str]:
        """
        Payload for getting value and volatility charts components;
        default value data.
        """
        return {**self.xml(), "0-1.1-": ""}

    def set_chart_period(self, period: ChartPeriod) -> Dict[str, str]:
        """
        Payload for setting time period and getting updated value charts.
        """
        return {**self.xml(), f"0-1.0-chartPanel-charts-content-dates-ptl_{period}": ""}

    def set_chart_value(self, value: ChartValue) -> Dict[str, str]:
        """
        Payload for setting value type and getting updated value charts.
        """
        return {
            **self.xml(),
            "0-1.0-chartPanel-charts-content-optionsPanel-selectContainer-valueType": "",
            "chartPanel:charts:content:optionsPanel:selectContainer:valueType": value,
        }

    def set_chart_currency(self, currency: str) -> Dict[str, str]:
        """
        Payload for setting currency and getting updated value charts.
        """
        code = CURRENCIES.get(currency, currency)
        return {
            **self.xml(),
            "0-1.0-chartPanel-charts-content-optionsPanel-selectContainer-currencies": "",
            "chartPanel:charts:content:optionsPanel:selectContainer:currencies": code,
        }

    def set_chart_dividends(self, with_dividends: bool) -> Dict[str, str]:
        """
        Payload for enabling/disabling dividends and getting updated value charts.
        """
        payload = {
            **self.xml(),
            "0-1.0-chartPanel-charts-content-optionsPanel-selectContainer-includePaymentContainer-includePayment": "",
        }
        if with_dividends:
            payload[
                "chartPanel:charts:content:optionsPanel:selectContainer:includePaymentContainer:includePayment"
            ] = "on"
        # For no dividends, no payload parameter is required.
        return payload
