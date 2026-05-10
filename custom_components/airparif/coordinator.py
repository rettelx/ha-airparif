"""DataUpdateCoordinator for Airparif."""

from __future__ import annotations

import asyncio
import logging
from datetime import date, timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import AirparifApiClient
from .const import DAY_TODAY, DAY_TOMORROW

_LOGGER = logging.getLogger(__name__)


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
                self.client.get_episodes(),
                self.client.get_version(),
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
            DAY_TODAY: {**today, "episode": bool(episodes.get("jour", {}).get("actif"))},
            DAY_TOMORROW: {**tomorrow, "episode": bool(episodes.get("demain", {}).get("actif"))},
        }
