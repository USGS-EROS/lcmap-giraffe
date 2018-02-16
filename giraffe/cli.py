""" Command-line-interface entrypoint for Docker """

import argparse


def parse_args(defaults=None):
    defaults = defaults or dict()
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=['run'])
    defaults.update(vars(parser.parse_args()))
    return defaults


def run():
    print('run giraffe run!')


def main():
    globals()[parse_args()['command']]()


if __name__ == '__main__':
    main()
