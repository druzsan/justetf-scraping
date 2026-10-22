"""
Scrape live ETF quote data from justETF.
"""

import json
from contextlib import closing
from typing import Generator, Iterator

import websocket

from .helpers import USER_AGENT
from .types import Quote, RawQuote, parse_quote

WEBSOCKET_URL = "wss://api.mobile.stock-data-subscriptions.justetf.com/?subscription=trend&parameters=isins:{isin}/currency:EUR/language:en"
# The initial quote usually comes in under a second. If it does not come at
# all, the ETF most likely has no gettex quotes.
DEFAULT_TIMEOUT = 10.0


def iterate_raw_live_quote(
    isin: str, timeout: float | None = DEFAULT_TIMEOUT
) -> Generator[RawQuote, None, None]:
    """
    Iterate over the live raw quote for the given ISIN. Updates are
    received automatically and their frequency cannot be controlled, also no
    updates besides the initial quote will be received outside of trade hours.

    For now, only EUR currency and gettex stock exchange are supported.

    Args:
        isin: The ISIN of the ETF.
        timeout: Timeout in seconds for connecting and receiving the initial
            quote. Updates are awaited without timeout. If `None`, wait forever.

    Yields:
        Raw live quote updates as `RawQuote`.

    Raises:
        TimeoutError: If the initial quote is not received in time, e.g.
            because the ETF has no gettex quotes.
    """
    try:
        ws = websocket.create_connection(
            WEBSOCKET_URL.format(isin=isin),
            headers={"User-Agent": USER_AGENT, "Origin": "https://www.justetf.com"},
            timeout=timeout,
        )
    except websocket.WebSocketTimeoutException as e:
        raise TimeoutError(f"Connecting for {isin} live quote timed out.") from e
    with closing(ws):
        try:
            data = ws.recv()
        except websocket.WebSocketTimeoutException as e:
            raise TimeoutError(
                f"No live quote for {isin} received within {timeout} seconds, "
                f"the ETF probably has no gettex quotes."
            ) from e
        yield json.loads(data)
        # Updates can be minutes or hours apart, e.g. outside of trade hours.
        ws.settimeout(None)
        while True:
            yield json.loads(ws.recv())


def iterate_live_quote(
    isin: str, timeout: float | None = DEFAULT_TIMEOUT
) -> Iterator[Quote]:
    """
    Iterate over the live quote for the given ISIN. Updates are
    received automatically and their frequency cannot be controlled, also no
    updates besides the initial quote will be received outside of trade hours.

    For now, only EUR currency and gettex stock exchange are supported.

    Args:
        isin: The ISIN of the ETF.
        timeout: Timeout in seconds for connecting and receiving the initial
            quote. Updates are awaited without timeout. If `None`, wait forever.

    Yields:
        Live quote updates as `Quote`.

    Raises:
        TimeoutError: If the initial quote is not received in time, e.g.
            because the ETF has no gettex quotes.
    """
    return map(parse_quote, iterate_raw_live_quote(isin, timeout))


def load_raw_live_quote(isin: str, timeout: float | None = DEFAULT_TIMEOUT) -> RawQuote:
    """
    Load the last live raw quote for the given ISIN.

    For now, only EUR currency and gettex stock exchange are supported.

    Args:
        isin: The ISIN of the ETF.
        timeout: Timeout in seconds for connecting and receiving the quote. If
            `None`, wait forever.

    Returns:
        Raw live quote as `RawQuote`.

    Raises:
        TimeoutError: If the quote is not received in time, e.g. because the
            ETF has no gettex quotes.
    """
    # Close the connection right away instead of waiting for garbage collection.
    with closing(iterate_raw_live_quote(isin, timeout)) as quotes:
        return next(quotes)


def load_live_quote(isin: str, timeout: float | None = DEFAULT_TIMEOUT) -> Quote:
    """
    Load the live quote for the given ISIN.

    For now, only EUR currency and gettex stock exchange are supported.

    Args:
        isin: The ISIN of the ETF.
        timeout: Timeout in seconds for connecting and receiving the quote. If
            `None`, wait forever.

    Returns:
        Live quote as `Quote`.

    Raises:
        TimeoutError: If the quote is not received in time, e.g. because the
            ETF has no gettex quotes.
    """
    return parse_quote(load_raw_live_quote(isin, timeout))
