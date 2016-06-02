from setuptools import setup

setup(name='python-plex-api',
      version='0.0.1',
      description='Python API for viewing Plex activity',
      url='https://github.com/nkgilley/python-plex-api',
      author='Nolan Gilley',
      license='MIT',
      install_requires=['requests>=2.0'],
      packages=['pyplex'],
      zip_safe=True)
