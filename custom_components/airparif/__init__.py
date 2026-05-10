"""Airparif integration setup (config entry lifecycle)."""

from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import AirparifApiClient
from .coordinator import AirparifCoordinator
from .const import DOMAIN, CONF_API_KEY, CONF_INSEE

PLATFORMS: tuple[Platform, ...] = (Platform.SENSOR, Platform.BINARY_SENSOR)


async def async_setup_entry(hass, entry) -> bool:
    session = async_get_clientsession(hass)
    client = AirparifApiClient(entry.data[CONF_API_KEY], session)

    coordinator = AirparifCoordinator(hass, client, entry.data[CONF_INSEE])
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass, entry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
