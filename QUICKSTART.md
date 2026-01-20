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

### 📦 Method 2: Manual Installation

**Step 1:** Download the code
- Click the green "Code" button on GitHub
- Select "Download ZIP"
- Extract the ZIP file

**Step 2:** Copy files
1. Find your Home Assistant configuration folder (usually `/config/`)
2. Create a folder called `custom_components` if it doesn't exist
3. Create a `space_weather` folder inside `custom_components`
4. Copy the integration files (`__init__.py`, `const.py`, `manifest.json`, `sensor.py`) from the repository root to `config/custom_components/space_weather/`
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
