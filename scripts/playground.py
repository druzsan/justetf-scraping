import logging
import re
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, fields
from typing import Dict, List, Literal, Optional, Tuple

import pandas as pd
import requests


URL = "https://www.justetf.com/en/etf-profile.html"

COMMON_HEADERS = {
    "Host": "www.justetf.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
    #"Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    #"Cookie": "pc=etf_close; ls=etf_open; ic=etf_close; spc=etf_close; replicationType=etf_close; instrumentType=etf_open; currencyHedged=etf_close; dc=etf_close; indexProvider=etf_close; fsg=etf_open; distributionPolicy=etf_open; age=etf_open; sustainable=etf_close; locale_=en; CookieConsent={stamp:%27EJ3syMnUXvsJH0OoY+wvNMy6fGdfkdbPdcKCE3fk4qR589DVIwN6/w==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cver:4%2Cutc:1648978956294%2Cregion:%27de%27}; universeCountry_=DE; universeDisclaimerAccepted_=true; universeType_=private; JSESSIONID=E0E70592ACA0427E04751D6BACC3C0B7; indexProvider_showMore=true; AWSALB=IqoNddPdO4y3c2CqaiVFKNPlHrFffqBuicchMlTSYTlO1gvuXudBvn1SAAejqek57/QNxwWCAo77M8sbZVu6kxm42BzOpg1auYyxFPl6rIVXsNoInPIE0FbPz4WD; AWSALBCORS=IqoNddPdO4y3c2CqaiVFKNPlHrFffqBuicchMlTSYTlO1gvuXudBvn1SAAejqek57/QNxwWCAo77M8sbZVu6kxm42BzOpg1auYyxFPl6rIVXsNoInPIE0FbPz4WD"
}
HTML_HEADERS = {
    **COMMON_HEADERS,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}
XML_HEADERS = {
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
8: ?0-1.0-chartPanel-chart-content-dates-ptl_max&isin=IE00B4L5Y983&_wicket=1&_=1654972505831
Wicket-FocusedElementId: id285
9: ?0-1.0-chartPanel-chart-content-optionsPanel-selectContainer-valueType&isin=IE00B4L5Y983&_wicket=1
+
"chartPanel:chart:content:optionsPanel:selectContainer:valueType": "absolute_change"
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Content-Length: 89
Wicket-FocusedElementId: id286
Origin: https://www.justetf.com
"""

"""
3: series: [{ id: 'IE00B4L5Y983', type: 'area', negativeFillColor: '#f4abab', negativeColor: '#b51212', fillColor: '#cded91', name: 'iShares Core MSCI World UCITS ETF USD (Acc)', color: '#72af08', data: [[Date.UTC(2021,5,11),0.00],<...>,[Date.UTC(2022,5,10),2.62]]}]
3: series: [{ id: 'IE00B4L5Y983', type: 'area', negativeFillColor: '#f4abab', negativeColor: '#b51212', fillColor: '#cded91', name: 'iShares Core MSCI World UCITS ETF USD (Acc)', color: '#72af08', data: [[Date.UTC(2021,5,11),0.00],<...>,[Date.UTC(2022,5,10),2.62]]}]
3: series: [{ id: 'IE00B4L5Y983', type: 'line', name: 'iShares Core MSCI World UCITS ETF USD (Acc)', color: '#2269b1', data: [[Date.UTC(2021,5,11),0.00],<...>,[Date.UTC(2022,5,10),2.62]]}, { id: 'onAxe', cursor: 'pointer', type: 'flags', color: '#2269b1', showInLegend: false, data: [], shape: 'squarepin', width: 40}]
4/5/6: series: [{ id: 'IE00B4L5Y983', type: 'line', name: 'Volatility', color: '#2269b1', data: [[Date.UTC(2010,8,25),14.863007042001875],<...>,[Date.UTC(2022,5,10),15.97959529061427]]}]
7: _8100ae450d794a0381baad9048616703.addSeries({ id: 'IE00B4L5Y983', name: 'iShares Core MSCI World UCITS ETF USD (Acc)', type: 'line', color: '#2269b1', data: [[Date.UTC(2009,8,25),0.00],<...>,[Date.UTC(2022,5,10),318.35]]}, false);
7: _8100ae450d794a0381baad9048616703.addSeries({ id: 'onAxe', cursor: 'pointer', type: 'flags', allowOverlapX: true, color: '#2269b1', showInLegend: false, data: [], shape: 'squarepin', width: 40}, false);
8: _8100ae450d794a0381baad9048616703.addSeries({ id: 'IE00B4L5Y983', name: 'iShares Core MSCI World UCITS ETF USD (Acc)', type: 'line', color: '#2269b1', data: [[Date.UTC(2009,8,25),0.00],<...>,[Date.UTC(2022,5,10),53.26]]}, false);
8: _8100ae450d794a0381baad9048616703.addSeries({ id: 'onAxe', cursor: 'pointer', type: 'flags', allowOverlapX: true, color: '#2269b1', showInLegend: false, data: [], shape: 'squarepin', width: 40}, false);
"""

SPACES_PATTERN = re.compile(r"\s")
META_FIELDS_PATTERN = re.compile(r"(\w+)\s*:\s*'([^']*)'")
DATA_KEY_PATTERN = re.compile(r"data\s*:\s\[")
DATA_SAMPLE_PATTERN = re.compile(r"\[Date.UTC\((\d{4}),(\d{1,2}),(\d{1,2})[,\d]*\),([-+]?[0-9]*\.?[0-9]+)\]")


@dataclass
class Series:
    id: str
    type: str
    name: str
    color: str
    data: pd.Series

    @classmethod
    def fromstring(cls, text: str) -> "Series":
        keys = [field.name for field in fields(cls)]
        meta_data = dict(META_FIELDS_PATTERN.findall(text))
        meta_data = {key: value for key, value in meta_data.items() if key in keys}
        match = DATA_KEY_PATTERN.search(text)
        if match is None:
            raise ValueError("No data field found in the string.")
        _, end, data_text = parse_brackets(text[match.end() - 1:], "[")
        if end == -1:
            raise ValueError("No data array found in the string.")
        matches = DATA_SAMPLE_PATTERN.findall(data_text)
        if not matches:
            raise ValueError("No data samples found in the string.")
        *ymds, values = zip(*matches)
        # Patch months from weird 0..11 to 1..12.
        dates = [f"{y}-{str(int(m) + 1)}-{d}" for y, m, d in zip(*ymds)]
        data = pd.Series(values, index=pd.to_datetime(dates, format="%Y-%m-%d"), dtype=float)
        return cls(**meta_data, data=data)


def parse_brackets(text: str, bracket: str, closing_bracket: Optional[str] = None) -> Tuple[int, int, str]:
    if closing_bracket is None:
        closing_bracket = {"(": ")", "[": "]", "{": "}", "<": ">"}.get(bracket, bracket)
    if text[0] != bracket:
        return -1, -1, ""
    text = text[1:]
    counter = 1
    end = -1
    for i, char in enumerate(text):
        if char == closing_bracket:
            counter -= 1
        elif char == bracket:
            counter += 1
        if counter == 0:
            end = i + 1
            text = text[:i]
            break
    return 0, end, text


def parse_series(text: str) -> Tuple[List[Series], int]:
    text = text.lstrip()
    if len(text) == 0:
        return [], 0
    char = text[0]
    if char == "{":
        _, end, subtext = parse_brackets(text, char)
        if end != -1:
            # Parse an object.
            try:
                return [Series.fromstring(subtext)], end
            except (TypeError, ValueError):
                ...
    elif char == "(":
        _, end, subtext = parse_brackets(text, char)
        if end != -1:
            # Parse content of a function.
            return parse_series(subtext)
    elif char == "[":
        start, end, subtext = parse_brackets(text, char)
        if end != -1:
            # Parse an array.
            all_series = []
            while True:
                series, offset = parse_series(subtext[start:])
                all_series.extend(series)
                start += offset
                if len(subtext[start:]) == 0 or subtext[start] != ",":
                    break
                start += 1
            return all_series, start
    return [], 0


def parse_js(text: str) -> List[Series]:
    text = SPACES_PATTERN.sub(" ", text)
    all_series, res = [], False
    for prefix in ("series:", "addSeries"):
        start = 0
        while True:
            start = text.find(prefix, start)
            if start == -1:
                break
            start += len(prefix)
            series, offset = parse_series(text[start:])
            all_series.extend(series)
            start += offset
    return all_series


def parse_xml(text: str) -> List[Series]:
    all_series = []
    root = ET.fromstring(text)
    for header_contribution in root.findall("header-contribution"):
        if header_contribution.text is None:
            continue
        inner_root = ET.fromstring(header_contribution.text)
        for script in inner_root.findall("script"):
            if script.text is None:
                continue
            series = parse_js(script.text)
            all_series.extend(series)
    return all_series


ChartPeriod = Literal["1m", "3m", "6m", "1y", "3y", "5y", "ytd", "max"]
ChartValue = Literal["market_value", "absolute_change", "relative_change"]
ChartCurrency = Literal["0", "1", "2", "3"]


class Payload:

    _isin: str

    def __init__(self, isin: str) -> None:
        self._isin = isin

    def html(self) -> Dict[str, str]:
        return {"isin": self._isin}

    def xml(self) -> Dict[str, str]:
        return {**self.html(), "_wicket": "1"}

    def overview_panel(self) -> Dict[str, str]:
        return {**self.xml(), "0-1.0-overviewPanel": ""}

    def returns_panel(self) -> Dict[str, str]:
        return {**self.xml(), "0-1.0-returnsPanel": ""}

    def default_chart(self) -> Dict[str, str]:
        return {**self.xml(), "0-1.1-": ""}

    def chart_period(self, period: ChartPeriod) -> Dict[str, str]:
        return {**self.xml(), f"0-1.0-chartPanel-chart-content-dates-ptl_{period}": ""}

    def chart_value(self, value: ChartValue) -> Dict[str, str]:
        return {**self.xml(), "0-1.0-chartPanel-chart-content-optionsPanel-selectContainer-valueType": "", "chartPanel:chart:content:optionsPanel:selectContainer:valueType": value}

    def chart_currency(self, currency: ChartCurrency) -> Dict[str, str]:
        return {**self.xml(), "0-1.0-chartPanel-chart-content-optionsPanel-selectContainer-currencies": "", "chartPanel:chart:content:optionsPanel:selectContainer:currencies": currency}

    def chart_dividends(self, dividends: bool) -> Dict[str, str]:
        payload = {**self.xml(), "0-1.0-chartPanel-chart-content-optionsPanel-selectContainer-includePaymentContainer-includePayment": ""}
        if dividends:
            payload["chartPanel:chart:content:optionsPanel:selectContainer:includePaymentContainer:includePayment"] = "on"
        # Otherwise, no parameter is required.
        return payload


def filter_series(series: List[Series], **kwargs: str) -> Optional[Series]:
    for series_ in series:
        if len(series_.data) and all(getattr(series_, key, None) == value for key, value in kwargs.items()):
            return series_
    return None


def parse_xml2(text: str):

    def findrec(element: ET.Element, tag: str) -> List[ET.Element]:
        if element.tag == tag:
            return [element]
        return sum((findrec(x, tag) for x in element), [])

    # Patch text
    text = text.replace("&nbsp", " ")
    root = ET.fromstring(text)
    for component in root.findall("component"):
        if component.text is None:
            continue
        inner_root = ET.fromstring(component.text)
        for select in inner_root.findall("select"):
            if select.text is None:
                continue
            print()


def experiment2(isin: str) -> None:
    payload = Payload(isin)

    with requests.Session() as session:
        # Setup cookies.
        response = session.head(URL, params=payload.html(), headers=HTML_HEADERS)
        assert response.status_code == requests.codes.ok

        # Setup default chart
        response = session.head(URL, params=payload.default_chart(), headers=XML_HEADERS)
        assert response.status_code == requests.codes.ok

        for _ in range(20):
            # After some time, we can receive the full period volatility series
            # through the same endpoint.
            time.sleep(1)
            response = session.get(URL, params=payload.default_chart(), headers=XML_HEADERS)
            assert response.status_code == requests.codes.ok

            series = parse_xml(response.text)
            if len(series) > 0:
                break
        else:
            logging.warning("Volatility chart not received.")
        volatility = filter_series(series, id=isin, name="Volatility", type="line")

        # Set max time period.
        response = session.head(URL, params=payload.chart_period("max"), headers=XML_HEADERS)
        assert response.status_code == requests.codes.ok

        response = session.get(URL, params=payload.chart_value("market_value"), headers=XML_HEADERS)
        assert response.status_code == requests.codes.ok
        series = parse_xml(response.text)
        market_value = filter_series(series, id=isin, type="line")

        response = session.get(URL, params=payload.chart_value("relative_change"), headers=XML_HEADERS)
        assert response.status_code == requests.codes.ok
        series = parse_xml(response.text)
        change = filter_series(series, id=isin, type="line")

        response = session.get(URL, params=payload.chart_value("absolute_change"), headers=XML_HEADERS)
        assert response.status_code == requests.codes.ok
        series = parse_xml(response.text)
        price = filter_series(series, id=isin, type="line")
        print()




def experiment1(isin: str) -> None:
    payload = dict(isin=isin)
    xml_payload = {**payload, "_wicket": "1"}

    with requests.Session() as session:
        response = session.head(URL, params=payload, headers=HTML_HEADERS)
        print(response.request.url)
        assert response.status_code == requests.codes.ok
        print(response.text[:200])
        print()
        with open("0.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        # response = session.get(URL, params={**xml_payload, "0-1.0-overviewPanel": ""}, headers=XML_HEADERS)
        # print(response.request.url)
        # assert response.status_code == requests.codes.ok
        # print(response.text[:400])
        # print()
        # with open("1.xml", "w", encoding="utf-8") as f:
        #     f.write(response.text)
        # response = session.get(URL, params={**xml_payload, "0-1.0-returnsPanel": ""}, headers=XML_HEADERS)
        # print(response.request.url)
        # assert response.status_code == requests.codes.ok
        # print(response.text[:400])
        # print()
        # with open("2.xml", "w", encoding="utf-8") as f:
        #     f.write(response.text)
        response = session.get(URL, params={**xml_payload, "0-1.1-": ""}, headers=XML_HEADERS)
        print(response.request.url)
        assert response.status_code == requests.codes.ok
        print(response.text[:400])
        print()
        with open("3.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
        series = parse_xml(response.text)
        print(len(series))
        while True:
            # After some time, we can receive the volatility series through the same endpoint.
            time.sleep(1)
            response = session.get(URL, params={**xml_payload, "0-1.1-": ""}, headers=XML_HEADERS)
            print(response.request.url)
            assert response.status_code == requests.codes.ok
            print(response.text[:400])
            print()
            series = parse_xml(response.text)
            print(len(series))
            if len(series) > 0:
                break
        # time.sleep(5)
        response = session.get(URL, params={**xml_payload, "0-1.1-": ""}, headers=XML_HEADERS)
        print(response.request.url)
        assert response.status_code == requests.codes.ok
        print(response.text[:400])
        print()
        with open("4.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
        series = parse_xml(response.text)
        print(len(series))
        time.sleep(5)
        response = session.get(URL, params={**xml_payload, "0-1.1-": ""}, headers=XML_HEADERS)
        print(response.request.url)
        assert response.status_code == requests.codes.ok
        print(response.text[:400])
        print()
        with open("5.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
        series = parse_xml(response.text)
        print(len(series))
        time.sleep(5)
        response = session.get(URL, params={**xml_payload, "0-1.1-": ""}, headers=XML_HEADERS)
        print(response.request.url)
        assert response.status_code == requests.codes.ok
        print(response.text[:400])
        print()
        with open("6.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
        series = parse_xml(response.text)
        print(len(series))
        response = session.get(URL, params={**xml_payload, "0-1.0-chartPanel-chart-content-dates-ptl_max": ""}, headers=XML_HEADERS)
        print(response.request.url)
        assert response.status_code == requests.codes.ok
        print(response.text[:400])
        print()
        with open("7.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
        series = parse_xml(response.text)
        print(len(series))
        response = session.get(URL, params={**xml_payload, "0-1.0-chartPanel-chart-content-optionsPanel-selectContainer-valueType": "", "chartPanel:chart:content:optionsPanel:selectContainer:valueType": "absolute_change"}, headers=XML_HEADERS)
        print(response.request.url)
        assert response.status_code == requests.codes.ok
        print(response.text[:400])
        print()
        with open("8.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
        series = parse_xml(response.text)
        print(len(series))


if __name__ == "__main__":
    experiment2("IE00B4L5Y983")
