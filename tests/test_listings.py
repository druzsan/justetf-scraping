"""
Tests for stock exchange listings parsing in `justetf_scraping.etf_profile`.
"""

from bs4 import BeautifulSoup

from justetf_scraping.etf_profile import _parse_listings

LISTINGS_HTML_WITH_PLACEHOLDERS = """<table data-testid="etf-trade-data-panel_table">
<tr data-testid="etf-trade-data-panel_row-xetr">
  <td data-testid="etf-trade-data-panel_row-xetr_listing">XETRA</td>
  <td data-testid="etf-trade-data-panel_row-xetr_trade-currency">EUR</td>
  <td data-testid="etf-trade-data-panel_row-xetr_ticker">N/A</td>
  <td><span data-testid="etf-trade-data-panel_row-xetr_bloomberg">-</span></td>
</tr>
<tr data-testid="etf-trade-data-panel_row-xlon">
  <td data-testid="etf-trade-data-panel_row-xlon_listing">-</td>
</tr>
</table>"""


def test_parse_listings(etf_profile_html: str) -> None:
    """Test parsing listings from a captured profile page."""
    listings = _parse_listings(BeautifulSoup(etf_profile_html, "html.parser"))

    assert [
        (listing["exchange_code"], listing["exchange"], listing["currency"])
        for listing in listings
    ] == [
        ("MUND", "gettex", "EUR"),
        ("XSTU", "Stuttgart Stock Exchange", "EUR"),
        ("XMEX", "Bolsa Mexicana de Valores", "MXN"),
        ("XMIL", "Borsa Italiana", "EUR"),
        ("XAMS", "Euronext Amsterdam", "EUR"),
        # Multiple currencies on the same exchange are separate listings.
        ("XLON", "London Stock Exchange", "GBX"),
        ("XLON", "London Stock Exchange", "USD"),
        ("XLON", "London Stock Exchange", "GBP"),
        ("XSWX", "SIX Swiss Exchange", "USD"),
        ("XETR", "XETRA", "EUR"),
    ]
    assert listings[-1] == {
        "exchange_code": "XETR",
        "exchange": "XETRA",
        "currency": "EUR",
        "ticker": "EUNL",
        "bloomberg": "EUNL GY",
        "inav_bloomberg": "INAVIWDE",
        "reuters": "EUNL.DE",
        "inav_reuters": "IWDAEUR.DE",
        "market_maker": None,
    }
    # Placeholders ("-") are parsed as missing values.
    assert listings[0]["bloomberg"] is None
    assert listings[2]["ticker"] is None


def test_parse_listings_placeholders() -> None:
    """Test that placeholders and missing cells are parsed as missing values."""
    soup = BeautifulSoup(LISTINGS_HTML_WITH_PLACEHOLDERS, "html.parser")

    # The row without exchange name is skipped.
    assert _parse_listings(soup) == [
        {
            "exchange_code": "XETR",
            "exchange": "XETRA",
            "currency": "EUR",
            "ticker": None,
            "bloomberg": None,
            "inav_bloomberg": None,
            "reuters": None,
            "inav_reuters": None,
            "market_maker": None,
        }
    ]


def test_parse_listings_missing_table() -> None:
    """Test that other tables are not mistaken for listings."""
    soup = BeautifulSoup("<table><tr><td>XETRA</td></tr></table>", "html.parser")
    assert _parse_listings(soup) == []
