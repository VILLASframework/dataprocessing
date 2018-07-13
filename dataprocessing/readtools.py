#!/usr/bin/python
# coding: utf8 

import numpy as np
import pandas as pd
from timeseries import *
import re



def read_timeseries_Modelica(filename, timeseries_names=None, is_regex=False):
    from modelicares import SimRes
    sim = SimRes(filename)
    if timeseries_names is None and is_regex is False:
        # No trajectory names or regex specified, thus read in all
        timeseries = []
        for name in sim.names():
            timeseries.append(TimeSeries(name, sim(name).times(), sim(name).values()))
        timeseries_names = sim.names()
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
        column_names = list(pd_df.columns.values)

        # Remove timestamps column name and store separately
        column_names.remove('time')
        timestamps = pd_df.iloc[:,0]

        for name in column_names:
            timeseries_list.append(TimeSeries(name, timestamps, pd_df[name].values))
    else:
        # Read in specified time series
        print('no column names specified yet')

    print('DPsim results column names: ' + str(column_names))
    print('DPsim results number: ' + str(len(timeseries_list)))

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
        timestamps = pd_df.iloc[:,0]
        # Calculate number of network nodes since array is [real, imag]
        node_number = int(len(column_names) / 2)
        node_index = 1
        for column in column_names:
            if node_index <= node_number:
                ts_name = 'n'+ str(node_index)
                timeseries_list.append(
                TimeSeries(ts_name, timestamps, np.vectorize(complex)(pd_df.iloc[:,node_index],pd_df.iloc[:,node_index + node_number])))
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
                node_name = 'node '+ str(node_index) +' Re'
                timeseries_list.append(TimeSeries(node_name, timestamps, pd_df.iloc[:,column]))
            else:
                node_name = 'node '+ str(node_index - node_number) +' Im'
                timeseries_list.append(TimeSeries(node_name, timestamps, pd_df.iloc[:,column]))

            node_index = node_index + 1
    else:
        # Read in specified time series
        print('no column names specified yet')

    print('DPsim results file length:')
    print(len(timeseries_list))
    for result in timeseries_list:
        print(result.name)
    return timeseries_list


def read_timeseries_NEPLAN_loadflow(file_name, timeseries_names=None, is_regex=False):
    """
    Read in NEPLAN loadflow result from result file, the result is in angle notation, amplitude and angle are stored
    separately
    To keep consistent with the names of voltage in most cases, the name of voltage variables are changed into '.V*'
    instead of '.U*' as in the result file

    :param file_name: name of the mat file for the loadflow result from neplan
    :param timeseries_names: column name to be read
    :param is_regex: flag for using regular expression
    :return: list of Timeseries objects
    """
    str_tmp = open(file_name, "r")  # Read in files
    low = 0  # flag for the start of a new data in str_cmp
    high = 0  # flag for the end of this new data in str_cmp
    flag = True  # To judge if this is the first line of the file, which will be the names for the data type

    # Read in data from result file of neplan
    seq = []  # list for data type names
    value = []  # list for data


    namelist = ['U', 'ANGLEU', 'P', 'Q', 'I', 'ANGLEI']  # Suffix of the data name
    timeseries = []
    line_del = []  # a list for the value to be deleted
    isfloat = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')  # regular expression to find float values

    # Transfer ',' in the floats in result file to '.'
    for line in str_tmp.readlines():  # Check the data to find out floats with ','
        line = line.replace(",", ".")
        high -= high
        low -= low
        del value[:]
        # read in different data and start processing
        for letter in line:
            if letter == "	" or letter == "\n":  # different data(separated by '	') or end(/n)
                if low is not high:  # if low is equal to high, no data read in
                    if flag:  # first line of the file, list for data-type name
                        seq.append(line[low:high])
                    else:  # not first line of the file,list for data
                        if isfloat.match(line[low:high]):
                            value.append(float(line[low:high]))
                        else:
                            value.append(line[low:high])
                else:  # no data for this datatype
                    value.append(r'#')  # No value, set as #
                low = high + 1  # refresh low flag
            high += 1

        """
        A typical line current in neplan has two parts from both end, but we doesn't have to calculate them 
        with the assumption that the topology of the gird should be correct with which we can validate the 
        current by comparing the voltage of the nodes connected to the ends of the line 
        """
        if flag is not True:  # flag is true when it's the first line
            if value[3] is not '#':
                for m in range(6):
                    timeseries.append(TimeSeries(value[3] + '.' + namelist[m],
                                                 np.array([0., 1.]), np.array([value[m + 6], value[m + 6]])))
            else:
                for m in range(2):
                    timeseries.append(TimeSeries(value[1] + '.' + namelist[m],
                                                 np.array([0., 1.]), np.array([value[m + 6], value[m + 6]])))
        flag = False
    str_tmp.close()

    # Read in variables which match with regex
    if is_regex is True:
        p = re.compile(timeseries_names)
        length = len(timeseries)
        for rule_check in range(length):
            if p.search(timeseries[rule_check].name):
                pass
            else:
                line_del.append(rule_check)

    # Read in specified time series
    elif timeseries_names is not None:
        length = len(timeseries)
        for rule_check in range(length):
            if timeseries_names == timeseries[rule_check].name:
                pass
            else:
                line_del.append(rule_check)

    # delete those values that are not needed.
    line_del = set(line_del)
    line_del = sorted(line_del)
    for num_to_del in range(len(line_del)):
        del timeseries[line_del[len(line_del) - num_to_del - 1]]

    return timeseries


def read_timeseries_simulink_loadflow(file_name, timeseries_names=None, is_regex=False):
    """
    Read in simulink load-flow result from result file(.rep), the result is in angle notation, amplitude and angle are stored
    separately.
    A suffix is used to tag different data for a component:
        .Arms/.IDegree for current/current angle,
        .Vrms/.VDegree for voltage/voltage angle.

    :param file_name:path of the .rep file for the loadflow result from simulink
    :param timeseries_names: specific values to be read
    :param is_regex: flag for using regular expression
    :return: list of Timeseries objects
    """
    str_tmp = open(file_name, 'r', encoding='latin-1')  # Read in files, using latin-1 to decode /xb0

    # Read in data from result file of neplan
    name = []  # list for data type names
    value = []  # list for data
    timeseries = []
    line_del = []  # a list for the value to be deleted

    for line in str_tmp.readlines():
        line = line.replace("°", "")
        del value[:]
        del name[:]
        # read in different data and start processing
        if len(line) > 37:
            if line[31:35] == '--->':
                if line[13:17] == 'Arms':
                    name = [line[37:len(line)].rstrip() + '.Arms', line[37:len(line)].rstrip() + '.IDegree']
                elif line[13:17] == 'Vrms':
                    name = [line[37:len(line)].rstrip() + '.Vrms', line[37:len(line)].rstrip() + '.VDegree']
                value = [float(line[0:13]), float(line[18:31])]
                timeseries.append(TimeSeries(name[0],
                                             np.array([0., 1.]), np.array([value[0], value[0]])))
                timeseries.append(TimeSeries(name[1],
                                             np.array([0., 1.]), np.array([value[1], value[1]])))

    # Read in variables which match with regex
    if is_regex is True:
        p = re.compile(timeseries_names)
        length = len(timeseries)
        for rule_check in range(length):
            if p.search(timeseries[rule_check].name):
                pass
            else:
                line_del.append(rule_check)

    # Read in specified time series
    elif timeseries_names is not None:
        length = len(timeseries)
        for rule_check in range(length):
            if timeseries_names == timeseries[rule_check].name:
                pass
            else:
                line_del.append(rule_check)

    # delete those values that are not needed.
    line_del = set(line_del)
    line_del = sorted(line_del)
    for num_to_del in range(len(line_del)):
        del timeseries[line_del[len(line_del) - num_to_del - 1]]
    return timeseries
