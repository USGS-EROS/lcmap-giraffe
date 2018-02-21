""" Interface to a NoSQL Document Store """

from giraffe import logger

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk


def make_index(client, index='my-index-name', settings=None):
    try:
        client.indices.create(index=index, body=settings)
    except TransportError as e:
        if '_already_exists_' in e.error:
            pass
        else:
            raise
    finally:
        return client


def push(client, index='my-new-index', data=None, chunk=50):
    for ok, result in streaming_bulk(client, data, index=index,
                                     doc_type='doc', chunk_size=chunk):
        action, result = result.popitem()
        doc_id = '/%s/doc/%s' % (index, result['_id'])
        logger.info(' '.join([doc_id, action, result['result']]))
    return client


def index(host, index, data):
    push(make_index(Elasticsearch(host=host), index),
         index, data).indices.refresh(index=index)


def query(host, index, size=10, **kwargs):
    body = dict(query=kwargs, size=size)
    return Elasticsearch(host=host).search(index=index, body=body)


def sorted(host, index, field, order='desc'):
    body = dict(size=1, query=dict(match_all=dict()),
                sort=[{field: dict(order=order)}])
    return Elasticsearch(host=host).search(index=index, body=body
                         )['hits']['hits'][-1]['_source'][field]


def missing(host, index, field, size=1000):
    body = dict(size=size, query=dict(query_string={"query":
                "NOT _exists_:{}".format(field)}),
                sort=[{'@timestamp': dict(order='asc')}])
    return Elasticsearch(host=host).search(index=index, body=body)['hits']['hits']
