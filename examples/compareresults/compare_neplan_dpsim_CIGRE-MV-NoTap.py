from villas.dataprocessing.readtools import *
from villas.dataprocessing.timeseries import *
import villas.dataprocessing.validationtools as validationtools

# reference rtf data directory
file=r"..\..\..\reference-results\Neplan\ReferenceGrids\CIGRE_MV_NoTap.rlf"

# Read in NEPLAN data

print('************************ Test for read in all variable start ****************')
ts_NEPLAN = read_timeseries_NEPLAN_loadflow(file)
for i in range(len(ts_NEPLAN)):
    print('%s is %s' % (ts_NEPLAN[i].name, ts_NEPLAN[i].values)) # result as list of TimeSeries
print('************************ Test for read in all variable end ****************')
print('\n')

# Read in CIM powerflow data
print('************************ reading dpsim power flow data start ****************')
path = "D:\\HiWi_ACS\\dpsim_jzh_pfinteg\\dpsim\\build\\Dependencies\\fpotencia\\src\\test\\Logs\\"
logName = 'CIGRE-MV-NoTap-Neplan';
dataType = '.csv';
logFilename = path + logName + dataType;
ts_dpsim = read_timeseries_csv(logFilename)
for ts,values in ts_dpsim.items():
    ts_abs = values.abs(ts + '.Vpp')
    ts_phase = values.phase(ts + '.Vangle')
    print(ts_abs.name + ': ' + str(ts_abs.values) + '\n' +ts_phase.name+' :'+ str(ts_phase.values))
print('************************ reading dpsim power flow data end ****************')

# compare CIM-pf data with NEPLAN
net_name='WSCC-9bus'
threshold=0.5
print('************************ convert neplan to modelica start ****************')
res_ref=validationtools.convert_neplan_to_modelica_timeseries(ts_NEPLAN)
for i in range(len(res_ref)):
    print(res_ref[i].name)
    print(res_ref[i].values)
print('************************  convert neplan to modelica end  ****************')


print('************************ convert dpsim to modelica start  ****************')

ts_dpsimList=validationtools.convert_dpsim_to_modelica_timeseries(ts_dpsim)
for i in range(len(ts_dpsimList)):
    print(ts_dpsimList[i].name)
    print(ts_dpsimList[i].values)
print('************************ convert dpsim to modelica end  ****************')


res_err=validationtools.compare_timeseries(res_ref,ts_dpsimList)
validationtools.assert_modelia_results(net_name,res_err,threshold)

