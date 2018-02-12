""" Interface to a NoSQL Document Store """

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
    return client


def index(host, index, data):
    push(make_index(Elasticsearch(host=host), index),
         index, data).indices.refresh(index=index)