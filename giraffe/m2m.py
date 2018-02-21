""" Client for EarthExplorer MachineToMachine API """
import json
from functools import partial
from functools import reduce
from operator import add
from giraffe import asynchttp


def fmt_body(data=None):
    return {'jsonRequest': json.dumps(data)} if data else {}


def _api(url, endpoint, searches=None):
    mreq = partial(asynchttp.make_req, verb='POST',
                   url='{}/{}'.format(url, endpoint))
    searches = list(map(lambda s: mreq(data=s), map(fmt_body, searches)))
    return asynchttp.request(searches)


def _data(series):
    errors = list(filter(None, map(lambda x: x.get('error'), series)))
    if errors:
        raise IOError('m2m not working: {}'.format(errors))
    return list(map(lambda x: x.get('data'), series))


def _results(series):
    return reduce(add, list(map(lambda x: x.get('results'), series)))


def login(url, username='username', password='password', **kwargs):
    return _data(_api(url, 'login',
                [{'username': username, 'password': password}]))[-1]


def add_additional(dataset='ARD_TILE', **kwargs):
    fields = {
        'ARD_TILE': { # 'fieldId' values differ for each M2M dataset
            'tile_h': 21787,
            'tile_v': 21788,
            'region': 21789,
        }
    }
    return {} if len(kwargs) < 1 else {
        'additionalCriteria': {
        "filterType": "and",
            "childFilters": [
                {"filterType": "value", "fieldId": fields[dataset][k], "value": v}
                for k,v in kwargs.items()
            ]
        }}


def add_temporal(**kwargs):
    fields = {'start': 'startDate', 'end': 'endDate'}
    return {} if len(kwargs) < 1 else {
        'temporalFilter':
            dict(dateField='search_date',
                 **{fields[k]: v for k,v in kwargs.items()})
        }


def build_meta_search(**kwargs):
    funcs = {'add_': add_additional, 'temporal_': add_temporal}
    return dict([(key,d[key]) for d in [f(**{k.split(y)[1]: v for k,v in kwargs.items()
                 if k.startswith(y)}) for y,f in funcs.items()] for key in d])


def make_search(token, dataset='ARD_TILE', start=1, limit=5e4, **kwargs):
    query = {'apiKey': token, 'datasetName': dataset, "sortOrder": "ASC",
             'startingNumber': start, 'maxResults': limit}
    return dict(query, **build_meta_search(**kwargs))


def search(url, token, dataset='ARD_TILE', start=1, chunk=5e3, limit=5e4, **kwargs):
    limit = limit or slimit(url, token, **kwargs)
    chunk = min(map(int, [limit, chunk]))
    msearch = make_search(token=token, dataset=dataset, **kwargs)
    searches = [dict(msearch, startingNumber=i+1, maxResults=chunk)
                for i in range(0, int(limit), int(chunk))]
    return _results(_data(_api(url, 'search', searches)))


def slimit(url, token, dataset='ARD_TILE', **kwargs):
    searches = [make_search(token, dataset, limit=1, **kwargs)]
    return _data(_api(url, 'search', searches))[0].get('totalHits')
