"""Data coordinator for Reolink Cloud."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from aiohttp import ClientSession
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import ReolinkCloudApi
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN


class ReolinkCloudCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinate updates from Reolink Cloud."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: ClientSession,
    ) -> None:
        """Initialize the coordinator."""
        self.api = ReolinkCloudApi(session)

        super().__init__(
            hass,
            logger=__import__("logging").getLogger(DOMAIN),
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Reolink Cloud."""
        return await self.api.test_connection()
