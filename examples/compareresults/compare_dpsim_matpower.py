from villas.dataprocessing.readtools import *
from villas.dataprocessing.timeseries import *
import villas.dataprocessing.validationtools as validationtools
import os

os.chdir(os.path.dirname(__file__))

# Path to mpc result file (power flow result in *.mat format)
mpc_result_file = os.path.abspath(os.path.join(os.getcwd(),"../sampledata/case145results.mat"))
print(mpc_result_file)

# Path to DPsim result file (power flow result in *.csv format)
dpsim_result_file = os.path.abspath(os.path.join(os.getcwd(),"../sampledata/case145.csv"))
print(dpsim_result_file)


mpc_mapping_file = os.path.abspath(os.path.join(os.getcwd(),"../sampledata/case145_mapping_busID_uuid.csv"))
print(mpc_mapping_file)



# Read mpc files9B70998E-2283-11EA-998E-000000000000.V
print('************************ reading mpc power flow data start ****************')
mpc_objects = read_timeseries_matpower(mpc_result_file, mpc_mapping_file)
for obj in mpc_objects:
    print('%s is %s' % (obj.name, obj.values)) # result as list of TimeSeries
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
net_name='Case9' # TODO: fix
threshold=0.5

print('************************ convert dpsim to standard start  ****************')
ts_dpsimList=validationtools.convert_dpsim_to_standard_timeseries(ts_dpsim)
for i in range(len(ts_dpsimList)):
    print(ts_dpsimList[i].name)
    print(ts_dpsimList[i].values)
print('************************ convert dpsim to standard end  ****************')

print('************************ comparison and assertion start  ****************')
res_err=validationtools.compare_timeseries(mpc_objects,ts_dpsimList)
validationtools.assert_modelica_results(net_name,res_err,threshold)
print('************************ comparison and assertion end  ****************')

