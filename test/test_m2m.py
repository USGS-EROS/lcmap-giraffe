import os
from giraffe import m2m
import test


@test.vcr.use_cassette(test.m_cassette)
def test_login():
    token = m2m.login(username=test.m_username, password=test.m_passwurd)
    assert isinstance(token, str)
    assert len(token) == 32


@test.vcr.use_cassette(test.m_cassette)
def test_search():
    response = m2m.search(m2m.login(username=test.m_username, password=test.m_passwurd), limit=1)
    assert isinstance(response, dict)
    assert isinstance(response.get('results'), list)
    assert len(response.get('results')) == 1
