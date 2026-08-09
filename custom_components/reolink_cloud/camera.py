"""Reolink camera platform."""

from **future** import annotations

import asyncio
import logging
from typing import Any

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import ReolinkCloudCoordinator

_LOGGER = logging.getLogger(**name**)

async def async_setup_entry(
hass: HomeAssistant,
entry: ConfigEntry,
async_add_entities: AddEntitiesCallback,
) -> None:
"""Set up the Reolink camera."""

```
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
```

class ReolinkCameraEntity(Camera):
"""Representation of a Reolink camera."""

```
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
    self._attr_unique_id = f"{entry.entry_id}_camera"

    self._image: bytes | None = None

    # Only one snapshot request may use pyneolink at a time.
    self._snapshot_lock = asyncio.Lock()

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

    async with self._snapshot_lock:
        try:
            _LOGGER.info(
                "Requesting snapshot from Reolink camera %s",
                self._coordinator.api.uid,
            )

            image = await self.hass.async_add_executor_job(
                self._coordinator.api.snapshot
            )

            if not image:
                _LOGGER.warning(
                    "Reolink camera %s returned an empty snapshot",
                    self._coordinator.api.uid,
                )
                return self._image

            if not isinstance(image, bytes):
                _LOGGER.error(
                    "Reolink camera %s returned invalid image type: %s",
                    self._coordinator.api.uid,
                    type(image).__name__,
                )
                return self._image

            _LOGGER.info(
                "Received snapshot from Reolink camera %s: %d bytes",
                self._coordinator.api.uid,
                len(image),
            )

            # Basic JPEG validation.
            if len(image) < 4:
                _LOGGER.error(
                    "Snapshot from Reolink camera %s is too small: %d bytes",
                    self._coordinator.api.uid,
                    len(image),
                )
                return self._image

            if image[:2] != b"\xff\xd8":
                _LOGGER.error(
                    "Snapshot from Reolink camera %s has invalid JPEG header: %s",
                    self._coordinator.api.uid,
                    image[:16].hex(),
                )
                return self._image

            if image[-2:] != b"\xff\xd9":
                _LOGGER.error(
                    "Snapshot from Reolink camera %s has invalid JPEG trailer: %s",
                    self._coordinator.api.uid,
                    image[-16:].hex(),
                )
                return self._image

            self._image = image

            _LOGGER.info(
                "Valid JPEG received from Reolink camera %s: %d bytes",
                self._coordinator.api.uid,
                len(image),
            )

            return self._image

        except Exception:
            _LOGGER.exception(
                "Error requesting snapshot from Reolink camera %s",
                self._coordinator.api.uid,
            )

            # Keep the last valid image if a new request fails.
            return self._image
