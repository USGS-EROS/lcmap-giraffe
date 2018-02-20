""" Client for LCMAP Information Warehouse Data Store """

from giraffe import asynchttp


def inventory(host, tifs):
    urls = ('{}/inventory?only=source&only=extra&source={}'
            .format(host, tif) for tif in tifs)
    return asynchttp.request(list(map(asynchttp.make_req, urls)))


def http_date(response):
    return response['extra']['http']['headers']['date']
