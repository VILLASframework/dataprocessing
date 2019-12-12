#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import pandas as pd
import re
from .timeseries import *
from scipy.io import loadmat
from os.path import splitext
import csv



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

def read_timeseries_csv(filename, timeseries_names=None, print_status=True):
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
        suffixes = [ ('_re', '_im'), ('.re', '.im'), ('.real', '.imag') ]
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

    if print_status :
        print('column number: ' + str(len(timeseries_list)))
        print('results length: ' + str(len(timestamps)))
        print('real column names: ' + str(real_result_columns))
        print('complex column names: ' + str(cmpl_result_columns))

    return timeseries_list

def read_timeseries_dpsim(filename, timeseries_names=None, print_status=True):
    return read_timeseries_csv(filename, timeseries_names, print_status)

def read_timeseries_simulink(filename, timeseries_names=None, print_status=True):
    return read_timeseries_csv(filename, timeseries_names, print_status)

def read_dpsim_log(log_path):
    log_file = open(log_path, "r")
    log_lines = [line.rstrip() for line in log_file]
    log_file.close()

    # Sectionize
    log_sections = {'none':[], 'nodenumbers':[], 'sysmat_stamp':[], 'sysmat_final':[], 'sourcevec_stamp':[], 'sourcevec_final':[], 'ludecomp':[]}
    for line_pos in range(len(log_lines)):
        if re.search('\[D\] Stamping .+ into system matrix:', log_lines[line_pos]):
            section = 'sysmat_stamp'
        elif re.search('\[I\] System matrix:', log_lines[line_pos]):
            section = 'sysmat_final'
        elif re.search('\[D\] Stamping .+ into source vector:', log_lines[line_pos]):
            section = 'sourcevec_stamp'
        elif re.search('\[I\] Right side vector:', log_lines[line_pos]):
            section = 'sourcevec_final'
        elif re.search('\[I\] LU decomposition:', log_lines[line_pos]):
            section = 'ludecomp'
        elif re.search('\[I\] Number of network (and virtual )?nodes:', log_lines[line_pos]):
            section = 'nodenumbers'
        elif re.search('\[I\] Added .+ to simulation.', log_lines[line_pos]):
            section = 'none'
        elif re.search('\[I\] Initial switch status:', log_lines[line_pos]):
            section = 'none'
        elif re.search('\[(.*?)\]', log_lines[line_pos]):
            section = 'none'
        log_sections[section].append(line_pos)

    return log_lines, log_sections

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

def read_timeseries_NEPLAN_loadflow(filename, timeseries_names=None, is_regex=False):
    """
    Read in NEPLAN loadflow result from result file, the result is in angle notation, amplitude and angle are stored
    separately
    To keep consistent with the names of voltage in most cases, the name of voltage variables are changed into '.V*'
    instead of '.U*' as in the result file

    :param filename: name of the mat file for the loadflow result from neplan
    :param timeseries_names: column name to be read
    :param is_regex: flag for using regular expression
    :return: list of Timeseries objects
    """
    str_tmp = open(filename, "r")  # Read in files
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


def read_timeseries_simulink_loadflow(filename, timeseries_names=None, is_regex=False):
    """
    Read in simulink load-flow result from result file(.rep), the result is in angle notation, amplitude and angle are stored
    separately.
    A suffix is used to tag different data for a component:
        .Arms/.IDegree for current/current angle,
        .Vrms/.VDegree for voltage/voltage angle.

    :param filename:path of the .rep file for the loadflow result from simulink
    :param timeseries_names: specific values to be read
    :param is_regex: flag for using regular expression
    :return: list of Timeseries objects
    """
    str_tmp = open(filename, 'r', encoding='latin-1')  # Read in files, using latin-1 to decode /xb0

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

def read_timeseries_villas(filename):
    """
    Read data in "villas.human" format.

    See: https://villas.fein-aachen.org/doc/node-formats.html
    Format:   seconds.nanoseconds+offset(sequenceno)      value0 value1 ... valueN
    Example:  1438959964.162102394(6)     3.489760        -1.882725       0.860070

    :param filename: name of the file that contains the data
    """

    from villas.node.sample import Sample

    with open(filename, 'r') as fp:

        timeseries = [ ]
        times = [ ]
        fields = [ ]
        names = [ ]

        for line in fp.readlines():
            if line[0] == '#':
                names = line.split()[2:]
                continue

            sample = Sample.parse(line)

            times.append(sample.ts)

            for index, field in enumerate(sample.values, start=0):
                if len(fields) <= index:
                    fields.append([])

                fields[index].append(field)

        for index, field in enumerate(fields):
            if len(names) <= index:
                name = names[index]
            else:
                name = 'signal_{}'.format(index)

            series = TimeSeries(name, times, field)

            timeseries.append(series)

        return timeseries


def read_timeseries_matpower(input_mat, mapping_conf):
    input_map = csv.reader(open(mapping_conf))
    headers = next(input_map, None)
    map = {}
    for row in input_map:
        k, v = row
        k = int(k)
        map[k] = v

    data = loadmat(input_mat, struct_as_record=True)
    rootname, extension = splitext(input_mat)
    rootname = rootname.split("/")[-1]
    busses = data[rootname]['bus'][0][0]

    if len(busses) != len(map):
        print ("numbers of busses in mapping differs from number of busses in .mat")
        return


    timeseries = []
    timeseries_names = [(map[int(bus[0])] + ".V") for bus in busses]
    values = [bus[7] * bus[9] for bus in busses]
    for i in range(0, len(timeseries_names)):
        timeseries.append(TimeSeries(timeseries_names[i], 0, values[i]))

    return timeseries
