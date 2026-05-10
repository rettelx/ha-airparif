"""Binary sensor platform for Airparif pollution episodes."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass, ENTITY_ID_FORMAT as BINARY_ENTITY_ID_FORMAT
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DAY_TODAY, DAY_TOMORROW, BINARY_KEYS


def _device_info(insee: str) -> dict:
    return {
        "identifiers": {(DOMAIN, insee)},
        "name": f"Airparif {insee}",
        "manufacturer": "Airparif",
        "model": "Air quality forecast",
        "entry_type": DeviceEntryType.SERVICE,
        "configuration_url": "https://www.airparif.fr",
    }


def _object_id(*parts: str) -> str:
    return "_".join(parts).lower()


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    insee = entry.data["insee"]

    entities: list[BinarySensorEntity] = []

    for day in (DAY_TODAY, DAY_TOMORROW):
        ent = AirparifEpisodeBinarySensor(coordinator, insee, day)
        # binary_sensor.airparif_<INSEE>_pollution_episode_<day>
        ent.entity_id = async_generate_entity_id(
            BINARY_ENTITY_ID_FORMAT,
            _object_id("airparif", insee, "pollution_episode", day),
            hass=hass,
        )
        entities.append(ent)

    async_add_entities(entities)


class AirparifEpisodeBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """True if a pollution episode is active."""

    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:alert-circle"

    def __init__(self, coordinator, insee: str, day: str) -> None:
        super().__init__(coordinator)
        self._insee = insee
        self._day = day

        self._attr_unique_id = f"{insee}_episode_{day}"
        self._attr_translation_key = BINARY_KEYS[day]

    @property
    def device_info(self) -> dict:
        return _device_info(self._insee)

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.get(self._day, {}).get("episode"))
