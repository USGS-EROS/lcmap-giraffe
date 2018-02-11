from giraffe import landsat

def test_conversion():
    assert(set(landsat.info('LC08_CU_027009_20130701_20170729_C01_V01_SRB4')) ==
           {'layer','date_modified','region','collection','version',
            'tileid','sensor','date_acquired'})

