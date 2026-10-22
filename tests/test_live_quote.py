"""
Tests for `justetf_scraping.live_quote` module.
"""

import datetime
import json
from typing import Iterator

import pytest
import websocket

import justetf_scraping.live_quote
import justetf_scraping.types

INITIAL_QUOTE: justetf_scraping.types.RawQuote = {
    "isin": "test",
    "timestamp": "2026-01-30T00:00:00.000Z",
    "trend": "I",
    "ask": {"raw": 110, "localized": "110"},
    "bid": {"raw": 110, "localized": "110"},
    "mid": {"raw": 110, "localized": "110"},
    "last": {"raw": 110, "localized": "110"},
    "currency": "EUR",
    "dtdDec": {"raw": 0.1, "localized": "0.1"},
    "dtdPrc": {"raw": 10, "localized": "10"},
    "dtdAmt": {"raw": 10, "localized": "10"},
    "spreadAmt": {"raw": 0, "localized": "0"},
    "spreadDec": {"raw": 0, "localized": "0"},
    "spreadPrc": {"raw": 0, "localized": "0"},
    "stockExchange": "gettex",
    "quoteType": "R",
}
DOWN_QUOTE: justetf_scraping.types.RawQuote = {
    "isin": "test",
    "timestamp": "2026-01-30T00:00:00.020Z",
    "trend": "D",
    "ask": {"raw": 90, "localized": "90"},
    "bid": {"raw": 90, "localized": "90"},
    "mid": {"raw": 90, "localized": "90"},
    "last": {"raw": 90, "localized": "90"},
    "currency": "EUR",
    "dtdDec": {"raw": -0.1, "localized": "-0.1"},
    "dtdPrc": {"raw": -10, "localized": "-10"},
    "dtdAmt": {"raw": -10, "localized": "-10"},
    "spreadAmt": {"raw": 0, "localized": "0"},
    "spreadDec": {"raw": 0, "localized": "0"},
    "spreadPrc": {"raw": 0, "localized": "0"},
    "stockExchange": "gettex",
    "quoteType": "R",
}
UP_QUOTE: justetf_scraping.types.RawQuote = {
    "isin": "test",
    "timestamp": "2026-01-30T00:00:00.010Z",
    "trend": "U",
    "ask": {"raw": 120, "localized": "120"},
    "bid": {"raw": 120, "localized": "120"},
    "mid": {"raw": 120, "localized": "120"},
    "last": {"raw": 120, "localized": "120"},
    "currency": "EUR",
    "dtdDec": {"raw": 0.2, "localized": "0.2"},
    "dtdPrc": {"raw": 20, "localized": "20"},
    "dtdAmt": {"raw": 20, "localized": "20"},
    "spreadAmt": {"raw": 0, "localized": "0"},
    "spreadDec": {"raw": 0, "localized": "0"},
    "spreadPrc": {"raw": 0, "localized": "0"},
    "stockExchange": "gettex",
    "quoteType": "R",
}


def _iterate_mocked_raw_live_quote(
    isin: str,
    timeout: float | None = None,
) -> Iterator[justetf_scraping.types.RawQuote]:
    """
    Mocked version of `justetf_scraping.live_quote.iterate_raw_live_quote`.

    Only takes predefined values as ISIN.

    In contrast to the actual function, this iterator is finite
    """
    if isin == "initial":
        yield INITIAL_QUOTE
    elif isin == "down":
        yield DOWN_QUOTE
    elif isin == "up":
        yield UP_QUOTE
    elif isin == "iterable":
        yield from [INITIAL_QUOTE, DOWN_QUOTE, UP_QUOTE]
    else:
        raise ValueError(f"'{isin}' is not predefined for mocked data.")


def test_load_initial_live_quote(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test loading the initial live quote.
    """
    monkeypatch.setattr(
        "justetf_scraping.live_quote.iterate_raw_live_quote",
        _iterate_mocked_raw_live_quote,
    )

    quote = justetf_scraping.live_quote.load_live_quote("initial")
    assert quote.trend is None
    assert quote.timestamp == datetime.datetime(
        2026, 1, 30, tzinfo=datetime.timezone.utc
    )


def test_load_down_live_quote(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test loading the down live quote.
    """
    monkeypatch.setattr(
        "justetf_scraping.live_quote.iterate_raw_live_quote",
        _iterate_mocked_raw_live_quote,
    )

    quote = justetf_scraping.live_quote.load_live_quote("down")
    assert quote.trend == "down"


def test_load_up_live_quote(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test loading the up live quote.
    """
    monkeypatch.setattr(
        "justetf_scraping.live_quote.iterate_raw_live_quote",
        _iterate_mocked_raw_live_quote,
    )

    quote = justetf_scraping.live_quote.load_live_quote("up")
    assert quote.trend == "up"


def test_iterate_live_quote(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test iterating over the live quote.
    """
    monkeypatch.setattr(
        "justetf_scraping.live_quote.iterate_raw_live_quote",
        _iterate_mocked_raw_live_quote,
    )

    quotes = list(justetf_scraping.live_quote.iterate_live_quote("iterable"))
    assert len(quotes) == 3
    assert quotes[0].trend is None
    assert quotes[1].trend == "down"
    assert quotes[2].trend == "up"


class _FakeWebSocket:
    """
    Fake `websocket.WebSocket` sending predefined messages, then timing out.
    """

    def __init__(self, messages: list[justetf_scraping.types.RawQuote]) -> None:
        self.messages = [json.dumps(message) for message in messages]
        self.timeout: float | None = None
        self.closed = False

    def recv(self) -> str:
        """
        Receive the next message, time out if there are no more messages.
        """
        if not self.messages:
            raise websocket.WebSocketTimeoutException("Connection timed out")
        return self.messages.pop(0)

    def settimeout(self, timeout: float | None) -> None:
        """
        Set the receive timeout.
        """
        self.timeout = timeout

    def close(self) -> None:
        """
        Close the connection.
        """
        self.closed = True


def _mock_websocket(
    monkeypatch: pytest.MonkeyPatch, messages: list[justetf_scraping.types.RawQuote]
) -> _FakeWebSocket:
    """
    Mock the websocket connection to send the given messages.
    """
    ws = _FakeWebSocket(messages)

    def create_connection(
        url: str,
        headers: dict[str, str],
        timeout: float | None,
    ) -> _FakeWebSocket:
        ws.settimeout(timeout)
        return ws

    monkeypatch.setattr(
        "justetf_scraping.live_quote.websocket.create_connection", create_connection
    )
    return ws


def test_load_live_quote_closes_connection(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test that loading the live quote closes the connection.
    """
    ws = _mock_websocket(monkeypatch, [INITIAL_QUOTE])

    quote = justetf_scraping.live_quote.load_live_quote("IE00TEST")

    assert quote.isin == INITIAL_QUOTE["isin"]
    assert ws.timeout == justetf_scraping.live_quote.DEFAULT_TIMEOUT
    assert ws.closed


def test_load_live_quote_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test that a missing initial quote raises `TimeoutError`.
    """
    ws = _mock_websocket(monkeypatch, [])

    with pytest.raises(TimeoutError, match="IE00TEST"):
        justetf_scraping.live_quote.load_live_quote("IE00TEST")
    assert ws.closed


def test_iterate_live_quote_waits_for_updates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Test that only the initial quote is awaited with timeout, updates without.
    """
    ws = _mock_websocket(monkeypatch, [INITIAL_QUOTE, DOWN_QUOTE])

    quotes = justetf_scraping.live_quote.iterate_live_quote("IE00TEST", timeout=1.0)

    assert next(quotes).trend is None
    assert ws.timeout == 1.0
    assert next(quotes).trend == "down"
    assert ws.timeout is None
