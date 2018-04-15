import numpy as np
import pandas as pd
from .timeseries import *
import re
import cmath

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


def read_timeseries_NEPLAN_loadflow(file_name, timeseries_names = None, is_regex = False):
    str_tmp = open(file_name, "r")  # Read in files
    low = 0  # flag for the start of a new data in str_cmp
    high = 0  # flag for the end of this new data in str_cmp
    flag = True  # To judge if this the first line of the file, which will be the names for the data type

    # Read in data from result file of neplan
    seq = []  # list for datatype names
    value = []  # list for data
    i = 0
    namelist = ['Vpp', 'Vangle', 'I', 'Iangle']
    timeseries = []
    line_del = [] # a list for the value to be deleted
    isfloat = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    for line in str_tmp.readlines():
        line = line.replace(",", ".")
        high -= high
        low -= low
        del value[:]

        for letter in line:
            if letter == "	" or letter == "\n":  # different data( separated by '	') or end(/n)
                if low is not high:  # low is high, no data read in
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
        A typical load current in neplan has two parts from both end, so the calculation of the 
        current is necessary, which is the function of this part
        """
        if flag is False:
            i += 1
            check_pass = True  # Check for current of the same component
            if value[0] == '0':  # value[0] == '0', no current data to be expected
                for m in range(2):
                    timeseries.append(TimeSeries(value[1] + '.' + namelist[m], np.array([0., 1.]), np.array([value[m + 6], value[m + 6]])))
            else:
                for check in range(len(timeseries) - 1):
                    if timeseries[check].name == value[3] + '.' + namelist[2]:
                        check_pass = False  # Find current of the same component, Calculate the current using (r,tha)
                        line_del.append(check)
                if check_pass:
                    for m in range(2, 4):
                        timeseries.append(TimeSeries(value[3] + '.' + namelist[m], np.array([0., 1.]), np.array([value[m + 8], value[m + 8]])))
        flag = False
    str_tmp.close()



    if is_regex is True:
    # Read in variables which match with regex
        p = re.compile(timeseries_names)
        length = len(timeseries)
        for rule_check in range(length):
            if p.search(timeseries[rule_check].name):
                pass
            else:
                line_del.append(rule_check)

    elif timeseries_names is not None:
    # Read in specified time series
        length = len(timeseries)
        for rule_check in range(length):
            if timeseries_names == timeseries[rule_check].name:
                pass
            else:
                line_del.append(rule_check)
    line_del = set(line_del)
    line_del = sorted(line_del)
    for num_to_del in range(len(line_del)):
        del timeseries[line_del[len(line_del) - num_to_del - 1]]
    return timeseries