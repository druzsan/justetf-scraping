from typing import Dict, Literal

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

STRATEGIES: Dict[Strategy, str] = {
    "epg-longOnly": "Long-only",
    "epg-activeEtfs": "Active",
    "epg-shortAndLeveraged": "Short & Leveraged",
}
ASSET_CLASSES: Dict[AssetClass, str] = {
    "class-equity": "Equity",
    "class-bonds": "Bonds",
    "class-preciousMetals": "Precious Metals",
    "class-commodities": "Commodities",
    "class-currency": "Cryptocurrencies",
    "class-realEstate": "Real Estate",
    "class-moneyMarket": "Money Market",
}
REGIONS: Dict[Region, str] = {
    "Africa": "Africa",
    "Asia%2BPacific": "Asia & Pacific",
    "Eastern%2BEurope": "Eastern Europe",
    "Emerging%2BMarkets": "Emerging Markets",
    "Europe": "Europe",
    "Latin%2BAmerica": "Latin America",
    "North%2BAmerica": "North America",
    "World": "World",
}
EXCHANGES: Dict[Exchange, str] = {
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
INSTRUMENTS: Dict[Instrument, str] = {
    "ETC": "ETC",
    "ETF": "ETF",
    "ETN": "ETN",
}
