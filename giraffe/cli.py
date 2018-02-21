""" Command-line-interface entrypoint for Docker """

import argparse
import logging, time
from itertools import islice

from . import available
from . import ingested
from . import docstore
from . import cfg
from . import logger
from . import funcs as f


def parse_args(defaults=None):
    defaults = defaults or dict()
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=['run'])
    defaults.update(vars(parser.parse_args()))
    return defaults


def configure_log(level='INFO'):
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)


def run():
    while time.sleep(3) is None:
        try:
            config = cfg.get('m2m', lower=True)
            start = config.get('temporal_start') or docstore.sorted(cfg.get('ard')['ES_HOST'], cfg.get('ard')['ES_INDEX'], 'acquisition_date')
            config.update(temporal_start=start[:10])
            docstore.index(host=cfg.get('ard')['ES_HOST'], index=cfg.get('ard')['ES_INDEX'], data=available.updates(**config))
            # TODO: this should update any new as "missing" right away

            missing = map(f.unpack, docstore.missing(cfg.get('iwds')['ES_HOST'],
                                     cfg.get('iwds')['ES_INDEX'], 'http_date')) # TODO: this should check the @timestamp > now() - 30mins
            docstore.index(host=cfg.get('iwds')['ES_HOST'],
                            index=cfg.get('iwds')['ES_INDEX'],
                            data=ingested.updates(host=cfg.get('iwds')['URL'],
                                                  tiles=missing))
        except KeyboardInterrupt:
            exit(1)
        except BaseException as e:
            logger.critical(e, exc_info=True)


def main():
    configure_log()
    globals()[parse_args()['command']]()


if __name__ == '__main__':
    main()
