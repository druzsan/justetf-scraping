"""
Common constants and functions used in package.
"""

import requests

from .types import AssetClass, Exchange, Instrument, Region, Strategy

# justETF seems to block default requests' user agent, so define a custom one
USER_AGENT = "My User Agent 1.0"

STRATEGIES: dict[Strategy, str] = {
    "epg-longOnly": "Long-only",
    "epg-activeEtfs": "Active",
    "epg-shortAndLeveraged": "Short & Leveraged",
}
ASSET_CLASSES: dict[AssetClass, str] = {
    "class-equity": "Equity",
    "class-bonds": "Bonds",
    "class-preciousMetals": "Precious Metals",
    "class-commodities": "Commodities",
    "class-currency": "Cryptocurrencies",
    "class-realEstate": "Real Estate",
    "class-moneyMarket": "Money Market",
}
REGIONS: dict[Region, str] = {
    "Africa": "Africa",
    "Asia%2BPacific": "Asia & Pacific",
    "Eastern%2BEurope": "Eastern Europe",
    "Emerging%2BMarkets": "Emerging Markets",
    "Europe": "Europe",
    "Latin%2BAmerica": "Latin America",
    "North%2BAmerica": "North America",
    "World": "World",
}
EXCHANGES: dict[Exchange, str] = {
    "MUND": "gettex",
    "XETR": "XETRA",
    "XLON": "London",
    "XPAR": "Euronext Paris",
    "XSTU": "Stuttgart",
    "XSWX": "SIX Swiss Exchange",
    "XMIL": "Borsa Italiana",
    "XAMS": "Euronext Amsterdam",
    "XBRU": "Euronext Brussels",
}
INSTRUMENTS: dict[Instrument, str] = {
    "ETC": "ETC",
    "ETF": "ETF",
    "ETN": "ETN",
}


def assert_response_status_ok(
    response: requests.Response, name: str | None = None
) -> None:
    """
    Check response status code, fail and save error page if not equal to 200.

    Args:
        response: Response to check.
        name: Optional name to use in error page file name and error message.
    """
    if response.status_code != requests.codes.ok:
        message = f"Got status {response.status_code}"
        if name:
            message += f" when requesting {name}"
            filepath = f"{name}-error-page.html"
        else:
            filepath = "error-page.html"
        message += f".\nError page saved to '{filepath}'."

        with open(filepath, "w") as file:
            file.write(response.text)
        raise RuntimeError(message)
