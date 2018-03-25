import re
from dataprocessing.readtools import *
from dataprocessing.plottools import *
import matplotlib.pyplot as plt
def readsim(file_name,timeseries_names=None, is_regex=False):
    str_tmp = open(file_name,"r")
    low = 0
    high = 0
    flag = True
    dic = {}
    seq = []
    value = []
    i = 0
    namelist = ['U','ANGLEU','P','Q','I','ANGLEI']
    timeseries = []
    isfloat = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    for line in str_tmp.readlines():
        line = line.replace(",",".")
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
                    value.append(r'#') #No value, set as #
                low = high + 1
            high += 1
        if flag is False:
            dic[i] = dict(zip(seq, value))
            i += 1
            if value[0] is not '0':
                nameindex = []
                for m in range(5):
                    nameindex.append(seq[1] + '.' + seq[2] + '.' + namelist[m])
                if timeseries_names is None and is_regex is False:
                        for m in range(5):
                            timeseries.append(TimeSeries(nameindex[m],0,value[m + 6]))
                elif is_regex is True:
                    # Read in variables which match with regex
                    p = re.compile(timeseries_names)
                    for m in range(5):
                        if p.search(nameindex[m]):
                            timeseries.append(TimeSeries(nameindex[m], 0, value[m + 6]))
                else:
                    # Read in specified time series
                    for m in range(5):
                        if timeseries_names is namelist[m]:
                            timeseries.append(TimeSeries(nameindex[m], 0, value[m + 6]))
        flag = False
    str_tmp.close()
    return dic
