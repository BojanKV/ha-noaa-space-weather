import gc
import logging
import os
import pickle
import sys
import time
from datetime import datetime, timezone

import numpy as np
import paho.mqtt.client as mqtt
from dateutil.parser import parse
from redis import Redis

from lib.glotec import plot_glotec_map

logging.basicConfig(level=logging.INFO)

MQTT_BROKER_HOST = os.getenv('MQTT_BROKER_HOST', '')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', 1883))
MQTT_CLIENT_ID = os.getenv('MQTT_CLIENT_ID', 'space_weather')
MQTT_USERNAME = os.getenv('MQTT_USERNAME', '')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', '')
MQTT_TOPIC_PREFIX = os.getenv('MQTT_TOPIC_PREFIX', 'space-weather')

LAT_RANGE_MIN = os.getenv('LAT_RANGE_MIN')
LAT_RANGE_MAX = os.getenv('LAT_RANGE_MAX')
LON_RANGE_MIN = os.getenv('LON_RANGE_MIN')
LON_RANGE_MAX = os.getenv('LON_RANGE_MAX')
if not LAT_RANGE_MIN or not LAT_RANGE_MAX or not LON_RANGE_MIN or not LON_RANGE_MAX:
    logging.critical('Must set LAT_RANGE_MIN, LAT_RANGE_MAX, LON_RANGE_MIN, and LON_RANGE_MAX environment variables')
    print(LAT_RANGE_MIN, LAT_RANGE_MAX, LON_RANGE_MIN, LON_RANGE_MAX)
    sys.exit(1)

client = mqtt.Client(client_id=MQTT_CLIENT_ID)
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.will_set(MQTT_TOPIC_PREFIX + '/status', payload='Offline', qos=1, retain=True)
client.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT)
client.loop_start()


def publish(topic: str, msg):
    topic_expanded = MQTT_TOPIC_PREFIX + '/' + topic
    retries = 10
    for i in range(retries):  # retry
        result = client.publish(topic_expanded, msg)
        status = result[0]
        if status == 0:
            logging.info(f'Sent {msg} to topic {topic_expanded}')
            return
        else:
            logging.warning(f'Failed to send message to topic {topic_expanded}: {result}. Retry {i + 1}/{retries}')
            time.sleep(10)
    logging.error(f'Failed to send message to topic {topic_expanded}.')


def main():
    redis = Redis(host='localhost', port=6379, db=0)

    while True:
        data = redis.get('glotec')
        while data is None:
            logging.warning('Redis has not been populated yet. Is cache.py running? Sleeping 10s...')
            time.sleep(10)
            data = redis.get('glotec')
        geojson = pickle.loads(data)

        utc_hr = datetime.now(timezone.utc).hour
        logging.info(f'Using hour {utc_hr}')

        glotec_map_ranged, _ = plot_glotec_map(geojson, [float(LON_RANGE_MIN), float(LON_RANGE_MAX)], [float(LAT_RANGE_MIN), float(LAT_RANGE_MAX)])
        avg_tec = np.mean(glotec_map_ranged)
        logging.info(f'Data timestamp: {parse(geojson["time_tag"]).isoformat()}')
        latest = round(avg_tec, 1)
        publish('glotec', latest)

        del data
        del geojson
        del glotec_map_ranged
        del avg_tec
        del latest
        gc.collect()

        time.sleep(60)


if __name__ == '__main__':
    main()
