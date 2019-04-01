from villas.dataprocessing.readtools import *
from villas.dataprocessing.timeseries import *
import villas.dataprocessing.validationtools as validationtools

# Path to NEPLAN result file (power flow result in *.rlf format)
neplan_result_file=r"D:\git\data\reference-results\Neplan\ReferenceGrids\CIGRE_MV_NoTap.rlf"

# Path to DPsim result file (power flow result in *.csv format)
dpsim_result_file = "D:\\git\\code\\dpsim-powerflow-integration\\dpsim\\build\\Dependencies\\fpotencia\\src\\test\\Logs\\CIGRE-MV-NoTap-Neplan.csv"

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
    ts_abs = values.abs(ts + '.Vpp')
    ts_phase = values.phase(ts + '.Vangle')
    print(ts_abs.name + ': ' + str(ts_abs.values) + '\n' +ts_phase.name+' :'+ str(ts_phase.values))
print('************************ reading dpsim power flow data end ****************')

# Converting both timeseries objects to a common format (here the Modelica format) and afterwards compare and assert the results
net_name='CIGRE_MV_NoTap'
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
validationtools.assert_modelica_results(net_name,res_err,threshold)