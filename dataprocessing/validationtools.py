#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from dataprocessing.readtools import *


def convert_neplan_to_modelica_timeseries(neplan_timeseries):
    """
    Mapping the variable names between modelica and neplan
        - Voltage: change *.U and *.ANGLEU to *.V and *.Vangle
        - Current: remove unnecessary current variables
    :param neplan_timeseries: result of neplan in timeseries
    :return: a mapped neplan_timeseries
    """
    line_del = []
    # remove all the line current

    # Find current of the same component, which means the current needn't to be validated
    for check in range(len(neplan_timeseries)):
        if neplan_timeseries[check].values[0] == '#':
            line_del.append(check)
        if '.P' in neplan_timeseries[check].name:
            line_del.append(check)
        if '.Q' in neplan_timeseries[check].name:
            line_del.append(check)
        for i in range(check + 1, len(neplan_timeseries)):
            if neplan_timeseries[check].name == neplan_timeseries[i].name:
                line_del.append(check)  # delete list of the unnecessary data
                line_del.append(i)
    line_del = sorted(set(line_del))
    for num_to_del in range(len(line_del)):
        del neplan_timeseries[line_del[len(line_del) - num_to_del - 1]]

    # Change the unit of variables to keep consistent with those in modelica
    for i in range(len(neplan_timeseries)):
        if 'ANGLE' in neplan_timeseries[i].name:
            neplan_timeseries[i].values = neplan_timeseries[i].values / 180 * cmath.pi  # unification of the unit
        elif '.U' in neplan_timeseries[i].name or '.I' in neplan_timeseries[i].name:
            neplan_timeseries[i].values = neplan_timeseries[i].values * 1000

    # Change the name of variables to keep consistent with those in modelica
    for i in range(len(neplan_timeseries)):
        neplan_timeseries[i].name = neplan_timeseries[i].name.replace(' ', '')
        neplan_timeseries[i].name = neplan_timeseries[i].name.replace('.ANGLEU', '.Vangle')
        neplan_timeseries[i].name = neplan_timeseries[i].name.replace('.U', '.Vpp')
        neplan_timeseries[i].name = neplan_timeseries[i].name.replace('.ANGLEI', '.Iangle')

    return neplan_timeseries

def convert_simulink_to_modelica_timeseries(simseri):
    res = []
    for check in range(len(simseri)):
        if 'U AB:' in simseri[check].name:
            simseri[check].name = simseri[check].name.replace('U AB:', '')
            simseri[check].name = simseri[check].name.replace('Vrms', 'Vpp')
            simseri[check].name = simseri[check].name.replace('VDegree', 'Vangle')
            simseri[check].name = simseri[check].name.replace(' ', '')
            simseri[check].name = simseri[check].name.replace('_', '')
            if 'Vangle' in simseri[check].name:
                simseri[check].values = (simseri[check].values - 30)/180 * cmath.pi
            res.append(simseri[check])
    return res


def compare_timeseries(ts1, ts2):
    """
    Compare the result from two timeseries.
    :param ts1: timeseries
    :param ts2: timeseries
    :return: an error dic
    """
    if len(ts1) > len(ts2):
        tmp = ts2
        ts2 = ts1
        ts1 = tmp
    for i in range(len(ts1)):
        ts1[i].name = ts1[i].name.upper()
    for i in range(len(ts2)):
        ts2[i].name = ts2[i].name.upper()

    timeseries_names = []  # list for names of components
    timeseries_error = []  # list for error
    len_ts1 = len(ts1)
    len_limit = len(ts2)

    # Match the components in result files, and compare them
    for i in range(len_ts1):
        flag_not_found = False
        for j in range(len_limit):
            if ts1[i].name == ts2[j].name:  # Find the same variable
                timeseries_names.append(ts1[i].name)
                timeseries_error.append(TimeSeries.rmse(ts2[j], ts1[i])/ts1[i].values[1])
                print(ts1[i].name)
                print(TimeSeries.rmse(ts2[j], ts1[i])/ts1[i].values[len(ts1[i].values) - 1])
                flag_not_found = True
        if flag_not_found is False:
            # No such variable in Modelica model, set the error to -1
            timeseries_names.append(ts1[i].name)
            timeseries_error.append(-1)
    return dict(zip(timeseries_names, timeseries_error))


def assert_modelia_results(net_name, error):
    """
    assert the result data of a net.
    :param net_name: name of the network
    :param modelica_res: timeseries of modelica result
    :param simulink_res: timeseries of reference result
    :return: outputs to command line which are the results of the assert
    """
    fail_list = []  # List for all the failed test
    #  the limitations are set to 0.5
    for name in error.keys():
        if abs(error[name]) > 0.01:
            fail_list.append(name)
        else:
            print("Test on %s Passed" % name)

    #  fail_list is 0, which means all the tests are passed
    if len(fail_list) is 0:
        print("\033[1;36;40mModel %s Passed\033[0m" % net_name)
    else:
        for name in fail_list:
            print("\033[1;31;40mTest on %s of %s Failed\033[0m" % (name, net_name))
        raise ValueError('Test on %s is not passed!' % net_name)


def validate_modelica_res(net_name, modelica_res_path, reference_res_path):
    """
    Top level function for the validation of modelica, calls all the function needed to execute the validation.
    :param modelica_res_path: the path of the modelica result file, whose suffix should be .mat
    :param reference_res_path: the path of the reference result file, whose suffix should be .rep(simulink)/.rlf(neplan)
    :return: outputs to command line which are the results of the validation.
    """
    res_mod = read_timeseries_Modelica (modelica_res_path)
    if os.path.splitext(reference_res_path)[1] == '.rep':
        res_ref = convert_simulink_to_modelica_timeseries(read_timeseries_simulink_loadflow(reference_res_path))
    elif os.path.splitext(reference_res_path)[1] == '.rlf':
        res_ref = convert_neplan_to_modelica_timeseries(read_timeseries_NEPLAN_loadflow(reference_res_path))
    
    res_err = compare_timeseries(res_ref, res_mod)
    assert_modelia_results(net_name, res_err)
