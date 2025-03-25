import logging
import pickle
import time

from redis import Redis

from lib.glotec import get_latest_glotec

logging.basicConfig(level=logging.INFO)


def main():
    redis = Redis(host='localhost', port=6379, db=0)
    while True:
        logging.info('Fetching latest GLOTEC data')
        geojson = get_latest_glotec()
        redis.set('glotec', pickle.dumps(geojson))
        logging.info('Scrape complete')
        if geojson is None:
            logging.info('Sleeping for 120s due to error...')
            time.sleep(120)
        else:
            logging.info('Sleeping for 30 minutes...')
            time.sleep(1800)  # 30 minutes


if __name__ == '__main__':
    main()
