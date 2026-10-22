"""
Capture justETF profile pages as test data for `justetf_scraping.etf_profile`.

Usage:
    uv run python tests/data/capture_etf_profile.py IE00B4L5Y983 [ISIN ...]

Only the page sections parsed by `justetf_scraping.etf_profile` are kept, so
captured files stay small and reviewable. When the parser starts reading a new
section, add its data-testid to `SECTION_TESTIDS` and recapture.
"""

import datetime
import sys
import warnings
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Comment

from justetf_scraping.etf_profile import BASE_URL
from justetf_scraping.helpers import USER_AGENT

OUTPUT_DIR = Path(__file__).parent / "etf_profile"
SECTION_TESTIDS = [
    "etf-quote-section_description-label",
    "etf-basics_data_table",
    "etf-holdings_top-holdings_container",
    "etf-holdings_countries_container",
    "etf-holdings_sectors_container",
    "tl_etf-holdings_reference-date",
    "etf-trade-data-panel_table",
]


def trim_page(html: str, source: str) -> str:
    """
    Keep only the page title and the parsed sections of a profile page.
    """
    soup = BeautifulSoup(html, "html.parser")
    trimmed = BeautifulSoup(
        "<html><head><title></title></head><body></body></html>", "html.parser"
    )
    assert trimmed.title is not None and trimmed.body is not None
    if soup.title is not None:
        trimmed.title.string = soup.title.get_text(strip=True)
    for testid in SECTION_TESTIDS:
        section = soup.find(attrs={"data-testid": testid})
        if section is None:
            warnings.warn(f"No section '{testid}' in {source}.", stacklevel=2)
            continue
        trimmed.body.append(section.extract())
    today = datetime.date.today().isoformat()
    trimmed.insert(
        0, Comment(f" Captured from {source} on {today} by {Path(__file__).name} ")
    )
    # Strip trailing whitespace to keep pre-commit hooks happy.
    lines = (line.rstrip() for line in trimmed.prettify().splitlines())
    return "\n".join(lines) + "\n"


def capture(isin: str) -> Path:
    """
    Capture the profile page of the given ETF.
    """
    response = requests.get(
        BASE_URL, params={"isin": isin}, headers={"User-Agent": USER_AGENT}
    )
    response.raise_for_status()
    path = OUTPUT_DIR / f"{isin}.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(trim_page(response.text, response.url), encoding="utf-8")
    return path


if __name__ == "__main__":
    for isin_ in sys.argv[1:]:
        print(f"Captured {capture(isin_)}")
