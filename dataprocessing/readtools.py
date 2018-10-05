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
        real_string = '.real'
        imaginary_string = '.imag'
        for column in column_names:
            if real_string in column:
                tmp = column.replace(real_string, '')
                cmpl_result_columns.append(tmp)
                #print("Found complex variable: " + tmp)
            elif not imaginary_string in column:
                real_result_columns.append(column)
                #print("Found real variable: " + column)       
        
        for column in real_result_columns:                
            timeseries_list[column] = TimeSeries(column, timestamps, pd_df[column])

        for column in cmpl_result_columns:                
            timeseries_list[column] = TimeSeries(column, timestamps, 
                np.vectorize(complex)(pd_df[column + real_string], 
                pd_df[column + imaginary_string]))
           
    else:
        # Read in specified time series
        print('cannot read specified columns yet')

    print('Simulink results real column names: ' + str(real_result_columns))
    print('Simulink results complex column names: ' + str(cmpl_result_columns))
    print('Simulink results variable number: ' + str(len(timeseries_list)))
    print('Simulink results length: ' + str(len(timestamps)))

    return timeseries_list

def read_timeseries_dpsim(filename, timeseries_names=None, print_status=True):
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
        real_string = '.real'
        imaginary_string = '.imag'
        for column in column_names:
            if real_string in column:
                tmp = column.replace(real_string, '')
                cmpl_result_columns.append(tmp)
                #print("Found complex variable: " + tmp)
            elif not imaginary_string in column:
                real_result_columns.append(column)
                #print("Found real variable: " + column)       
        
        for column in real_result_columns:                
            timeseries_list[column] = TimeSeries(column, timestamps, pd_df[column])

        for column in cmpl_result_columns:                
            timeseries_list[column] = TimeSeries(column, timestamps, 
                np.vectorize(complex)(pd_df[column + real_string], 
                pd_df[column + imaginary_string]))
           
    else:
        # Read in specified time series
        print('cannot read specified columns yet')

    if print_status :
        print('DPsim results real column names: ' + str(real_result_columns))
        print('DPsim results complex column names: ' + str(cmpl_result_columns))
        print('DPsim results variable number: ' + str(len(timeseries_list)))
        print('DPsim results length: ' + str(len(timestamps)))

    return timeseries_list

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