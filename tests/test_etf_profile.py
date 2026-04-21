"""
Tests for `justetf_scraping.etf_profile` module.
"""

from unittest.mock import patch

from justetf_scraping.etf_profile import (
    _parse_allocation_from_ajax,
    _parse_percentage,
    get_etf_overview,
)

# --- Test helpers ---


def test_parse_percentage_valid() -> None:
    """Test parsing valid percentage strings."""
    assert _parse_percentage("59.03%") == 59.03
    assert _parse_percentage("0.19% p.a.") == 0.19
    assert _parse_percentage("100%") == 100.0


def test_parse_percentage_invalid() -> None:
    """Test parsing invalid or empty percentage strings."""
    assert _parse_percentage("") is None
    assert _parse_percentage("no percent here") is None


# --- Bug 1: get_gettex_quote NameError ---


def test_include_gettex_uses_load_live_quote() -> None:
    """Test that include_gettex=True calls load_live_quote, not get_gettex_quote."""
    # Mock the session/request to avoid real HTTP calls
    mock_quote = object()

    with (
        patch("justetf_scraping.etf_profile.requests.Session") as mock_session_cls,
        patch("justetf_scraping.etf_profile.load_live_quote", return_value=mock_quote) as mock_llq,
    ):
        mock_session = mock_session_cls.return_value
        # Return a minimal valid HTML page
        mock_response = mock_session.get.return_value
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test ETF | WKN | IE00TEST</title></head><body></body></html>"

        result = get_etf_overview("IE00TEST", include_gettex=True, expand_allocations=False)

        mock_llq.assert_called_once_with("IE00TEST")
        assert result["gettex"] is mock_quote


def test_include_gettex_false_skips_quote() -> None:
    """Test that include_gettex=False does not call load_live_quote."""
    with (
        patch("justetf_scraping.etf_profile.requests.Session") as mock_session_cls,
        patch("justetf_scraping.etf_profile.load_live_quote") as mock_llq,
    ):
        mock_session = mock_session_cls.return_value
        mock_response = mock_session.get.return_value
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test ETF | WKN | IE00TEST</title></head><body></body></html>"

        result = get_etf_overview("IE00TEST", include_gettex=False, expand_allocations=False)

        mock_llq.assert_not_called()
        assert result["gettex"] is None


# --- Bug 2: AJAX allocation parsing with dynamic Wicket IDs ---

# Simulate a real AJAX XML response with a dynamic element ID (id46 instead of id47)
COUNTRIES_AJAX_XML = """<?xml version="1.0" encoding="UTF-8"?>
<ajax-response>
<component id="id46" encoding="wicket1"><![CDATA[
<table data-testid="etf-holdings_countries_table">
<tr data-testid="etf-holdings_countries_row">
  <td data-testid="tl_etf-holdings_countries_value_name">United States</td>
  <td><span data-testid="tl_etf-holdings_countries_value_percentage">59.03%</span></td>
</tr>
<tr data-testid="etf-holdings_countries_row">
  <td data-testid="tl_etf-holdings_countries_value_name">Japan</td>
  <td><span data-testid="tl_etf-holdings_countries_value_percentage">6.12%</span></td>
</tr>
<tr data-testid="etf-holdings_countries_row">
  <td data-testid="tl_etf-holdings_countries_value_name">United Kingdom</td>
  <td><span data-testid="tl_etf-holdings_countries_value_percentage">3.85%</span></td>
</tr>
</table>
]]></component>
</ajax-response>"""

SECTORS_AJAX_XML = """<?xml version="1.0" encoding="UTF-8"?>
<ajax-response>
<component id="id99" encoding="wicket1"><![CDATA[
<table data-testid="etf-holdings_sectors_table">
<tr data-testid="etf-holdings_sectors_row">
  <td data-testid="tl_etf-holdings_sectors_value_name">Technology</td>
  <td><span data-testid="tl_etf-holdings_sectors_value_percentage">23.45%</span></td>
</tr>
<tr data-testid="etf-holdings_sectors_row">
  <td data-testid="tl_etf-holdings_sectors_value_name">Financials</td>
  <td><span data-testid="tl_etf-holdings_sectors_value_percentage">15.67%</span></td>
</tr>
</table>
]]></component>
</ajax-response>"""


def test_parse_countries_from_ajax_with_dynamic_id() -> None:
    """Test that AJAX parsing works regardless of the Wicket element ID."""
    countries = _parse_allocation_from_ajax(
        COUNTRIES_AJAX_XML,
        "etf-holdings_countries_table",
        "tl_etf-holdings_countries_value_name",
        "tl_etf-holdings_countries_value_percentage",
    )

    assert len(countries) == 3
    assert countries[0]["name"] == "United States"
    assert countries[0]["percentage"] == 59.03
    assert countries[1]["name"] == "Japan"
    assert countries[1]["percentage"] == 6.12
    assert countries[2]["name"] == "United Kingdom"
    assert countries[2]["percentage"] == 3.85


def test_parse_sectors_from_ajax_with_dynamic_id() -> None:
    """Test that sector AJAX parsing works regardless of the Wicket element ID."""
    sectors = _parse_allocation_from_ajax(
        SECTORS_AJAX_XML,
        "etf-holdings_sectors_table",
        "tl_etf-holdings_sectors_value_name",
        "tl_etf-holdings_sectors_value_percentage",
    )

    assert len(sectors) == 2
    assert sectors[0]["name"] == "Technology"
    assert sectors[0]["percentage"] == 23.45
    assert sectors[1]["name"] == "Financials"
    assert sectors[1]["percentage"] == 15.67


def test_parse_ajax_no_matching_testid() -> None:
    """Test that AJAX parsing returns empty list when no matching data-testid is found."""
    result = _parse_allocation_from_ajax(
        COUNTRIES_AJAX_XML,
        "etf-holdings_nonexistent_table",
        "tl_etf-holdings_countries_value_name",
        "tl_etf-holdings_countries_value_percentage",
    )
    assert result == []


def test_parse_ajax_multiple_components() -> None:
    """Test AJAX parsing when response contains multiple components."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<ajax-response>
<component id="id10" encoding="wicket1"><![CDATA[
<div>Some other content</div>
]]></component>
<component id="id20" encoding="wicket1"><![CDATA[
<table data-testid="etf-holdings_countries_table">
<tr data-testid="row">
  <td data-testid="tl_etf-holdings_countries_value_name">France</td>
  <td><span data-testid="tl_etf-holdings_countries_value_percentage">2.50%</span></td>
</tr>
</table>
]]></component>
</ajax-response>"""

    countries = _parse_allocation_from_ajax(
        xml,
        "etf-holdings_countries_table",
        "tl_etf-holdings_countries_value_name",
        "tl_etf-holdings_countries_value_percentage",
    )

    assert len(countries) == 1
    assert countries[0]["name"] == "France"
    assert countries[0]["percentage"] == 2.50


def test_parse_ajax_invalid_xml() -> None:
    """Test that AJAX parsing handles invalid XML gracefully."""
    result = _parse_allocation_from_ajax(
        "this is not xml",
        "etf-holdings_countries_table",
        "tl_etf-holdings_countries_value_name",
        "tl_etf-holdings_countries_value_percentage",
    )
    assert result == []
