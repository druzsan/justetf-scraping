"""
Parse ETF overview data from justETF (https://www.justetf.com/en/find-etf.html).
"""

import itertools
import re
import warnings
from typing import Any, Dict, List, Literal, Optional, cast

import pandas as pd
import pycountry
import pycountry.db
import requests

from .helpers import (
    ASSET_CLASSES,
    EXCHANGES,
    INSTRUMENTS,
    REGIONS,
    STRATEGIES,
    USER_AGENT,
    assert_response_status_ok,
)
from .types import (
    AssetClass,
    Country,
    Currency,
    Exchange,
    Instrument,
    Language,
    Region,
    Strategy,
    Universe,
)

BASE_URL = "https://www.justetf.com/en/search.html"
BASE_DATA = {"draw": 1, "start": 0, "length": -1}
PATTERN = re.compile(
    r"(\d)-1.0-container-tabsContentContainer-tabsContentRepeater-1-container-content-etfsTablePanel&search=ETFS&_wicket=1"
)


LAST_FOUR_YEARS = [
    str((pd.Timestamp("now") - pd.DateOffset(years=i)).year) for i in range(1, 5)
]
COLUMN_NAMES = {
    # IDs
    "isin": "isin",
    "wkn": "wkn",
    "ticker": "ticker",
    "valorNumber": "valor",
    # Basic info
    "name": "name",
    # "groupValue": "index",
    "inceptionDate": "inception_date",
    "strategy": "strategy",  # Custom field added during request
    "domicileCountry": "domicile_country",
    "fundCurrency": "currency",
    "hasSecuritiesLending": "securities_lending",
    "distributionPolicy": "dividends",
    "ter": "ter",
    "replicationMethod": "replication",
    "fundSize": "size",
    "sustainable": "is_sustainable",
    "numberOfHoldings": "number_of_holdings",
    # Value return
    "ytdReturnCUR": "yesterday",
    "weekReturnCUR": "last_week",
    "monthReturnCUR": "last_month",
    "threeMonthReturnCUR": "last_three_months",
    "sixMonthReturnCUR": "last_six_months",
    "yearReturnCUR": "last_year",
    "threeYearReturnCUR": "last_three_years",
    "fiveYearReturnCUR": "last_five_years",
    "yearReturn1CUR": LAST_FOUR_YEARS[0],
    "yearReturn2CUR": LAST_FOUR_YEARS[1],
    "yearReturn3CUR": LAST_FOUR_YEARS[2],
    "yearReturn4CUR": LAST_FOUR_YEARS[3],
    # Dividends
    "currentDividendYield": "last_dividends",
    "yearDividendYield": "last_year_dividends",
    # Volatility
    "yearVolatilityCUR": "last_year_volatility",
    "threeYearVolatilityCUR": "last_three_years_volatility",
    "fiveYearVolatilityCUR": "last_five_years_volatility",
    # Return/Risk
    "yearReturnPerRiskCUR": "last_year_return_per_risk",
    "threeYearReturnPerRiskCUR": "last_three_years_return_per_risk",
    "fiveYearReturnPerRiskCUR": "last_five_years_return_per_risk",
    # Drawdown
    "maxDrawdownCUR": "max_drawdown",
    "yearMaxDrawdownCUR": "last_year_max_drawdown",
    "threeYearMaxDrawdownCUR": "last_three_years_max_drawdown",
    "fiveYearMaxDrawdownCUR": "last_five_years_max_drawdown",
}
IGNORED_COLUMNS = [
    "groupParam",  # Same as "groupValue" but prepared for a request
    "selected",  # Irrelevant
    "clazz",  # The most values are empty strings, some are "highl_c"
    "savingsPlanReady",  # "Savings plan ready from x.xx EUR" text
]
BOOL_COLUMNS = ["securities_lending", "is_sustainable"]
INT64_COLUMNS = ["size", "number_of_holdings"]
CATEGORY_COLUMNS = [
    "domicile_country",
    "dividends",
    "replication",
]
FLOAT_COLUMNS = [
    "ter",
    "yesterday",
    "last_week",
    "last_month",
    "last_three_months",
    "last_six_months",
    "last_year",
    "last_three_years",
    "last_five_years",
    "last_dividends",
    "last_year_dividends",
    "last_year_volatility",
    "last_three_years_volatility",
    "last_five_years_volatility",
    "last_year_return_per_risk",
    "last_three_years_return_per_risk",
    "last_five_years_return_per_risk",
    "max_drawdown",
    "last_year_max_drawdown",
    "last_three_years_max_drawdown",
    "last_five_years_max_drawdown",
] + LAST_FOUR_YEARS


def get_etf_params(
    strategy: Strategy = "epg-longOnly",
    exchange: Optional[Literal[Exchange, "any"]] = "any",
    asset_class: Optional[AssetClass] = None,
    region: Optional[Region] = None,
    country: Optional[str] = None,
    instrument: Optional[Instrument] = None,
    provider: Optional[str] = None,
    index_provider: Optional[str] = None,
    index: Optional[str] = None,
    isin: Optional[str] = None,
    extra_queries: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Build `etfParams` for ETF data request for `BASE_PARAMS` enrichment.

    Args
        strategy: Optional strategy query, see `STRATEGIES`. Strategies are
            disjunctive. There is no known way to request all the strategies at
            once, so you should make 3 requests for full results.
        exchange: Optional exchange query, see `EXCHANGES`. If "any" (default),
            all exchanges are requested. If `None`, it seems that country specific
            exchanges are requested (gettex, XETRA and Stuttgart exchanges for DE).
        asset_class: Optional asset class query, see `ASSETS`. Assets are
            disjunctive. If `None` (default), all assets are requested.
        region: Optional region query, see `REGIONS`. Regions are currently
            disjunctive. If `None` (default), all regions are requested.
        country: Optional country query, represents the country targeted by the
            respective ETFs. Can be a country name or an alpha-2 code. If `None`
            (default), all target countries are selected.
        instrument: optional instrument query, see `INSTRUMENTS`. Instruments
            are disjunctive, If `None` (default), all instruments are requested.
        provider: Optional asset provider query.
        index_provider: Optional index provider query.
        index: Optional index query. Can be spotted in `qroupIndex` field in any
            response.
        isin: Optional ISIN query.
        extra_queries: Raw extra queries. Will be appended to the `etfParams` as
            is, so be sure not to duplicate any queries explicitaly listed as
            arguments and to use proper raw keys, e.g.:
                equity: "sector", "equityStrategy", "theme",
                bonds: "currency", "bondType", "bm", "bondRating", "bondStrategy",
                commodities: "cf" and "ctype",
                money market: "currency".
    """
    etf_params = f"search=ETF&productGroup={strategy}"
    if exchange is not None:
        etf_params += f"&ls={exchange}"
    if asset_class is not None:
        etf_params += f"&assetClass={asset_class}"
    if region is not None:
        etf_params += f"&region={region}"
    if country is not None:
        if len(country) == 2 and country == country.upper():
            py_country: pycountry.db.Country = pycountry.countries.get(alpha_2=country)
            if py_country is None:
                raise ValueError(f"Country alpha-2 code '{country}' not found.")
        if len(country) != 2 or country != country.upper():
            try:
                matches = pycountry.countries.search_fuzzy(country)
            except LookupError as e:
                raise ValueError(f"Country '{country}' not recognized.") from e
            try:
                py_country = matches[0]  # type: ignore
            except IndexError as e:
                raise ValueError(f"Country '{country}' not recognized.") from e
            country = py_country.alpha_2
        etf_params += f"&country={country}"
    if instrument is not None:
        etf_params += f"&instrumentType={instrument}"
    if provider is not None:
        etf_params += f"&ic={provider}"
    if index_provider is not None:
        etf_params += f"&indexProvider={index_provider}"
    if index is not None:
        etf_params += f"&index={index}"
    if isin is not None:
        etf_params += f"&query={isin}"
    if extra_queries is not None:
        for key, value in extra_queries.items():
            etf_params += f"&{key}={value}"
    return etf_params


def get_raw_overview(
    strategy: Optional[Strategy] = None,
    exchange: Optional[Literal[Exchange, "any"]] = "any",
    asset_class: Optional[AssetClass] = None,
    region: Optional[Region] = None,
    country: Optional[str] = None,
    instrument: Optional[Instrument] = None,
    provider: Optional[str] = None,
    index_provider: Optional[str] = None,
    index: Optional[str] = None,
    isin: Optional[str] = None,
    extra_queries: Optional[Dict[str, Any]] = None,
    language: Language = "en",
    local_country: Country = "DE",
    universe: Universe = "private",
    currency: Currency = "EUR",
) -> List[Dict[str, Any]]:
    """
    Args
        strategy: Optional strategy query, see `STRATEGIES`. Strategies are
            disjunctive. If `None` (default), merge requests for all strategies.
        exchange: Optional exchange query, see `EXCHANGES`. If "any" (default),
            all exchanges are requested. If `None`, it seems that country specific
            exchanges are requested (gettex, XETRA and Stuttgart exchanges for DE).
        asset_class: Optional asset class query, see `ASSETS`. Assets are
            disjunctive. If `None` (default), all assets are requested.
        region: Optional region query, see `REGIONS`. Regions are currently
            disjunctive. If `None` (default), all regions are requested.
        country: Optional country query, represents the country targeted by the
            respective ETFs. Can be a country name or an alpha-2 code. If `None`
            (default), all target countries are selected.
        instrument: optional instrument query, see `INSTRUMENTS`. Instruments
            are disjunctive, If `None` (default), all instruments are requested.
        provider: Optional asset provider query.
        index_provider: Optional index provider query.
        index: Optional index query. Can be spotted in `qroupIndex` field in any
            response.
        isin: Optional ISIN query.
        language: Optional response language, see `Language`.
        local_country: Optional response country, see `Country`.
        universe: Optional investor type, see `Universe`.
        currency: Currency to get data in, see `Currency`.
        extra_queries: Raw extra queries. Will be appended to the `etfParams` as
            is, so be sure not to duplicate any queries explicitaly listed as
            arguments and to use proper raw keys, e.g.:
                equity: "sector", "equityStrategy", "theme",
                bonds: "currency", "bondType", "bm", "bondRating", "bondStrategy",
                commodities: "cf" and "ctype",
                money market: "currency".
    """
    # If `strategy` is `None`, make requests for all strategies.
    strategies = list(STRATEGIES) if strategy is None else [strategy]
    rows: List[Dict[str, Any]] = []
    with requests.Session() as session:
        session.headers["User-Agent"] = USER_AGENT
        html_response = session.get(f"{BASE_URL}?search=ETFS")
        assert_response_status_ok(html_response, "overview-html")
        if match := PATTERN.search(html_response.text):
            counter = int(match.group(1))
        else:
            warnings.warn("Cannot parse dynamic counter from HTML page, assuming 0.")
            counter = 0
        for strategy_ in strategies:
            response = session.post(
                f"{BASE_URL}?{counter}-1.0-container-tabsContentContainer-tabsContentRepeater-1-container-content-etfsTablePanel=&search=ETFS&_wicket=1",
                {
                    **BASE_DATA,
                    "lang": language,
                    "country": local_country,
                    "universeType": universe,
                    "defaultCurrency": currency,
                    "etfsParams": get_etf_params(
                        strategy_,
                        exchange,
                        asset_class,
                        region,
                        country,
                        instrument,
                        provider,
                        index_provider,
                        index,
                        isin,
                    ),
                },
            )
            assert_response_status_ok(response, "overview")
            strategy_rows = response.json()["data"]
            for row in strategy_rows:
                for old_row in rows:
                    if row["isin"] == old_row["isin"]:
                        old_value = old_row["strategy"]
                        old_row["strategy"] = f"{old_value}, {STRATEGIES[strategy_]}"
                        break
                else:
                    row["strategy"] = STRATEGIES[strategy_]
                    rows.append(row)
    return rows


def load_overview(
    strategy: Optional[Strategy] = None,
    exchange: Optional[Literal[Exchange, "any"]] = "any",
    asset_class: Optional[AssetClass] = None,
    region: Optional[Region] = None,
    country: Optional[str] = None,
    instrument: Optional[Instrument] = None,
    provider: Optional[str] = None,
    index_provider: Optional[str] = None,
    index: Optional[str] = None,
    isin: Optional[str] = None,
    extra_queries: Optional[Dict[str, Any]] = None,
    language: Language = "en",
    local_country: Country = "DE",
    universe: Universe = "private",
    currency: Currency = "EUR",
    enrich: bool = False,
) -> pd.DataFrame:
    """
    Args
        strategy: Optional strategy query, see `STRATEGIES`. Strategies are
            disjunctive. If `None` (default), merge requests for all strategies.
        exchange: Optional exchange query, see `EXCHANGES`. If "any" (default),
            all exchanges are requested. If `None`, it seems that country
            specific exchanges are requested (e.g. gettex, XETRA and Stuttgart
            exchanges for DE).
        asset_class: Optional asset class query, see `ASSETS`. Assets are
            disjunctive. If `None` (default), all assets are requested.
        region: Optional region query, see `REGIONS`. Regions are currently
            disjunctive. If `None` (default), all regions are requested.
        country: Optional country query, represents the country targeted by the
            respective ETFs. Can be a country name or an alpha-2 code. If `None`
            (default), all target countries are selected.
        instrument: optional instrument query, see `INSTRUMENTS`. Instruments
            are disjunctive, If `None` (default), all instruments are requested.
        provider: Optional asset provider query.
        index_provider: Optional index provider query.
        index: Optional index query. Can be spotted in `qroupIndex` field in any
            response.
        isin: Optional ISIN query.
        extra_queries: Raw extra queries. Will be appended to the `etfParams` as
            is, so be sure not to duplicate any queries explicitaly listed as
            arguments and to use proper raw keys, e.g.:
                equity: "sector", "equityStrategy", "theme",
                bonds: "currency", "bondType", "bm", "bondRating", "bondStrategy",
                commodities: "cf" and "ctype",
                money market: "currency".
        language: Optional language for the response data, see `Language` for
            available options.
        local_country: Optional response country, see `Country` for available
            options.
        universe: Optional investor type, see `Universe` for available options.
        currency: Currency to get data in, see `Currency` for available options.
        enrich: Whether to enrich data with extra information. Currently, adds
            the following fields:
                `asset_class`: equity, bonds etc.
                `instrument`: ETC, ETF or ETN
                `region`: target region
                `exchange`: all exchanges the asset is available at.
    """
    rows = get_raw_overview(
        strategy,
        exchange,
        asset_class,
        region,
        country,
        instrument,
        provider,
        index_provider,
        index,
        isin,
        extra_queries,
        language,
        local_country,
        universe,
        currency,
    )
    # Rebuild rows to columns
    data: Dict[str, list] = {key: [] for key in itertools.chain.from_iterable(rows)}
    for row in rows:
        for key, values in data.items():
            values.append(row.get(key))

    df = pd.DataFrame(data)
    # Remove ignored columns.
    df = df.drop(columns=df.columns.intersection(IGNORED_COLUMNS))
    if len(df) == 0:
        # No rows received.
        return df
    # Reorder columns.
    if set(df.columns.tolist()) == set(COLUMN_NAMES):
        columns = list(COLUMN_NAMES)
    else:
        missing_columns = [column for column in COLUMN_NAMES if column not in df]
        unknown_columns = df.columns.difference(list(COLUMN_NAMES)).tolist()
        message = "Received overview columns are not as expected."
        if missing_columns:
            message += "\n\tMissing columns: '" + "', '".join(missing_columns) + "'."
        if unknown_columns:
            message += "\n\tUnknown columns: '" + "', '".join(unknown_columns) + "'."
        warnings.warn(message)
        columns = [
            column for column in COLUMN_NAMES if column in df
        ] + df.columns.difference(list(COLUMN_NAMES)).tolist()
    df = df[columns]
    # Rename columns.
    df = df.rename(columns=COLUMN_NAMES)
    # Clean up data.
    for column in df.columns.difference(["strategy"]):
        df[column] = (
            df[column]
            .str.replace("<br />", " ")
            .str.replace(",", "")
            .replace("-", pd.NA)
        )
    # Convert columns.
    for column in df.columns.intersection(BOOL_COLUMNS):
        df[column] = df[column].replace({"Yes": True, "No": False}).astype("bool")
    for column in df.columns.intersection(INT64_COLUMNS):
        if column in df:
            df[column] = df[column].astype("Int64")
    for column in df.columns.intersection(CATEGORY_COLUMNS):
        if column in df:
            df[column] = df[column].astype("category")
    for column in df.columns.intersection(FLOAT_COLUMNS):
        if column in df:
            df[column] = (
                df[column].str.removesuffix("%").fillna("nan").astype("float64")
            )
    if "inception_date" in df:
        df["inception_date"] = pd.to_datetime(df["inception_date"], format="%d.%m.%y")
    # Enrich existing columns.
    if "inception_date" in df:
        columns = df.columns.tolist()
        df["age_in_days"] = (pd.Timestamp("now") - df["inception_date"]).dt.days  # type: ignore
        df["age_in_years"] = df["age_in_days"] / 365
        columns.insert(columns.index("inception_date") + 1, "age_in_days")
        columns.insert(columns.index("age_in_days") + 1, "age_in_years")
        df = df[columns]
    if "currency" in df:
        columns = df.columns.tolist()
        df["hedged"] = df["currency"].str.endswith("Hedged")
        df["currency"] = df["currency"].str.removesuffix(" Hedged").astype("category")
        columns.insert(columns.index("currency") + 1, "hedged")
        df = df[columns]
    # Make requests for further enrichment.
    if enrich:
        for enrichment_name, enrichments in {
            "asset_class": ASSET_CLASSES,
            "instrument": INSTRUMENTS,
            "region": REGIONS,
            "exchange": EXCHANGES,
        }.items():
            df[enrichment_name] = ""
            for enrichment, value in cast(dict, enrichments).items():
                kwargs = {
                    "strategy": strategy,
                    enrichment_name: enrichment,
                    "language": language,
                    "universe": universe,
                }
                for row in get_raw_overview(**kwargs):
                    for index_ in df[df["isin"] == row["isin"]].index:
                        old_value = df.at[index_, enrichment_name]
                        if old_value == "":
                            df.at[index_, enrichment_name] = value
                        elif value not in old_value:
                            df.at[index_, enrichment_name] = f"{old_value}, {value}"
    return df.set_index("isin")
