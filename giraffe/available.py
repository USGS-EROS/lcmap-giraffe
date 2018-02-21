""" Put available ARD tile information in NoSQL """
from functools import partial
from giraffe import landsat
from giraffe import m2m
from giraffe import docstore
from giraffe import funcs as f


def metadata(series):
    return [dict(item, **landsat.info(item['_id'])) for item in series]


def transform(search_result):
    keep_keys = {'displayId': '_id'}
    strptimes = {'date_acquired': '%Y%m%d',
                 'date_modified': '%Y%m%d'}
    return map(partial(f.parse_date, strptimes=strptimes),
                       metadata(map(lambda x: f.clean(keep_keys, x),
                                    search_result)))


def updates(url, username, password, **kwargs):
    return f.timestamp(transform(
                m2m.search(url, m2m.login(url, username, password), **kwargs)))


def tiles(host, index, **kwargs):
    return map(f.unpack, docstore.query(host, index, **kwargs)['hits']['hits'])
