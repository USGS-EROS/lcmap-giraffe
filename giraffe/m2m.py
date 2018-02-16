""" Client for EarthExplorer MachineToMachine API """
import json
import requests


def _api(host, endpoint, data=None):
    url = '{}/{}'.format(host, endpoint)
    body = {'jsonRequest': json.dumps(data)} if data else {}
    return requests.post(url, data=body).json().get('data')


def login(host, username='username', password='password'):
    return _api(host, 'login',
                {'username': username, 'password': password})


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


def search(host, token, dataset='ARD_TILE', start=1, limit=5e4, **kwargs):
    query = {'apiKey': token, 'datasetName': dataset, "sortOrder": "ASC",
             'startingNumber': start, 'maxResults': limit}
    return _api(host, 'search', dict(query, **build_meta_search(**kwargs)))


def slimit(host, token, dataset='ARD_TILE', **kwargs):
    return search(host, token, dataset, limit=1, **kwargs).get('totalHits')
