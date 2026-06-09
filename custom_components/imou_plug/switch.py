from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PROP_SWITCH
from .const import PROP_SWITCH


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            ImouPlugSwitch(
                coordinator,
            )
        ]
    )


class ImouPlugSwitch(
    CoordinatorEntity,
    SwitchEntity,
):

    def __init__(
        self,
        coordinator,
    ):
        super().__init__(coordinator)

        self._attr_name = "Imou Plug"
        self._attr_unique_id = (
            coordinator.device_id
        )

        self._attr_device_info = {
            "identifiers": {("imou_plug", coordinator.device_id)},
            "name": "CE2P-NGLP",
            "manufacturer": "Imou",
            "model": coordinator.product_id,
        }

    @property
    def is_on(self):

        value = self.coordinator.data[
            "properties"
        ][PROP_SWITCH]

        return value == 1

    async def async_turn_on(
        self,
        **kwargs,
    ):

        await self.coordinator.api.set_properties(
            self.coordinator.product_id,
            self.coordinator.device_id,
            {
                PROP_SWITCH: 1
            },
        )

        await self.coordinator.async_request_refresh()

    async def async_turn_off(
        self,
        **kwargs,
    ):

        await self.coordinator.api.set_properties(
            self.coordinator.product_id,
            self.coordinator.device_id,
            {
                PROP_SWITCH: 0
            },
        )

        await self.coordinator.async_request_refresh()
