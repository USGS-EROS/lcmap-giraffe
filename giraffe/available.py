""" Put available ARD tile information in NoSQL """

import datetime

from giraffe import landsat
from giraffe import m2m
from giraffe import docstore


def clean(item):
    keep_keys = {'acquisitionDate': 'acquisition_date', 'displayId': '_id',
                 'entityId':'entity_id', 'modifiedDate': 'modified_date'}
    return {n: item.pop(o) for o,n in keep_keys.items()}


def parse_date(item):
    strptimes = {'acquisition_date': '%Y-%m-%d',
                 'modified_date': '%Y-%m-%dT%H:%M:%S'}
    return {k:v if k not in strptimes else datetime.datetime.strptime(v, strptimes[k])
            for k,v in item.items()}


def timestamp(series):
    now = datetime.datetime.utcnow()
    return [dict(item, **{"@timestamp": now}) for item in series]


def metadata(series):
    return [dict(item, **landsat.info(item['_id'])) for item in series]


def push(username, password, host, index, chunk=5e3, limit=None):
    docstore.index(host, index,
                   timestamp(map(parse_date, metadata(map(clean,
                         m2m.psearch(m2m.login(username, password),
                                    chunk=chunk, limit=limit)
                   )))))
