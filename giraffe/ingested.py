""" Interface to ingested tiles/chips """

from functools import partial, reduce
from operator import add

from giraffe import funcs as f
from giraffe import iwds
from giraffe import landsat
from giraffe import location


TIFFS = {
        'LC08': ('_SRB4', '_SRB3', '_SRB2', '_SRB5', '_SRB6', '_SRB7', '_BTB10', '_PIXELQA'),
        'LE07': ('_SRB3', '_SRB2', '_SRB1', '_SRB4', '_SRB5', '_SRB7', '_BTB6',  '_PIXELQA'),
        'LT05': ('_SRB3', '_SRB2', '_SRB1', '_SRB4', '_SRB5', '_SRB7', '_BTB6',  '_PIXELQA'),
        'LT04': ('_SRB3', '_SRB2', '_SRB1', '_SRB4', '_SRB5', '_SRB7', '_BTB6',  '_PIXELQA'),
}


def all_tifs(item, tifs=TIFFS):
    return [item['_id'] + s  + '.tif' for s in tifs[item['sensor']] ]


def subset(response):
    return dict(_id=response['source'], http_date=iwds.http_date(response),
                **landsat.info(response['source']))


def expand_tifs(item, tifs=TIFFS):
    return [dict(item, _id=s, layer=s[s.rindex('_'):])
            for s in all_tifs(item, tifs)]


def parse(responses):
    strptimes = {'date_acquired': '%Y%m%d',
                 'date_modified': '%Y%m%d',
                 'http_date': '%a, %d %b %Y %H:%M:%S GMT'}
    return map(location.add,
               map(partial(f.parse_date, strptimes=strptimes),
                   map(subset, responses)))


def refresh(host, tif_list):
    return f.timestamp(parse(iwds.inventory(host, tif_list)))


def updates(host, tiles):
    return refresh(host, reduce(add, map(all_tifs, tiles)))
