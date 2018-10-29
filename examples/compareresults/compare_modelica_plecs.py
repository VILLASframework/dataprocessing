from dataprocessing.readtools import *
from dataprocessing.plottools import *
import matplotlib.pyplot as plt
import numpy as np

results_path = r'\\tsclient\N\Research\German Public\ACS0049_SINERGIEN_bsc\Data\WorkData\SimulationResults\InductionMachine\results'

### --- Read in section --- ###
# Stator currents
stator_currents_mo = read_time_series_Modelica(results_path + r'\Modelica3hpMachineRRFs.mat', ['inductionMachineSquirrelCage.i[1]', 'inductionMachineSquirrelCage.i[2]', 'inductionMachineSquirrelCage.i[3]'])
stator_currents_pls = read_time_series_PLECS(results_path + r'\PLECS3hpMachineStatorCurrents.csv')

# Rotor currents
rotor_currents_mo = read_time_series_Modelica(results_path + r'\Modelica3hpMachineRRFs.mat', ['inductionMachineSquirrelCage.i_qd0r[1]', 'inductionMachineSquirrelCage.i_qd0r[2]'])
rotor_currents_pls = read_time_series_PLECS(results_path + r'\PLECS3hpMachineRotorCurrentsDqRRFs.csv')
rotor_currents_pls[1].values = -rotor_currents_pls[1].values # transformation DQ0->QD0

# Torque and speed
torque_speed_mo = read_time_series_Modelica(results_path + r'\Modelica3hpMachineRRFs.mat', ['inductionMachineSquirrelCage.T_e', 'inductionMachineSquirrelCage.omega_rm'])
torque_speed_pls = read_time_series_PLECS(results_path + r'\PLECS3hpMachineTorqueSpeed.csv')
torque_speed_mo[1].values = torque_speed_mo[1].values/2/np.pi*60 # transformation to r/min

### --- Plot section --- ###
# Stator currents
figure_id = 1
plt.figure(figure_id)
plt.title("Stator currents")
set_time_series_labels(stator_currents_mo, ['Modelica: Ias [A]', 'Modelica: Ibs [A]', 'Modelica: Ics [A]'])
plot_in_subplots(figure_id, stator_currents_mo)
set_time_series_labels(stator_currents_pls, ['PLECS: Ias [A]', 'PLECS: Ibs [A]', 'PLECS: Ics [A]'])
plot_in_subplots(figure_id, stator_currents_pls, plt_linestyle='--')
plt.xlabel('Time [s]')
plt.show(block=False)

# Rotor currents
figure_id = 2
plt.figure(figure_id)
plt.title("Rotor currents (in synchronously rotating reference frame)")
set_time_series_labels(rotor_currents_mo, ['Modelica: Iqr\' [A]', 'Modelica: Idr\' [A]'])
plot_in_subplots(figure_id, rotor_currents_mo)
set_time_series_labels(rotor_currents_pls, ['PLECS: Iqr\' [A]', 'PLECS: Idr\' [A]'])
plot_in_subplots(figure_id, rotor_currents_pls, plt_linestyle='--')
plt.xlabel('Time [s]')
plt.show(block=False)

# Torque and speed
figure_id = 3
plt.figure(figure_id)
plt.title("Rotor currents (in synchronously rotating reference frame)")
set_time_series_labels(torque_speed_mo, ['Modelica: Torque [Nm]', 'Modelica: Speed [r/min]'])
plot_in_subplots(figure_id, torque_speed_mo)
set_time_series_labels(torque_speed_pls, ['PLECS: Torque [Nm]', 'PLECS: Speed [r/min]'])
plot_in_subplots(figure_id, torque_speed_pls, plt_linestyle='--')
plt.xlabel('Time [s]')
plt.show()