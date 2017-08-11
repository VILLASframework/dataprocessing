import numpy as np
import pandas as pd
from .timeseries import *

def read_time_series_Modelica(filename, time_series_names=None):
    from modelicares import SimRes
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

def read_time_series_DPsim(filename, time_series_names=None):
    pd_df = pd.read_csv(filename, header=None)
    timeseries_list = []

    if time_series_names is None:
        # No trajectory names specified, thus read in all
        column_names = list(pd_df.columns.values)
        column_names.remove(0)
        node_index = 1
        node_number = int(len(column_names) / 2)
        for column in column_names:
            if node_index <= node_number:
                node_name = node_index
                timeseries_list.append(TimeSeries('node '+ str(node_name) +' Re', pd_df.iloc[:,0], pd_df.iloc[:,column]))
            else:
                node_name = node_index - node_number
                timeseries_list.append(TimeSeries('node '+ str(node_name) +' Im', pd_df.iloc[:,0], pd_df.iloc[:,column]))

            node_index = node_index + 1
    else:
        # Read in specified time series
        print('no column names specified yet')

    print('DPsim results file length:')
    print(len(timeseries_list))
    for result in timeseries_list:
        print(result.name)
    return timeseries_list
