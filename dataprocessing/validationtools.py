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


def compare_modelica_neplan(modelica_res, neplan_res):  # compare the result file from NEPLAN and Modelica
    """
    Compare Results from modelic and neplan, the name of the components should be kept consistent.
    :param modelica_res: the path of the modelica result file, whose suffix should be .mat
    :param neplan_res: the path of the neplan result file, whose suffix should be .rlf
    :return:
    """
    # Read in original neplan result file
    file_Neplan = os.path.abspath(neplan_res)
    # Read in original Modelica result file
    file_Modelica = os.path.abspath(modelica_res)
    result_neplan = convert_neplan_to_modelica_timeseries(read_timeseries_NEPLAN_loadflow(file_Neplan))
    result_modelica = read_timeseries_Modelica(file_Modelica)

    # Transfer the angle unit to degree
    for i in range(len(result_neplan)):
        result_neplan[i].name = result_neplan[i].name.upper()
        if 'ANGLE' in result_neplan[i].name:
            result_neplan[i].values = result_neplan[i].values / cmath.pi * 180  
    for i in range(len(result_modelica)):
        result_modelica[i].name = result_modelica[i].name.upper()
        if 'ANGLE' in result_modelica[i].name:
            result_modelica[i].values = result_modelica[i].values / cmath.pi * 180

    timeseries_names = []  # list for names of components
    timeseries_error = []  # list for error
    len_limit = len(result_modelica)

    # Match the components in result files, and compare them
    for i in range(len(result_neplan)):
        flag_not_found = False
        for j in range(len_limit):
            if result_neplan[i].name == result_modelica[j].name:  # Find the same variable
                timeseries_names.append(result_neplan[i].name)
                timeseries_error.append(TimeSeries.rmse(result_modelica[j], result_neplan[i]))
                flag_not_found = True
        if flag_not_found is False:
            # No such variable in Modelica model, set the error to -1
            timeseries_error.append(-1)
    return dict(zip(timeseries_names, timeseries_error))

def assert_modelia_neplan_results(net_name, modelica_res, neplan_res):  # Assert the model using the function above
    """
    Assert the result in Modelica according to the results from neplan
    :param net_name: The name of the net should be clarified manually
    :param modelica_res: the path of the modelica result file, whose suffix should be .mat
    :param neplan_res: the path of the neplan result file, whose suffix should be .rlf
    :return:
    """
    fail_list = []  # List for all the failed test
    error = compare_modelica_neplan(modelica_res, neplan_res)
    #  the limitations are set to 0.5
    for name in error.keys():
        if abs(error[name]) > 0.5:
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






