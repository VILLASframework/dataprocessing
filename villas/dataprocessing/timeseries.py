import numpy as np
import cmath
from scipy.signal import hilbert, find_peaks

class TimeSeries:
    """Stores data from different simulation sources.
        A TimeSeries object always consists of timestamps and datapoints.
    """
    def __init__(self, name, time, values, label=""):
        self.time = np.array(time)
        self.values = np.array(values)
        self.name = name
        if not label:
            self.label = name
        else:
            self.label = label

    def scale(self, factor):
        """Returns scaled timeseries.
        """
        ts_scaled = TimeSeries(self.name+'_scl', self.time, self.values * factor)
        return ts_scaled

    def slice_ts(self, start_time, end_time, reindex=False):
        time_step=self.time[1]-self.time[0]
        start_index=int(start_time/time_step)
        end_index=int(end_time/time_step)
        if reindex:
            slice_time=self.time[0 : int((end_time-start_time)/time_step)]
        else:
            slice_time=self.time[start_index:end_index]
        slice_values=self.values[start_index:end_index]
        if(isinstance(slice_values[0], str)):
            slice_values = [float(v_) for v_ in slice_values]
        ts_slice=TimeSeries(self.name+'_slice', slice_time, slice_values, self.label)
        return ts_slice

    def abs(self):
        """ Calculate absolute value of complex time series.
        """
        abs_values = []
        for value in self.values:
            abs_values.append(np.abs(value))
        ts_abs = TimeSeries(self.name+'_abs', self.time, abs_values, self.label+'_abs')
        return ts_abs

    def phase(self):
        """ Calculate phase of complex time series.
        """
        phase_values = []
        for value in self.values:
            phase_values.append(np.angle(value, deg=True))
        ts_phase = TimeSeries(self.name+'_phase', self.time, phase_values, self.label+'_phase')
        return ts_phase

    def real(self):
        """ get the real part of complex time series.
        """
        _real = []
        for value in self.values:
            _real.append(np.real(value))
        ts_real = TimeSeries(self.name+'_real', self.time, _real)
        return ts_real

    def imag(self):
        """ get the imaginary part of complex time series.
        """
        _imag = []
        for value in self.values:
            _imag.append(np.imag(value))
        ts_imag = TimeSeries(self.name+'_real', self.time, _imag)
        return ts_imag

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

    def interpolate(self, timestep):
        """ Interpolates timeseries with new timestep
        :param timestep:
        :return:
        """
        interpl_time = np.arange(self.time[0], self.time[-1], timestep)
        values = np.interp(interpl_time, self.time, self.values)
        ts_return = TimeSeries(self.name+'_intpl', interpl_time, values)
        return ts_return

    def interpolate_cmpl(self, timestep):
        """ Interpolates complex timeseries with new timestep
        :param timestep:
        :return:
        """
        interpl_time = np.arange(self.time[0], self.time[-1], timestep)
        realValues = np.interp(interpl_time, self.time, self.values.real)
        imagValues = np.interp(interpl_time, self.time, self.values.imag)
        ts_return = TimeSeries(self.name+'_intpl', interpl_time, np.vectorize(complex)(realValues, imagValues))
        return ts_return
    
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
    def frequency_shift_list(timeseries_list, freqs_list):
        """ Calculate shifted frequency results of all time series in list by using 
            the frequency with the same index in the frequency list
            or the same frequency if there is only one frequency defined.
        :param timeseries_list: timeseries list retrieved from dpsim results
        :param freqs_list: frequency or list of frequencies by which the timeseries should be shifted
        :return: list of shifted time series
        """
        if not isinstance(freqs_list, list):
            result_list = {}
            for name, ts in timeseries_list.items():
                ts_shift = ts.frequency_shift(freqs_list)
                result_list[ts_shift.name] = ts_shift            
            return result_list
        else:
            result_list = {}
            for ts, freq in zip(timeseries_list, freqs_list):
                ts_shift = ts.frequency_shift(freq)
                result_list[ts.name] = ts_shift       
            return result_list

    @staticmethod
    def interpolate_list(timeseries_list, timestep):
        """ Interpolates timeseries list with new timestep
        :param timestep:
        :return:
        """
        result_list = {}
        for name, ts in timeseries_list.items():
            ts_intp = ts.interpolate(timestep)
            result_list[ts_intp.name] = ts_intp     
        return result_list

    @staticmethod
    def interpolate_cmpl_list(timeseries_list, timestep):
        """ Interpolates list of complex timeseries with new timestep
        :param timestep:
        :return:
        """
        result_list = {}
        for name, ts in timeseries_list.items():
            ts_intp = ts.interpolate_cmpl(timestep)
            result_list[ts_intp.name] = ts_intp            
        return result_list

    @staticmethod 
    def create_emt_from_dp(timeseries_list, freqs_list, new_name = 'emt_signal'):
        """ Calculate shifted frequency results of all time series in list
            and synthesize emt signal by summing them.
        :param timeseries_list: timeseries list retrieved from dpsim results
        :param freqs_list: frequency or list of frequencies by which the timeseries should be shifted
        :return: emt equivalent time series
        """
        result = np.zeros_like(timeseries_list[0].values)

        for ts, freq in zip(timeseries_list, freqs_list):
            ts_shift = ts.frequency_shift(freq)
            result = result + ts_shift.values

        ts_result = TimeSeries(new_name, timeseries_list[0].time, result.real)
        return ts_result    

    @staticmethod
    def rmse(ts1, ts2):
        """ Calculate root mean square error between two time series
        """
        return np.sqrt((TimeSeries.diff('diff', ts1, ts2).values ** 2).mean())

    @staticmethod
    def max_abs_err(ts1, ts2):
        """ Calculate max absolute error between two time series
        """
        return np.absolute((TimeSeries.diff('diff', ts1, ts2).values)).max()

    @staticmethod
    def max_rel_abs_err(ts1, ts2, normalize = None, avoid_zero = False, threshold = 0):
        """ Calculate max relative absolute error between two time series objects to the first
        """
        return np.absolute(TimeSeries.rel_diff('rel_diff', ts1, ts2,\
             normalize = None, avoid_zero = False, threshold = 0).values).max()

    @staticmethod
    def mean_rel_abs_err(ts1, ts2, normalize = None, avoid_zero = False, threshold = 0):
        """ Calculate mean relative absolute error between two time series objects to the first
        """
        return np.absolute(TimeSeries.rel_diff('rel_diff', ts1, ts2,\
            normalize = None, avoid_zero = False, threshold = 0).values).mean()

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
    def rel_diff(name, ts1, ts2, normalize = None, avoid_zero = False, threshold = 0):
        """
        Returns relative difference between two time series objects to the first.
        calculated against the max of ts1.
        """
        if normalize is not None:
            diff_val=TimeSeries.diff('diff', ts1, ts2).values
            rel_diff_to_ts1 = diff_val/normalize
            ts_rel_diff_to_ts1 = TimeSeries(name, ts1.time, rel_diff_to_ts1)
            return ts_rel_diff_to_ts1
        # relative error to the max value of ts1
        if not avoid_zero:
            diff_val=TimeSeries.diff('diff', ts1, ts2).values
            rel_diff_to_ts1 = diff_val/ts1.values.max()
            ts_rel_diff_to_ts1 = TimeSeries(name, ts1.time, rel_diff_to_ts1)
        else:
            index_=np.where(np.abs(ts1.values)>threshold)
            ts1_filtered_val_=ts1.values[index_]
            ts1_filtered_time_=ts1.time[index_]
            ts2_filtered_val_=ts2.values[index_]
            diff_val=TimeSeries.diff('diff', ts1_filtered_val_, ts2_filtered_val_).values
            rel_diff_to_ts1 = diff_val/ts1_filtered_val_.values
            ts_rel_diff_to_ts1 = TimeSeries(name, ts1_filtered_time_, rel_diff_to_ts1)
        return ts_rel_diff_to_ts1
    
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
            phasor_list[name] = ts.phasor()
        return phasor_list

    @staticmethod
    def instFrequency(ts):
        duration = ts.time.max()
        samples = ts.time.size
        sampling_freq = samples / duration
        analytic_signal = hilbert(ts.values)
        instaneous_phase=np.unwrap(np.angle(analytic_signal))
        instantaneous_frequency = (np.diff(instaneous_phase) / (2.0 * np.pi) * sampling_freq)
        ts_instFreq=TimeSeries(str(ts.name + "instFreq"), ts.time[:-1], instantaneous_frequency)
        return ts_instFreq

    @staticmethod
    def getPeaks(ts, nom, tolerance):
        peaks_, properties_ = find_peaks(ts.values, height=nom+tolerance)
        ts_peaks=TimeSeries(str(ts.name+".peaks"), ts.time[peaks_], ts.values[peaks_])
        return ts_peaks

    @staticmethod
    def getDeviation(ts, nom, tolerance):
        dev_=np.where(np.abs(ts.abs().values-nom)>tolerance)
        ts_dev=TimeSeries(str(ts.name+".peaks"), ts.time[dev_], ts.values[dev_])
        return ts_dev