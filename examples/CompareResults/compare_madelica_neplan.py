#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

from dataprocessing.readtools import *
from readin import read_timeseries_NEPLAN_loadflow1

# Read in original nepaln result file
file_Neplan = r"C:\Users\admin\Desktop\Slack_RxLine_PVNode\Slack_RxLine_PVNode.rlf"
# Read in original Modeliac result file
file_Modelica = r"C:\Users\admin\Desktop\Slack_RxLine_PVNode\Slack_RxLine_PVNode.mat"
result_neplan = read_timeseries_NEPLAN_loadflow1(file_Neplan)
result_modelica = read_timeseries_Modelica(file_Modelica)

# neplan result output
f_neplan = open(r"C:\Users\admin\Desktop\Slack_RxLine_PVNode\Slack_RxLine_PVNode_neplan.txt", "w")
# modelica result output
f_modelica = open(r"C:\Users\admin\Desktop\Slack_RxLine_PVNode\Slack_RxLine_PVNode_modelica.txt", "w")
# error result output
f_error = open(r"C:\Users\admin\Desktop\Slack_RxLine_PVNode\output_error_modelica-neplan.txt", "w")
list_del = []
for i in range(len(result_neplan)):
    result_neplan[i].name = result_neplan[i].name.replace(' ', '')
    result_neplan[i].name = result_neplan[i].name.upper()
    if 'ANGLE' in result_neplan[i].name:
        pass
    else:
        result_neplan[i].values = result_neplan[i].values * 1000  # unification of the unit,which is kV/kA in neplan
    f_neplan.write('%s is %s \n' % (result_neplan[i].name, result_neplan[i].values[0]))  # result as list of TimeSeries

for i in range(len(result_modelica)):
    result_modelica[i].name = result_modelica[i].name.upper()
    if 'ANGLE' in result_modelica[i].name:
        result_modelica[i].values = result_modelica[i].values / cmath.pi * 180  # unification of the unit
    f_modelica.write('%s is %s \n' % (result_modelica[i].name, result_modelica[i].values[1]))

timeseries_error = []  # list for error

len_limit = len(result_modelica)
for i in range(len(result_neplan)):
    flag_NOT_found = False
    for j in range(len_limit):
        if result_neplan[i].name == result_modelica[j].name:  # Find the same variable
            timeseries_error.append(TimeSeries(result_neplan[i].name, result_modelica[j].time,
                                               TimeSeries.rmse(result_modelica[j], result_neplan[i])))
            j = len_limit + 1
            flag_NOT_found = True
    if not flag_NOT_found:
        timeseries_error.append(TimeSeries(result_neplan[i].name, 0, -1))
        # No such variable in Modelica model, set the error to -1

    f_error.write('Error of %s is %f \n Base value'
                  ' of %s is %s \n\n' % (timeseries_error[i].name, timeseries_error[i].values,
                                         timeseries_error[i].name, result_neplan[i].values[0]))

