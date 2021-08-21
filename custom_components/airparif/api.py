"""Airparif API Client."""
import asyncio
import logging
import socket

import aiohttp
import async_timeout

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)


class AirparifApiClient:
    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        """Airparif API Client."""
        self._api_key = api_key
        self._session = session
        self._headers = {"Content-type": f"application/json; charset=UTF-8;", "X-Api-Key": f"{api_key}"}

    async def async_get_previsions(self, insee: str) -> dict:
        """Get air quality prevision data for a city based on its INSEE code."""
        url = f"https://api.airparif.asso.fr/indices/prevision/commune?insee={insee}"
        try:
            async with async_timeout.timeout(TIMEOUT, loop=asyncio.get_event_loop()):
                response = await self._session.get(url, headers=self._headers)
                if response.status == 200:
                    r = await response.json()
                    if r == {}:
                        raise ValueError(f"City {insee} does not exist or INSEE code is invalid")
                    return r[str(insee)]
                elif response.status == 403:
                    raise PermissionError
                else:
                    raise ValueError("Invalid request")

        except asyncio.TimeoutError as exception:
            _LOGGER.error("Timeout error fetching information from %s - %s", url, exception)
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error("Error fetching information from %s - %s", url, exception)
        except PermissionError as exception:
            _LOGGER.error("Invalid key %s", key)
        except (KeyError, TypeError) as exception:
            _LOGGER.error("Error parsing information from %s - %s", url, exception)
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
