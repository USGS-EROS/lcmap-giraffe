""" Generalized, reusable functions """

import datetime
from functools import singledispatch


@singledispatch
def clean(keep, item):
    return {n: item.pop(o) for o,n in keep.items()}


@clean.register(tuple)
@clean.register(list)
def _(keep, item):
    return {n: item[n] for n in keep}


def parse_date(item, strptimes):
    return {k:v if k not in strptimes else datetime.datetime.strptime(v, strptimes[k])
            for k,v in item.items()}


def timestamp(series):
    now = datetime.datetime.utcnow()
    return [dict(item, **{"@timestamp": now}) for item in series]


def unpack(result):
    return clean(list(result['_source'].keys()) + ['_id'],
                 dict(result, **result['_source']))
