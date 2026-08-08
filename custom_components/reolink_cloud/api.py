"""Reolink Cloud API client."""

from __future__ import annotations

from typing import Any

import aiohttp


class ReolinkCloudApi:
    """Client for the Reolink Cloud service."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        username: str,
        password: str,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._username = username
        self._password = password
        self._token: str | None = None

    async def login(self) -> dict[str, Any]:
        """Authenticate against Reolink Cloud.

        The exact cloud authentication endpoint is intentionally kept
        isolated here while the current API is being verified.
        """
        # Temporary diagnostic request only.
        # No credentials are sent yet.
        url = "https://apis.reolink.com/"

        async with self._session.get(
            url,
            headers={
                "User-Agent": "HomeAssistant-ReolinkCloud/0.1.0",
                "Accept": "application/json",
            },
            timeout=aiohttp.ClientTimeout(total=15),
        ) as response:
            return {
                "status": response.status,
                "url": str(response.url),
            }
