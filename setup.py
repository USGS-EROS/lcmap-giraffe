from setuptools import find_packages
from setuptools import setup

from giraffe import __version__


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='lcmap-giraffe',
      version=__version__,
      description='Python to ElasticSearch monitor for LCMAP tile ingest status',
      long_description=readme(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: Public Domain',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='usgs lcmap eros',
      url='http://github.com/usgs-eros/lcmap-giraffe',
      author='USGS EROS LCMAP',
      author_email='',
      license='Unlicense',
      packages=find_packages(),
      install_requires=[
          'requests',
          'elasticsearch',
          'aiohttp',
          'aiodns',
          'geojson',
      ],
      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[test]
      extras_require={
          'test': ['pytest',
                   'pytest-cov',
                   'vcrpy',
                  ],
          'doc': [],
          'dev': [],
      },
      entry_points={
          'console_scripts': [
            'giraffe = giraffe.cli:main'
          ],
      },
      include_package_data=True,
      zip_safe=False
)
