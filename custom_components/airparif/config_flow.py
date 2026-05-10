"""Config flow for Airparif."""

from __future__ import annotations

import re

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import AirparifApiClient
from .const import DOMAIN, CONF_API_KEY, CONF_INSEE

_INSEE_RE = re.compile(r"^\d{5}$")


class AirparifConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}

        if user_input:
            insee = user_input[CONF_INSEE].strip()

            if not _INSEE_RE.match(insee):
                errors["base"] = "invalid_insee"
            else:
                await self.async_set_unique_id(insee)
                self._abort_if_unique_id_configured()

                session = async_get_clientsession(self.hass)
                client = AirparifApiClient(user_input[CONF_API_KEY], session)

                try:
                    await client.get_version()
                except Exception:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(
                        title=f"Airparif {insee}",
                        data={CONF_API_KEY: user_input[CONF_API_KEY], CONF_INSEE: insee},
                    )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_API_KEY): str, vol.Required(CONF_INSEE): str}),
            errors=errors,
        )
