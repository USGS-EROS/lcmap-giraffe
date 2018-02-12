from giraffe import funcs

{'acquisitionDate': '1982-11-11',
 'displayId': 'LT04_CU_028004_19821111_20170912_C01_V01',
 'entityId': 'LT04_CU_028004_19821111_C01_V01',
 'modifiedDate': '2017-09-12T15:14:35',
 'other': 'stuff'
}

def test_clean():
    assert(set(funcs.clean({'acquisitionDate': 'acquisition_date', 'displayId': '_id'},
                           {'acquisitionDate': '1982-11-11',
                            'displayId': 'LT04_CU_028004_19821111_20170912_C01_V01',
                            'other': 'stuff'}))
        == {'_id', 'acquisition_date'})


def test_parse_date():
    assert(list(funcs.parse_date({'acquisition_date': '1900-01-01'},
                {'acquisition_date': '%Y-%m-%d'}).values())[0].year == 1900)


def test_timestamp():
    assert(all('@timestamp' in x for x in funcs.timestamp([dict()])))
