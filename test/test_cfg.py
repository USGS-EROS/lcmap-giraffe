import os
from giraffe import cfg

def test_environ():
    os.environ['GIRAFFE_M2M_USERNAME'] = 'george'
    assert(cfg.get('m2m')['USERNAME'] == 'george')
    assert('username' in cfg.get('m2m', lower=True))
