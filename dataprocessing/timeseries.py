import numpy as np
import cmath

class TimeSeries:
    """Stores data from different simulation sources.
    A TimeSeries object always consists of timestamps and datapoints.
    """
    def __init__(self, name, time, values, label=""):
        self.time = np.array(time)
        self.values = np.array(values)
        self.name = name
        self.label = name

    @staticmethod
    def diff(name, ts1, ts2):
        """Returns difference between values of two Timeseries objects.
        """
        if ts1.time==ts2.time:
            ts_diff = TimeSeries(name, ts1.time, (ts1.values - ts2.values))
        else:  # different timestamps, common time vector and interpolation required before substraction
            time = sorted(set(list(ts1.time) + list(ts2.time)))
            interp_vals_ts1 = np.interp(time, ts1.time, ts1.values)
            interp_vals_ts2 = np.interp(time, ts2.time, ts2.values)
            ts_diff = TimeSeries(name, time, (interp_vals_ts2 - interp_vals_ts1))
        return ts_diff


    def scale_ts(self, name, factor):
        """Returns scaled timeseries.
        Assumes the same time steps for both timeseries.
        """
        ts_scaled = TimeSeries(name, self.time, self.values * factor)
        return ts_scaled

    @staticmethod
    def complex_abs_dep(name, ts_real, ts_imag):
        """ Calculate absolute value of complex variable.
        Assumes the same time steps for both timeseries.
        """
        ts_abs = TimeSeries(name, ts_real.time, np.sqrt(ts_real.values ** 2 + ts_imag.values ** 2))
        return ts_abs

    @staticmethod
    def complex_abs(name, ts_real, ts_imag):
        """ Calculate absolute value of complex variable.
        Assumes the same time steps for both timeseries.
        """
        ts_complex = np.vectorize(complex)(ts_real.values, ts_imag.values)
        ts_abs = TimeSeries(name, ts_real.time, ts_complex.abs())
        return ts_abs

    def abs(self, name):
        """ Calculate absolute value of complex time series.
        """
        abs_values = []
        for value in self.values:
            abs_values.append(np.abs(value))
        ts_abs = TimeSeries(name, self.time, abs_values)
        return ts_abs

    def phase(self, name):
        """ Calculate absolute value of complex time series.
        """
        phase_values = []
        for value in self.values:
            phase_values.append(np.angle(value, deg=True))
        ts_abs = TimeSeries(name, self.time, phase_values)
        ts_phase = TimeSeries(name, self.time, phase_values)
        return ts_phase

    @staticmethod
    def dyn_phasor_shift_to_emt(name, real, imag, freq):
        """ Shift dynamic phasor values to EMT by frequency freq.
            Assumes the same time steps for both timeseries.
        """
        ts_shift = TimeSeries(name, real.time, real.values*np.cos(2*np.pi*freq*real.time) - imag.values*np.sin(2*np.pi*freq*real.time))
        return ts_shift

    @staticmethod
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

    @staticmethod
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