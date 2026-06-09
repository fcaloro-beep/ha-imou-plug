from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PROP_POWER, PROP_CURRENT, PROP_VOLTAGE


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [
            ImouSensor(
                coordinator,
                "Power",
                PROP_POWER,
                "W",
            ),
            ImouSensor(
                coordinator,
                "Current",
                PROP_CURRENT,
                "A",
            ),
            ImouSensor(
                coordinator,
                "Voltage",
                PROP_VOLTAGE,
                "V",
            ),
        ]
    )


class ImouSensor(
    CoordinatorEntity,
    SensorEntity,
):

    def __init__(
        self,
        coordinator,
        name,
        prop,
        unit,
    ):
        super().__init__(coordinator)

        self.prop = prop
        self._attr_name = f"Imou {name}"
        self._attr_unique_id = (
            f"{coordinator.device_id}_{prop}"
        )
        self._attr_native_unit_of_measurement = unit

        self._attr_device_info = {
            "identifiers": {("imou_plug", coordinator.device_id)},
            "name": "CE2P-NGLP",
            "manufacturer": "Imou",
            "model": coordinator.product_id,
        }

    @property
    def native_value(self):

        value = self.coordinator.data["properties"].get(self.prop)

        if self.prop == PROP_VOLTAGE:
            return round(value / 1000, 3)

        if self.prop == PROP_CURRENT:
            return round(value / 1000, 3)

        return value
