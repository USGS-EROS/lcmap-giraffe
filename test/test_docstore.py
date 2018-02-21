
from giraffe import docstore
import test


@test.vcr.use_cassette(test.a_cassette)
def test_index():
    token = docstore.index(test.a_es_host, test.a_es_index, [{'@timestamp': 'data'}])
    assert True
