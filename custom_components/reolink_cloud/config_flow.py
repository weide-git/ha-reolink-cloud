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
        errors = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]

            # Authentication will be implemented in the next step.
            # For now we store the credentials and continue.
            return self.async_create_entry(
                title=username,
                data={
                    CONF_USERNAME: username,
                    CONF_PASSWORD: password,
                },
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): vol.All(
                    str,
                    vol.Length(min=1),
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
