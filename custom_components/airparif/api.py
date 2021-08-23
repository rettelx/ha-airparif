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

VALUE_ENUM = ["Bon", "Moyen", "Dégradé", "Mauvais", "Très Mauvais", "Extrêmement Mauvais"]

SCHEMA = {
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


class AirparifApiClient:
    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        """Airparif API Client."""
        self._api_key = api_key
        self._session = session
        self._headers = {"Content-type": f"application/json; charset=UTF-8;", "X-Api-Key": f"{api_key}"}

    async def async_get_previsions(self, insee: str) -> list:
        """Get air quality prevision data for a city based on its INSEE code."""
        url = f"https://api.airparif.asso.fr/indices/prevision/commune?insee={insee}"
        try:
            async with async_timeout.timeout(TIMEOUT, loop=asyncio.get_event_loop()):
                response = await self._session.get(url, headers=self._headers)
                if response.status == 200:
                    r = await response.json()
                    if r == {}:
                        raise ValueError(f"City {insee} does not exist or INSEE code is invalid")
                    else:
                        if jsonschema.Draft7Validator(SCHEMA).is_valid(r):
                            return sorted(r[str(insee)], key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"))
                        else:
                            raise ValueError("Invalid data received from Airparif API")
                elif response.status == 403:
                    raise PermissionError
                else:
                    raise ValueError(f"Invalid request: {response.status}")

        except asyncio.TimeoutError as exception:
            _LOGGER.error("Timeout error fetching information from %s - %s", url, exception)
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error("Error fetching information from %s - %s", url, exception)
        except PermissionError as exception:
            _LOGGER.error("Invalid API key %s", self._api_key)
        except (KeyError, TypeError) as exception:
            _LOGGER.error("Error parsing information from %s - %s", url, exception)
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
