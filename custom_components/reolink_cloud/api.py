"""Reolink Cloud API client."""

from __future__ import annotations

import aiohttp


class ReolinkCloudApi:
    """Small asynchronous client for the Reolink Cloud API."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session

    async def test_connection(self) -> dict:
        """Test connectivity to the Reolink Cloud service."""
        url = "https://apis.reolink.com/"

        async with self._session.get(
            url,
            headers={
                "User-Agent": "HomeAssistant-ReolinkCloud/0.1.0",
            },
            timeout=aiohttp.ClientTimeout(total=15),
        ) as response:
            return {
                "status": response.status,
                "url": str(response.url),
            }
