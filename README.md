
# Airparif – Home Assistant Integration (Unofficial)

[![GH-release](https://img.shields.io/github/v/release/rettelx/ha-airparif.svg?style=flat-square)](https://github.com/rettelx/ha-airparif/releases)
[![GH-downloads](https://img.shields.io/github/downloads/rettelx/ha-airparif/total?style=flat-square)](https://github.com/rettelx/ha-airparif/releases)
[![GH-last-commit](https://img.shields.io/github/last-commit/rettelx/ha-airparif.svg?style=flat-square)](https://github.com/rettelx/ha-airparif/commits/main)
[![GH-code-size](https://img.shields.io/github/languages/code-size/rettelx/ha-airparif.svg?color=red&style=flat-square)](https://github.com/rettelx/ha-airparif)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://github.com/hacs)
## 📌 Overview

This is an **unofficial** Home Assistant integration that lets you monitor **air quality forecasts in Île-de-France** directly from Home Assistant, using official Airparif data.

This Home Assistant integration is **not developed, maintained, or supported by Airparif**.  
It is a community-driven project that relies on the **public Airparif API**, with no official affiliation.


The integration works **per municipality**, identified by its **INSEE code** (⚠️usually different from its postcode).

---

## ✅ Features

### 🌫️ Air quality sensors (qualitative)
For **today** and **tomorrow**:
- Global Air Quality Index (AQI / Airparif index)
- NO₂ (Nitrogen dioxide)
- O₃ (Ozone)
- PM10
- PM2.5
- SO₂ (Sulfur dioxide)

Values are **qualitative** (`Good`, `Average`, `Degraded`, etc.), following the official Airparif scale.

---

### 📊 Numeric AQI sensors (derived)
- Converts qualitative AQI into a **numeric value (1–6)**
- Designed for **graphs, statistics, thresholds, and automations**
- The qualitative label is preserved as an **attribute**

---

### 🚨 Pollution episode sensors
- Indicates whether a **pollution episode is active**
- Available for today and tomorrow
- Implemented as `binary_sensor` entities

---

### 🧩 Diagnostic sensor
- Exposes the current **Airparif API version**

---



## 🔧 Installation via HACS (recommended)

### 1️⃣ Add the custom repository

1. Open **HACS**
2. Go to **⋮ → Custom repositories**
3. Add:
   - **Repository**:
     ```
     https://github.com/rettelx/ha-airparif
     ```
   - **Category**: `Integration`

---

### 2️⃣ Install the integration

1. In **HACS → Integrations**
2. Search for **Airparif**
3. Click **Download**
4. Restart Home Assistant

---

### 3️⃣ Configure the integration

1. Go to **Settings → Devices & Services**
2. Click **Add integration**
3. Search for **Airparif**
4. Enter:
   - ✅ Airparif API key
   - ✅ Municipality INSEE code (5 digits)

⚠️The INSEE code of your municipality is usually **NOT** equal to its postcode.

You can retrieve the proper code [here](https://www.insee.fr/fr/recherche/recherche-geographique?debut=0) and selecting the "Commune" filter.


---

## 🔑 Useful link

- Airparif API access request:  
  https://www.airparif.fr/interface-de-programmation-applicative

---

## 📄 License

This project is released under the **MIT License**.

---

## 🤝 Disclaimer & contributions

This is a **community, unofficial project**.
Issues, suggestions, and pull requests are welcome via GitHub.

Please note:
- Airparif does not provide support for this integration
- API availability and data accuracy depend entirely on Airparif services
