FROM python:alpine3.6

WORKDIR /usr/local/src
COPY ./setup.py .
COPY ./README.md .
COPY ./giraffe ./giraffe

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir .

COPY ./setup/.giraffe.ini ~/.usgs/.giraffe.ini
ENV GIRAFFE_CONFIG_PATH="~/.usgs/.giraffe.ini"
ENTRYPOINT ["giraffe", "run"]
