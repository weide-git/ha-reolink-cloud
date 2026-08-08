"""Reolink Cloud integration for Home Assistant."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .coordinator import ReolinkCloudCoordinator

PLATFORMS: list[str] = []


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Reolink Cloud integration."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Reolink Cloud from a config entry."""

    session = async_get_clientsession(hass)

    coordinator = ReolinkCloudCoordinator(
    hass,
    session,
    entry.data["token"],
)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a Reolink Cloud config entry."""

    hass.data[DOMAIN].pop(entry.entry_id, None)

    return True
