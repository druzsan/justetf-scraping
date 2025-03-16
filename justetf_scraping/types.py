"""
Common types used in package.
"""

from typing import Literal

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
