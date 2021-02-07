from setuptools import setup

setup(name='Dragon',
      version='1.4',
      description='A powerful toolkit targeting Apple development research, '
      'and packaging.',
      author='kritanta',
      url='https://github.com/DragonBuild/dragon',
      requires=['pyyaml'],
      packages=['dragongen', 'dragongen.buildgen', 'dragontools'],
      package_dir={
          'dragongen': 'DragonGen/dragongen',
          'dragontools': 'dragontools',
          'dragongen.buildgen': 'DragonGen/dragongen/buildgen',
      },
      package_data={
          'dragontools': ['shscripts/*', 'deployable/*'],
      },
      scripts=['dragon']
      )
