import matplotlib.pyplot as plt
import numpy as np
from .timeseries import *

def diff(name, ts1, ts2):
    """ Calculate difference.
    Assumes the same time steps for both timeseries.
    """
    ts_diff = TimeSeries(name, ts1.time, (ts1.values - ts2.values))
    return ts_diff

def scale_ts(name, ts, factor):
    """ Scale timeseries.
    Assumes the same time steps for both timeseries.
    """
    ts_scaled = TimeSeries(name, ts.time, ts.values * factor)
    return ts_scaled

def complex_abs(name, real, imag):
    """ Calculate absolute value of complex variable.
    Assumes the same time steps for both timeseries.
    """
    ts_abs = TimeSeries(name, real.time, np.sqrt(real.values ** 2 + imag.values ** 2))
    return ts_abs

def dyn_phasor_shift_to_emt(name, real, imag, freq):
    """ Shift dynamic phasor values to EMT by frequency freq.
        Assumes the same time steps for both timeseries.
    """
    ts_shift = TimeSeries(name, real.time, real.values*np.cos(2*np.pi*freq*real.time) - imag.values*np.sin(2*np.pi*freq*real.time))
    return ts_shift

def check_node_number_comp(ts_comp, node):
    """
    Check if node number is available in complex time series.
    :param ts_comp: complex time series
    :param node: node number to be checked
    :return: true if node number is available, false if out of range
    """
    ts_comp_length = len(ts_comp)
    im_offset = int(ts_comp_length / 2)
    if im_offset <= node or node < 0:
        print('Complex node not available')
        return false
    else:
        return true

def check_node_number(ts, node):
    """
    Check if node number is available in time series.
    :param ts: time series
    :param node: node number to be checked
    :return: true if node number is available, false if out of range
    """
    ts_length = len(ts)
    if ts_length <= node or node < 0:
        print('Node not available')
        return false
    else:
        return true
