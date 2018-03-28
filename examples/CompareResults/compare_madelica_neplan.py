#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

from dataprocessing.readtools import *
from readin import read_timeseries_NEPLAN_loadflow1
file_Neplan = r"C:\Users\admin\Desktop\Load_read\WCSS\Load_flow_WCSS.rlf"
file_Modelica = r"C:\Users\admin\Desktop\Load_read\WCSS.mat"
result_neplan = read_timeseries_NEPLAN_loadflow1(file_Neplan)
result_modelica = read_timeseries_Modelica(file_Modelica)
f = open(r"C:\Users\admin\Desktop\Load_read\output_neplan.txt", "w")
f_modelica = open(r"C:\Users\admin\Desktop\Load_read\output_modelica.txt", "w")
list_del = []
for i in range(len(result_neplan)):
    result_neplan[i].name = result_neplan[i].name.replace(' ', '')
    result_neplan[i].name = result_neplan[i].name.upper()
    if 'ANGLE' in result_neplan[i].name:
        pass
    elif '.P' in result_neplan[i].name or '.Q' in result_neplan[i].name: #  No need to compare Q,P since we have V,I,angle
        list_del.append(i)
    else:
        result_neplan[i].values = result_neplan[i].values * 1000
    f.write('%s is %s \n' % (result_neplan[i].name, result_neplan[i].values))  # result as list of TimeSeries

'''for num_to_del in range(len(list_del)):
    del result_neplan[list_del[len(list_del) - num_to_del - 1]]'''

for i in range(len(result_modelica)):
    result_modelica[i].name = result_modelica[i].name.upper()
    f_modelica.write('%s is %s \n' % (result_modelica[i].name, result_modelica[i].values[1]))

timeseries_error = []

len_limit = len(result_modelica)
for i in range(len(result_neplan)):
    flag_NOT_found = False
    for j in range(len_limit):
        if result_neplan[i].name == result_modelica[j].name:
            timeseries_error.append(TimeSeries(result_neplan[i].name, 0, abs(result_modelica[j].values[1] - result_neplan[i].values)))
            j = len_limit + 1
            flag_NOT_found = True
    if flag_NOT_found == False:
        timeseries_error.append(TimeSeries(result_neplan[i].name, 0, -1))
    print('Error of %s is %f' % (timeseries_error[i].name, timeseries_error[i].values))

