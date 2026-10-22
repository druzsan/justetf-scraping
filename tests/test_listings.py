"""
Tests for stock exchange listings parsing in `justetf_scraping.etf_profile`.
"""

import copy
from pathlib import Path
from unittest.mock import patch

from bs4 import BeautifulSoup, Tag

from justetf_scraping.etf_profile import _parse_listings, get_etf_overview

# Listings table captured from https://www.justetf.com/en/etf-profile.html?isin=IE000F354Q61
LISTINGS_HTML = (
    Path(__file__).parent / "fixtures" / "listings_IE000F354Q61.html"
).read_text()


def _select_one(tag: Tag, selector: str) -> Tag:
    """
    Select exactly one element, fail if it is missing.
    """
    element = tag.select_one(selector)
    assert element is not None, f"No element matches '{selector}'."
    return element


def test_overview_listings() -> None:
    """Test that listings are parsed from the profile page without extra requests."""
    with patch("justetf_scraping.etf_profile.requests.Session") as mock_session_cls:
        mock_session = mock_session_cls.return_value
        mock_response = mock_session.get.return_value
        mock_response.status_code = 200
        mock_response.text = LISTINGS_HTML

        result = get_etf_overview(
            "IE000F354Q61", include_gettex=False, expand_allocations=False
        )

        mock_session.get.assert_called_once()

    listings = result["listings"]
    assert [
        (listing["exchange_code"], listing["exchange"], listing["currency"])
        for listing in listings
    ] == [
        ("MUND", "gettex", "EUR"),
        ("XMIL", "Borsa Italiana", "EUR"),
        ("XLON", "London Stock Exchange", "USD"),
        ("XSTO", "Stockholm Stock Exchange", "SEK"),
        ("XETR", "XETRA", "EUR"),
    ]
    assert listings[-1] == {
        "exchange_code": "XETR",
        "exchange": "XETRA",
        "currency": "EUR",
        "ticker": "XSWC",
        "bloomberg": None,
        "inav_bloomberg": None,
        "reuters": "XSWC.DE",
        "inav_reuters": None,
        "market_maker": None,
    }
    # Placeholders ("-") are parsed as missing values.
    assert listings[0]["bloomberg"] is None
    assert listings[3]["ticker"] is None


def test_multiple_currencies_and_vendor_codes() -> None:
    """Test that repeated exchange codes do not merge different listings."""
    soup = BeautifulSoup(LISTINGS_HTML, "html.parser")
    row = _select_one(soup, 'tr[data-testid="etf-trade-data-panel_row-xlon"]')
    duplicate = copy.copy(row)
    _select_one(duplicate, '[data-testid$="_trade-currency"]').string = "GBP"
    _select_one(duplicate, '[data-testid$="_ticker"]').string = "OTHER"
    _select_one(duplicate, '[data-testid$="_inav-bloomberg"]').string = "INAV CODE"
    _select_one(duplicate, '[data-testid$="_inav-reuters"]').string = "INAV.RIC"
    _select_one(duplicate, '[data-testid$="_market-maker"]').string = "N/A"
    _select_one(soup, "tbody").append(duplicate)

    listings = _parse_listings(soup)

    assert len(listings) == 6
    assert listings[2]["currency"] == "USD"
    assert listings[-1] == {
        "exchange_code": "XLON",
        "exchange": "London Stock Exchange",
        "currency": "GBP",
        "ticker": "OTHER",
        "bloomberg": "XSWC LN",
        "inav_bloomberg": "INAV CODE",
        "reuters": "XSWC.L",
        "inav_reuters": "INAV.RIC",
        "market_maker": None,
    }


def test_missing_listings_table() -> None:
    """Test that other tables are not mistaken for listings."""
    soup = BeautifulSoup("<table><tr><td>XETRA</td></tr></table>", "html.parser")
    assert _parse_listings(soup) == []
