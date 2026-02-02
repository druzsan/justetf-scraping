"""
Scrape ETF profile data from justETF (https://www.justetf.com/en/etf-profile.html).

This module provides functions to:
1. Get real-time gettex quote data via WebSocket
2. Get ETF overview including description, basic data, countries, and sectors
"""

import re
from typing import List, Optional, TypedDict
from xml.etree import ElementTree

import requests
from bs4 import BeautifulSoup

from .types import Quote


# Type definitions
class AllocationItem(TypedDict):
    """
    Allocation item.
    """

    name: str
    percentage: float


class HoldingItem(TypedDict):
    """
    Holding item.
    """

    name: str
    percentage: float
    isin: Optional[str]


class EtfOverview(TypedDict):
    """
    ETF overview.
    """

    isin: str
    name: Optional[str]
    description: Optional[str]
    index: Optional[str]
    investment_focus: Optional[str]
    fund_size_eur: Optional[float]
    ter: Optional[float]
    replication: Optional[str]
    legal_structure: Optional[str]
    strategy_risk: Optional[str]
    sustainability: Optional[bool]
    fund_currency: Optional[str]
    currency_hedged: Optional[bool]
    volatility_1y: Optional[float]
    inception_date: Optional[str]
    distribution_policy: Optional[str]
    distribution_frequency: Optional[str]
    fund_domicile: Optional[str]
    fund_provider: Optional[str]
    top_holdings: List[HoldingItem]
    countries: List[AllocationItem]
    sectors: List[AllocationItem]
    holdings_date: Optional[str]
    gettex: Optional[Quote]


# Constants
BASE_URL = "https://www.justetf.com/en/etf-profile.html"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def _parse_percentage(value: str) -> Optional[float]:
    """Parse percentage string to float (e.g., '59.03%' -> 59.03)."""
    if not value:
        return None
    match = re.search(r"([\d.]+)\s*%", value)
    if match:
        return float(match.group(1))
    return None


def _parse_fund_size(value: str) -> Optional[float]:
    """Parse fund size string to float in millions (e.g., 'EUR 18,588 m' -> 18588.0)."""
    if not value:
        return None
    match = re.search(r"([\d,]+)\s*m", value, re.I)
    if match:
        return float(match.group(1).replace(",", ""))
    return None


def _parse_ter(value: str) -> Optional[float]:
    """Parse TER string to float (e.g., '0.19% p.a.' -> 0.19)."""
    return _parse_percentage(value)


def _parse_date(value: str) -> Optional[str]:
    """Extract date from string (e.g., '22 May 2012' or 'As of 29/10/2025')."""
    if not value:
        return None
    # Try to extract date pattern
    value = value.replace("As of ", "").strip()
    return value


def _fetch_ajax_data(
    session: requests.Session, isin: str, endpoint: str, element_id: str
) -> Optional[str]:
    """
    Fetch expanded data via AJAX request (for countries/sectors load more).

    Args:
        session: requests Session with cookies from main page
        isin: The ISIN of the ETF
        endpoint: The AJAX endpoint path (e.g., 'holdingsSection-countries-loadMoreCountries')
        element_id: The element ID for Wicket (e.g., 'id6')

    Returns:
        HTML content from AJAX response, or None if failed
    """
    ajax_url = f"{BASE_URL}?0-1.0-{endpoint}&isin={isin}&_wicket=1"
    ajax_headers = {
        **DEFAULT_HEADERS,
        "X-Requested-With": "XMLHttpRequest",
        "Wicket-Ajax": "true",
        "Wicket-Ajax-BaseURL": f"en/etf-profile.html?isin={isin}",
        "Accept": "application/xml, text/xml, */*; q=0.01",
        "Referer": f"{BASE_URL}?isin={isin}",
    }

    try:
        resp = session.get(ajax_url, headers=ajax_headers)
        if resp.status_code == 200 and resp.text:
            return resp.text
    except Exception as e:
        print(f"AJAX request error: {e}")

    return None


def _parse_allocation_from_ajax(
    xml_response: str, table_id: str, name_testid: str, pct_testid: str
) -> List[AllocationItem]:
    """
    Parse allocation data (countries/sectors) from AJAX XML response.

    Args:
        xml_response: XML response from AJAX call
        table_id: ID of the table element (e.g., 'id47')
        name_testid: data-testid for name element
        pct_testid: data-testid for percentage element

    Returns:
        List of AllocationItem dictionaries
    """
    allocations = []

    try:
        # Parse XML and extract CDATA content for the table
        root = ElementTree.fromstring(xml_response)
        for component in root.findall(".//component"):
            if component.get("id") == table_id:
                html_content = component.text
                if html_content:
                    soup = BeautifulSoup(html_content, "html.parser")
                    rows = soup.find_all("tr", attrs={"data-testid": True})
                    for row in rows:
                        name_elem = row.find("td", attrs={"data-testid": name_testid})
                        pct_elem = row.find("span", attrs={"data-testid": pct_testid})
                        if name_elem and pct_elem:
                            name = name_elem.get_text(strip=True)
                            pct = _parse_percentage(pct_elem.get_text(strip=True))
                            if name and pct is not None:
                                allocations.append(
                                    AllocationItem(name=name, percentage=pct)
                                )
                break
    except Exception as e:
        print(f"Error parsing allocation data: {e}")

    return allocations


def _parse_allocation_from_soup(
    soup: BeautifulSoup, row_testid: str, name_testid: str, pct_testid: str
) -> List[AllocationItem]:
    """
    Parse allocation data from main page soup (fallback if AJAX fails).
    """
    allocations = []
    rows = soup.find_all("tr", attrs={"data-testid": row_testid})
    for row in rows:
        name_elem = row.find("td", attrs={"data-testid": name_testid})
        pct_elem = row.find("span", attrs={"data-testid": pct_testid})
        if name_elem and pct_elem:
            name = name_elem.get_text(strip=True)
            pct = _parse_percentage(pct_elem.get_text(strip=True))
            if name and pct is not None:
                allocations.append(AllocationItem(name=name, percentage=pct))
    return allocations


def get_etf_overview(
    isin: str, include_gettex: bool = True, expand_allocations: bool = True
) -> EtfOverview:
    """
    Get comprehensive ETF overview data from justETF.

    Args:
        isin: The ISIN of the ETF
        include_gettex: Whether to fetch real-time gettex quote (default: True)
        expand_allocations: Whether to fetch full countries/sectors lists via AJAX (default: True)

    Returns:
        EtfOverview dictionary with all available data
    """
    session = requests.Session()

    # Fetch main page
    url = f"{BASE_URL}?isin={isin}"
    response = session.get(url, headers=DEFAULT_HEADERS)

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch ETF page for {isin}: status {response.status_code}"
        )

    soup = BeautifulSoup(response.text, "html.parser")

    # Parse description
    desc_elem = soup.find(
        "div", attrs={"data-testid": "etf-quote-section_description-label"}
    )
    description = desc_elem.get_text(strip=True) if desc_elem else None

    # Parse name from title
    title_elem = soup.find("title")
    name = None
    if title_elem:
        title_text = title_elem.get_text(strip=True)
        # Format: "ETF Name | WKN | ISIN"
        if "|" in title_text:
            name = title_text.split("|")[0].strip()

    # Parse basic data from table 2
    basic_data = {}
    tables = soup.find_all("table")
    if len(tables) >= 2:
        table = tables[1]
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all(["th", "td"])
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                basic_data[key] = value

    # Parse top 10 holdings
    top_holdings = []
    holdings_rows = soup.find_all(
        "tr", attrs={"data-testid": "etf-holdings_top-holdings_row"}
    )
    for row in holdings_rows:
        name_elem = row.find(
            "a", attrs={"data-testid": "tl_etf-holdings_top-holdings_link_name"}
        )
        pct_elem = row.find(
            "span",
            attrs={"data-testid": "tl_etf-holdings_top-holdings_value_percentage"},
        )
        if name_elem and pct_elem:
            holding_name = name_elem.get_text(strip=True)
            pct = _parse_percentage(pct_elem.get_text(strip=True))
            # Try to extract ISIN from link
            href = name_elem.get("href", "")
            holding_isin = None
            if "/stock-profiles/" in href:
                holding_isin = href.split("/stock-profiles/")[-1]
            if holding_name and pct is not None:
                top_holdings.append(
                    HoldingItem(name=holding_name, percentage=pct, isin=holding_isin)
                )

    # Parse countries
    if expand_allocations:
        # Try AJAX for full list
        countries_xml = _fetch_ajax_data(
            session, isin, "holdingsSection-countries-loadMoreCountries", "id6"
        )
        if countries_xml:
            countries = _parse_allocation_from_ajax(
                countries_xml,
                "id47",
                "tl_etf-holdings_countries_value_name",
                "tl_etf-holdings_countries_value_percentage",
            )
        else:
            countries = _parse_allocation_from_soup(
                soup,
                "etf-holdings_countries_row",
                "tl_etf-holdings_countries_value_name",
                "tl_etf-holdings_countries_value_percentage",
            )
    else:
        countries = _parse_allocation_from_soup(
            soup,
            "etf-holdings_countries_row",
            "tl_etf-holdings_countries_value_name",
            "tl_etf-holdings_countries_value_percentage",
        )

    # Parse sectors
    if expand_allocations:
        # Try AJAX for full list
        sectors_xml = _fetch_ajax_data(
            session, isin, "holdingsSection-sectors-loadMoreSectors", "id7"
        )
        if sectors_xml:
            sectors = _parse_allocation_from_ajax(
                sectors_xml,
                "id48",
                "tl_etf-holdings_sectors_value_name",
                "tl_etf-holdings_sectors_value_percentage",
            )
        else:
            sectors = _parse_allocation_from_soup(
                soup,
                "etf-holdings_sectors_row",
                "tl_etf-holdings_sectors_value_name",
                "tl_etf-holdings_sectors_value_percentage",
            )
    else:
        sectors = _parse_allocation_from_soup(
            soup,
            "etf-holdings_sectors_row",
            "tl_etf-holdings_sectors_value_name",
            "tl_etf-holdings_sectors_value_percentage",
        )

    # Parse holdings date
    ref_date_elem = soup.find(
        "div", attrs={"data-testid": "tl_etf-holdings_reference-date"}
    )
    holdings_date = (
        _parse_date(ref_date_elem.get_text(strip=True)) if ref_date_elem else None
    )

    # Get gettex quote
    gettex = None
    if include_gettex:
        gettex = get_gettex_quote(isin)

    # Build result
    return EtfOverview(
        isin=isin,
        name=name,
        description=description,
        index=basic_data.get("Index"),
        investment_focus=basic_data.get("Investment focus"),
        fund_size_eur=_parse_fund_size(basic_data.get("Fund size")),
        ter=_parse_ter(basic_data.get("Total expense ratio")),
        replication=basic_data.get("Replication"),
        legal_structure=basic_data.get("Legal structure"),
        strategy_risk=basic_data.get("Strategy risk"),
        sustainability=basic_data.get("Sustainability", "").lower() == "yes",
        fund_currency=basic_data.get("Fund currency"),
        currency_hedged=basic_data.get("Currency risk", "").lower()
        != "currency unhedged",
        volatility_1y=_parse_percentage(basic_data.get("Volatility 1 year (in EUR)")),
        inception_date=basic_data.get("Inception/ Listing Date"),
        distribution_policy=basic_data.get("Distribution policy"),
        distribution_frequency=basic_data.get("Distribution frequency"),
        fund_domicile=basic_data.get("Fund domicile"),
        fund_provider=basic_data.get("Fund Provider"),
        top_holdings=top_holdings,
        countries=countries,
        sectors=sectors,
        holdings_date=holdings_date,
        gettex=gettex,
    )


if __name__ == "__main__":
    # Test with VGWL
    import pprint

    isin = "IE00B3RBWM25"
    print(f"Fetching ETF overview for {isin}...")

    overview = get_etf_overview(isin)

    print("\n" + "=" * 60)
    print("ETF OVERVIEW")
    print("=" * 60)
    pprint.pprint(dict(overview), width=100)
