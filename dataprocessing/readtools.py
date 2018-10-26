import numpy as np
import pandas as pd
import re
from .timeseries import *


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
    log_lines = [line for line in log_file]
    log_file.close()

    # Sectionize
    log_sections = {'init':[], 'none':[], 'sysmat_stamp':[], 'sysmat_final':[], 'sourcevec_stamp':[], 'sourcevec_final':[], 'ludecomp':[]}
    section = 'init'
    for line_pos in range(len(log_lines)):
        if re.search('DEBUG: Stamping .+ into system matrix:', log_lines[line_pos]):
            section = 'sysmat_stamp'
        elif re.search('INFO: System matrix:', log_lines[line_pos]):
            section = 'sysmat_final'
        elif re.search('DEBUG: Stamping .+ into source vector:', log_lines[line_pos]):
            section = 'sourcevec_stamp'
        elif re.search('INFO: Right side vector:', log_lines[line_pos]):
            section = 'sourcevec_final'
        elif re.search('INFO: LU decomposition:', log_lines[line_pos]):
            section = 'ludecomp'
        elif re.search('INFO: Number of network simulation nodes:', log_lines[line_pos]):
            section = 'none'
        elif re.search('INFO: Added .+ to simulation.', log_lines[line_pos]):
            section = 'none'
        elif re.search('INFO: Initial switch status:', log_lines[line_pos]):
            section = 'none'
        log_sections[section].append(line_pos)

    return log_lines, log_sections
