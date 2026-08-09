"""Config flow for Reolink P2P."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries

from .const import (
    CONF_PASSWORD,
    CONF_UID,
    CONF_USERNAME,
    DOMAIN,
)


class ReolinkCloudConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle the Reolink P2P config flow."""

    VERSION = 2

    async def async_step_user(
        self,
        user_input=None,
    ):
        """Handle the initial setup step."""

        if user_input is not None:
            return self.async_create_entry(
                title="Reolink P2P",
                data={
                    CONF_UID: user_input[CONF_UID].strip(),
                    CONF_USERNAME: user_input[
                        CONF_USERNAME
                    ].strip(),
                    CONF_PASSWORD: user_input[
                        CONF_PASSWORD
                    ],
                },
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_UID): str,
                vol.Required(
                    CONF_USERNAME,
                    default="admin",
                ): str,
                vol.Required(CONF_PASSWORD): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
