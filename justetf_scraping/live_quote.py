"""
Scrape live ETF quote data from justETF.
"""

import json
from contextlib import closing
from typing import Iterator

import websocket

from .helpers import USER_AGENT
from .types import Quote, RawQuote, parse_quote

WEBSOCKET_URL = "wss://api.mobile.stock-data-subscriptions.justetf.com/?subscription=trend&parameters=isins:{isin}/currency:EUR/language:en"


def iterate_raw_live_quote(isin: str) -> Iterator[RawQuote]:
    """
    Iterate over the live raw quote for the given ISIN. Updates are
    received automatically and their frequency cannot be controlled, also no
    updates besides the initial quote will be received outside of trade hours.

    For now, only EUR currency and gettex stock exchange are supported.

    Args:
        isin: The ISIN of the ETF.

    Yields:
        Raw live quote updates as `RawQuote`.
    """
    with closing(
        websocket.create_connection(
            WEBSOCKET_URL.format(isin=isin),
            headers={"User-Agent": USER_AGENT, "Origin": "https://www.justetf.com"},
        )
    ) as ws:
        while True:
            data = ws.recv()
            yield json.loads(data)


def iterate_live_quote(isin: str) -> Iterator[Quote]:
    """
    Iterate over the live quote for the given ISIN. Updates are
    received automatically and their frequency cannot be controlled, also no
    updates besides the initial quote will be received outside of trade hours.

    For now, only EUR currency and gettex stock exchange are supported.

    Args:
        isin: The ISIN of the ETF.

    Yields:
        Live quote updates as `Quote`.
    """
    return map(parse_quote, iterate_raw_live_quote(isin))


def load_raw_live_quote(isin: str) -> RawQuote:
    """
    Load the last live raw quote for the given ISIN.

    For now, only EUR currency and gettex stock exchange are supported.

    Args:
        isin: The ISIN of the ETF.

    Returns:
        Raw live quote as `RawQuote`.
    """
    return next(iterate_raw_live_quote(isin))


def load_live_quote(isin: str) -> Quote:
    """
    Load the live quote for the given ISIN.

    For now, only EUR currency and gettex stock exchange are supported.

    Args:
        isin: The ISIN of the ETF.

    Returns:
        Live quote as `Quote`.
    """
    return next(iterate_live_quote(isin))
