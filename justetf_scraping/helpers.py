"""
Common functions used in package.
"""

from typing import Optional

import requests

# justETF seems to block default requests' user agent, so define a custom one
USER_AGENT = "My User Agent 1.0"


def assert_response_status_ok(
    response: requests.Response,
    name: Optional[str] = None,
) -> None:
    """
    Check response status code, fail and save error page if not equal to 200.

    Args:
        response: Response to check.
        name: Optional name to use in error page file name and error message.
    """
    if response.status_code != requests.codes.ok:
        message = f"Got status {response.status_code}"
        if name:
            message += f" when requesting {name}"
            filepath = f"{name}-error-page.html"
        else:
            filepath = "error-page.html"
        message += f".\nError page saved to '{filepath}'."

        with open(filepath, "w") as file:
            file.write(response.text)
        raise RuntimeError(message)
