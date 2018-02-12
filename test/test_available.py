from giraffe import available
from giraffe import landsat

{'acquisitionDate': '1982-11-11',
 'displayId': 'LT04_CU_028004_19821111_20170912_C01_V01',
 'entityId': 'LT04_CU_028004_19821111_C01_V01',
 'modifiedDate': '2017-09-12T15:14:35',
 'other': 'stuff'
}

def test_clean():
    assert(set(available.clean({
        'acquisitionDate': '1982-11-11',
        'displayId': 'LT04_CU_028004_19821111_20170912_C01_V01',
        'entityId': 'LT04_CU_028004_19821111_C01_V01',
        'modifiedDate': '2017-09-12T15:14:35',
        'other': 'stuff'}))
        == {'_id', 'acquisition_date', 'entity_id', 'modified_date'})


def test_parse_date():
    assert(list(available.parse_date({'acquisition_date': '1900-01-01'}).values())[0].year == 1900)


def test_timestamp():
    assert(all('@timestamp' in x for x in available.timestamp([dict()])))


def test_metadata():
    assert(set(available.metadata([{'_id': 'LT04_CU_029005_19821111_20170912_C01_V01'}])[0])
           - set(landsat.info('LT04_CU_029005_19821111_20170912_C01_V01')) == {'_id'})
