"""
Common types used in package.
"""

import dataclasses
import datetime
import warnings
from typing import Literal, TypedDict

# Global settings for all return data.
Language = Literal["en", "de", "fr", "it", "es"]
Country = Literal["DE", "AT", "CH", "GB", "IT", "FR", "ES", "NL", "BE"]
Universe = Literal["private", "institutional"]
Currency = Literal["EUR", "USD", "CHF", "GBP"]

# Some settings for filtering data.
Strategy = Literal["epg-longOnly", "epg-activeEtfs", "epg-shortAndLeveraged"]
AssetClass = Literal[
    "class-equity",
    "class-bonds",
    "class-preciousMetals",
    "class-commodities",
    "class-currency",
    "class-realEstate",
    "class-moneyMarket",
]
Region = Literal[
    "Africa",
    "Asia%2BPacific",
    "Eastern%2BEurope",
    "Emerging%2BMarkets",
    "Europe",
    "Latin%2BAmerica",
    "North%2BAmerica",
    "World",
]
Exchange = Literal[
    "MUND", "XETR", "XLON", "XPAR", "XSTU", "XSWX", "XMIL", "XAMS", "XBRU"
]
Instrument = Literal["ETC", "ETF", "ETN"]


class RawValue(TypedDict):
    """
    A raw value.
    """

    raw: float
    localized: str


class RawSeriesItem(TypedDict):
    """
    Raw series item.
    """

    date: str
    value: RawValue


class RawChart(TypedDict):
    """
    Raw chart data.
    """

    latestQuote: RawValue
    latestQuoteDate: str
    price: RawValue
    performance: RawValue
    prevDaySeries: list[RawSeriesItem]
    series: list[RawSeriesItem]
    latestDate: str
    endOfDay: str
    features: dict[str, list[RawSeriesItem]]


# "I" for initial quote, "D" for down, "U" for up.
RawQuoteTrend = Literal["I", "D", "U"]


class RawQuote(TypedDict):
    """
    A raw ETF quote.
    """

    isin: str
    timestamp: str
    trend: RawQuoteTrend
    ask: RawValue
    bid: RawValue
    mid: RawValue
    last: RawValue
    currency: str
    dtdDec: RawValue
    dtdPrc: RawValue
    dtdAmt: RawValue
    spreadAmt: RawValue
    spreadDec: RawValue
    spreadPrc: RawValue
    stockExchange: str
    quoteType: str


QuoteTrend = Literal["down", "up"]


def parse_quote_trend(raw_quote_trend: RawQuoteTrend) -> QuoteTrend | None:
    """
    Parse a raw quote trend.
    """
    if raw_quote_trend == "D":
        return "down"
    elif raw_quote_trend == "U":
        return "up"
    elif raw_quote_trend != "I":
        warnings.warn(f"Invalid raw quote trend: {raw_quote_trend}", stacklevel=2)
    return None


@dataclasses.dataclass
class Quote:
    """
    A parsed ETF quote.

    Attrs:
        isin: The ISIN of the ETF.
        timestamp: The timestamp of the quote.
        exchange: The exchange of the quote.
        currency: The currency of the quote.
        trend: The trend of the quote.
        ask: Best offer price (price to buy).
        bid: Best bid price (price to sell).
        mid: Mid-price: (bid + ask) / 2.
        last: Last traded price.
        spread: Absolute spread: ask - bid.
        spread_relative: Spread relative to the last traded price.
        spread_percentage: Spread percentage relative to the last traded price.
        day_to_day: Price change since the previous day.
        day_to_day_relative: Relative price change since the previous day.
        day_to_day_percentage: Price change percentage since the previous day.
    """

    isin: str
    timestamp: datetime.datetime
    exchange: str
    currency: str
    trend: QuoteTrend | None

    ask: float
    bid: float
    mid: float
    last: float

    spread: float
    spread_relative: float
    spread_percentage: float

    day_to_day: float
    day_to_day_relative: float
    day_to_day_percentage: float


def parse_quote(raw_quote: RawQuote) -> Quote:
    """
    Parse a raw quote.
    """
    return Quote(
        isin=raw_quote["isin"],
        timestamp=datetime.datetime.fromisoformat(raw_quote["timestamp"]),
        exchange=raw_quote["stockExchange"],
        currency=raw_quote["currency"],
        trend=parse_quote_trend(raw_quote["trend"]),
        ask=raw_quote["ask"]["raw"],
        bid=raw_quote["bid"]["raw"],
        mid=raw_quote["mid"]["raw"],
        last=raw_quote["last"]["raw"],
        spread=raw_quote["spreadAmt"]["raw"],
        spread_relative=raw_quote["spreadDec"]["raw"],
        spread_percentage=raw_quote["spreadPrc"]["raw"],
        day_to_day=raw_quote["dtdAmt"]["raw"],
        day_to_day_relative=raw_quote["dtdDec"]["raw"],
        day_to_day_percentage=raw_quote["dtdPrc"]["raw"],
    )
