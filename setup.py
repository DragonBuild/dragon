from setuptools import setup

setup(name='dragon',
      version='1.6.8',
      description='A powerful toolkit targeting Apple development, research, and packaging.',
      author='kritanta',
      url='https://dragon.krit.me/',
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
