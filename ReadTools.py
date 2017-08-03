import numpy as np
from modelicares import SimRes
import pandas as pd


class TimeSeries:
    def __init__(self, name, time, values, label=""):
        self.time = np.array(time)
        self.values = np.array(values)
        self.name = name
        self.label = name

def read_time_series_Modelica(filename, time_series_names=None):
    sim = SimRes(filename)
    times_series = []
    if time_series_names is None:
        # No trajectory names specified, thus read in all
        print('TBD')
    else:
        # Read in specified time series
        for name in time_series_names:
            times_series.append(TimeSeries(name, sim(name).times(), sim(name).values()))
    return times_series


def read_time_series_PLECS(filename, time_series_names=None):
    pd_df = pd.read_csv(filename)
    times_series = []
    if time_series_names is None:
        # No trajectory names specified, thus read in all
        time_series_names = list(pd_df.columns.values)
        time_series_names.remove('Time')
        for name in time_series_names:
            times_series.append(TimeSeries(name, pd_df['Time'].values, pd_df[name].values))
    else:
        # Read in specified time series
        for name in time_series_names:
            times_series.append(TimeSeries(name, pd_df['Time'].values, pd_df[name].values))
    return times_series