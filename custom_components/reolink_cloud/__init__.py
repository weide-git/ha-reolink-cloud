"""Reolink Cloud integration for Home Assistant."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "reolink_cloud"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Reolink Cloud integration."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Reolink Cloud from a config entry."""
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a Reolink Cloud config entry."""
    return True
