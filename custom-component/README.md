# Space Weather Custom Component

This is the Home Assistant custom component for NOAA Space Weather data.

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots in the top right corner
3. Select "Custom repositories"
4. Add this repository URL: `https://github.com/BojanKV/ha-noaa-space-weather`
5. Select category: "Integration"
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `space_weather` folder to your Home Assistant `config/custom_components` directory
   - Full path: `config/custom_components/space_weather/`
2. Restart Home Assistant

## Configuration

Add to your `configuration.yaml`:

### Basic (without GloTEC)
```yaml
sensor:
  - platform: space_weather
```

### With GloTEC (optional)
```yaml
sensor:
  - platform: space_weather
    lat_range_min: 25.0    # Your region's southern latitude
    lat_range_max: 50.0    # Your region's northern latitude
    lon_range_min: -125.0  # Your region's western longitude
    lon_range_max: -65.0   # Your region's eastern longitude
```

The GloTEC sensor calculates the average Total Electron Content for your specified geographic region.

## Available Sensors

All sensors are automatically created:

- Space Weather Scales (R, S, G) - Current values
- Space Weather Scales (R, S, G) - 24hr maximum
- Predictions for Today, 1-day, and 2-day forecasts
- Planetary K-Index (updated every 5 minutes)
- Proton Flux 10 MeV
- Aurora Forecast Coverage
- GloTEC (if configured)

After restarting Home Assistant, all sensors will be available with the `sensor.space_weather_*` entity IDs.
