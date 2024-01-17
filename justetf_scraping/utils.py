from typing import Dict, List, Literal, Optional

import requests


HIDDEN_URL = "https://www.justetf.com/servlet/etfs-table"
BASE_PARAMS = {
    "draw": 1,
    "start": 0,
    "length": -1,
    "lang": "en",
    "country": "DE",
    "universeType": "private",
}


Language = Literal["en", "de", "fr", "it", "es"]
Country = Literal["DE", "AT", "CH", "GB", "IT", "FR", "ES", "NL", "BE"]
Universe = Literal["private", "institutional"]
Strategy = Literal["epg-longOnly", "epg-activeEtfs", "epg-shortAndLeveraged"]
Asset = Literal[
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
ASSETS: Dict[Asset, str] = {
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


def build_query(
    strategy: Strategy = "epg-longOnly",
    exchange: Optional[Literal[Exchange, "any"]] = "any",
    asset: Optional[Asset] = None,
    region: Optional[Region] = None,
    instrument: Optional[Instrument] = None,
    provider: Optional[str] = None,
    index_provider: Optional[str] = None,
    index: Optional[str] = None,
    isin: Optional[str] = None,
) -> str:
    """
    Build custom query for ETF data request.
    Used to enrich `BASE_PARAMS`.

    Args
        strategy: optional strategy query, see `STRATEGIES`. Strategies are
            disjunctive. There is no known way to request all the strategies at
            once, so you should make 3 requests for full results.
        exchange: optional exchange query, see `EXCHANGES`. If "any" (default),
            all exchanges are requested. If `None`, it seems that country specific
            exchanges are requested (gettex, XETRA and Stuttgart exchanges for DE).
        asset: optional asset query, see `ASSETS`. Assets are disjunctive.
            If `None` (default), all assets are requested.
        region: optional region query, see `REGIONS`. Regions are currently
            disjunctive. If `None` (default), all regions are requested.
        instrument: optional instrument query, see `INSTRUMENTS`. Instruments
            are disjunctive, If `None` (default), all instruments are requested.
        provider: optional asset provider query.
        index_provider: optional index provider query.
        index: optional index query. Can be spotted in `qroupIndex` field in any
            response.
        isin: optional ISIN query.
    """
    params = f"groupField=index&productGroup={strategy}"
    if exchange is not None:
        params += f"&ls={exchange}"
    if asset is not None:
        params += f"&assetClass={asset}"
    if region is not None:
        params += f"&region={region}"
    if instrument is not None:
        params += f"&instrumentType={instrument}"
    if provider is not None:
        params += f"&ic={provider}"
    if index_provider is not None:
        params += f"&indexProvider={index_provider}"
    if index is not None:
        params += f"&index={index}"
    if isin is not None:
        params += f"&query={isin}"
    return params


def make_request(
    strategy: Optional[Strategy] = None,
    exchange: Optional[Literal[Exchange, "any"]] = "any",
    asset: Optional[Asset] = None,
    region: Optional[Region] = None,
    instrument: Optional[Instrument] = None,
    provider: Optional[str] = None,
    index_provider: Optional[str] = None,
    index: Optional[str] = None,
    isin: Optional[str] = None,
) -> List[Dict[str, str]]:
    """
    Request ETF data, append strategy key to each.

    Args:
        see `build_query`.
        if `strategy` is None (default), merge requests for all strategies.
    """
    if strategy is None:
        # Make request for every strategy.
        data = []
        for strategy_ in STRATEGIES:
            data.extend(
                make_request(
                    strategy_,
                    exchange,
                    asset,
                    region,
                    instrument,
                    provider,
                    index_provider,
                    index,
                    isin,
                )
            )
        return data
    response = requests.post(
        HIDDEN_URL,
        {
            **BASE_PARAMS,
            "etfsParams": build_query(
                strategy,
                exchange,
                asset,
                region,
                instrument,
                provider,
                index_provider,
                index,
                isin,
            ),
        },
    )
    assert response.status_code == requests.codes.ok
    data = response.json()["data"]
    # Enrich data with strategy name.
    for sample in data:
        sample["strategy"] = STRATEGIES[strategy]
    return data
