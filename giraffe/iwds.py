""" Client for LCMAP Information Warehouse Data Store """

from functools import reduce
from operator import add
import requests


def inventory(host, tifs):
    return reduce(add,
                  [requests.get('{}/inventory?source={}'.format(host, tif)).json() for tif in tifs])


def http_date(response):
    return response['extra']['http']['headers']['date']


def n_chips(response):
    return len(response['chips'])

