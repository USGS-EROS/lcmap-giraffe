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


def configure_log(level='INFO'):
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)


def start_crawl(start=None, fmt='%Y-%m-%d', offset=-1):
    if not start:
        try:
            start = docstore.sorted(cfg.get('ard')['ES_HOST'], cfg.get('ard')['ES_INDEX'], 'acquisition_date')[:10]
        except:
            start = '1900-01-01'
    return dict(temporal_start=(datetime.datetime.strptime(start, fmt) + datetime.timedelta(offset)).strftime(fmt))


def run():
    while time.sleep(3) is None:
        try:
            config = cfg.get('m2m', lower=True)
            config.update(start_crawl(config.get('temporal_start')))
            new_acqs = available.updates(**config)
            docstore.index(host=cfg.get('ard')['ES_HOST'], index=cfg.get('ard')['ES_INDEX'], data=new_acqs)

            fixes = f.timestamp(map(location.add, reduce(add, map(ingested.expand_tifs, new_acqs))))
            docstore.index(host=cfg.get('iwds')['ES_HOST'], index=cfg.get('iwds')['ES_INDEX'], data=fixes)

            found = ingested.updates(host=cfg.get('iwds')['URL'],
                                                  tiles=new_acqs)
            docstore.index(host=cfg.get('iwds')['ES_HOST'],
                            index=cfg.get('iwds')['ES_INDEX'],
                            data=found)

            missing = list(map(f.unpack, docstore.missing(cfg.get('iwds')['ES_HOST'],
                           cfg.get('iwds')['ES_INDEX'], 'http_date'))) # TODO: this should check the @timestamp > now() - 30mins
            found = ingested.updates(host=cfg.get('iwds')['URL'],
                                                  tiles=missing)
            docstore.index(host=cfg.get('iwds')['ES_HOST'],
                            index=cfg.get('iwds')['ES_INDEX'],
                            data=found)

            missing = list(map(f.unpack, docstore.missing(cfg.get('iwds')['ES_HOST'],
                           cfg.get('iwds')['ES_INDEX'], 'http_date'))) # TODO: this should check the @timestamp > now() - 30mins
            found = ingested.updates(host=cfg.get('iwds')['URL'],
                                                  tiles=missing)
            docstore.index(host=cfg.get('iwds')['ES_HOST'],
                            index=cfg.get('iwds')['ES_INDEX'],
                            data=found)

            found_ids = [x['_id'] for x in found]
            still_missing = f.timestamp(dict(x) for x in missing if x['_id'] not in found_ids)
            docstore.index(host=cfg.get('iwds')['ES_HOST'],
                            index=cfg.get('iwds')['ES_INDEX'],
                            data=still_missing)
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
