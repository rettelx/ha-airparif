"""Airparif API client (stateless)."""

from __future__ import annotations

import re

import aiohttp
import async_timeout

API_ROOT = "https://api.airparif.asso.fr"
TIMEOUT = 10

_INSEE_RE = re.compile(r"^\d{5}$")


class AirparifApiClient:
    """Minimal async client for Airparif endpoints."""

    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        self._session = session
        self._headers = {
            "Accept": "application/json",
            "X-Api-Key": api_key,
        }

    async def _get_json(self, path: str, params: dict | None = None) -> dict:
        async with async_timeout.timeout(TIMEOUT):
            async with self._session.get(
                f"{API_ROOT}{path}", headers=self._headers, params=params
            ) as resp:
                if resp.status == 403:
                    raise ValueError("Invalid API key")
                if resp.status != 200:
                    raise RuntimeError(f"HTTP {resp.status}")
                return await resp.json(content_type=None)

    async def get_previsions(self, insee: str) -> dict:
        if not _INSEE_RE.match(insee):
            raise ValueError("Invalid INSEE code")
        return await self._get_json("/indices/prevision/commune", params={"insee": insee})

    async def get_episodes(self) -> dict:
        return await self._get_json("/episodes/en-cours-et-prevus")

    async def get_version(self) -> str:
        data = await self._get_json("/version")
        return data.get("version", "unknown")
