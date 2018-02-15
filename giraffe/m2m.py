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


def search(host, token, dataset='ARD_TILE', start=1, limit=5e4):
    return _api(host, 'search',
                {'apiKey': token, 'datasetName': dataset, "sortOrder": "ASC",
                 'startingNumber': start, 'maxResults': limit}).get('results')


def slimit(host, token, dataset='ARD_TILE'):
    return search(host, token, dataset, limit=1).get('totalHits')
