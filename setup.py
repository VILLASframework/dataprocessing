import os
import re
from setuptools import setup

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def read(fname):
    dname = os.path.dirname(__file__)
    fname = os.path.join(dname, fname)

    with open(fname) as f:
        contents = f.read()
        sanatized = cleanhtml(contents)

        try:
            from m2r import M2R
            m2r = M2R()
            return m2r(sanatized)
        except:
            return sanatized

setup(
    name = 'villas-dataprocessing',
    version = '0.3.2',
    author = 'Markus Mirz, Jan Dinkelbach, Steffen Vogel',
    author_email = 'acs-software@eonerc.rwth-aachen.de',
    description = 'Several tools for processing simulation results',
    long_description_content_type='text/markdown',
    license = 'Apache-2.0',
    keywords = 'simulation power system real-time data processing',
    url = 'https://git.rwth-aachen.de/acs/public/villas/dataprocessing',
    packages = [ 'villas.dataprocessing', 'villas.web' ],
    long_description = read('README.md'),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'
    ],
    install_requires = [
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'requests',
        'python-dateutil'
    ],
    setup_requires = [
        'm2r',
        'wheel'
    ]
)

