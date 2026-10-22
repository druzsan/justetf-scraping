"""
Shared test fixtures.
"""

from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def etf_profile_html() -> str:
    """
    Captured profile page of iShares Core MSCI World (IE00B4L5Y983), see
    `tests/data/capture_etf_profile.py`.
    """
    return (DATA_DIR / "etf_profile" / "IE00B4L5Y983.html").read_text(encoding="utf-8")
