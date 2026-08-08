"""Config flow for Reolink Cloud."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries

from .const import CONF_TOKEN, DOMAIN


class ReolinkCloudConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Reolink Cloud config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""

        if user_input is not None:
            return self.async_create_entry(
                title="Reolink Cloud",
                data={
                    CONF_TOKEN: user_input[CONF_TOKEN],
                },
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_TOKEN): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
