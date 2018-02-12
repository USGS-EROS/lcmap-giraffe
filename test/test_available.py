from giraffe import available
from giraffe import landsat


def test_metadata():
    assert(set(available.metadata([{'_id': 'LT04_CU_029005_19821111_20170912_C01_V01'}])[0])
           - set(landsat.info('LT04_CU_029005_19821111_20170912_C01_V01')) == {'_id'})
