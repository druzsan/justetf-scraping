"""
Helpers for parsing chart data from AJAX responses.

All *right* XML responses have tag "header-contribution", whose data is XML
again and it has tag "script", whose data is JavaScript code with one of the
following contents:
    `<...>, series: [{<chart object>}, <...>], <...>` (default response)
    `<...>.addSeries({<chart object>}, <...>); <...>` (custom response)
    `<...>.get('<isin>').setData([<chart data>], <...>); <...>`
        (custom volatility response, currently not parsed)

Chart object has the following structure:
    `{id: '<isin>', type: '<type>', name: '<name>', color: '<color>', data: [<chart data>], <...>}`

Chart data has the following structure:
    `[[Date.UTC(<year>,<month>,<day>),<value>],<...>]`
with months from 0..1 and days from 1..31.

Dividends enabling responses also provide the following information in the
"script" tag:
    `<...>.get('onAxe').setData([{<dividends object>}, <...>], <...>); <...>`

Dividends object has the following structure:
    `{ x: Date.UTC(<year>,<month>,<day>), events: {click: function() {  }}, title: 'D', text: 'Dividend <currency> <value>', id: ''}`
"""
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, fields
from typing import List, Literal, Optional, Tuple, Union, overload

import pandas as pd


# Not compiled patterns
FLOAT_PATTERN = r"([-+]?[0-9]*\.?[0-9]+)"
JS_DATE_PATTERN = r"Date.UTC\((\d{4}),(\d{1,2}),(\d{1,2})[,\d]*\)"
# Pre-compiled patterns
SPACE_PATTERN = re.compile(r"\s")
META_FIELDS_PATTERN = re.compile(r"(\w+)\s*:\s*'([^']*)'")
DATA_KEY_PATTERN = re.compile(r"data\s*:\s*\[")
DATA_SAMPLE_PATTERN = re.compile(rf"\[{JS_DATE_PATTERN},{FLOAT_PATTERN}\]")
DIVIDEND_SAMPLE_PATTERN = re.compile(rf"\{{(?=.*?x\s*:\s*{JS_DATE_PATTERN})(?=.*?text\s*:\s*'Dividend[\w ]* {FLOAT_PATTERN}').*?\}}")


ParsingTarget = Literal["charts", "dividends"]


def _patch_js_date(year: str, month: str, day: str) -> str:
    """
    Patch months from 0..11 to 1..12 and merge date.
    """
    return f"{year}-{str(int(month) + 1)}-{day}"


@dataclass
class Chart:
    """
    A Chart object. Has only fields which are always present, ignores the other.
    """
    id: str
    type: str
    name: str
    color: str
    data: pd.Series

    @classmethod
    def fromstring(cls, text: str) -> "Chart":
        keys = [field.name for field in fields(cls)]
        meta_data = dict(META_FIELDS_PATTERN.findall(text))
        meta_data = {key: value for key, value in meta_data.items() if key in keys}
        match = DATA_KEY_PATTERN.search(text)
        if match is None:
            raise ValueError("No data field found in the string.")
        _, end, data_text = parse_brackets(text[match.end() - 1 :], "[")
        if end == -1:
            raise ValueError("No data array found in the string.")
        data = cls.parse_data(data_text)
        return cls(**meta_data, data=data)

    @staticmethod
    def parse_data(text: str) -> pd.Series:
        matches = DATA_SAMPLE_PATTERN.findall(text)
        if not matches:
            raise ValueError("No data samples found in the string.")
        *ymds, values = zip(*matches)

        dates = [_patch_js_date(*ymd) for ymd in zip(*ymds)]
        data = pd.Series(
            values, index=pd.to_datetime(dates, format="%Y-%m-%d"), dtype=float
        )
        return data


def parse_brackets(
    text: str, bracket: str, closing_bracket: Optional[str] = None
) -> Tuple[int, int, str]:
    """

    Returns:
        start: Position of the opening bracket: 0 if bracket is found at the
            first position, -1 otherwise.
        end: Position of the closing bracket, -1 otherwise.
        content: Text *between* brackets if found, empty string otherwise.
    """
    if len(text) == 0:
        return -1, -1, ""
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
            end = i + 2
            text = text[:i]
            break
    return 0, end, text


def parse_charts(text: str) -> Tuple[List[Chart], int]:
    text = text.lstrip()
    if len(text) == 0:
        return [], 0
    char = text[0]
    if char == "{":
        _, end, subtext = parse_brackets(text, char)
        if end != -1:
            # Parse an object.
            try:
                return [Chart.fromstring(subtext)], end
            except (TypeError, ValueError):
                ...
    elif char == "(":
        _, end, subtext = parse_brackets(text, char)
        if end != -1:
            # Parse content of a function.
            return parse_charts(subtext)
    elif char == "[":
        start, end, subtext = parse_brackets(text, char)
        if end != -1:
            # Parse an array.
            all_charts = []
            while True:
                charts, offset = parse_charts(subtext[start:])
                all_charts.extend(charts)
                start += offset
                if len(subtext[start:]) == 0 or subtext[start] != ",":
                    break
                start += 1
            return all_charts, start
    return [], 0


def parse_dividends(text: str) -> Tuple[List[pd.Series], int]:
    _, end, text = parse_brackets(text, "(")
    if end == -1:
        return [], 0
    _, offset, text = parse_brackets(text, "[")
    if offset == -1:
        return [], 0

    matches = DIVIDEND_SAMPLE_PATTERN.findall(text)
    if not matches:
        return [], 0
    *ymds, values = zip(*matches)

    dates = [_patch_js_date(*ymd) for ymd in zip(*ymds)]
    data = pd.Series(
        values, index=pd.to_datetime(dates, format="%Y-%m-%d"), dtype=float
    )
    return [data], offset + 1


@overload
def parse_js(text: str, target: Literal["charts"]) -> List[Chart]:
    ...


@overload
def parse_js(text: str, target: Literal["dividends"]) -> List[pd.Series]:
    ...


def parse_js(text: str, target: ParsingTarget) -> Union[List[Chart], List[pd.Series]]:
    """
    Parse a script block, extract either all charts or all dividends, depending
    on the `target` parameter.
    """
    prefixes = []
    parse_fn = None
    if target == "charts":
        prefixes.extend(("series:", "addSeries"))
        parse_fn = parse_charts
    elif target == "dividends":
        prefixes.append(".get('onAxe').setData")
        parse_fn = parse_dividends

    text = SPACE_PATTERN.sub(" ", text)
    all_data = []
    for prefix in prefixes:
        start = 0
        while True:
            start = text.find(prefix, start)
            if start == -1:
                break
            start += len(prefix)
            data, offset = parse_fn(text[start:])
            all_data.extend(data)
            start += offset
    return all_data


@overload
def parse_xml(text: str, target: Literal["charts"]) -> List[Chart]:
    ...


@overload
def parse_xml(text: str, target: Literal["dividends"]) -> List[pd.Series]:
    ...


def parse_xml(text: str, target: ParsingTarget) -> Union[List[Chart], List[pd.Series]]:
    """
    Parse a XML response, extract either all charts or all dividends, depending
    on the `target` parameter.
    """
    all_data = []
    root = ET.fromstring(text)
    for header_contribution in root.findall("header-contribution"):
        if header_contribution.text is not None:
            inner_root = ET.fromstring(header_contribution.text)
            for script in inner_root.findall("script"):
                if script.text is not None:
                    data = parse_js(script.text, target)
                    all_data.extend(data)
    return all_data


def filter_charts(charts: List[Chart], **kwargs: str) -> Optional[Chart]:
    for chart in charts:
        if len(chart.data) and all(
            getattr(chart, key, None) == value for key, value in kwargs.items()
        ):
            return chart
    return None
