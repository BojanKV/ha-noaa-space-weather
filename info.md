# NOAA Space Weather

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Integrate NOAA Space Weather data into your Home Assistant!

## Features

- **No external services required** - Everything runs directly in Home Assistant
- **Real-time space weather monitoring** with 5-minute updates
- **Comprehensive sensor coverage**:
  - Solar radiation scales (R, S, G)
  - Geomagnetic storm predictions
  - Planetary K-Index
  - Proton flux monitoring
  - Aurora forecast coverage
  - Global Total Electron Content (GloTEC) - Optional

## Quick Start

After installation via HACS:

1. Add to your `configuration.yaml`:
   ```yaml
   sensor:
     - platform: space_weather
   ```

2. Restart Home Assistant

3. All sensors will be available as `sensor.space_weather_*`

## Optional: Enable GloTEC

To monitor Total Electron Content for your region:

```yaml
sensor:
  - platform: space_weather
    lat_range_min: 25.0    # Southern latitude
    lat_range_max: 50.0    # Northern latitude
    lon_range_min: -125.0  # Western longitude
    lon_range_max: -65.0   # Eastern longitude
```

## Dashboard Cards

Custom Lovelace cards are available in the repository's `dashboard/www` folder for beautiful visualizations of space weather data.

See the [README](https://github.com/BojanKV/ha-noaa-space-weather) for full documentation.

## What's New in v2.0

- ✨ **GloTEC integrated** - No more external services needed!
- 🚀 **Simplified installation** - Just install and configure
- 📦 **HACS support** - Easy updates and management
- 🔧 **No MQTT, Redis, or systemd services required**

---

Data sourced from [NOAA Space Weather Prediction Center](https://www.swpc.noaa.gov/)
