#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import os
import sys
sys.path.append(r'/home/cafi/Desktop/data-processing/dataprocessing')
from readtools import *


def compare_modelica_neplan(Net_Name):  # compare the result file from NEPLAN and Modelica
    # Read in original nepaln result file
    file_Neplan = os.path.abspath("/home/cafi/Desktop/" + Net_Name + "/" + Net_Name + ".rlf")
    # Read in original Modelica result file
    file_Modelica = os.path.abspath("/home/cafi/Desktop/" + Net_Name + "/" + Net_Name + ".mat")
    result_neplan = read_timeseries_NEPLAN_loadflow(file_Neplan)
    result_modelica = read_timeseries_Modelica(file_Modelica)

    list_del = []
    for i in range(len(result_neplan)):
        result_neplan[i].name = result_neplan[i].name.replace(' ', '')
        result_neplan[i].name = result_neplan[i].name.upper()
        if 'ANGLE' in result_neplan[i].name:
            pass
        else:
            result_neplan[i].values = result_neplan[i].values * 1000  # unification of the unit,which is kV/kA in neplan

    for i in range(len(result_modelica)):
        result_modelica[i].name = result_modelica[i].name.upper()
        if 'ANGLE' in result_modelica[i].name:
            result_modelica[i].values = result_modelica[i].values / cmath.pi * 180  # unification of the unit
        #f_modelica.write('%s is %s \n' % (result_modelica[i].name, result_modelica[i].values[1]))
    timeseries_names = []  # list for names
    timeseries_error = []  # list for error
    len_limit = len(result_modelica)
    for i in range(len(result_neplan)):
        flag_NOT_found = False
        for j in range(len_limit):
            if result_neplan[i].name == result_modelica[j].name:  # Find the same variable
                timeseries_names.append(result_neplan[i].name)
                timeseries_error.append(TimeSeries.rmse(result_modelica[j], result_neplan[i]))
                flag_NOT_found = True
        if not flag_NOT_found:
            timeseries_error.append(TimeSeries(result_neplan[i].name, 0, -1))
            # No such variable in Modelica model, set the error to -1
    return dict(zip(timeseries_names, timeseries_error))

def assert_modelia_neplan_results(net_name):  # Assert the model using the function above
    fail_list = []
    error = compare_modelica_neplan(net_name)
    for name in error.keys():
        if abs(error[name]) > 0.5:
            fail_list.append(name)
        else:
            print("Test on %s Passed" % name)
    if len(fail_list) is 0:
        print("\033[1;36;40mModel Passed\033[0m")
    else:
        for name in fail_list:
            print("\033[1;31;40mTest on %s Failed\033[0m" % name)






