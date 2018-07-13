#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from dataprocessing.readtools import *


file = r"C:\Users\admin\Desktop\Load_read\Load_flow_WCSS.rlf"


# Example 1: Read in all variable
print('************************ Test for read in all variable start ****************')
result_ALL = read_timeseries_NEPLAN_loadflow(file)
for i in range(len(result_ALL)):
    print('%s is %s' % (result_ALL[i].name, result_ALL[i].values)) # result as list of TimeSeries
print('************************ Test for read in all variable end ****************')
print('\n')


# Example 2: Read in specific variable
print('************************ Test for read in specific variable start ****************')

print('************************ Read in specific Voltage ****************')
result_U = read_timeseries_NEPLAN_loadflow(file, 'FOUR.U')
for i in range(len(result_U)):
    print('%s is %s' % (result_U[i].name, result_U[i].values))

print('************************ Read in specific Voltage Angel ****************')
result_ANGELU = read_timeseries_NEPLAN_loadflow(file, 'FOUR.ANGELU')
for i in range(len(result_ANGELU)):
    print('%s is %s' % (result_ANGELU[i].name, result_ANGELU[i].values))

print('************************ Read in specific Current ****************')
result_I = read_timeseries_NEPLAN_loadflow(file, 'LINE89.I')
for i in range(len(result_I)):
    print('%s is %s' % (result_I[i].name, result_I[i].values))

print('************************ Read in specific Current Angel ****************')
result_ANGELI = read_timeseries_NEPLAN_loadflow(file, 'LINE89.ANGELI')
for i in range(len(result_ANGELI)):
    print('%s is %s' % (result_ANGELI[i].name, result_ANGELI[i].values))
print('************************ Test for read in specific variable end ****************')
print('\n')


# Example 3: Read in using regular expression
print('************************ Test for read in using Regular Expression start ****************')
print('************************ Read in Current using Regular Expression ****************')
result_I_REG = read_timeseries_NEPLAN_loadflow(file, '^.*\.I$', True)
for i in range(len(result_I_REG)):
    print('%s is %s' % (result_I_REG[i].name, result_I_REG[i].values))

print('************************ Read in Current Angel using Regular Expression ****************')
result_ANGERLI_REG = read_timeseries_NEPLAN_loadflow(file, '^.*\.ANGELI$', True)
for i in range(len(result_ANGERLI_REG)):
    print('%s is %s' % (result_ANGERLI_REG[i].name, result_ANGERLI_REG[i].values))

print('************************ Read in Voltage using Regular Expression ****************')
result_U_REG = read_timeseries_NEPLAN_loadflow(file, '^.*\.U$', True)
for i in range(len(result_U_REG)):
    print('%s is %s' % (result_U_REG[i].name, result_U_REG[i].values))

print('************************ Read in Voltage Angel using Regular Expression ****************')
result_ANGELU_REG = read_timeseries_NEPLAN_loadflow(file, '^.*\.ANGELU$', True)
for i in range(len(result_ANGELU_REG)):
    print('%s is %s' % (result_ANGELU_REG[i].name, result_ANGELU_REG[i].values))
print('************************ Test for read in using Regular Expression end ****************')