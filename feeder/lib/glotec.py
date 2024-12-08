import logging
import time
import traceback

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import requests
from dateutil.parser import parse
from dateutil.tz import tzutc, tzlocal
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import griddata


def get_latest_glotec():
    try:
        r = requests.get('https://services.swpc.noaa.gov/experimental/products/glotec/geojson_2d_urt.json')
        r.raise_for_status()
        index_json = r.json()[-1]
        data_url = 'https://services.swpc.noaa.gov' + index_json['url']
        r2 = requests.get(data_url)
        r2.raise_for_status()
        return r2.json()
    except:
        logging.basicConfig()
        logger = logging.getLogger(__name__)
        logger.error(traceback.format_exc())
        return None


def plot_glotec_map(data: dict, lon_range: list, lat_range: list):
    lons = []
    lats = []
    tec_values = []
    for feature in data['features']:
        lon, lat = feature['geometry']['coordinates']
        tec = feature['properties']['tec']
        lons.append(lon)
        lats.append(lat)
        tec_values.append(tec)

    lons = np.array(lons)
    lats = np.array(lats)
    tec_values = np.array(tec_values)

    lon_grid, lat_grid = np.meshgrid(np.linspace(lon_range[0], lon_range[1], 100), np.linspace(lat_range[0], lat_range[1], 100))

    # Interpolate the TEC values onto the regular grid
    tec_grid = griddata((lons, lats), tec_values, (lon_grid, lat_grid), method='linear')

    proj = ccrs.PlateCarree()
    f, ax = plt.subplots(1, 1, subplot_kw=dict(projection=proj))

    colors = ['#33184a', '#4454c3', '#4294ff', '#1ad2d2', '#3cf58e', '#9cfe40', '#dde037', '#fdac34', '#f26014', '#ca2a04', '#7A0403']
    custom_cmap = LinearSegmentedColormap.from_list('custom', colors)

    h = ax.pcolormesh(lon_grid, lat_grid, tec_grid, cmap=custom_cmap, vmin=0, vmax=100, transform=proj)

    ax.coastlines()

    timestamp_utc = parse(data['time_tag'])
    timestamp_local = timestamp_utc.replace(tzinfo=tzutc()).astimezone(tzlocal())
    plt.title(timestamp_local.strftime(f'%H:%M %m-%d-%Y {time.tzname[0]}'), fontsize=12, y=1.04)

    plt.suptitle('Global Total Electron Content', fontsize=16, y=0.87)
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size='5%', pad=0.1, axes_class=plt.Axes)
    f.add_axes(ax_cb)
    cb = plt.colorbar(h, cax=ax_cb)
    plt.rc('text', usetex=True)
    cb.set_label('VTEC ($10^{16}*\\mathrm{m}^{-2}$)')

    return tec_grid, plt
