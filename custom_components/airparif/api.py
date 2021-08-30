"""Airparif API Client."""
import asyncio
import logging
import socket
from datetime import datetime

import aiohttp
import async_timeout
import jsonschema

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)

API_ROOT = "https://api.airparif.asso.fr"

VALUE_ENUM = ["Bon", "Moyen", "Dégradé", "Mauvais", "Très Mauvais", "Extrêmement Mauvais"]

SCHEMA_PREVISIONS = {
    "type": "object",
    "patternProperties": {
        "^\\d{5}$": {
            "type": "array",
            "minItems": 1,
            "maxItems": 2,
            "items": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "format": "date"},
                    "no2": {"enum": VALUE_ENUM},
                    "o3": {"enum": VALUE_ENUM},
                    "pm10": {"enum": VALUE_ENUM},
                    "pm25": {"enum": VALUE_ENUM},
                    "so2": {"enum": VALUE_ENUM},
                    "indice": {"enum": VALUE_ENUM},
                },
                "additionalProperties": False,
                "required": ["date", "no2", "o3", "pm10", "pm25", "so2", "indice"]
            },
        },
    },
    "additionalProperties": False,
    "maxProperties": 1,
    "minProperties": 1
}

SCHEMA_EPISODES = {
    "type": "object",
    "properties": {
        "actif": {"type": "boolean"},
        "message": {"type": "object", "properties": {"fr": {"type": "string"}, "en": {"type": "string"}}},
        "jour": {
            "type": "object",
            "properties": {
                "actif": {"type": "boolean"},
                "polluants": {"type": "array",
                              "items": {
                                  "type": "object",
                                  "properties": {
                                      "nom": {"type": "string"},
                                      "niveau": {"type": "string"}
                                  }
                              }}
            }
        },
        "demain": {
            "type": "object",
            "properties": {
                "actif": {"type": "boolean"},
                "polluants": {"type": "array",
                              "items": {
                                  "type": "object",
                                  "properties": {
                                      "nom": {"type": "string"},
                                      "niveau": {"type": "string"}
                                  }
                              }}
            }
        }
    }
}


class AirparifApiClient:
    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        """Airparif API Client."""
        self._api_key = api_key
        self._session = session
        self._headers = {"Content-type": f"application/json; charset=UTF-8;", "X-Api-Key": f"{api_key}"}

    async def api_wrapper(self, url: str) -> dict:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT, loop=asyncio.get_event_loop()):
                response = await self._session.get(f"{API_ROOT}{url}", headers=self._headers)
                if response.status == 403:
                    raise PermissionError("Access denied (403)")
                elif response.status == 200:
                    return await response.json()
                else:
                    raise ValueError(f"Invalid request: {response.status}")

        except asyncio.TimeoutError as exception:
            _LOGGER.error("Timeout error fetching information from %s - %s", url, exception)
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error("Error fetching information from %s - %s", url, exception)
        except PermissionError as exception:
            _LOGGER.error("Permission error - %s", exception)
        except (KeyError, TypeError) as exception:
            _LOGGER.error("Error parsing information from %s - %s", url, exception)
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)

    async def async_get_version(self) -> str:
        """Get Airparif API version."""
        url = f"/version"
        response = await self.api_wrapper(url)
        return response["version"]

    async def async_get_previsions(self, insee: str) -> dict:
        """Get air quality prevision data for a city based on its INSEE code."""
        url = f"/indices/prevision/commune?insee={insee}"
        response = await self.api_wrapper(url)
        if response == {}:
            _LOGGER.error(f"City {insee} does not exist or INSEE code is invalid")
            return {"today": {}, "tomorrow": {}}
        else:
            if jsonschema.Draft7Validator(SCHEMA_PREVISIONS).is_valid(response):
                p = sorted(response[str(insee)], key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"))
                return {"today": p[0], "tomorrow": p[1] if len(p) == 2 else {}}
            else:
                _LOGGER.error("Received invalid previsions data from Airparif API")
                return {"today": {}, "tomorrow": {}}

    async def async_get_episodes(self) -> dict:
        """Get Airparif polution episodes previsions."""
        url = f"/episodes/en-cours-et-prevus"
        response = await self.api_wrapper(url)
        if jsonschema.Draft7Validator(SCHEMA_EPISODES).is_valid(response):
            return {"today": {"episode": response["jour"]["actif"]},
                    "tomorrow": {"episode": response["demain"]["actif"]}}
        else:
            _LOGGER.error("Received invalid previsions data from Airparif API")
            return {"today": {}, "tomorrow": {}}

    async def async_get_data(self, insee: str) -> dict:
        #TODO: Rework exceptions handling
        previsions = await self.async_get_previsions(insee)
        episodes = await self.async_get_episodes()
        response = {"today": previsions["today"], "tomorrow": previsions["tomorrow"]}
        response["today"].update(episodes["today"])
        response["tomorrow"].update(episodes["tomorrow"])
        return response
