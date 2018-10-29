from dataprocessing.dpsim import *
from dataprocessing.plottools import *

path = 'D:\\path\\to\\logs\\'
logName = 'simulation_name_LeftVector'
logFilename = path + logName + '.csv'

ts_dpsim = read_timeseries_dpsim_cmpl(logFilename)

phasors = get_node_voltage_phasors(ts_dpsim)
print('Print phasors for all nodes at first time step:')
for node, phasor in phasors.items():
    print(node + ': ' + str(phasor['abs'].values[0]) + '<' + str(phasor['phase'].values[0]))
print('Print phasors for all nodes at last time step:')
for node, phasor in phasors.items():
    print(node + ': ' + str(phasor['abs'].values[-1]) + '<' + str(phasor['phase'].values[-1]))

emt_voltages = get_node_emt_voltages(ts_dpsim, 50)
print('Print EMT voltages for all nodes at last time step:')
for node, voltage in emt_voltages.items():
    print(node + ': ' + str(voltage.values[-1]))

# Change node number to fit example
#plot_timeseries(1, phasors['n2']['abs'])
plot_timeseries(2, emt_voltages['n2'])
plt.show()

