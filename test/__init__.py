import vcr as _vcr
vcr = _vcr.VCR(record_mode='none') # TODO: none

m_cassette = 'test/resources/ee-m2m-1-4-1-cassette.yaml'
m_username = 'guest'
m_passwurd = 'admin1234'