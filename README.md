[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Homeassistant Airparif integration</h3>

  <p align="center">
    Create Airparif previsions sensors in Homeassistant
    <br />
    <br />
    <a href="https://github.com/rettelx/ha-airparif/issues">Report Bug</a>
    ·
    <a href="https://github.com/rettelx/ha-airparif/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project provides an **unofficial** Homeassistant integration for Airparif data.

This integration retrieves the data from the official Airparif API and requires an official API key obtainable from Airparif [on this page](https://www.airparif.asso.fr/interface-de-programmation-applicative).

<!-- GETTING STARTED -->
## Getting Started

To get up and running follow these simple steps.

### Prerequisites

You need to know the INSEE code for the cities you want to integrate.

Note that the INSEE code is **different from the city postal code**.

It can be found [on the INSEE website](https://www.insee.fr/fr/information/5057840) or with a quick Google search.

For instance, Paris' first arrondissement INSEE code is 75101.

### Installation

1. Copy the ```custom_components/airparif``` folder into your ```custom_components``` folder.

2. Add the following configuration in your configuration file:
```yaml
sensor:
  - platform: airparif
    token: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    locations:
      - 75101
      - 75102
```

4. Restart your Homeassistant instance.

## Usage
A sensor is created for each location defined in the configuration.

For now, the integration provides pollution indexes for the current and the next day:

```yaml
date: '2021-08-21'
tomorrow_date: '2021-08-22'
pm_2_5: Bon
tomorrow_pm_2_5: Bon
pm_10: Bon
tomorrow_pm_10: Bon
ozone: Moyen
tomorrow_ozone: Moyen
nitrogen_dioxide: Moyen
tomorrow_nitrogen_dioxide: Moyen
sulfur_dioxide: Bon
tomorrow_sulfur_dioxide: Bon
aqi: Moyen
tomorrow_aqi: Moyen
friendly_name: Airparif 75056
```

<!-- ROADMAP -->
## Roadmap
See the [open issues](https://github.com/rettelx/ha-airparif/issues) for a list of proposed features (and known issues).
<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
This repository is based on:
* The official [WAQI integration](https://github.com/home-assistant/core/tree/dev/homeassistant/components/waqi)
* The [custom_component/integration_blueprint](![img.png](img.png)) project





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/rettelx/ha-airparif.svg?style=for-the-badge
[contributors-url]: https://github.com/rettelx/ha-airparif/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/rettelx/ha-airparif.svg?style=for-the-badge
[forks-url]: https://github.com/rettelx/ha-airparif/network/members
[stars-shield]: https://img.shields.io/github/stars/rettelx/ha-airparif.svg?style=for-the-badge
[stars-url]: https://github.com/rettelx/ha-airparif/stargazers
[issues-shield]: https://img.shields.io/github/issues/rettelx/ha-airparif.svg?style=for-the-badge
[issues-url]: https://github.com/rettelx/ha-airparif/issues
[license-shield]: https://img.shields.io/github/license/rettelx/ha-airparif.svg?style=for-the-badge
[license-url]: https://github.com/rettelx/ha-airparif/blob/master/LICENSE.txt
