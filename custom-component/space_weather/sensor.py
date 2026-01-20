import io
import logging
from datetime import timedelta, datetime

import aiohttp
import numpy as np
from PIL import Image
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

SCALES_URL = 'https://services.swpc.noaa.gov/products/noaa-scales.json'
SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    session = async_get_clientsession(hass)
    
    entities = [
        SpaceWeatherScaleSensor(session, 'R', '0', None),
        SpaceWeatherScaleSensor(session, 'S', '0', None),
        SpaceWeatherScaleSensor(session, 'G', '0', None),
        SpaceWeatherScaleSensor(session, 'R', '-1', '24hr_max'),
        SpaceWeatherScaleSensor(session, 'S', '-1', '24hr_max'),
        SpaceWeatherScaleSensor(session, 'G', '-1', '24hr_max'),

        SpaceWeatherPredictionSensor(session, 'R', 'MinorProb', '1', 'today'),
        SpaceWeatherPredictionSensor(session, 'R', 'MajorProb', '1', 'today'),
        SpaceWeatherPredictionSensor(session, 'S', 'Scale', '1', 'today'),
        SpaceWeatherPredictionSensor(session, 'S', 'Prob', '1', 'today'),
        SpaceWeatherPredictionSensor(session, 'G', 'Scale', '1', 'today'),
        SpaceWeatherPredictionSensor(session, 'R', 'MinorProb', '2', '1day'),
        SpaceWeatherPredictionSensor(session, 'R', 'MajorProb', '2', '1day'),
        SpaceWeatherPredictionSensor(session, 'S', 'Scale', '2', '1day'),
        SpaceWeatherPredictionSensor(session, 'S', 'Prob', '2', '1day'),
        SpaceWeatherPredictionSensor(session, 'G', 'Scale', '2', '1day'),
        SpaceWeatherPredictionSensor(session, 'R', 'MinorProb', '3', '2day'),
        SpaceWeatherPredictionSensor(session, 'R', 'MajorProb', '3', '2day'),
        SpaceWeatherPredictionSensor(session, 'S', 'Scale', '3', '2day'),
        SpaceWeatherPredictionSensor(session, 'S', 'Prob', '3', '2day'),
        SpaceWeatherPredictionSensor(session, 'G', 'Scale', '3', '2day'),

        PlanetaryKIndexSensor(session),

        ProtonFlux10MEV(session),
        ProtonFlux10MEVWarningThreshold(session),

        AuroraForecastSensor(session),
    ]
    
    # Add GloTEC sensor if configured
    lat_min = config.get('lat_range_min')
    lat_max = config.get('lat_range_max')
    lon_min = config.get('lon_range_min')
    lon_max = config.get('lon_range_max')
    
    if all(param is not None for param in [lat_min, lat_max, lon_min, lon_max]):
        entities.append(GloTECSensor(session, lat_min, lat_max, lon_min, lon_max))
        _LOGGER.info(f'GloTEC sensor enabled with lat range [{lat_min}, {lat_max}] and lon range [{lon_min}, {lon_max}]')
    else:
        _LOGGER.info('GloTEC sensor not configured. Add lat_range_min, lat_range_max, lon_range_min, lon_range_max to configuration.yaml to enable.')
    
    async_add_entities(entities, True)


class SpaceWeatherScaleSensor(Entity):
    def __init__(self, session, scale_key, data_selector, trailing):
        self._session = session
        self._scale_key = scale_key

        self._name = f'Space Weather Scale {scale_key}'
        if trailing is not None and len(trailing):
            self._name = self._name + ' ' + trailing.replace('_', ' ').replace('  ', ' ')

        self._data = None
        assert isinstance(data_selector, str)
        self._data_selector = data_selector
        self._trailing = trailing

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        s = f'space_weather_scale_{self._scale_key.lower()}'
        if self._trailing is not None and len(self._trailing):
            s = s + '_' + self._trailing.strip('_')
        return s

    @property
    def state(self):
        return int(self._data[self._scale_key]["Scale"])

    @property
    def extra_state_attributes(self):
        if self._data:
            return {
                'text': self._data[self._scale_key]['Text'],
                'timestamp': datetime.fromisoformat(self._data["DateStamp"] + 'T' + self._data["TimeStamp"] + '+00:00').isoformat(),
                'state_class': 'measurement'
            }
        return None

    @Throttle(SCAN_INTERVAL)
    async def async_update(self):
        try:
            async with self._session.get(SCALES_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    self._data = data[self._data_selector]
                else:
                    _LOGGER.error(f'Error fetching data from {SCALES_URL}')
        except aiohttp.ClientError as err:
            _LOGGER.error(f'Error fetching data from {SCALES_URL}: {err}')


class SpaceWeatherPredictionSensor(Entity):
    def __init__(self, session, scale_key, pred_key, data_selector, trailing):
        self._session = session
        self._scale_key = scale_key
        self._pred_key = pred_key
        self._data_selector = data_selector
        self._trailing = trailing
        self._name = f'Space Weather Prediction {scale_key} {pred_key} {trailing.replace("_", " ").replace("  ", " ")}'
        self._state = None
        self._data = None

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return f'space_weather_pred_{self._scale_key}_{self._pred_key}_{self._trailing}'.lower()

    @property
    def state(self):
        if self._state:
            if self._pred_key == 'Scale':
                return int(self._state)
            else:
                try:
                    return float(self._state)
                except ValueError:
                    return None
        return None

    @property
    def unit_of_measurement(self):
        if self._pred_key in ['MinorProb', 'MajorProb', 'Prob']:
            return '%'
        return None

    @property
    def extra_state_attributes(self):
        if self._data:
            return {
                'timestamp': datetime.fromisoformat(self._data["DateStamp"] + 'T' + self._data["TimeStamp"] + '+00:00').isoformat(),
                'state_class': 'measurement'
            }
        return None

    @Throttle(SCAN_INTERVAL)
    async def async_update(self):
        try:
            async with self._session.get(SCALES_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    self._data = data[self._data_selector]
                    self._state = self._data[self._scale_key][self._pred_key]
                else:
                    _LOGGER.error(f'Error fetching data from {SCALES_URL}')
        except aiohttp.ClientError as err:
            _LOGGER.error(f'Error fetching data from {SCALES_URL}: {err}')


class PlanetaryKIndexSensor(Entity):
    def __init__(self, session):
        self._session = session
        self._name = 'Space Weather Planetary K-Index'
        self._data = None

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return 'space_weather_planetary_k_index'

    @property
    def state(self):
        if self._data:
            return float(self._data['kp_index'])
        return None

    # @property
    # def device_class(self):
    #     return None

    @property
    def extra_state_attributes(self):
        if self._data:
            return {
                'kp_index': float(self._data['kp_index']),
                'estimated_kp': float(self._data['estimated_kp']),
                'timestamp': datetime.fromisoformat(self._data['time_tag']).isoformat(),
                'state_class': 'measurement'
            }
        return None

    @Throttle(SCAN_INTERVAL)
    async def async_update(self):
        try:
            async with self._session.get('https://services.swpc.noaa.gov/json/planetary_k_index_1m.json') as response:
                if response.status == 200:
                    data = await response.json()
                    self._data = data[-1]
                else:
                    _LOGGER.error(f'Error fetching data from planetary_k_index_1m.json')
        except aiohttp.ClientError as err:
            _LOGGER.error(f'Error fetching data from planetary_k_index_1m.json: {err}')


class ProtonFlux10MEV(Entity):
    """
    https://www.swpc.noaa.gov/products/goes-proton-flux
    """

    def __init__(self, session):
        self._session = session
        self._name = 'Space Weather Proton Flux 10 MeV'
        self._data = None

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return 'space_weather_proton_flux_10_mev'

    @property
    def state(self):
        if self._data:
            return round(float(self._data['flux']), 2)
        return None

    @property
    def extra_state_attributes(self):
        if self._data:
            return {
                'satellite': self._data['satellite'],
                'timestamp': datetime.fromisoformat(self._data['time_tag']).isoformat(),
                'state_class': 'measurement'
            }
        return None

    @Throttle(SCAN_INTERVAL)
    async def async_update(self):
        try:
            async with self._session.get('https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json') as response:
                if response.status == 200:
                    data = await response.json()
                    self._data = {}
                    for x in list(reversed(data)):
                        if x['energy'] == '>=10 MeV':
                            self._data = x
                            break
                else:
                    _LOGGER.error(f'Error fetching data from integral-protons-1-day.json')
        except aiohttp.ClientError as err:
            _LOGGER.error(f'Error fetching data from integral-protons-1-day.json: {err}')


class ProtonFlux10MEVWarningThreshold(Entity):
    def __init__(self, session):
        self._session = session
        self._name = 'Space Weather Proton Flux 10 MeV Warning Threshold'

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return 'space_weather_proton_flux_10_mev_warning_threshold'

    @property
    def state(self):
        return 10

    @property
    def extra_state_attributes(self):
        return {
            'state_class': 'measurement'
        }


class AuroraForecastSensor(Entity):
    def __init__(self, session):
        self._session = session
        self._name = 'Space Weather Aurora Forecast Coverage'
        self._percentage = None
        self._last_update = None
        self._url = 'https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tonights_static_viewline_forecast.png'

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return 'space_weather_aurora_forecast_coverage'

    @property
    def state(self):
        return self._percentage

    @property
    def unit_of_measurement(self):
        return '%'

    @property
    def extra_state_attributes(self):
        if self._last_update:
            return {
                'timestamp': self._last_update.isoformat(),
                'state_class': 'measurement',
                'image_url': self._url
            }
        return None

    @Throttle(SCAN_INTERVAL)
    async def async_update(self):
        try:
            async with self._session.get(self._url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image = Image.open(io.BytesIO(image_data))
                    if image.mode != 'RGB':
                        image = image.convert('RGB')

                    # Convert to numpy array
                    img_array = np.array(image)
                    target_color = np.array([224, 14, 1])  # #e00e01 in RGB

                    # Create mask for pixels matching the target color
                    # Allow small tolerance for compression artifacts
                    tolerance = 5
                    mask = np.all(np.abs(img_array - target_color) <= tolerance, axis=2)

                    # Calculate percentage
                    total_pixels = img_array.shape[0] * img_array.shape[1]
                    matching_pixels = np.sum(mask)
                    self._percentage = int((matching_pixels / total_pixels) * 100)

                    self._last_update = datetime.utcnow()

                else:
                    _LOGGER.error(f'Error fetching aurora forecast image: HTTP {response.status}')
        except aiohttp.ClientError as err:
            _LOGGER.error(f'Error fetching aurora forecast image: {err}')
        except Exception as err:
            _LOGGER.error(f'Error processing aurora forecast image: {err}')


class GloTECSensor(Entity):
    """
    Global Total Electron Content (GloTEC) sensor.
    Fetches GloTEC data from NOAA and calculates average TEC for a specified region.
    """
    
    def __init__(self, session, lat_min, lat_max, lon_min, lon_max):
        self._session = session
        self._name = 'Space Weather GloTEC'
        self._lat_min = float(lat_min)
        self._lat_max = float(lat_max)
        self._lon_min = float(lon_min)
        self._lon_max = float(lon_max)
        self._state = None
        self._last_update = None
        
        # Validate coordinate ranges
        if self._lat_min >= self._lat_max:
            raise ValueError(f'lat_range_min ({self._lat_min}) must be less than lat_range_max ({self._lat_max})')
        if self._lon_min >= self._lon_max:
            raise ValueError(f'lon_range_min ({self._lon_min}) must be less than lon_range_max ({self._lon_max})')
        if not (-90 <= self._lat_min <= 90) or not (-90 <= self._lat_max <= 90):
            raise ValueError(f'Latitude values must be between -90 and 90')
        if not (-180 <= self._lon_min <= 180) or not (-180 <= self._lon_max <= 180):
            raise ValueError(f'Longitude values must be between -180 and 180')

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return 'space_weather_glotec'

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return '10¹⁶/m²'

    @property
    def extra_state_attributes(self):
        if self._last_update:
            return {
                'timestamp': self._last_update.isoformat(),
                'state_class': 'measurement',
                'lat_range': [self._lat_min, self._lat_max],
                'lon_range': [self._lon_min, self._lon_max]
            }
        return None

    @Throttle(timedelta(minutes=30))
    async def async_update(self):
        """Fetch and process GloTEC data."""
        try:
            # Fetch the index to get the latest data URL
            async with self._session.get('https://services.swpc.noaa.gov/products/glotec/geojson_2d_urt.json') as response:
                if response.status == 200:
                    index_data = await response.json()
                    if not index_data:
                        _LOGGER.error('GloTEC index data is empty')
                        return
                    
                    latest_entry = index_data[-1]
                    data_url = 'https://services.swpc.noaa.gov' + latest_entry['url']
                    
                    # Fetch the actual GloTEC data
                    async with self._session.get(data_url) as data_response:
                        if data_response.status == 200:
                            geojson = await data_response.json()
                            
                            # Extract TEC values for the specified region
                            tec_values = []
                            for feature in geojson.get('features', []):
                                lon, lat = feature['geometry']['coordinates']
                                tec = feature['properties']['tec']
                                
                                # Check if point is within the specified region
                                if (self._lon_min <= lon <= self._lon_max and 
                                    self._lat_min <= lat <= self._lat_max):
                                    tec_values.append(tec)
                            
                            if tec_values:
                                # Filter out any NaN or invalid values
                                valid_tec_values = [v for v in tec_values if not np.isnan(v) and v >= 0]
                                
                                if valid_tec_values:
                                    # Calculate average TEC for the region
                                    avg_tec = np.mean(valid_tec_values)
                                    self._state = round(avg_tec, 1)
                                    self._last_update = datetime.utcnow()
                                    _LOGGER.debug(f'GloTEC updated: {self._state} (from {len(valid_tec_values)} valid points out of {len(tec_values)} total)')
                                else:
                                    _LOGGER.warning(f'All GloTEC data points in region were invalid')
                            else:
                                _LOGGER.warning(f'No GloTEC data points found in region lat[{self._lat_min}, {self._lat_max}], lon[{self._lon_min}, {self._lon_max}]')
                        else:
                            _LOGGER.error(f'Error fetching GloTEC data: HTTP {data_response.status}')
                else:
                    _LOGGER.error(f'Error fetching GloTEC index: HTTP {response.status}')
        except aiohttp.ClientError as err:
            _LOGGER.error(f'Error fetching GloTEC data: {err}')
        except Exception as err:
            _LOGGER.error(f'Error processing GloTEC data: {err}')
