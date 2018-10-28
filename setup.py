import os
from setuptools import setup

def read(fname):
    dname = os.path.dirname(__file__)
    fname = os.path.join(dname, fname)

    try:
        import m2r
        return m2r.parse_from_file(fname)
    except ImportError:
        with open(fname) as f:
            return f.read()

setup(
    name = "villas-dataprocessing",
    version = "0.2.0",
    author = "Markus Mirz, Jan Dinkelbach, Steffen Vogel",
    author_email = "acs-software@eonerc.rwth-aachen.de",
    description = "Several tools for processing simulation results",
    license = "GPL-3.0",
    keywords = "simulation power system real-time data processing",
    url = "https://git.rwth-aachen.de/acs/public/simulation/data-processing",
    packages = [ "villas.dataprocessing" ],
    long_description = read('README.md'),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3"
    ],
    install_requires = [
        "matplotlib",
        "numpy",
        "pandas"
    ],
    setup_requires = [
        'm2r',
        'wheel'
    ]
)

