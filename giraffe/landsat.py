""" Landsat Product Name to Metadata """

import re

regex = re.compile(r'(?P<sensor>^L[CETO]\d{2})_(?P<region>\w{2})_(?P<tileid>(?P<tile_h>\d{3})'
                    '(?P<tile_v>\d{3}))_(?P<date_acquired>\d{8})_(?P<date_modified>\d{8})_'
                    '(?P<collection>C\d{2})_(?P<version>V\d{2})(?P<layer>.*)$')

def info(product_id='LC08_CU_027009_20130701_20170729_C01_V01_SRB4'):
    return regex.match(product_id).groupdict()

