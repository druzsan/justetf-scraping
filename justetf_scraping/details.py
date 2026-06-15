"""
Scrape ETF stock exchange listings from justETF
(e.g. https://www.justetf.com/en/etf-profile.html?isin=IE00B4L5Y983).
"""

import re
import warnings
from typing import Any

import lxml.html
import requests

from .helpers import USER_AGENT, assert_response_status_ok

BASE_URL = "https://www.justetf.com/en/etf-profile.html"


def _parse_text_from_element(
    tree: lxml.html.HtmlElement, data_testid: str
) -> str | None:
    nodes = tree.xpath(f'//*[@data-testid="{data_testid}"]')
    if not nodes:
        return None
    if len(nodes) > 1:
        warnings.warn(
            f'{len(nodes)} elements with data-testid="{data_testid}" found in '
            "the HTML page, using the first one.",
            stacklevel=2,
        )
    return nodes[0].text_content().strip()


def _parse_ter(tree: lxml.html.HtmlElement) -> float | None:
    ter_text = _parse_text_from_element(tree, "etf-profile-header_ter-value")
    if ter_text:
        match = re.match(r"^([-+]?\d*\.\d+|\d+)", ter_text)
        if match:
            ter_value: str = match.group(0)
            try:
                return float(ter_value)
            except Exception:
                return None
    return None


def _parse_investment_focus(tree: lxml.html.HtmlElement) -> list[str]:
    investment_focus_text = _parse_text_from_element(
        tree, "tl_etf-basics_value_investment-focus"
    )
    return investment_focus_text.split(", ") if investment_focus_text else []


def load_details(isin: str) -> Any:
    """
    Load stock exchange listings for the given ISIN.
    """
    response = requests.get(
        BASE_URL,
        params={"isin": isin},
        headers={"User-Agent": USER_AGENT},
    )
    assert_response_status_ok(response, f"overview-html-isin-{isin}")
    tree: lxml.html.HtmlElement = lxml.html.fromstring(response.text)

    name = _parse_text_from_element(tree, "etf-profile-header_etf-name")
    isin_ = _parse_text_from_element(tree, "etf-profile-header_isin-value")
    wkr = _parse_text_from_element(tree, "etf-profile-header_identifier-value-wkn")
    ticker = _parse_text_from_element(
        tree, "etf-profile-header_identifier-value-ticker"
    )
    ter = _parse_ter(tree)
    dividends = _parse_text_from_element(
        tree, "etf-profile-header_distribution-policy-value"
    )
    replication = _parse_text_from_element(tree, "etf-profile-header_replication-value")
    size = _parse_text_from_element(tree, "etf-profile-header_fund-size-value-wrapper")
    inception_date = _parse_text_from_element(
        tree, "etf-profile-header_inception-date-value"
    )
    holdings = _parse_text_from_element(tree, "etf-profile-header_holdings-value")

    description = _parse_text_from_element(tree, "etf-quote-section_description-label")
    summary = _parse_text_from_element(tree, "etf-quote-section_summary-text")

    index = _parse_text_from_element(tree, "tl_etf-basics_value_index-name")
    investment_focus = _parse_investment_focus(tree)
    ter_text = _parse_text_from_element(tree, "tl_etf-basics_value_ter")

    from pathlib import Path

    Path(f"overview-html-isin-{isin}.html").write_text(response.text)
