from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import ImouCoordinator
from .const import (
    PROP_POWER,
    PROP_CURRENT,
    PROP_VOLTAGE,
)


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):

    coordinator = ImouCoordinator(
        hass,
        entry.data,
    )

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
                "mA",
            ),
            ImouSensor(
                coordinator,
                "Voltage",
                PROP_VOLTAGE,
                "mV",
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

    @property
    def native_value(self):

        return self.coordinator.data[
            "properties"
        ].get(
            self.prop
        )
