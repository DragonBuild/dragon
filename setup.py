from setuptools import setup

setup(name='dragon',
      version='2.0.0',
      description='A powerful toolkit targeting Apple development research, '
      'and packaging.',
      author='kritanta',
      url='https://dragon.krit.me/',
      install_requires=['pyyaml', 'ruyaml'],
      packages=['dragon', 'dragongen', 'buildgen', 'hummingbird'],
      package_dir={
          'dragon': 'src/dragon',
          'dragongen': 'src/dragongen',
          'buildgen': 'src/buildgen',
          'hummingbird': 'src/hummingbird'
      },
      package_data={
          'dragon': ['shscripts/*', 'config/*'],
      },
      scripts=['bin/dragon']
      )
