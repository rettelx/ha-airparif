"""DataUpdateCoordinator for Airparif."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable
from datetime import date, timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import AirparifApiClient
from .const import DAY_TODAY, DAY_TOMORROW

_LOGGER = logging.getLogger(__name__)


async def _optional[T](name: str, request: Awaitable[T]) -> T | None:
    """Return None instead of raising, so only this request's entities go unavailable."""
    try:
        return await request
    except Exception as err:
        _LOGGER.warning("Airparif %s request failed: %s", name, err)
        return None


def _episode_active(episodes: dict | None, day_key: str) -> bool | None:
    if episodes is None:
        return None
    return bool(episodes.get(day_key, {}).get("actif"))


class AirparifCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator fetching and normalizing Airparif data."""

    def __init__(self, hass, client: AirparifApiClient, insee: str) -> None:
        self.client = client
        self.insee = insee
        super().__init__(
            hass,
            _LOGGER,
            name=f"Airparif {insee}",
            update_interval=timedelta(hours=6),
        )

    async def _async_update_data(self) -> dict:
        try:
            previsions, episodes, version = await asyncio.gather(
                self.client.get_previsions(self.insee),
                _optional("episodes", self.client.get_episodes()),
                _optional("version", self.client.get_version()),
            )
        except Exception as err:
            raise UpdateFailed(str(err)) from err

        previs_list = previsions.get(self.insee, [])

        by_date: dict[date, dict] = {}
        for item in previs_list:
            try:
                d = date.fromisoformat(item.get("date"))
            except Exception:
                continue
            by_date[d] = item

        today_date = date.today()
        tomorrow_date = today_date + timedelta(days=1)

        today = by_date.get(today_date, {})
        tomorrow = by_date.get(tomorrow_date, {})

        return {
            "version": version,
            DAY_TODAY: {**today, "episode": _episode_active(episodes, "jour")},
            DAY_TOMORROW: {**tomorrow, "episode": _episode_active(episodes, "demain")},
        }
