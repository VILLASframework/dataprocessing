from dataprocessing.readtools import *
from dataprocessing.plottools import *
import matplotlib.pyplot as plt
from plottingtools.config import *

current_emt_mod = read_timeseries_Modelica(r"\\tsclient\N\Research\German Public\ACS0049_SINERGIEN_bsc\Data\WorkData\SimulationResults\SynchronousGenerator\EMT\UnitTest_Kundur_FullModel_Euler_1us.mat", ["synchronousGenerator_Park.i[1]"]) # Note: both results include only one damper winding in q axis
current_emt_dpsim = read_timeseries_dpsim_real(r"\\tsclient\N\Research\German Public\ACS0049_SINERGIEN_bsc\Data\WorkData\SimulationResults\SynchronousGenerator\EMT\DPsim\UnitTest_FullModel_Trap_1us\data_j.csv")[0]
current_emt_dpsim.values = -current_emt_dpsim.values

# Comparison EMT
figure_id = 1
plt.figure(figure_id, figsize=(12,8))
set_timeseries_labels(current_emt_mod, ["EMT Modelica"])
plot_timeseries(figure_id, current_emt_mod)
set_timeseries_labels(current_emt_dpsim, "EMT DPsim") # TODO: modelica timeseries needs list element, dpsim timeseries needs string
plot_timeseries(figure_id, current_emt_dpsim, plt_linestyle=':')
plt.xlabel('Zeit [s]')
plt.ylabel('Strom [A]')
plt.show(block=False)

# Comparison DP
current_dp_mod = read_timeseries_Modelica(r"\\tsclient\N\Research\German Public\ACS0049_SINERGIEN_bsc\Data\WorkData\SimulationResults\SynchronousGenerator\DP\UnitTest_Kundur_FullModel_Euler_1us.mat", ["synchronousGenerator_Park.I[1]"]) # Note: both results include only one damper winding in q axis
current_dp_dpsim = read_timeseries_dpsim_cmpl(r"\\tsclient\N\Research\German Public\ACS0049_SINERGIEN_bsc\Data\WorkData\SimulationResults\SynchronousGenerator\DP\DPsim\UnitTest_FullModel_Trap_1us\data_j.csv")[0]
current_dp_dpsim.values = -current_dp_dpsim.values
current_dpabs_dpsim = current_dp_dpsim.abs(current_dp_dpsim.name + ' abs')

figure_id = 2
plt.figure(figure_id, figsize=(12,8))
set_timeseries_labels(current_dp_mod, ["DP Modelica"])
plot_timeseries(figure_id, current_dp_mod)
set_timeseries_labels(current_dpabs_dpsim, "DP DPsim") # TODO: modelica timeseries needs list element, dpsim timeseries needs string
plot_timeseries(figure_id, current_dpabs_dpsim, plt_linestyle=':')
plt.xlabel('Zeit [s]')
plt.ylabel('Strom [A]')
plt.show(block=True)


