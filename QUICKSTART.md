# Quick Start Guide for Beginners

This guide will help you install the NOAA Space Weather integration even if you're new to Home Assistant.

## What You'll Get

After installation, you'll have sensors showing:
- Current space weather conditions (solar storms, radiation levels)
- 3-day forecasts
- Real-time aurora activity
- And more!

## Installation Methods

### ⭐ Method 1: HACS (Easiest)

HACS is the Home Assistant Community Store - like an app store for Home Assistant.

**Step 1:** Install HACS if you haven't already
- Follow the official guide: https://hacs.xyz/docs/setup/download

**Step 2:** Add this integration
1. Open HACS in your Home Assistant
2. Click the three dots (⋮) in the top right
3. Select "Custom repositories"
4. Paste this URL: `https://github.com/BojanKV/ha-noaa-space-weather`
5. Select "Integration" as the category
6. Click "Add"
7. Click "Install" on the NOAA Space Weather card

**Step 3:** Configure it
1. Go to your Home Assistant configuration folder
   - Usually `/config/` or `~/.homeassistant/`
2. Open `configuration.yaml` in a text editor
3. Add these lines at the end:
   ```yaml
   sensor:
     - platform: space_weather
   ```
4. Save the file

**Step 4:** Restart Home Assistant
- Go to Settings → System → Restart

**Done!** Your sensors will appear as `sensor.space_weather_*`

## ✅ Verify Installation Worked

After restarting Home Assistant:

1. **Go to Developer Tools → States**
2. **Search for** `space_weather`
3. **You should see multiple sensors** (at least 18):
   - `sensor.space_weather_scale_r`
   - `sensor.space_weather_scale_s`
   - `sensor.space_weather_scale_g`
   - `sensor.space_weather_planetary_k_index`
   - `sensor.space_weather_proton_flux_10_mev`
   - And many more...

**If you don't see any sensors:**
- Wait 2-3 minutes and refresh the page
- Check Settings → System → Logs for errors containing "space_weather"
- Verify your `configuration.yaml` syntax (Settings → System → Check configuration)

## 📊 Viewing Your Data

Now that the sensors are installed, you need to add them to your dashboard:

### Quick Method: Add to Overview Dashboard

1. **Edit your dashboard** (click the pencil icon)
2. **Click "Add Card"**
3. **Select "Entities"** card type
4. **Click "Choose Entity"** and search for `space_weather`
5. **Add the sensors you want**, for example:
   ```yaml
   type: entities
   entities:
     - entity: sensor.space_weather_scale_r
       name: Radio Blackouts (R-Scale)
     - entity: sensor.space_weather_scale_s
       name: Solar Radiation (S-Scale)
     - entity: sensor.space_weather_scale_g
       name: Geomagnetic Storms (G-Scale)
     - entity: sensor.space_weather_planetary_k_index
       name: Planetary K-Index
     - entity: sensor.space_weather_proton_flux_10_mev
       name: Proton Flux
     - entity: sensor.space_weather_aurora_forecast_coverage
       name: Aurora Coverage
   ```
6. **Save** the card

### Better Method: Custom Cards (Recommended)

For a nicer visualization like the example screenshot in the README:

1. **Copy custom card files:**
   - From this repo's `dashboard/www/` folder
   - To your Home Assistant `config/www/` folder

2. **Add resources to your dashboard:**
   - Dashboard → Edit → ⋮ → **Manage resources**
   - Add these three resources:
     ```
     /local/space-weather-card.js
     /local/space-weather-24hr-max-card.js
     /local/space-weather-pred-card.js
     ```

3. **Add the custom cards:**
   - Dashboard → Edit → **Add Card** → **Manual**
   - Use these card configurations:
   
   **Current Scales Card:**
   ```yaml
   type: custom:space-weather-current
   ```
   
   **24-Hour Max Card:**
   ```yaml
   type: custom:space-weather-24hr-max
   ```
   
   **Prediction Card:**
   ```yaml
   type: custom:space-weather-prediction
   ```

See the complete example in `dashboard/example-dashboard.yml`

### 📦 Method 2: Manual Installation

**Step 1:** Download the code
- Click the green "Code" button on GitHub
- Select "Download ZIP"
- Extract the ZIP file

**Step 2:** Copy files
1. Find your Home Assistant configuration folder (usually `/config/`)
2. Create a folder called `custom_components` if it doesn't exist
3. Copy the entire `custom_components/space_weather` folder from the repository to your Home Assistant `config/custom_components/` directory
   - Final path: `config/custom_components/space_weather/`

**Step 3:** Configure it (same as HACS method above)

**Step 4:** Restart Home Assistant (same as HACS method above)

### 🚀 Method 3: Quick Install Script (Linux/Mac)

**Step 1:** Download and extract the repository (same as Manual Installation)

**Step 2:** Run the install script
```bash
cd path/to/ha-noaa-space-weather
./install.sh
```

**Step 3:** Follow the prompts and restart Home Assistant

## Optional: Enable GloTEC

GloTEC shows Total Electron Content (affects GPS and radio) for your region.

Edit your `configuration.yaml` to include your region's coordinates:

```yaml
sensor:
  - platform: space_weather
    lat_range_min: 25.0    # Your region's south border
    lat_range_max: 50.0    # Your region's north border
    lon_range_min: -125.0  # Your region's west border
    lon_range_max: -65.0   # Your region's east border
```

**Finding your coordinates:**
1. Open Google Maps
2. Find your area
3. Right-click and select coordinates
4. Use those to define a box around your region

**Example regions** are in `configuration.example.yaml`

## Troubleshooting

### "I only see an update string saying it's up-to-date"

**This is the most common issue!** The integration creates **individual sensors**, not a single status message.

❌ **Wrong:** Looking for one "space weather" entity that shows everything  
✅ **Right:** Multiple `sensor.space_weather_*` entities, each showing different data

**Solution:**
1. Go to **Developer Tools → States**
2. Search for just `space_weather` (no `sensor:` or `sensor.` prefix)
3. You should see 18+ sensors
4. Add these sensors to your dashboard (see "Viewing Your Data" above)
5. Each sensor shows different information (K-Index, scales, predictions, etc.)

### "I only see one update/sensor item"

If you only see one item when searching:

**Most Common Issue: Missing Configuration**

The integration requires configuration in `configuration.yaml`:

```yaml
sensor:
  - platform: space_weather
```

**Steps to fix:**
1. ✅ Verify files are in `config/custom_components/space_weather/`
2. ✅ Add the configuration above to `configuration.yaml`
3. ✅ Check configuration: Settings → System → Check configuration
4. ✅ Restart Home Assistant
5. ✅ Wait 2-3 minutes
6. ✅ Search Developer Tools → States for `space_weather` (no prefix)
7. ✅ Look in logs (Settings → System → Logs) for "space_weather"

**Expected log message after restart:**
- `GloTEC sensor not configured` (if no lat/lon in config)
- OR `GloTEC sensor enabled` (if lat/lon configured)

This confirms the integration loaded. If you don't see this, the configuration isn't being read.

### No sensors appearing

**Check these in order:**

### "Component not found"
- Make sure you restarted Home Assistant after installation
- Check that files are in `config/custom_components/space_weather/`

### "Invalid config"
- Check your `configuration.yaml` for typos
- Make sure indentation is correct (use spaces, not tabs)
- Validate config: Settings → System → Check configuration

### No sensors appearing
- Wait a few minutes after restart
- Check logs: Settings → System → Logs
- Search for "space_weather"

## Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Look at [configuration.example.yaml](configuration.example.yaml) for examples
- Open an issue on GitHub if you need help

## What's Next?

After installation, you can:
1. Create dashboard cards to visualize the data (see `dashboard/` folder)
2. Set up automations based on space weather conditions
3. Monitor aurora activity for your location

Enjoy monitoring space weather! ☀️🌍🛰️
