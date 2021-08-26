from setuptools import setup

setup(name='dragon',
      version='1.5.1',
      description='A powerful toolkit targeting Apple development research, '
      'and packaging.',
      author='kritanta',
      url='https://github.com/DragonBuild/dragon',
      requires=['pyyaml'],
      packages=['dragongen', 'buildgen', 'dragontools'],
      package_dir={
          'dragongen': 'src/dragongen',
          'dragontools': 'src/dragontools',
          'buildgen': 'src/buildgen',
      },
      package_data={
          'dragontools': ['shscripts/*', 'deployable/*'],
      },
      scripts=['dragon']
      )
