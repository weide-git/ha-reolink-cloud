"""Data coordinator for Reolink P2P."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import ReolinkCloudApi
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN


class ReolinkCloudCoordinator(
    DataUpdateCoordinator[dict[str, Any]]
):
    """Coordinate updates from the Reolink camera."""

    def __init__(
        self,
        hass: HomeAssistant,
        uid: str,
        username: str,
        password: str,
    ) -> None:
        """Initialize the coordinator."""

        self.api = ReolinkCloudApi(
            uid=uid,
            username=username,
            password=password,
        )

        super().__init__(
            hass,
            logger=__import__("logging").getLogger(DOMAIN),
            name=DOMAIN,
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL
            ),
        )

    async def _async_update_data(
        self,
    ) -> dict[str, Any]:
        """Connect to the camera without blocking HA."""

        return await self.hass.async_add_executor_job(
            self.api.connect
        )
