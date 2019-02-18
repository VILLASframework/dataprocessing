#!/usr/bin/python

import sys
import villas.dataprocessing.readtools as rt
import villas.dataprocessing.plottools as pt
import matplotlib.pyplot as plt

filename = sys.argv[1]

timeseries = rt.read_timeseries_villas(filename)

pt.plot_timeseries(1, timeseries)

plt.show()
