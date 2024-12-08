This is an MQTT sensor to send NOAA space weather data to Home Assistant. Fetching the data requires a login to NASA's
EarthData which is done through Selenium and the Chrome browser.

![](dashboard/dashboard.png)

## Install

1. `pip install -r requirements.txt`
2. `sudo apt-get install redis-server`
3. `sudo systemctl enable --now redis-server`

## Run

The lat/lon range is used to pick the region of the planet for generating statistics, for example your home state. To

```shell
LAT_RANGE_MIN=<lower range for lat bounding box> \
LAT_RANGE_MAX=<upper range for lat bounding box> \
LON_RANGE_MIN=<lower range for lon bounding box> \
LON_RANGE_MAX=<upper range for lon bounding box> \
MQTT_BROKER_HOST="<Home Assistant IP>" MQTT_BROKER_PORT=1883 MQTT_USERNAME="user" MQTT_PASSWORD="<password>" \
python3 mqtt.py
```

Example systemd service files are provided.

### Home Assistant MQTT Config

```yaml
- state_topic:         "space-weather/glotec"
  name:                "GloTEC"
  unit_of_measurement: "(10^16) / m^-2"
  state_class:         measurement
  unique_id:           space_weather_glotec
```

## Data

### GloTEC

<https://www.swpc.noaa.gov/experimental/glotec>

Unit: `(10^16) / m^-2`

Updated hourly.