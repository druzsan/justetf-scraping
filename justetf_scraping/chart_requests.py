"""
Helpers for charts requests.

Unnecessary headers are removed.

Extra XML POST headers are:
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    Content-Length: 89
    Origin: https://www.justetf.com
but such POST requests hang so we use equivalent GET requests.
"""
from dataclasses import dataclass
from typing import Dict, Literal


"""
Common:
Host: www.justetf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

HTML:
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1

XML:
Accept: application/xml, text/xml, */*; q=0.01
Wicket-Ajax: true
Wicket-Ajax-BaseURL: en/etf-profile.html?isin=IE00B4L5Y983
X-Requested-With: XMLHttpRequest
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Referer: https://www.justetf.com/en/etf-profile.html?isin=IE00B4L5Y983
TE: trailers

XML POST:
Wicket-Ajax-BaseURL: en/etf-profile.html?isin=IE00B4L5Y983
Origin: https://www.justetf.com
Content-Length: <int>
optional (if length > 0): Content-Type: application/x-www-form-urlencoded; charset=UTF-8


GET /en/etf-profile.html?isin=IE00B4L5Y983 HTTP/1.1
================================================================================
GET /en/etf-profile.html?7-1.0-overviewPanel&isin=IE00B4L5Y983&_wicket=1&_=1655536264414 HTTP/2
================================================================================
GET /en/etf-profile.html?7-1.0-returnsPanel&isin=IE00B4L5Y983&_wicket=1&_=1655536264415 HTTP/2
================================================================================
GET /en/etf-profile.html?7-1.1-&isin=IE00B4L5Y983&_wicket=1&_=1655536264416 HTTP/2
================================================================================
GET /en/etf-profile.html?7-1.0-chartPanel-chart-content-dates-ptl_max&isin=IE00B4L5Y983&_wicket=1&_=1655536264417 HTTP/2
Wicket-FocusedElementId: id514
================================================================================
POST /en/etf-profile.html?8-1.0-chartPanel-chart-content-optionsPanel-selectContainer-includePaymentContainer-includePayment&isin=LU1437016972&_wicket=1 HTTP/2
Wicket-FocusedElementId: includePaymentOptionsPanel
Content-Length: 0
================================================================================
POST /en/etf-profile.html?8-1.0-chartPanel-chart-content-optionsPanel-selectContainer-valueType&isin=LU1437016972&_wicket=1 HTTP/2
{
    "chartPanel:chart:content:optionsPanel:selectContainer:valueType": "market_value"
}
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Content-Length: 86
Wicket-FocusedElementId: id5b5
"""

"""
curl "https://www.justetf.com/en/etf-profile.html?1-1.0-chartPanel-chart-content-optionsPanel-selectContainer-includePaymentContainer-includePayment&isin=LU1737652237&_wicket=1" -X POST -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" -H "Accept: application/xml, text/xml, */*; q=0.01" -H "Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3" -H "Accept-Encoding: gzip, deflate, br" -H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" -H "Wicket-Ajax: true" -H "Wicket-Ajax-BaseURL: en/etf-profile.html?isin=LU1737652237" -H "Wicket-FocusedElementId: includePaymentOptionsPanel" -H "X-Requested-With: XMLHttpRequest" -H "Origin: https://www.justetf.com" -H "Sec-Fetch-Dest: empty" -H "Sec-Fetch-Mode: cors" -H "Sec-Fetch-Site: same-origin" -H "Referer: https://www.justetf.com/en/etf-profile.html?isin=LU1737652237" -H "Connection: keep-alive" -H "Cookie: pc=etf_close; ls=etf_open; ic=etf_close; spc=etf_close; replicationType=etf_close; instrumentType=etf_open; currencyHedged=etf_close; dc=etf_close; indexProvider=etf_close; fsg=etf_open; distributionPolicy=etf_open; age=etf_open; sustainable=etf_open; locale_=en; CookieConsent={stamp:"%"27EJ3syMnUXvsJH0OoY+wvNMy6fGdfkdbPdcKCE3fk4qR589DVIwN6/w=="%"27"%"2Cnecessary:true"%"2Cpreferences:false"%"2Cstatistics:false"%"2Cmarketing:false"%"2Cver:4"%"2Cutc:1648978956294"%"2Cregion:"%"27de"%"27}; universeCountry_=DE; universeDisclaimerAccepted_=true; universeType_=private; AWSALB=AZb5M2PYWKM9kl3AzRaqcmbVl0Ljf+sjyAULFQcNBjg4O4T2bfLiTTqlHNwrZVX22ZAF2iKhKJYINRQQwlruktHr4NuqD88fgSD2xOitZtKZ3Gf8SBIvliWsrrvX; AWSALBCORS=AZb5M2PYWKM9kl3AzRaqcmbVl0Ljf+sjyAULFQcNBjg4O4T2bfLiTTqlHNwrZVX22ZAF2iKhKJYINRQQwlruktHr4NuqD88fgSD2xOitZtKZ3Gf8SBIvliWsrrvX; JSESSIONID=7773A3352C25EA949271754D9F7374DB; indexProvider_showMore=true" -H "TE: trailers" --data-raw "chartPanel"%"3Achart"%"3Acontent"%"3AoptionsPanel"%"3AselectContainer"%"3AincludePaymentContainer"%"3AincludePayment=on"
"""


URL = "https://www.justetf.com/en/etf-profile.html"


ChartPeriod = Literal["1m", "3m", "6m", "1y", "3y", "5y", "ytd", "max"]
ChartValue = Literal["market_value", "absolute_change", "relative_change"]
ChartCurrency = Literal["0", "1", "2", "3"]

CURRENCIES: Dict[str, ChartCurrency] = {
    "EUR": "0",
    "USD": "1",
    "CHF": "2",
    "GBP": "3",
}


@dataclass
class Headers:
    """
    Headers generator for getting charts data.
    """

    isin: str

    def _common(self) -> Dict[str, str]:
        """
        Common HTML and XML headers.
        """
        return {
            "Host": "www.justetf.com",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    def html(self) -> Dict[str, str]:
        """
        HTML headers.
        """
        return {
            **self._common(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        }

    def xml(self) -> Dict[str, str]:
        """
        XML headers.
        """
        return {
            **self._common(),
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Wicket-Ajax": "true",
            "Wicket-Ajax-BaseURL": f"en/etf-profile.html?isin={self.isin}",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Referer": f"https://www.justetf.com/en/etf-profile.html?isin={self.isin}",
            "TE": "trailers",
        }


@dataclass
class Payload:
    """
    Payload generator for getting charts data.
    """

    isin: str

    def html(self) -> Dict[str, str]:
        """
        Base HTML payload.
        """
        return {"isin": self.isin}

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
        return {**self.xml(), f"0-1.0-chartPanel-chart-content-dates-ptl_{period}": ""}

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
