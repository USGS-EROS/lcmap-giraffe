""" Put available ARD tile information in NoSQL """
from functools import partial
from giraffe import landsat
from giraffe import m2m
from giraffe import docstore
from giraffe import funcs as f


def metadata(series):
    return [dict(item, **landsat.info(item['_id'])) for item in series]


def transform(search_result):
    keep_keys = {'acquisitionDate': 'acquisition_date', 'displayId': '_id',
                 'entityId':'entity_id', 'modifiedDate': 'modified_date'}
    strptimes = {'acquisition_date': '%Y-%m-%d',
                 'modified_date': '%Y-%m-%dT%H:%M:%S'}
    return map(partial(f.parse_date, strptimes=strptimes),
                       metadata(map(lambda x: f.clean(keep_keys, x),
                                    search_result)))


def updates(host, username, password, chunk=5e3, limit=5e4):
    limit = limit or m2m.slimit(host, m2m.login(host, username, password))
    chunk = min(map(int, [limit, chunk]))
    for i in range(0, limit, chunk):
        yield f.timestamp(transform(
                    m2m.search(host, m2m.login(host, username, password),
                               start=i+1, limit=chunk)))


def tiles(host, index, **kwargs):
    return map(f.unpack, docstore.query(host, index, **kwargs)['hits']['hits'])
