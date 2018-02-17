""" Command-line-interface entrypoint for Docker """

import argparse
import logging, time
from itertools import islice

from . import available
from . import ingested
from . import docstore
from . import cfg


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
            data = available.updates(**cfg.get('m2m', lower=True))
            for d in data:
                docstore.index(host=cfg.get('ard')['ES_HOST'], index=cfg.get('ard')['ES_INDEX'], data=d)

                docstore.index(host=cfg.get('iwds')['ES_HOST'],
                                index=cfg.get('iwds')['ES_INDEX'],
                                data=ingested.updates(host=cfg.get('iwds')['URL'],
                                tiles=d))
        except KeyboardInterrupt:
            exit(1)
        except BaseException as e:
            print(e)


def main():
    configure_log()
    globals()[parse_args()['command']]()


if __name__ == '__main__':
    main()
