"""
Scrape ETF stock exchange listings from justETF
(e.g. https://www.justetf.com/en/etf-profile.html?isin=IE00B4L5Y983#stock-exchange).
"""

import warnings

import pandas as pd
import requests
from lxml import html
from lxml.etree import _Element

from .helpers import USER_AGENT, assert_response_status_ok

BASE_URL = "https://www.justetf.com/en/etf-profile.html"


def find_tables_bottom_up(element: _Element, max_steps: int = 5) -> list[_Element]:
    """
    Find all tables under an HTML element starting from the given element and
    going up until at least one table is found, but no more than given number of
    steps.

    Args:
        element: HTML element to start from.
        max_steps: Maximum steps to go up until giveup.
    """
    assert max_steps >= 0
    for _ in range(max_steps + 1):
        tables = element.xpath(".//table")
        if tables:
            break
        parent_element = element.getparent()
        if parent_element is None:
            break
        element = parent_element
    return tables


def load_listings(isin: str) -> pd.DataFrame:
    """
    Load stock exchange listings for the given ISIN.
    """
    response = requests.get(
        BASE_URL,
        params={"isin": isin},
        headers={"User-Agent": USER_AGENT},
    )
    assert_response_status_ok(response, f"overview-html-isin-{isin}")
    tree = html.fromstring(response.text)

    elements = tree.xpath('//div[@id="stock-exchange"]')
    if not elements:
        raise ValueError("No divs with ID 'stock-exchange' found in the HTML page.")
    if len(elements) > 1:
        warnings.warn(
            f"{len(elements)} divs with ID 'stock-exchange' found in the HTML "
            "page, processing all of them."
        )
    tables = []
    for element in elements:
        tables.extend(find_tables_bottom_up(element))
    if not tables:
        raise ValueError("No listings tables found in the HTML page.")
    if len(tables) > 1:
        warnings.warn(
            f"{len(elements)} listings tables found in the HTML page, "
            "processing the first of them."
        )
    table = tables[0]
    table_dfs = pd.read_html(
        html.tostring(table, encoding="UTF-8", with_tail=False).decode(), flavor="lxml"  # type: ignore[call-overload]
    )
    if len(table_dfs) > 1:
        warnings.warn(
            f"{len(table_dfs)} listings tables parsed from the HTML page, "
            "returning the first of them."
        )
    return table_dfs[0]
