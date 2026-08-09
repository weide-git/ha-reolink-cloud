"""Reolink camera platform."""

from __future__ import annotations

from typing import Any

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import ReolinkCloudCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Reolink camera."""

    coordinator: ReolinkCloudCoordinator = hass.data[DOMAIN][
        entry.entry_id
    ]

    async_add_entities(
        [
            ReolinkCameraEntity(
                coordinator=coordinator,
                entry=entry,
            )
        ]
    )


class ReolinkCameraEntity(Camera):
    """Representation of a Reolink camera."""

    def __init__(
        self,
        coordinator: ReolinkCloudCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the camera."""

        super().__init__()

        self._coordinator = coordinator
        self._entry = entry

        self._attr_name = "Reolink P2P"
        self._attr_unique_id = (
            f"{entry.entry_id}_camera"
        )

        self._image: bytes | None = None

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""

        return {
            "identifiers": {
                (DOMAIN, self._coordinator.api.uid)
            },
            "name": "Reolink P2P",
            "manufacturer": "Reolink",
        }

    async def async_camera_image(
        self,
        width: int | None = None,
        height: int | None = None,
    ) -> bytes | None:
        """Return the latest camera image."""

        self._image = await self.hass.async_add_executor_job(
            self._coordinator.api.snapshot
        )

        return self._image

