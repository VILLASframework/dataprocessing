import matplotlib.pyplot as plt
import numpy as np
from .timeseries import *

def diff(name, ts1, ts2):
    """ Calculate difference.
    Assumes the same time steps for both timeseries.
    """
    ts_diff = TimeSeries(name, ts1.time, (ts1.values - ts2.values))
    return ts_diff

def complex_abs(name, real, imag):
    """ Calculate absolute value of complex variable.
    Assumes the same time steps for both timeseries.
    """
    ts_abs = TimeSeries(name, real.time, np.sqrt(real.values ** 2 + imag.values ** 2))
    return ts_abs

