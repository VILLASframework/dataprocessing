#!/usr/bin/python
# -*- coding: UTF-8 -*-
import read_NEPLAN
import re

file = r"C:\Users\jdi-bli\Desktop\Test\Slack_Rxline_PQLoad.rlf"

# Example 1: Read in all variable
result = read_NEPLAN.readsim(file)
for i in range(6):
    print(result[i]) # result as list of TimeSeries

# Example 2: Read in specific variable
# all_bus_voltages = readsim_Neplan.readsim(file, )
# all_comp_currents = ...