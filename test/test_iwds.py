import os
from giraffe import iwds
import test


@test.vcr.use_cassette(test.i_cassette)
def test_search():
    response = iwds.inventory(test.i_url, ['LT05_CU_022013_20070906_20170923_C01_V01_BTB6.tif'])
    assert isinstance(response, list)
    print(response)
    assert set(response[0]) == {'extra', 'source'}
