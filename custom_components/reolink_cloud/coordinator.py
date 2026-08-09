"""Data coordinator for Reolink P2P."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import ReolinkCloudApi
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


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

        self._connected = False
        self._connecting = False

        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL
            ),
        )

    @property
    def connected(self) -> bool:
        """Return whether the camera is connected."""

        return self._connected

    async def async_connect(self) -> bool:
        """Connect to the camera in the executor."""

        if self._connecting:
            _LOGGER.debug(
                "Reolink camera %s connection attempt already running",
                self.api.uid,
            )
            return self._connected

        self._connecting = True

        try:
            _LOGGER.info(
                "Starting background connection to Reolink camera %s",
                self.api.uid,
            )

            data = await self.hass.async_add_executor_job(
                self.api.connect
            )

            self._connected = bool(
                data.get("connected", False)
            )

            if self._connected:
                _LOGGER.info(
                    "Reolink camera %s is connected",
                    self.api.uid,
                )
            else:
                _LOGGER.warning(
                    "Reolink camera %s connection returned disconnected",
                    self.api.uid,
                )

            return self._connected

        except Exception:
            self._connected = False

            _LOGGER.exception(
                "Failed to connect to Reolink camera %s",
                self.api.uid,
            )

            return False

        finally:
            self._connecting = False

    async def _async_update_data(
        self,
    ) -> dict[str, Any]:
        """Update camera connection state."""

        if self._connected:
            return {
                "connected": True,
                "uid": self.api.uid,
            }

        if not self._connecting:
            _LOGGER.info(
                "Reolink camera %s is not connected; "
                "starting connection in background",
                self.api.uid,
            )

            self.hass.async_create_task(
                self.async_connect()
            )

        return {
            "connected": False,
            "uid": self.api.uid,
        }
