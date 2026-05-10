"""Sensor platform for Airparif."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass, ENTITY_ID_FORMAT as SENSOR_ENTITY_ID_FORMAT
from homeassistant.const import EntityCategory
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    DAY_TODAY,
    DAY_TOMORROW,
    ATTR_DAY,
    ATTR_EPISODE,
    ATTR_COLOR,
    ATTR_LABEL,
    ATTRIBUTION,
    AQI_COLORS,
    QUALI_TO_NUM,
    FIELDS,
    ICONS,
    SENSOR_KEYS,
    NUMERIC_KEYS,
)


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
    """Build a deterministic object_id (without platform prefix)."""
    return "_".join(parts).lower()


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    insee = entry.data["insee"]

    entities: list[SensorEntity] = []

    for pollutant in FIELDS:
        for day in (DAY_TODAY, DAY_TOMORROW):
            ent = AirparifQualitativeSensor(coordinator, insee, pollutant, day)
            # Suggest readable entity_id: sensor.airparif_<INSEE>_<pollutant>_<day>
            ent.entity_id = async_generate_entity_id(
                SENSOR_ENTITY_ID_FORMAT,
                _object_id("airparif", insee, pollutant, day),
                hass=hass,
            )
            entities.append(ent)

    for day in (DAY_TODAY, DAY_TOMORROW):
        ent = AirparifAqiNumericSensor(coordinator, insee, day)
        ent.entity_id = async_generate_entity_id(
            SENSOR_ENTITY_ID_FORMAT,
            _object_id("airparif", insee, "aqi_numeric", day),
            hass=hass,
        )
        entities.append(ent)

    ent = AirparifApiVersionSensor(coordinator, insee)
    ent.entity_id = async_generate_entity_id(
        SENSOR_ENTITY_ID_FORMAT,
        _object_id("airparif", insee, "api_version"),
        hass=hass,
    )
    entities.append(ent)

    async_add_entities(entities)


class AirparifQualitativeSensor(CoordinatorEntity, SensorEntity):
    """Qualitative pollutant or AQI sensor (string state)."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, insee: str, pollutant: str, day: str) -> None:
        super().__init__(coordinator)
        self._insee = insee
        self._pollutant = pollutant
        self._day = day

        self._attr_unique_id = f"{insee}_{pollutant}_{day}"
        self._attr_translation_key = SENSOR_KEYS[(pollutant, day)]
        self._attr_icon = ICONS[pollutant]

    @property
    def device_info(self) -> dict:
        return _device_info(self._insee)

    @property
    def native_value(self):
        return self.coordinator.data.get(self._day, {}).get(FIELDS[self._pollutant])

    @property
    def extra_state_attributes(self) -> dict:
        label = self.native_value
        return {
            ATTR_DAY: self._day,
            ATTR_EPISODE: self.coordinator.data.get(self._day, {}).get("episode"),
            ATTR_COLOR: AQI_COLORS.get(label),
            "attribution": ATTRIBUTION,
        }


class AirparifAqiNumericSensor(CoordinatorEntity, SensorEntity):
    """Derived numeric AQI sensor (1–6) with qualitative label preserved."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:numeric"

    def __init__(self, coordinator, insee: str, day: str) -> None:
        super().__init__(coordinator)
        self._insee = insee
        self._day = day

        self._attr_unique_id = f"{insee}_aqi_numeric_{day}"
        self._attr_translation_key = NUMERIC_KEYS[day]

    @property
    def device_info(self) -> dict:
        return _device_info(self._insee)

    @property
    def native_value(self):
        label = self.coordinator.data.get(self._day, {}).get("indice")
        return QUALI_TO_NUM.get(label)

    @property
    def extra_state_attributes(self) -> dict:
        label = self.coordinator.data.get(self._day, {}).get("indice")
        return {ATTR_DAY: self._day, ATTR_LABEL: label, "attribution": ATTRIBUTION}


class AirparifApiVersionSensor(CoordinatorEntity, SensorEntity):
    """Diagnostic sensor exposing the Airparif API version."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_translation_key = "api_version"
    _attr_icon = "mdi:api"

    def __init__(self, coordinator, insee: str) -> None:
        super().__init__(coordinator)
        self._insee = insee
        self._attr_unique_id = f"{insee}_api_version"

    @property
    def device_info(self) -> dict:
        return _device_info(self._insee)

    @property
    def native_value(self):
        return self.coordinator.data.get("version")
