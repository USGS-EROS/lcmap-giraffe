import vcr as _vcr
vcr = _vcr.VCR(record_mode='none')

m_cassette = 'test/resources/ee-m2m-1-4-1-cassette.yaml'
m_url = 'https://localhost:8080/inventory/json/v/1.4.1'
m_username = 'guest'
m_passwurd = 'admin1234'
m_token = '6c5ce1763e97496de808ca0446cdb4e2'

a_cassette = 'test/resources/elasticsearch-cassette.yaml'
a_es_host = 'localhost'
a_es_index = 'my-elastic-index'

i_cassette = 'test/resources/chipmunk-ard-v1-inventory-cassette.yaml'
i_url = 'http://localhost:5656'
