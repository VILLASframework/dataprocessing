import re
from dataprocessing.readtools import *
from dataprocessing.plottools import *
import cmath

import matplotlib.pyplot as plt

def readsim(file_name, timeseries_names = None, is_regex = False):
    str_tmp = open(file_name, "r")
    low = 0
    high = 0
    flag = True
    dic = {}
    seq = []
    value = []
    i = 0
    namelist = ['U', 'ANGLEU', 'P', 'Q', 'I', 'ANGLEI']
    timeseries = []
    isfloat = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    for line in str_tmp.readlines():
        line = line.replace(",", ".")
        high -= high
        low -= low
        del value[:]
        for letter in line:
            if letter == "	" or letter == "\n":  # different data or end
                if low is not high:  # not NONE
                    if flag:  # seq
                        seq.append(line[low:high])
                    else:  # value
                        if isfloat.match(line[low:high]):
                            value.append(float(line[low:high]))
                        else:
                            value.append(line[low:high])
                else:  # NONE
                    value.append(r'#')  # No value, set as #
                low = high + 1
            high += 1
        if flag is False:
            dic[i] = dict(zip(seq, value))
            i += 1
            check_pass = True
            if timeseries_names is None and is_regex is False:
                if value[0] == '0':
                    for m in range(2):
                        timeseries.append(TimeSeries(value[1] + '.' + namelist[m], 0, value[m + 6]))
                else:
                    for check in range(len(timeseries) - 1):
                        if timeseries[check].name == value[3] + '.' + namelist[4]:
                            check_pass = False
                            result = cmath.rect(timeseries[check].values,
                                                timeseries[check + 1].values / 180 * cmath.pi) + cmath.rect(
                                value[10], value[11] / 180 * cmath.pi)
                            (timeseries[check].value, timeseries[check + 1].value) = cmath.polar(result)
                            timeseries[check + 1].values = timeseries[check + 1].value / cmath.pi * 180
                            timeseries[check - 1].values += value[9]
                            timeseries[check - 2].values += value[8]
                    if check_pass:
                        for m in range(2, 6):
                            timeseries.append(TimeSeries(value[3] + '.' + namelist[m], 0, value[m + 6]))

            elif is_regex is True:
                # Read in variables which match with regex
                p = re.compile(timeseries_names)
                if value[0] == '0':
                    for m in range(2):
                        if p.search((value[1] + '.' + namelist[m])):
                            timeseries.append(TimeSeries(value[1] + '.' + namelist[m], 0, value[m + 6]))
                else:
                    for check in range(len(timeseries) - 1):
                        if timeseries[check].name == value[3] + '.' + namelist[4]:
                            check_pass = False
                            result = cmath.rect(timeseries[check].values,
                                                timeseries[check + 1].values / 180 * cmath.pi) + cmath.rect(
                                value[10], value[11] / 180 * cmath.pi)
                            (timeseries[check].values, timeseries[check + 1].values) = cmath.polar(result)
                            timeseries[check + 1].values = timeseries[check + 1].values / cmath.pi * 180
                            timeseries[check - 1].values += value[9]
                            timeseries[check - 2].values += value[8]
                    if check_pass:
                        for m in range(2, 6):
                            if p.search((value[3] + '.' + namelist[m])):
                                timeseries.append(TimeSeries(value[3] + '.' + namelist[m], 0, value[m + 6]))
            else:
                # Read in specified time series
                if value[0] == '0':
                    for m in range(2):
                        if timeseries_names == (value[1] + '.' + namelist[m]):
                            timeseries.append(TimeSeries(value[1] + '.' + namelist[m], 0, value[m + 6]))
                else:
                    for check in range(len(timeseries) - 1):
                        if timeseries[check].name == value[3] + '.' + namelist[4]:
                            check_pass = False
                            result = cmath.rect(timeseries[check].values,
                                                timeseries[check + 1].values / 180 * cmath.pi) + cmath.rect(
                                value[10], value[11] / 180 * cmath.pi)
                            (timeseries[check].values, timeseries[check + 1].values) = cmath.polar(result)
                            timeseries[check + 1].values = timeseries[check + 1].values / cmath.pi * 180
                            timeseries[check - 1].values += value[9]
                            timeseries[check - 2].values += value[8]

                    if check_pass:
                        for m in range(2, 6):
                            if timeseries_names == (value[3] + '.' + namelist[m]):
                                timeseries.append(TimeSeries(value[3] + '.' + namelist[m], 0, value[m + 6]))
        flag = False
    str_tmp.close()

    return timeseries
