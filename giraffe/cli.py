""" Command-line-interface entrypoint for Docker """

import argparse
import logging, time, datetime
from itertools import islice
from functools import reduce
from operator import add

from . import available
from . import ingested
from . import docstore
from . import cfg
from . import logger
from . import funcs as f
from . import landsat
from . import location


def parse_args(defaults=None):
    defaults = defaults or dict()
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=['run'])
    defaults.update(vars(parser.parse_args()))
    return defaults


def configure_log(level='WARNING'):
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)


def start_crawl(start=None, end=None, fmt='%Y-%m-%d', offset=-1):
    if not start:
        try:
            start = docstore.sorted(cfg.get('ard')['ES_HOST'], cfg.get('ard')['ES_INDEX'], 'date_acquired')[:10]
            if end == start:
                return None
        except Exception as e:
            logger.error(e)
            start = '1900-01-01'
    logger.warning('*** Start crawl: {} End: {}'.format(start, end))
    return (datetime.datetime.strptime(start, fmt) + datetime.timedelta(offset)).strftime(fmt)


def run():
    while time.sleep(3) is None:
        try:
            config = cfg.get('m2m', lower=True)
            config.update(temporal_start=start_crawl(config.get('temporal_start'), config.get('temporal_end')))
            if config.get('temporal_start'):
                new_acqs = available.updates(**config)
                logger.warning('**** {} new acqs'.format(len(new_acqs)))
                docstore.index(host=cfg.get('ard')['ES_HOST'], index=cfg.get('ard')['ES_INDEX'], data=new_acqs)

                fixes = f.timestamp(map(location.add, reduce(add, map(ingested.expand_tifs, new_acqs))))
                logger.warning('**** {} new tifs'.format(len(fixes)))
                docstore.index(host=cfg.get('iwds')['ES_HOST'], index=cfg.get('iwds')['ES_INDEX'], data=fixes)

                found = ingested.updates(host=cfg.get('iwds')['URL'],
                                                    tiles=new_acqs)
                logger.warning('**** {} ingested tifs'.format(len(found)))
                docstore.index(host=cfg.get('iwds')['ES_HOST'],
                                index=cfg.get('iwds')['ES_INDEX'],
                                data=found)
            else:
                logger.warning('*** Pause search for new acqusitions')
                time.sleep(5 * 60)

            missing = [x['_id'] for x in map(f.unpack, docstore.missing(cfg.get('iwds')['ES_HOST'],
                           cfg.get('iwds')['ES_INDEX'], 'http_date'))]
            logger.warning('**** {} previously missing tifs'.format(len(missing)))
            found = ingested.refresh(host=cfg.get('iwds')['URL'], tif_list=missing)
            logger.warning('**** {} ingested tifs'.format(len(found)))
            docstore.index(host=cfg.get('iwds')['ES_HOST'],
                            index=cfg.get('iwds')['ES_INDEX'],
                            data=found)

            found_ids = [x['_id'] for x in found]
            still_missing = f.timestamp(dict(x) for x in missing if x['_id'] not in found_ids)
            docstore.index(host=cfg.get('iwds')['ES_HOST'],
                           index=cfg.get('iwds')['ES_INDEX'],
                           data=still_missing)
            logger.warning('**** {} still missing tifs'.format(len(still_missing)))
        except KeyboardInterrupt:
            exit(1)
        except BaseException as e:
            logger.critical(e, exc_info=True)
            time.sleep(30)


def main():
    configure_log()
    globals()[parse_args()['command']]()


if __name__ == '__main__':
    main()
