import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.warning("IMOU coordinator module loaded")

from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .api import ImouApi
from .const import (
    PROP_SWITCH,
    PROP_POWER,
    PROP_CURRENT,
    PROP_VOLTAGE,
)


class ImouCoordinator(DataUpdateCoordinator):

    def __init__(
        self,
        hass,
        config,
    ):

        self.api = ImouApi(
            config["app_id"],
            config["app_secret"],
        )

        self.device_id = config["device_id"]
        self.product_id = config["product_id"]

        super().__init__(
            hass,
            _LOGGER,
            name="Imou Plug",
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        _LOGGER.warning("IMOU refresh started")
        data = await self.api.get_properties(
            self.product_id,
            self.device_id,
            [
                PROP_SWITCH,
                PROP_POWER,
                PROP_CURRENT,
                PROP_VOLTAGE,
            ],
        )
        _LOGGER.warning(f"IMOU refresh result: {data}")
        return data
