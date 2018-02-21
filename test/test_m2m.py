import os
from giraffe import m2m
import test


@test.vcr.use_cassette(test.m_cassette)
def test_login():
    token = m2m.login(url=test.m_url, username=test.m_username, password=test.m_passwurd)
    assert isinstance(token, str)
    assert len(token) == 32


@test.vcr.use_cassette(test.m_cassette)
def test_search():
    response = m2m.search(url=test.m_url, token=test.m_token, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
