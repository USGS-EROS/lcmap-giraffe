""" Client for LCMAP Information Warehouse Data Store """

from functools import reduce
from operator import add
from giraffe import asynchttp


def inventory(host, tifs):
    urls = ('{}/inventory?only=source&only=extra&source={}'
            .format(host, tif) for tif in tifs)
    return reduce(add, asynchttp.request(list(map(asynchttp.make_req, urls))))


def http_date(response):
    return response['extra']['http']['headers']['date']
