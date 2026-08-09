"""Reolink P2P integration for Home Assistant."""

from **future** import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
CONF_PASSWORD,
CONF_UID,
CONF_USERNAME,
DOMAIN,
)
from .coordinator import ReolinkCloudCoordinator

PLATFORMS: list[str] = ["camera"]

async def async_setup(
hass: HomeAssistant,
config: dict,
) -> bool:
"""Set up the Reolink integration."""

```
return True
```

async def async_setup_entry(
hass: HomeAssistant,
entry: ConfigEntry,
) -> bool:
"""Set up Reolink P2P from a config entry."""

```
coordinator = ReolinkCloudCoordinator(
    hass=hass,
    uid=entry.data[CONF_UID],
    username=entry.data[CONF_USERNAME],
    password=entry.data[CONF_PASSWORD],
)

hass.data.setdefault(DOMAIN, {})
hass.data[DOMAIN][entry.entry_id] = coordinator

await hass.config_entries.async_forward_entry_setups(
    entry,
    PLATFORMS,
)

return True
```

async def async_unload_entry(
hass: HomeAssistant,
entry: ConfigEntry,
) -> bool:
"""Unload a Reolink P2P config entry."""

```
unload_ok = await hass.config_entries.async_unload_platforms(
    entry,
    PLATFORMS,
)

coordinator = hass.data[DOMAIN].pop(
    entry.entry_id,
    None,
)

if coordinator is not None:
    await hass.async_add_executor_job(
        coordinator.api.close
    )

return unload_ok
