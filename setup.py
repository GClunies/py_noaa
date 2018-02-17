from setuptools import setup

setup(name='py_noaa',
      version='0.2',
      description='Python module to fetch data from NOAA APIs',
      url='https://github.com/GClunies/py_noaa',
      author='Greg Clunies',
      author_email='greg.clunies@gmail.com',
      license='MIT',
      packages=['py_noaa'],
      install_requires=['requests'],
      zip_safe=False)
      