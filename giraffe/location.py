""" Convert Region/TileID to Latitude/Longitude """

import glob
import geojson


RESOURCE = 'giraffe/resources/{}.geojson'
REGIONS = {
    'AK': 'ak_ard_grid',
    'CU': 'conus_ard_grid',
    'HI': 'hi_ard_grid',
}


def locations(geojson_obj):
    return {'{:03d}{:03d}'.format(int(f['properties']['h']), int(f['properties']['v'])):
                 f['geometry']['coordinates'][0][0]
             for f in geojson_obj['features'] if f['properties']['h']}


def read_all(regions=REGIONS, path_fmt=RESOURCE):
    return {r: locations(geojson.load(open(path_fmt.format(v))))
            for r, v in regions.items()}


PRELOADED = read_all(REGIONS, RESOURCE)


def load_region(region):
    return PRELOADED[region]


def add(item):
    return dict(item, **{'@location': load_region(item['region'])[item['tileid']]})
