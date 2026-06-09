import voluptuous as vol

from homeassistant import config_entries

from .const import (
    DOMAIN,
    CONF_APP_ID,
    CONF_APP_SECRET,
)


class ImouPlugConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):

    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ):

        if user_input is not None:

            return self.async_create_entry(
                title=user_input["device_id"],
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_APP_ID): str,
                vol.Required(CONF_APP_SECRET): str,
                vol.Required("device_id"): str,
                vol.Required("product_id"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
