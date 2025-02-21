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