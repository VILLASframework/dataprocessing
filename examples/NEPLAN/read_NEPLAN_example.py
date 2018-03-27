#!/usr/bin/python
# -*- coding: UTF-8 -*-
import read_NEPLAN
import re

file = r"C:\Users\admin\Desktop\Load_read\Load_flow_WCSS.rlf"



# Example 1: Read in all variable
print('************************ Test for read in all variable start ****************')
result = read_NEPLAN.readsim(file)
for i in range(len(result)):
    print('%s is %s' % (result[i].name,result[i].values)) # result as list of TimeSeries
print('************************ Test for read in all variable end ****************')

print('\n')



# Example 2: Read in specific variable
print('************************ Test for read in specific variable start ****************')
print('************************ Read in specific Voltage ****************')
result1 = read_NEPLAN.readsim(file, 'FOUR.U')
for i in range(len(result1)):
    print('%s is %s' % (result1[i].name, result1[i].values))

print('************************ Read in specific Current ****************')
result2 = read_NEPLAN.readsim(file, 'LINE89.I')
for i in range(len(result2)):
    print('%s is %s' % (result2[i].name, result2[i].values))
print('************************ Test for read in specific variable end ****************')
print('\n')



# Example 3: Read in using regular expression
print('************************ Test for read in using Regular Expression start ****************')
result3 = read_NEPLAN.readsim(file, '^LINE89.*$', True)
for i in range(len(result3)):
    print('%s is %s' % (result3[i].name, result3[i].values))
print('************************ Test for read in using Regular Expression end ****************')
print('\n')



# all_bus_voltages = readsim_Neplan.readsim(file, )
# all_comp_currents = ...