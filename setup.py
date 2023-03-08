#!/usr/bin/env python3

from setuptools import setup

setup(name='dragon',
      version='1.7.0',
      description='A powerful toolkit targeting Apple development, research, and packaging.',
      author='cynder',
      url='https://dragon.cynder.me/',
      install_requires=['ninja', 'pyyaml', 'ruyaml', 'packaging'],
      packages=['dragon', 'dragongen', 'buildgen'],
      package_dir={
          'dragon': 'src/dragon',
          'dragongen': 'src/dragongen',
          'buildgen': 'src/buildgen',
      },
      package_data={
          'dragon': ['shscripts/*', 'config/*'],
      },
      scripts=['bin/dragon']
      )
