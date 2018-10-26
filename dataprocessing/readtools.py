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

def read_timeseries_dpsim(filename, timeseries_names=None):
    """Reads complex time series data from DPsim log file. Real and
    imaginary part are stored in one complex variable.
    :param filename: name of the csv file that has the data
    :param timeseries_names: column name which should be read
    :return: list of Timeseries objects
    """
    pd_df = pd.read_csv(filename)
    timeseries_list = {}
    cmpl_result_columns = []
    real_result_columns = []

    if timeseries_names is None:
        # No column names specified, thus read in all and strip off spaces
        pd_df.rename(columns=lambda x: x.strip(), inplace=True)
        column_names = list(pd_df.columns.values)

        # Remove timestamps column name and store separately
        column_names.remove('time')
        timestamps = pd_df.iloc[:, 0]

        # Find real and complex variable names
        suffixes = [ ('_re', '_im'), ('.real', '.imag') ]
        for column in column_names:
            is_complex = False
            for suffix in suffixes:
                real_suffix = suffix[0]
                imag_suffix = suffix[1]

                if column.endswith(imag_suffix):
                    is_complex = True
                    break # Ignore imag columns

                if column.endswith(real_suffix):
                    is_complex = True
                    column_base = column.replace(real_suffix, '')

                    if column_base + imag_suffix not in column_names:
                        continue

                    cmpl_result_columns.append(column_base)
                    timeseries_list[column_base] = TimeSeries(column_base, timestamps,
                        np.vectorize(complex)(
                            pd_df[column_base + real_suffix],
                            pd_df[column_base + imag_suffix]
                        )
                    )
                    break

            if is_complex:
                continue

            real_result_columns.append(column)
            timeseries_list[column] = TimeSeries(column, timestamps, pd_df[column])

    else:
        # Read in specified time series
        print('cannot read specified columns yet')

    print('DPsim results real column names: ' + str(real_result_columns))
    print('DPsim results complex column names: ' + str(cmpl_result_columns))
    print('DPsim results variable number: ' + str(len(timeseries_list)))
    print('DPsim results length: ' + str(len(timestamps)))

    return timeseries_list
