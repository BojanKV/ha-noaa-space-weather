# Dashboard Cards for NOAA Space Weather

Custom Lovelace cards for visualizing space weather data in Home Assistant.

## Prerequisites

Before using these custom cards, ensure:
1. The NOAA Space Weather integration is installed and working
2. Sensors are visible in Developer Tools → States (search for `space_weather`)
3. You can see sensor data (if not, see main README troubleshooting)

## Install

### Step 1: Copy Files

Copy files from `www/` folder in this repo to your Home Assistant `config/www/` folder:
- `space-weather-card.js`
- `space-weather-24hr-max-card.js`
- `space-weather-pred-card.js`

Your directory structure should be:
```
config/
  www/
    space-weather-card.js
    space-weather-24hr-max-card.js
    space-weather-pred-card.js
```

### Step 2: Add Resources to Home Assistant

1. Go to your dashboard
2. Click **Edit** (pencil icon)
3. Click the **⋮** (three dots) menu
4. Select **Manage resources**
5. Click **Add Resource**
6. Add these three resources one by one:

   ```
   /local/space-weather-card.js
   ```
   Type: **JavaScript Module**

   ```
   /local/space-weather-24hr-max-card.js
   ```
   Type: **JavaScript Module**

   ```
   /local/space-weather-pred-card.js
   ```
   Type: **JavaScript Module**

## Use
## Use

### Adding Custom Cards to Your Dashboard

To add these custom cards, create a card of the **Manual** type:

1. Edit your dashboard
2. Click **Add Card**
3. Scroll down and click **Manual**
4. Paste one of the YAML configurations below
5. Click **Save**

### Available Card Types

**Current Space Weather Scales:**
```yaml
type: custom:space-weather-current
```
Shows the current R, S, and G scale values with color-coded severity.

**Predictions (1-Day Forecast):**
```yaml
type: custom:space-weather-prediction
```
Shows predictions for tomorrow's space weather conditions.

**24-Hour Maximum Scales:**
```yaml
type: custom:space-weather-24hr-max
```
Shows the maximum scale values observed in the past 24 hours.

### Alternative: Card Type Names

The cards can also be referenced using these type names:
```yaml
type: space-weather-current
```
```yaml
type: space-weather-prediction-1day
```
```yaml
type: space-weather-24hr-max
```

## Individual Sensor Cards

If you prefer not to use custom cards, you can display individual sensors using standard Home Assistant cards:

**Entities Card Example:**
```yaml
type: entities
title: Space Weather Status
entities:
  - entity: sensor.space_weather_scale_r
    name: Radio Blackouts (R)
  - entity: sensor.space_weather_scale_s
    name: Solar Radiation (S)
  - entity: sensor.space_weather_scale_g
    name: Geomagnetic Storms (G)
  - entity: sensor.space_weather_planetary_k_index
    name: Planetary K-Index
```

**Gauge Card Example (for K-Index):**
```yaml
type: gauge
entity: sensor.space_weather_planetary_k_index
name: Planetary K-Index
min: 0
max: 9
severity:
  green: 0
  yellow: 4
  red: 6
```

**History Graph Example:**
```yaml
type: history-graph
entities:
  - entity: sensor.space_weather_planetary_k_index
  - entity: sensor.space_weather_scale_r
  - entity: sensor.space_weather_scale_s
  - entity: sensor.space_weather_scale_g
hours_to_show: 24
```

## GloTEC Map

To display a visual map of GloTEC (Total Electron Content) data:

### Step 1: Enable Generic Camera Integration

1. Add this to your `configuration.yaml`:
   ```yaml
   camera:
     - platform: generic
       name: GloTEC Map
       still_image_url: https://services.swpc.noaa.gov/images/animations/glotec/100asm_urt/latest.png
       framerate: 0.00166  # 1/600 = updates approximately every 10 minutes
   ```

2. Restart Home Assistant

### Step 2: Add Camera Card to Dashboard

Create a picture entity card:
```yaml
type: picture-entity
entity: camera.glotec_map
show_state: false
show_name: false
camera_view: auto
```

### Image Source Options

**NOAA Generated Map (Recommended):**
```
https://services.swpc.noaa.gov/images/animations/glotec/100asm_urt/latest.png
```
This is the official NOAA map, updated regularly.

**Legacy Local Server (Deprecated):**
```
http://[server IP]:5000/global
```
*Note:* The local feeder service is no longer required and has been replaced by the integrated GloTEC sensor.

## Displaying GloTEC Sensor Data

If you configured the GloTEC sensor with lat/lon coordinates, you can display its numeric value:

**As an Entity:**
```yaml
type: entity
entity: sensor.space_weather_glotec
name: Total Electron Content (My Region)
icon: mdi:flash
```

**In a Graph:**
```yaml
type: history-graph
entities:
  - entity: sensor.space_weather_glotec
hours_to_show: 48
```

**Combined Card (Map + Sensor):**
```yaml
type: vertical-stack
cards:
  - type: picture-entity
    entity: camera.glotec_map
    show_state: false
    show_name: false
  - type: entity
    entity: sensor.space_weather_glotec
    name: My Region TEC
```

## Complete Example

See `example-dashboard.yml` in this folder for a complete dashboard configuration showing all sensors and cards.
