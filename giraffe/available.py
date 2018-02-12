""" Put available ARD tile information in NoSQL """
from functools import partial
from giraffe import landsat
from giraffe import m2m
from giraffe import docstore
from giraffe import funcs as f


def metadata(series):
    return [dict(item, **landsat.info(item['_id'])) for item in series]


def updates(username, password, chunk, limit, keep):
    return metadata(map(lambda x: f.clean(keep, x),
                    m2m.psearch(m2m.login(username, password),
                                chunk=chunk, limit=limit)))


def push(username, password, host, index, chunk=5e3, limit=None):
    keep_keys = {'acquisitionDate': 'acquisition_date', 'displayId': '_id',
                 'entityId':'entity_id', 'modifiedDate': 'modified_date'}
    strptimes = {'acquisition_date': '%Y-%m-%d',
                 'modified_date': '%Y-%m-%dT%H:%M:%S'}
    docstore.index(host, index,
                   f.timestamp(map(partial(f.parse_date, strptimes=strptimes),
                        updates(username, password, chunk, limit, keep_keys))))


def tiles(host, index, **kwargs):
    return map(f.unpack, docstore.query(host, index, **kwargs)['hits']['hits'])
