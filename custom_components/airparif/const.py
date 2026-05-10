"""Constants for the Airparif integration."""

from __future__ import annotations

DOMAIN = "airparif"

# Config entry keys
CONF_API_KEY = "api_key"
CONF_INSEE = "insee"

# Day buckets
DAY_TODAY = "today"
DAY_TOMORROW = "tomorrow"

# Shared attributes
ATTR_DAY = "day"
ATTR_EPISODE = "episode"
ATTR_COLOR = "airparif_color"
ATTR_LABEL = "label"  # keep the qualitative label on numeric sensors
ATTRIBUTION = "Data provided by Airparif"

# Official Airparif colors
AQI_COLORS = {
    "Bon": "#50f0e6",
    "Moyen": "#50ccaa",
    "Dégradé": "#f0e641",
    "Mauvais": "#ff5050",
    "Très Mauvais": "#960032",
    "Extrêmement Mauvais": "#7d2181",
}

# Qualitative -> numeric mapping used by derived AQI numeric sensors
QUALI_TO_NUM = {
    "Bon": 1,
    "Moyen": 2,
    "Dégradé": 3,
    "Mauvais": 4,
    "Très Mauvais": 5,
    "Extrêmement Mauvais": 6,
}

# API field mapping for qualitative sensors
FIELDS = {
    "aqi": "indice",
    "no2": "no2",
    "o3": "o3",
    "pm10": "pm10",
    "pm25": "pm25",
    "so2": "so2",
}

# Icons per pollutant
ICONS = {
    "aqi": "mdi:blur",
    "no2": "mdi:molecule",
    "o3": "mdi:weather-sunny-alert",
    "pm10": "mdi:chart-bubble",
    "pm25": "mdi:chart-bubble",
    "so2": "mdi:cloud-alert",
}

# Translation keys for qualitative sensors (pollutant x day)
SENSOR_KEYS = {
    ("aqi", DAY_TODAY): "aqi_today",
    ("aqi", DAY_TOMORROW): "aqi_tomorrow",
    ("no2", DAY_TODAY): "no2_today",
    ("no2", DAY_TOMORROW): "no2_tomorrow",
    ("o3", DAY_TODAY): "o3_today",
    ("o3", DAY_TOMORROW): "o3_tomorrow",
    ("pm10", DAY_TODAY): "pm10_today",
    ("pm10", DAY_TOMORROW): "pm10_tomorrow",
    ("pm25", DAY_TODAY): "pm25_today",
    ("pm25", DAY_TOMORROW): "pm25_tomorrow",
    ("so2", DAY_TODAY): "so2_today",
    ("so2", DAY_TOMORROW): "so2_tomorrow",
}

# Translation keys for derived numeric AQI sensors
NUMERIC_KEYS = {
    DAY_TODAY: "aqi_numeric_today",
    DAY_TOMORROW: "aqi_numeric_tomorrow",
}

# Translation keys for binary sensors
BINARY_KEYS = {
    DAY_TODAY: "pollution_episode_today",
    DAY_TOMORROW: "pollution_episode_tomorrow",
}
