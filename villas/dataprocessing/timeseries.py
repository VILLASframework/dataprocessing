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

    def scale(self, factor):
        """Returns scaled timeseries.
        """
        ts_scaled = TimeSeries(self.name+'_scl', self.time, self.values * factor)
        return ts_scaled

    def abs(self):
        """ Calculate absolute value of complex time series.
        """
        abs_values = []
        for value in self.values:
            abs_values.append(np.abs(value))
        ts_abs = TimeSeries(self.name+'_abs', self.time, abs_values)
        return ts_abs

    def phase(self):
        """ Calculate phase of complex time series.
        """
        phase_values = []
        for value in self.values:
            phase_values.append(np.angle(value, deg=True))
        ts_phase = TimeSeries(self.name+'_phase', self.time, phase_values)
        return ts_phase

    def phasor(self):
        """Calculate phasors of complex time series 
            and return dict with absolute value and phase.
        """
        ts_abs = self.abs()
        ts_phase = self.phase()
        ts_phasor = {}
        ts_phasor['abs'] = ts_abs
        ts_phasor['phase'] = ts_phase
        
        return ts_phasor
    
    def frequency_shift(self, freq):
        """ Shift dynamic phasor values to EMT by frequency freq.
            Only the real part is considered.
            Assumes the same time steps for both timeseries.
        :param freq: shift frequency
        :return: new timeseries with shifted time domain values
        """
        ts_shift = TimeSeries(self.name+'_shift', self.time, 
                            self.values.real*np.cos(2*np.pi * freq * self.time)
                            - self.values.imag*np.sin(2*np.pi * freq * self.time))
        return ts_shift
    
    def calc_freq_spectrum(self):
        """ Calculates frequency spectrum of the time series using FFT
        """
        Ts = self.time[1]-self.time[0]
        fft_values = np.fft.fft(self.values)
        freqs_num = int(len(fft_values)/2)
        fft_freqs = np.fft.fftfreq(len(fft_values), d=Ts)

        return fft_freqs[:freqs_num], np.abs(fft_values[:freqs_num])/freqs_num

    def interpolate_cmpl(self, timestep):
        """ Not tested yet!
            Interpolates complex timeseries with timestep
        :param timestep:
        :return:
        """
        interpl_time = np.arange(self.time[0], self.time[-1], timestep)
        realValues = interp1d(interpl_time, self.values.real)
        imagValues = interp1d(interpl_time, self.values.imag)
        ts_return = TimeSeries(self.name+'_intpl', time, np.vectorize(complex)(realValues, imagValues))
        return timeseries
    
    @staticmethod
    def multi_frequency_shift(timeseries_list, freqs_list):
        """ Calculate shifted frequency results of all time series
            in list by using the frequency with the same index in the frequency list.
        :param timeseries_list: timeseries list retrieved from dpsim results
        :param freq: frequency by which the timeseries should be shifted
        :return: dict of shifted time series
        """
        result_list = {}
        for ts, freq in zip(timeseries_list, freqs_list):
            ts_shift = ts.frequency_shift(freq)
            result_list[ts.name] = ts_shift

        return result_list
    
    @staticmethod 
    def create_emt_from_dp(timeseries_list, freqs_list):
        """Calculate shifted frequency results of all time series
        :param timeseries_list: timeseries list retrieved from dpsim results
        :param freq: frequency by which the timeseries should be shifted
        :return: list of shifted time series
        """
        result = np.zeros_like(timeseries_list[0].values)

        for ts, freq in zip(timeseries_list, freqs_list):
            ts_shift = ts.frequency_shift(freq)
            result = result + ts_shift.values

        ts_result = TimeSeries('emt_signal', timeseries_list[0].time, result.real)

        return ts_result
    
    @staticmethod
    def frequency_shift_list(timeseries_list, freq):
        """Calculate shifted frequency results of all time series
        :param timeseries_list: timeseries list retrieved from dpsim results
        :param freq: frequency by which the timeseries should be shifted
        :return: list of shifted time series
        """
        result_list = {}
        for name, ts in timeseries_list.items():
            ts_emt = ts.frequency_shift(freq)
            result_list[ts.name] = ts_emt

        return result_list

    @staticmethod
    def rmse(ts1, ts2):
        """ Calculate root mean square error between two time series
        """
        return np.sqrt((TimeSeries.diff('diff', ts1, ts2).values ** 2).mean())

    @staticmethod
    def norm_rmse(ts1, ts2):
        """ Calculate root mean square error between two time series,
        normalized using the mean value of both mean values of ts1 and ts2 
        """
        if np.mean(np.array(ts1.values.mean(),ts2.values.mean())) != 0:
          nrmse = np.sqrt((TimeSeries.diff('diff', ts1, ts2).values ** 2).mean())/np.mean(np.array(ts1.values.mean(),ts2.values.mean()))
          is_norm = True
        else:
          nrmse = np.sqrt((TimeSeries.diff('diff', ts1, ts2).values ** 2).mean())
          is_norm = False
        return (nrmse,is_norm)

    @staticmethod
    def diff(name, ts1, ts2):
        """Returns difference between values of two Timeseries objects.
        """
        if len(ts1.time) == len(ts2.time):
            ts_diff = TimeSeries(name, ts1.time, (ts1.values - ts2.values))
        else:  # different timestamps, common time vector and interpolation required before substraction
            time = sorted(set(list(ts1.time) + list(ts2.time)))
            interp_vals_ts1 = np.interp(time, ts1.time, ts1.values)
            interp_vals_ts2 = np.interp(time, ts2.time, ts2.values)
            ts_diff = TimeSeries(name, time, (interp_vals_ts2 - interp_vals_ts1))
        return ts_diff
    
    @staticmethod
    def complex_abs(name, ts_real, ts_imag):
        """ Calculate absolute value of complex variable.
            Assumes the same time steps for both timeseries.
        """
        ts_complex = np.vectorize(complex)(ts_real.values, ts_imag.values)
        ts_abs = TimeSeries(name, ts_real.time, np.absolute(ts_complex))
        return ts_abs

    @staticmethod
    def phasors(timeseries_list):
        """Calculate voltage phasors of all nodes
        :param timeseries_list: timeseries list with real and imaginary parts
        :return: timeseries list with abs and phase
        """
        phasor_list = {}
        for name, ts in timeseries_list.items():
            phasor_list[name] = ts.phasor(name)

        return phasor_list