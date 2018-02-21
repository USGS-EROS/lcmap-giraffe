#!/usr/bin/env bash
# Download from https://landsat.usgs.gov/ard/

PATH2SHAPES="${PATH2SHAPES:-./}"
for regionfile in $(ls $PATH2SHAPES/*/*.shp); do
    ogr2ogr -f GeoJSON -t_srs EPSG:4326 $(basename ${regionfile%.shp}.geojson) ${regionfile}
done
