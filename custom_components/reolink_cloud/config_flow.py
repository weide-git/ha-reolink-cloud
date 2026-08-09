```python
"""Config flow for Reolink Cloud / P2P."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN


class ReolinkCloudConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle the Reolink Cloud / P2P config flow."""

    VERSION = 2

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""

        if user_input is not None:
            return self.async_create_entry(
                title="Reolink P2P",
                data={
                    "uid": user_input["uid"].strip(),
                    "username": user_input["username"].strip(),
                    "password": user_input["password"],
                },
            )

        schema = vol.Schema(
            {
                vol.Required("uid"): str,
                vol.Required(
                    "username",
                    default="admin",
                ): str,
                vol.Required("password"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
```
