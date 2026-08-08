"""Reolink Cloud API client."""

from __future__ import annotations

from typing import Any

import aiohttp


class ReolinkCloudApi:
    """Client for the Reolink Cloud service."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token: str,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._token = token.strip()

    async def test_connection(self) -> dict[str, Any]:
        """Test authenticated access to Reolink Cloud."""

        url = "https://apis.reolink.com/v2/cloud/videos/records/"

        headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json",
            "User-Agent": "HomeAssistant-ReolinkCloud/0.2.0",
        }

        async with self._session.get(
            url,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=20),
        ) as response:
            text = await response.text()

            return {
                "status": response.status,
                "content_type": response.headers.get("content-type"),
                "body": text[:10000],
            }
