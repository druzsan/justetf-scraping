"""Regression tests for listings using a table retrieved from justETF."""
from pathlib import Path
from unittest.mock import patch

from bs4 import BeautifulSoup

from justetf_scraping.etf_profile import _parse_listings, get_etf_overview


def fixture_html() -> str:
    """Load the captured Xtrackers listings table."""
    return Path(__file__).with_name('fixtures').joinpath('listings_IE000F354Q61.html').read_text()


def test_overview_listings() -> None:
    """The overview returns actual page listings without another request."""
    with patch('justetf_scraping.etf_profile.requests.Session') as session:
        response = session.return_value.get.return_value
        response.status_code = 200
        response.text = fixture_html()
        result = get_etf_overview('IE000F354Q61', include_gettex=False, expand_allocations=False)
        session.return_value.get.assert_called_once()
    listings = result['listings']
    assert len(listings) == 5
    assert [(x['exchange'], x['currency']) for x in listings] == [
        ('gettex', 'EUR'), ('Borsa Italiana', 'EUR'),
        ('London Stock Exchange', 'USD'), ('Stockholm Stock Exchange', 'SEK'),
        ('XETRA', 'EUR'),
    ]
    assert listings[-1]['ticker'] == 'XSWC'
    assert listings[-1]['reuters'] == 'XSWC.DE'
    assert listings[-1]['bloomberg'] is None
    assert listings[0]['bloomberg'] is None
    assert listings[3]['ticker'] is None


def test_multiple_currencies_and_vendor_codes() -> None:
    """Repeated exchange identifiers must not merge different trading lines."""
    soup = BeautifulSoup(fixture_html(), 'html.parser')
    row = soup.select_one('tr[data-testid="etf-trade-data-panel_row-xlon"]')
    duplicate = BeautifulSoup(str(row), 'html.parser').tr
    duplicate.select_one('[data-testid$="_trade-currency"]').string = 'GBP'
    duplicate.select_one('[data-testid$="_ticker"]').string = 'OTHER'
    duplicate.select_one('[data-testid$="_inav-bloomberg"]').string = 'INAV CODE'
    duplicate.select_one('[data-testid$="_inav-reuters"]').string = 'INAV.RIC'
    duplicate.select_one('[data-testid$="_market-maker"]').decompose()
    soup.tbody.append(duplicate)
    listings = _parse_listings(soup)
    assert len(listings) == 6
    assert listings[2]['currency'] == 'USD'
    assert listings[-1]['currency'] == 'GBP'
    assert listings[-1]['ticker'] == 'OTHER'
    assert listings[-1]['bloomberg'] == 'XSWC LN'
    assert listings[-1]['inav_bloomberg'] == 'INAV CODE'
    assert listings[-1]['inav_reuters'] == 'INAV.RIC'
    assert listings[-1]['market_maker'] is None


def test_missing_table() -> None:
    """Other tables must not be mistaken for listings."""
    assert _parse_listings(BeautifulSoup('<table><tr><td>XETRA</td></tr></table>', 'html.parser')) == []
