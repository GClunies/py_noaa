from setuptools import setup

setup(name='py_noaa',
      version='0.2.1',
      description='Python module to fetch data from NOAA APIs',
      url='https://github.com/GClunies/py_noaa',
      author='Greg Clunies',
      author_email='greg.clunies@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      packages=['py_noaa'],
      install_requires=['requests', 'numpy', 'pandas'],
      zip_safe=False)
      
