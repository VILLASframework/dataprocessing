from villas.dataprocessing.readtools import *
from villas.dataprocessing.timeseries import *
import villas.dataprocessing.validationtools as validationtools
import os

# Path to NEPLAN result file (power flow result in *.rlf format)
neplan_result_file= os.path.abspath(r"..\sampledata\CIGRE_MV_NoTap.rlf")

# Path to DPsim result file (power flow result in *.csv format)
dpsim_result_file = os.path.abspath(r"..\sampledata\CIGRE-MV-NoTap.csv")

# Read in NEPLAN results
print('************************ reading neplan power flow data start ****************')
ts_NEPLAN = read_timeseries_NEPLAN_loadflow(neplan_result_file)
for i in range(len(ts_NEPLAN)):
    print('%s is %s' % (ts_NEPLAN[i].name, ts_NEPLAN[i].values)) # result as list of TimeSeries
print('************************ reading neplan power flow data end ****************')
print('\n')

# Read in DPsim powerflow results
print('************************ reading dpsim power flow data start ****************')
ts_dpsim = read_timeseries_csv(dpsim_result_file)
for ts,values in ts_dpsim.items():
    ts_abs = values.abs()
    ts_phase = values.phase()
    print(ts_abs.name + ': ' + str(ts_abs.values) + '\n' +ts_phase.name+' :'+ str(ts_phase.values))
print('************************ reading dpsim power flow data end ****************')

# Converting both timeseries objects to a common format and afterwards compare and assert the results
net_name='CIGRE_MV_NoTap'
threshold=0.5
print('************************ convert neplan to standard start ****************')
res_ref=validationtools.convert_neplan_to_standard_timeseries(ts_NEPLAN)
for i in range(len(res_ref)):
    print(res_ref[i].name)
    print(res_ref[i].values)
print('************************  convert neplan to standard end  ****************')

print('************************ convert dpsim to standard start  ****************')
ts_dpsimList=validationtools.convert_dpsim_to_standard_timeseries(ts_dpsim)
for i in range(len(ts_dpsimList)):
    print(ts_dpsimList[i].name)
    print(ts_dpsimList[i].values)
print('************************ convert dpsim to standard end  ****************')

print('************************ comparison and assertion start  ****************')
res_err=validationtools.compare_timeseries(res_ref,ts_dpsimList)
validationtools.assert_results(net_name,res_err,threshold)
print('************************ comparison and assertion end  ****************')