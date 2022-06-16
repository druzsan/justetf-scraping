import re
import xml.etree.ElementTree as ET
from typing import List, Optional, Tuple
import json

import pandas as pd
import requests


def parse_brackets(text: str, bracket: str) -> Tuple[int, int, str, bool]:
    closing_brackets = {"(": ")", "[": "]", "{": "}", "<": ">"}
    closing_bracket = closing_brackets.get(bracket, bracket)
    start = text.find(bracket)
    if start == -1:
        return -1, -1, "", False
    counter = 1
    end = None
    for i, char in enumerate(text[start + 1 :]):
        if char == closing_bracket:
            counter -= 1
        elif char == bracket:
            counter += 1
        if counter == 0:
            end = start + i + 1
            break
    return start, -1 if end is None else end, text[start + 1 : end], end != -1


def scrape_xml(text: str) -> List[pd.Series]:
    series = []
    pattern = re.compile(
        r"\[Date.UTC\((\d{4}),(\d{1,2}),(\d{1,2})[,\d]*\),([-+]?[0-9]*\.?[0-9]+)\]"
    )
    root = ET.fromstring(text)
    for header_contribution in root.findall("header-contribution"):
        for script in ET.fromstring(header_contribution.text).findall("script"):
            text = script.text
            if text is None:
                continue
            while True:
                start = text.find("addSeries")
                if start == -1:
                    break
                text = text[start:]
                # Extract content of `addSeries`.
                start, end, subtext, res = parse_brackets(text, "(")
                if not res:
                    continue
                text = text[end:]  # Prepare text for the next iteration
                # Extract object from `addSeries`.
                start, end, subtext, res = parse_brackets(subtext, "{")
                if not res:
                    continue
                start, end, data, res = parse_brackets(subtext, "[")
                if not res:
                    continue
                matches = pattern.findall(data)
                if len(matches) == 0:
                    continue
                *ymds, values = zip(*matches)
                dates = [f"{d}/{str(int(m) + 1)}/{y}" for y, m, d in zip(*ymds)]
                meta_text = subtext[:start] + subtext[end + 1 :]
                _, _, name, res = parse_brackets(meta_text[meta_text.find("name:") :], "'")
                if not res:
                    name = None
                series.append(
                    pd.Series(
                        values,
                        index=pd.to_datetime(dates, format="%d/%m/%Y"),
                        dtype=float,
                        name=name,
                    )
                )


def scrape_chart(isin: str) -> None:
    url = "https://www.justetf.com/en/etf-profile.html"
    headers = {
        "Host": "www.justetf.com",
        "Accept": "application/xml, text/xml, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Wicket-Ajax": "true",
        "Wicket-Ajax-BaseURL": "en/etf-profile.html?isin=IE00B4L5Y983",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.justetf.com/en/etf-profile.html?isin=IE00B4L5Y983",
    }
    default_payload = {
        "0-1.1-": "",
        "isin": isin,
        "_wicket": "1",
    }
    max_range_payload = {
        "0-1.0-chartPanel-chart-content-dates-ptl_max": "",
        "isin": isin,
        "_wicket": "1",
    }

    session = requests.Session()

    response = session.get(url, params=default_payload)
    print(response.request.url)
    with open("static-response.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    assert response.status_code == requests.codes.ok

    response = session.get(url, params=default_payload, headers=headers)
    print(response.request.url)
    with open("default-response.xml", "w", encoding="utf-8") as f:
        f.write(response.text)
    assert response.status_code == requests.codes.ok
    scrape_xml(response.text)

    response = session.get(url, params=max_range_payload, headers=headers)
    with open("max-range-response.xml", "w", encoding="utf-8") as f:
        f.write(response.text)
    assert response.status_code == requests.codes.ok
    scrape_xml(response.text)

    response = session.get(url, params=max_range_payload)
    assert response.status_code == requests.codes.ok
    print(response.text[:200])
    print()

    response = session.get(url, params=max_range_payload, headers=headers)
    assert response.status_code == requests.codes.ok
    print(response.text[:200])


if __name__ == "__main__":
    isin = "IE00B4L5Y983"
    scrape_chart(isin)
