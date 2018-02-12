""" Generalized, reusable functions """

import datetime


def clean(item, keep):
    return {n: item.pop(o) for o,n in keep.items()}


def parse_date(item, strptimes):
    return {k:v if k not in strptimes else datetime.datetime.strptime(v, strptimes[k])
            for k,v in item.items()}


def timestamp(series):
    now = datetime.datetime.utcnow()
    return [dict(item, **{"@timestamp": now}) for item in series]


def unpack(result):
    return clean(dict(result, **result['_source']),
                 {k:k for k in list(result['_source'].keys()) + ['_id']})
