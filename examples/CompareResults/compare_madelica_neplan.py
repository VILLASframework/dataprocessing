#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

from dataprocessing.readtools import *

file_Neplan = r"C:\Users\admin\Desktop\Load_read\WCSS\Load_flow_WCSS.rlf"
file_Modelica = r"C:\Users\admin\Desktop\Load_read\WCSS.mat"
result_neplan = read_timeseries_NEPLAN_loadflow1(file_Neplan)
result_modelica = read_timeseries_Modelica(file_Modelica)
f_neplan = open(r"C:\Users\admin\Desktop\Load_read\output_neplan.txt", "w")
f_modelica = open(r"C:\Users\admin\Desktop\Load_read\output_modelica.txt", "w")
f_error = open(r"C:\Users\admin\Desktop\Load_read\output_error_modelica-neplan.txt", "w")
list_del = []
for i in range(len(result_neplan)):
    result_neplan[i].name = result_neplan[i].name.replace(' ', '')
    result_neplan[i].name = result_neplan[i].name.upper()
    if 'ANGLE' in result_neplan[i].name:
        pass
    else:
        result_neplan[i].values = result_neplan[i].values * 1000
    f_neplan.write('%s is %s \n' % (result_neplan[i].name, result_neplan[i].values))  # result as list of TimeSeries

for i in range(len(result_modelica)):
    result_modelica[i].name = result_modelica[i].name.upper()
    if 'ANGLE' in result_modelica[i].name:
        result_modelica[i].values = result_modelica[i].values / cmath.pi * 180
    f_modelica.write('%s is %s \n' % (result_modelica[i].name, result_modelica[i].values[1]))

timeseries_error = []

len_limit = len(result_modelica)
for i in range(len(result_neplan)):
    flag_NOT_found = False
    for j in range(len_limit):
        if result_neplan[i].name == result_modelica[j].name:
            timeseries_error.append(TimeSeries(result_neplan[i].name, 0, abs(result_modelica[j].values[1] -
                                                                             result_neplan[i].values)))
            j = len_limit + 1
            flag_NOT_found = True
    if not flag_NOT_found:
        timeseries_error.append(TimeSeries(result_neplan[i].name, 0, -1))
    f_error.write('Error of %s is %f \n Base value'
                  ' of %s is %f \n\n' % (timeseries_error[i].name, timeseries_error[i].values,
                                         timeseries_error[i].name, result_neplan[i].values))

