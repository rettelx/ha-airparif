"""Support for the Airparif service."""
import asyncio
import logging
from datetime import timedelta

import aiohttp
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    ATTR_DATE,
    CONF_TOKEN,
)
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.config_validation import PLATFORM_SCHEMA

from .api import AirparifApiClient

_LOGGER = logging.getLogger(__name__)

ATTR_NITROGEN_DIOXIDE = "nitrogen_dioxide"
ATTR_OZONE = "ozone"
ATTR_PM10 = "pm_10"
ATTR_PM2_5 = "pm_2_5"
ATTR_SULFUR_DIOXIDE = "sulfur_dioxide"
ATTR_TOMORROW = "tomorrow"
ATTR_TODAY = "today"
ATTR_AQI = "aqi"
ATTR_EPISODE = "episode"

KEY_TO_ATTR = {
    "date": ATTR_DATE,
    "pm25": ATTR_PM2_5,
    "pm10": ATTR_PM10,
    "o3": ATTR_OZONE,
    "no2": ATTR_NITROGEN_DIOXIDE,
    "so2": ATTR_SULFUR_DIOXIDE,
    "indice": ATTR_AQI,
    "episode": ATTR_EPISODE
}

ATTRIBUTION = "Data provided by Airparif"

CONF_LOCATIONS = "locations"

SCAN_INTERVAL = timedelta(hours=6)

TIMEOUT = 10

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_TOKEN): cv.string,
        vol.Required(CONF_LOCATIONS): cv.ensure_list,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the requested Airparif locations."""

    token = config.get(CONF_TOKEN)
    locations = config.get(CONF_LOCATIONS)

    client = AirparifApiClient(token, async_get_clientsession(hass))
    dev = []
    try:
        for insee in locations:
            airparif_sensor = AirparifSensor(client, insee)
            dev.append(airparif_sensor)
    except (
            aiohttp.client_exceptions.ClientConnectorError,
            asyncio.TimeoutError,
    ) as err:
        _LOGGER.exception("Failed to connect to Airparif servers")
        raise PlatformNotReady from err
    async_add_entities(dev, True)


class AirparifSensor(SensorEntity):
    """Implementation of an Airparif sensor."""

    def __init__(self, client, insee):
        """Initialize the sensor."""
        self._client = client
        self._insee = insee
        self._data = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Airparif {self._insee}"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:blur"

    @property
    def state(self):
        """Return the state of the device."""
        if self._data is not None and "indice" in self._data[ATTR_TODAY].keys():
            return self._data["today"]["indice"]
        else:
            return None

    @property
    def available(self):
        """Return sensor availability."""
        return self._data is not None

    @property
    def unique_id(self):
        """Return unique ID."""
        return self._insee

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the last update."""
        attrs = {ATTR_TODAY: {}, ATTR_TOMORROW: {}, ATTR_ATTRIBUTION: ATTRIBUTION}
        if self._data is not None:
            try:
                for (k, attr) in KEY_TO_ATTR.items():
                    attrs[ATTR_TODAY][attr] = self._data["today"][k]
                    attrs[ATTR_TOMORROW][attr] = self._data["tomorrow"][k]
                return attrs
            except (IndexError, KeyError):
                return {ATTR_ATTRIBUTION: ATTRIBUTION}

    async def async_update(self):
        """Get the latest data and updates the states."""
        self._data = await self._client.async_get_data(self._insee)
