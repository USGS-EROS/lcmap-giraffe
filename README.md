# LCMAP-GIRAFFE [![build status][0]][1] [![Codecov branch][2]][3]

> How's the weather up there?

Giraffe watches the archive for new ARD tiles, and monitors the ingestion of the contained TIFs.

## Install

### Dependencies

* grafana 5.0.0
* elasticsearch 6.2.1
* python 3.5+

External services can be run using [docker-compose][DC], and giraffe can be run locally using [docker][DF]:
```bash
docker-compose -f setup/docker-compose.yaml up -d
docker build -t lcmap-giraffe .
docker run -it --rm --net=setup_lcmap_giraffe lcmap-giraffe
```

### References

* [lcmap-chipmunk][CC]
* [USGS Machine-to-Machine API][MM]

## Configuration

For production configuration, use the [`.giraffe.ini`][gg]

ENV |	Description
-|-
`GIRAFFE_CONFIG_PATH` | Path to configuration file

To override common parameters for different environments or situations:

ENV |	Description
-|-
`GIRAFFE_M2M_USERNAME` | Machine-to-Machine (M2M) Username
`GIRAFFE_M2M_PASSWORD` | M2M password
`GIRAFFE_M2M_URL` | M2M prefix URL (include version number)
`GIRAFFE_ARD_ES_HOST` | Hostname (ElasticSearch) for Archive ARD data
`GIRAFFE_ARD_ES_INDEX` | Index for Archive ARD status
`GIRAFFE_IWDS_URL` | IWDS URL (a.k.a. "chipmunk")
`GIRAFFE_IWDS_ES_HOST` | Hostname (ElasticSearch) for TIF Ingest status
`GIRAFFE_IWDS_ES_INDEX` | Index for TIF Ingest status

Also, to pass filter criteria to the M2M calls:

M2M ENV |	Description
-|-
`GIRAFFE_M2M_CHUNK` | Largest single read from M2M
`GIRAFFE_M2M_LIMIT` | Maximum result limit from M2M
`GIRAFFE_M2M_ADD_TILE_H` | Override M2M search for "Tile Horizontal"
`GIRAFFE_M2M_ADD_TILE_V` | Override M2M search for "Tile Vertical"
`GIRAFFE_M2M_ADD_REGION` | Override M2M search for "Tile Region"
`GIRAFFE_M2M_TEMPORAL_START` | Override M2M search for "startDate"
`GIRAFFE_M2M_TEMPORAL_END` | Override M2M search for "endDate"



[0]: https://img.shields.io/travis/USGS-EROS/lcmap-giraffe/develop.svg?style=flat-square
[1]: https://travis-ci.org/USGS-EROS/lcmap-giraffe
[2]: https://img.shields.io/codecov/c/github/USGS-EROS/lcmap-giraffe/develop.svg?style=flat-square
[3]: https://codecov.io/gh/USGS-EROS/lcmap-giraffe
[DC]: setup/docker-compose.yaml
[DF]: Dockerfile
[CC]: https://github.com/USGS-EROS/lcmap-chipmunk
[MM]: https://earthexplorer.usgs.gov/inventory/documentation/json-api
[gg]: setup/.giraffe.ini
