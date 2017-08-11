import matplotlib.pyplot as plt
import numpy as np
from .timeseries import *


def complex_abs(name, real, imag):
    ts_abs = TimeSeries(name, real.time, np.sqrt(real.values ** 2 + imag.values ** 2))
    return ts_abs

