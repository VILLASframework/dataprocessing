import numpy as np
import pandas as pd
from .timeseries import *
import re


def read_timeseries_Modelica(filename, timeseries_names=None, is_regex=False):
    from modelicares import SimRes
    sim = SimRes(filename)
    if timeseries_names is None and is_regex is False:
        # No trajectory names or regex specified, thus read in all
        timeseries = []
        for name in sim.names():
            timeseries.append(TimeSeries(name, sim(name).times(), sim(name).values()))
    elif is_regex is True:
        # Read in variables which match with regex
        timeseries = []
        p = re.compile(timeseries_names)
        timeseries_names = [name for name in sim.names() if p.search(name)]
        timeseries_names.sort()
        for name in timeseries_names:
            timeseries.append(TimeSeries(name, sim(name).times(), sim(name).values()))
    else:
        # Read in specified time series
        if not isinstance(timeseries_names, list):
            timeseries = TimeSeries(timeseries_names, sim(timeseries_names).times(), sim(timeseries_names).values())
        else:
            timeseries = []
            for name in timeseries_names:
                timeseries.append(TimeSeries(name, sim(name).times(), sim(name).values()))

    print('Modelica results column names: ' + str(timeseries_names))
    print('Modelica results number: ' + str(len(timeseries_names)))

    return timeseries


def read_timeseries_PLECS(filename, timeseries_names=None):
    pd_df = pd.read_csv(filename)
    timeseries_list = []
    if timeseries_names is None:
        # No trajectory names specified, thus read in all
        timeseries_names = list(pd_df.columns.values)
        timeseries_names.remove('Time')
        for name in timeseries_names:
            timeseries_list.append(TimeSeries(name, pd_df['Time'].values, pd_df[name].values))
    else:
        # Read in specified time series
        for name in timeseries_names:
            timeseries_list.append(TimeSeries(name, pd_df['Time'].values, pd_df[name].values))

    print('PLECS results column names: ' + str(timeseries_names))
    print('PLECS results number: ' + str(len(timeseries_list)))

    return timeseries_list

def read_timeseries_simulink(filename, timeseries_names=None):
    pd_df = pd.read_csv(filename)
    timeseries_list = []
    if timeseries_names is None:
        # No trajectory names specified, thus read in all
        timeseries_names = list(pd_df.columns.values)
        timeseries_names.remove('time')
        for name in timeseries_names:
            timeseries_list.append(TimeSeries(name, pd_df['time'].values, pd_df[name].values))
    else:
        # Read in specified time series
        for name in timeseries_names:
            timeseries_list.append(TimeSeries(name, pd_df['time'].values, pd_df[name].values))

    print('Simulink results column names: ' + str(timeseries_names))
    print('Simulink results number: ' + str(len(timeseries_list)))

    return timeseries_list

def read_timeseries_dpsim_real(filename, timeseries_names=None):
    """Reads real time series data from DPsim log file which may have a header.
    Timeseries names are assigned according to the header names if available.
    :param filename: name of the csv file that has the data
    :param timeseries_names: column names which should be read
    :return: list of Timeseries objects
    """
    timeseries_list = []
    pd_df = pd.read_csv(filename)

    if timeseries_names is None:
        # No column names specified, thus read in all and strip spaces
        pd_df.rename(columns=lambda x: x.strip(), inplace=True)
        timeseries_names = list(pd_df.columns.values)
        timeseries_names.remove('time')
    #else:
    #    # Read in specified column names
    #    pd_df = pd.read_csv(filename, names=timeseries_names)

    # store columns of interest in list of timeseries
    # note: timestamps must be given in first column of csv file
    timestamps = pd_df.iloc[:, 0]
    for name in timeseries_names:
        timeseries_list.append(TimeSeries(name, timestamps, pd_df[name].values))

    print('DPsim results column names: ' + str(timeseries_names))
    print('DPsim results number: ' + str(len(timeseries_list)))
    print('DPsim results timestamps number: ' + str(len(timestamps)))

    return timeseries_list


def read_timeseries_dpsim_cmpl(filename, timeseries_names=None):
    """Reads complex time series data from DPsim log file. Real and
    imaginary part are stored in one complex variable.
    :param filename: name of the csv file that has the data
    :param timeseries_names: column name which should be read
    :return: list of Timeseries objects
    """
    pd_df = pd.read_csv(filename)
    timeseries_list = []

    if timeseries_names is None:
        # No column names specified, thus read in all and strip off spaces
        pd_df.rename(columns=lambda x: x.strip(), inplace=True)
        column_names = list(pd_df.columns.values)

        # Remove timestamps column name and store separately
        column_names.remove('time')
        timestamps = pd_df.iloc[:, 0]
        # Calculate number of network nodes since array is [real, imag]
        node_number = int(len(column_names) / 2)
        node_index = 1
        for column in column_names:
            if node_index <= node_number:
                ts_name = 'n' + str(node_index)
                timeseries_list.append(
                    TimeSeries(ts_name, timestamps, np.vectorize(complex)(pd_df.iloc[:, node_index], pd_df.iloc[:, node_index + node_number])))
            else:
                break
            node_index = node_index + 1
    else:
        # Read in specified time series
        print('cannot read specified columns yet')

    print('DPsim results column names: ' + str(column_names))
    print('DPsim results number: ' + str(len(timeseries_list)))

    return timeseries_list


def read_timeseries_dpsim_cmpl_separate(filename, timeseries_names=None):
    """Deprecated - Reads complex time series data from DPsim log file. Real and
    imaginary part are stored separately.
    :param filename: name of the csv file that has the data
    :param timeseries_names: column name which should be read
    :return: list of Timeseries objects
    """
    pd_df = pd.read_csv(filename, header=None)
    timeseries_list = []

    if timeseries_names is None:
        # No trajectory names specified, thus read in all
        column_names = list(pd_df.columns.values)
        # Remove timestamps column name and store separately
        column_names.remove(0)
        timestamps = pd_df.iloc[:, 0]
        # Calculate number of network nodes since array is [real, imag]
        node_number = int(len(column_names) / 2)
        node_index = 1
        for column in column_names:
            if node_index <= node_number:
                node_name = 'node ' + str(node_index) + ' Re'
                timeseries_list.append(TimeSeries(node_name, timestamps, pd_df.iloc[:, column]))
            else:
                node_name = 'node ' + str(node_index - node_number) + ' Im'
                timeseries_list.append(TimeSeries(node_name, timestamps, pd_df.iloc[:, column]))

            node_index = node_index + 1
    else:
        # Read in specified time series
        print('no column names specified yet')

    print('DPsim results file length:')
    print(len(timeseries_list))
    for result in timeseries_list:
        print(result.name)
    return timeseries_list
