# ha-noaa-space-weather

_NOAA space weather data in Home Assistant._

I work in a field that is affected by space weather and wanted an easy way to tell at a glance if something funny is
going on up there. This is a plugin for Home Assistant that adds space weather data and predictions to your dashboard.
Data is sourced from the NOAA Space Weather Prediction Center.

![example dashboard](dashboard/example-dashboard.jpg)

## 🚀 New to Home Assistant or this integration?

Check out the **[Quick Start Guide](QUICKSTART.md)** for step-by-step beginner-friendly instructions!

## ✨ Simplified Installation

This component has been streamlined for easy deployment. **No external services, MQTT, or Redis required!**

### Option 1: HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots in the top right corner
3. Select "Custom repositories"
4. Add this repository URL: `https://github.com/BojanKV/ha-noaa-space-weather`
5. Select category: "Integration"
6. Click "Install"
7. Restart Home Assistant
8. Add to your `configuration.yaml` (see Configuration section below)

### Option 2: Manual Installation

1. Copy the `custom_components/space_weather` folder from this repository to your Home Assistant `config/custom_components` directory
   - Final path should be: `config/custom_components/space_weather/`
2. Restart Home Assistant
3. Add to your `configuration.yaml` (see Configuration section below)

## ⚙️ Configuration

Add this to your `configuration.yaml`:

### Basic Configuration (without GloTEC)

```yaml
sensor:
  - platform: space_weather
```

This will provide all sensors except GloTEC (Solar Scales, Predictions, K-Index, Proton Flux, Aurora Forecast).

### Full Configuration (with GloTEC)

To enable the GloTEC sensor, you need to specify your geographic region of interest:

```yaml
sensor:
  - platform: space_weather
    lat_range_min: 25.0    # Southern boundary of your region
    lat_range_max: 50.0    # Northern boundary of your region
    lon_range_min: -125.0  # Western boundary of your region
    lon_range_max: -65.0   # Eastern boundary of your region
```

**Finding Your Coordinates:**
- Use a map service to find the latitude and longitude boundaries of your region
- For the USA: approximately lat 25-50, lon -125 to -65
- For Europe: approximately lat 35-70, lon -10 to 40

After adding the configuration, restart Home Assistant.

## 👁️ Viewing Your Data

After installation and restart, the integration creates multiple sensors. Here's how to view them:

### Finding Your Sensors

1. Go to **Developer Tools** > **States** in Home Assistant
2. Search for `sensor.space_weather` to see all available sensors
3. You should see entities like:
   - `sensor.space_weather_scale_r`
   - `sensor.space_weather_scale_s`
   - `sensor.space_weather_scale_g`
   - `sensor.space_weather_planetary_k_index`
   - `sensor.space_weather_proton_flux_10_mev`
   - And many more (see complete list below)

### Adding Sensors to Your Dashboard

**Option 1: Using Built-in Cards**

1. Edit your dashboard
2. Click **Add Card**
3. Select **Entities** card
4. Add the sensors you want to display

Example configuration:
```yaml
type: entities
entities:
  - entity: sensor.space_weather_scale_r
    name: Radio Blackouts
  - entity: sensor.space_weather_scale_s
    name: Solar Radiation
  - entity: sensor.space_weather_scale_g
    name: Geomagnetic Storms
  - entity: sensor.space_weather_planetary_k_index
    name: K-Index
  - entity: sensor.space_weather_proton_flux_10_mev
    name: Proton Flux
  - entity: sensor.space_weather_aurora_forecast_coverage
    name: Aurora Coverage
```

**Option 2: Using Custom Cards** (Recommended for better visualization)

See the [Dashboard Cards](#-dashboard-cards) section below for custom Lovelace cards.

### Complete Sensor List

All available sensor entity IDs:

**Current Scales:**
- `sensor.space_weather_scale_r` - Radio Blackouts (current)
- `sensor.space_weather_scale_s` - Solar Radiation Storms (current)
- `sensor.space_weather_scale_g` - Geomagnetic Storms (current)

**24-hour Maximum Scales:**
- `sensor.space_weather_scale_r_24hr_max`
- `sensor.space_weather_scale_s_24hr_max`
- `sensor.space_weather_scale_g_24hr_max`

**Predictions (Today):**
- `sensor.space_weather_prediction_r_minorprob_today`
- `sensor.space_weather_prediction_r_majorprob_today`
- `sensor.space_weather_prediction_s_scale_today`
- `sensor.space_weather_prediction_s_prob_today`
- `sensor.space_weather_prediction_g_scale_today`

**Predictions (1-Day Forecast):**
- `sensor.space_weather_prediction_r_minorprob_1day`
- `sensor.space_weather_prediction_r_majorprob_1day`
- `sensor.space_weather_prediction_s_scale_1day`
- `sensor.space_weather_prediction_s_prob_1day`
- `sensor.space_weather_prediction_g_scale_1day`

**Predictions (2-Day Forecast):**
- `sensor.space_weather_prediction_r_minorprob_2day`
- `sensor.space_weather_prediction_r_majorprob_2day`
- `sensor.space_weather_prediction_s_scale_2day`
- `sensor.space_weather_prediction_s_prob_2day`
- `sensor.space_weather_prediction_g_scale_2day`

**Real-time Data:**
- `sensor.space_weather_planetary_k_index` - Updated every 5 minutes
- `sensor.space_weather_proton_flux_10_mev`
- `sensor.space_weather_proton_flux_10_mev_warning_threshold`
- `sensor.space_weather_aurora_forecast_coverage`

**Regional Data (if configured):**
- `sensor.space_weather_glotec` - Total Electron Content for your region

## 📊 Available Sensors

The integration provides the following sensors:

### NOAA Space Weather Scales (Current & 24hr Max)
- **R-Scale**: Radio Blackouts
- **S-Scale**: Solar Radiation Storms  
- **G-Scale**: Geomagnetic Storms

### Predictions (Today, 1-day, 2-day)
- Solar radiation probabilities
- Geomagnetic storm forecasts
- Radio blackout predictions

### Real-time Data
- **Planetary K-Index**: Updated every 5 minutes
- **Proton Flux (10 MeV)**: Solar particle levels
- **Aurora Forecast Coverage**: Percentage of aurora coverage
- **GloTEC**: Global Total Electron Content for your region (optional)

## 🎨 Dashboard Cards

Custom Lovelace cards are available in the `dashboard/www` folder.

1. Copy files from `dashboard/www/` to your `config/www/` folder
2. In your dashboard: `Edit` → `⋮` → `Manage resources`
3. Add these resources:
   ```
   /local/space-weather-card.js
   /local/space-weather-24hr-max-card.js
   /local/space-weather-pred-card.js
   ```
4. Add cards to your dashboard using Manual card type:
   ```yaml
   type: space-weather-current
   ```
   ```yaml
   type: space-weather-24hr-max
   ```
   ```yaml
   type: space-weather-prediction-1day
   ```

See `dashboard/README.md` for more details.

## 🔧 Troubleshooting

### "I only see 'up-to-date' or a status string, not the actual data"

This is a common issue! The integration creates **multiple individual sensors**, not a single status entity. After installation:

1. **Don't look for one "space weather" entity** - the integration provides 18+ separate sensors
2. **Add individual sensors** to your dashboard:
   - Go to **Developer Tools** > **States**
   - Search for `space_weather`
   - You'll see 18+ individual sensors (or 19+ if GloTEC is enabled)
   - Add these sensors to your dashboard using an Entities card or custom cards
3. **Use the custom cards** for the best experience (see Dashboard Cards section)
4. **Example:** Instead of looking for one "space weather" entity, you should see separate entities for K-Index, each scale, predictions, etc.

### "No sensors appearing after installation"

1. **Check that you restarted** Home Assistant after adding the configuration
2. **Verify configuration** is correct in `configuration.yaml`:
   ```yaml
   sensor:
     - platform: space_weather
   ```
3. **Check the logs**: Settings → System → Logs, search for "space_weather"
4. **Wait a few minutes** - sensors need time to fetch initial data from NOAA
5. **Verify entity IDs**: Go to Developer Tools → States and search for `space_weather`

### "Configuration errors or sensor not loading"

- Ensure proper YAML indentation (use spaces, not tabs)
- Make sure the `sensor:` section in `configuration.yaml` is properly formatted
- For GloTEC: verify lat/lon coordinates are valid (-90 to 90 for lat, -180 to 180 for lon)
- Run **Check Configuration** before restarting: Settings → System → Check configuration

### "Sensors show 'Unknown' or 'Unavailable'"

- Check your internet connection - data comes from NOAA servers
- Wait for the next update cycle (sensors update every 5 minutes)
- Check Home Assistant logs for specific error messages
- Verify NOAA services are operational: https://www.swpc.noaa.gov/

### "GloTEC sensor not showing up"

- Ensure you've added the lat/lon configuration parameters (see Configuration section)
- Check that your coordinates are valid and in the correct format
- Verify you've restarted Home Assistant after adding the configuration
- Check logs for any GloTEC-specific errors

## 🔗 Related Projects

Works well with [tcarwash/home-assistant_noaa-space-weather](https://github.com/tcarwash/home-assistant_noaa-space-weather). Both provide Planetary K-Index, but this integration is updated every 5 minutes. SWPC publishes new data every 1 minute.

## 📚 References

- GloTEC: <https://www.swpc.noaa.gov/products/glotec>
- GloTEC Technical: <https://www.gps.gov/cgsic/meetings/2023/fang.pdf>
- NOAA Space Weather Scales: <https://www.swpc.noaa.gov/noaa-scales-explanation>

## 📁 Legacy Components

The `feeder/` directory contains the legacy external service implementation that required Redis, MQTT, and systemd services. **This is no longer needed** as GloTEC functionality is now integrated directly into the custom component.
