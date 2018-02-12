
from giraffe import ingested

def test_all_tifs():
    assert len(ingested.all_tifs({'_id': 'LC08_CU_027009_20130701_20170729_C01_V01', 'sensor': 'LC08'})) == 8


def test_subset():
    assert(set(ingested.subset({'source': 'LC08_CU_027009_20130701_20170729_C01_V01_SRB1.tif', 'chips': [], 'extra': {'http': {'headers': {'date': 'Mon, 12 Feb 2018 21:01:22 GMT'}}}}))
           == {'n_chips', 'http_date', '_id', 'layer','date_modified','region','collection','version',
                     'tileid','sensor','date_acquired', 'tile_h', 'tile_v'})
