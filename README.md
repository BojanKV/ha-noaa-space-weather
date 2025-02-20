# ha-noaa-space-weather

_NOAA space weather data in Home Assistant._

I work in a field that is affected by space weather and wanted an easy way to tell at a glance if something funny is
going on up there. This is a plugin for Home Assistant that adds space weather data and predictions to your dashboard.
Data is sourced from the NOAA Space Weather Prediction Center.

Works well
with [tcarwash/home-assistant_noaa-space-weather](https://github.com/tcarwash/home-assistant_noaa-space-weather). Both
this and `tcarwash/home-assistant_noaa-space-weather` both provide Planetary K-Index, but ours is updated every 5
minutes. SWPC publishes new data every 1 minute.

Individual components have their own README files. See `custom-component/`, `dashboard/`, and `feeder/` for install
instructions.

<br><br>

![example dashboard](dashboard/example-dashboard.jpg)
