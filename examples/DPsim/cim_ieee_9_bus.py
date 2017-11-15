from dataprocessing.readtools import *
from dataprocessing.timeseries import *

path = 'C:\\Users\\mmi\\git\\PowerSystemSimulation\\DPsim\\VisualStudio\\DPsimVS2017\\'
logName = 'lvector-cim';
dataType = '.csv';
logFilename = path + logName + dataType;
ts_dpsim = read_timeseries_dpsim_cmpl(logFilename)
for ts in ts_dpsim:
    ts_abs = ts.abs(ts.name + ' abs')
    ts_phase = ts.phase(ts.name + ' phase')
    print(ts.name + ': ' + str(ts_abs.values[0]) + '<' + str(ts_phase.values[0] * 180/np.pi))

