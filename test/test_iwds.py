import os
from giraffe import iwds
import test


@test.vcr.use_cassette(test.i_cassette)
def test_search():
    response = iwds.inventory('http://localhost:5656', ['LC08_CU_027009_20130701_20170729_C01_V01_SRB1.tif'])
    assert isinstance(response, list)
    assert set(response[0]) == {'layer', 'extra', 'url', 'source', 'tile', 'chips'}
