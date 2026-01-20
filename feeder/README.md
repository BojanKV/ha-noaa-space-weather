# ⚠️ LEGACY - No Longer Needed

**This external feeder service is no longer required!** 

As of version 2.0, GloTEC functionality has been integrated directly into the custom component. You no longer need:
- External Python services
- Redis server
- systemd configuration
- MQTT broker setup

## Migration Guide

If you're currently using this feeder service:

1. **Uninstall the old setup:**
   ```bash
   sudo systemctl stop space-weather-cache.service space-weather-mqtt.service
   sudo systemctl disable space-weather-cache.service space-weather-mqtt.service
   ```

2. **Update the custom component** to version 2.0 or later

3. **Add GloTEC configuration** to your `configuration.yaml`:
   ```yaml
   sensor:
     - platform: space_weather
       lat_range_min: 25.0    # Use your existing LAT_RANGE_MIN value
       lat_range_max: 50.0    # Use your existing LAT_RANGE_MAX value
       lon_range_min: -125.0  # Use your existing LON_RANGE_MIN value
       lon_range_max: -65.0   # Use your existing LON_RANGE_MAX value
   ```

4. **Restart Home Assistant**

The GloTEC sensor will now work directly within Home Assistant without any external services!

---

## Old Documentation (for reference only)

This is an external service that generates GloTEC data and feeds it to Home Assistant. Originally, fetching the data
required a login to NASA's EarthData server which was only possible through Selenium and the Chrome browser. NASA has
transitioned away from VTEC to GloTEC and the data is now an easy to use JSON API. This feeder service should be
moved to a custom component someday but it works well enough for me like this.

The feeder service downloads the GloTEC data hourly and plots it on a map.

![](dashboard/dashboard.png)

## Install

1. `pip install -r requirements.txt`
2. `sudo apt-get install redis-server`
3. `sudo systemctl enable --now redis-server`
4. Start the systemd services. Examples are provided in `systemd/`

## Run

The lat/lon range is used to pick the region of the planet for generating GloTEC statistics. For example, your home
state.

```shell
LAT_RANGE_MIN=<lower range for lat bounding box> \
LAT_RANGE_MAX=<upper range for lat bounding box> \
LON_RANGE_MIN=<lower range for lon bounding box> \
LON_RANGE_MAX=<upper range for lon bounding box> \
MQTT_BROKER_HOST="<Home Assistant IP>" MQTT_BROKER_PORT=1883 MQTT_USERNAME="user" MQTT_PASSWORD="<password>" \
python3 mqtt.py
```

Example systemd service files are provided. Your environment variables should go in `/etc/secrets/space-weather`

### Home Assistant MQTT Config

```yaml
- state_topic: "space-weather/glotec"
  name: "GloTEC"
  unit_of_measurement: "(10^16) / m^-2"
  state_class: measurement
  unique_id: space_weather_glotec
``