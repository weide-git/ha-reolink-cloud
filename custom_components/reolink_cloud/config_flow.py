"""Config flow for Reolink Cloud."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from . import DOMAIN


class ReolinkCloudConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Reolink Cloud config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_USERNAME],
                data={
                    CONF_USERNAME: user_input[CONF_USERNAME],
                    CONF_PASSWORD: user_input[CONF_PASSWORD],
                },
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
