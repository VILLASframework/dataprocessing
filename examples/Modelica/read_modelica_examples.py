from dataprocessing.readtools import *
from dataprocessing.plottools import *
import matplotlib.pyplot as plt


# Example 1: read in single variable included in the Modelica results file
voltage_node126 = read_timeseries_Modelica(
    r"\\tsclient\N\Research\German Public\ACS0049_SINERGIEN_bsc\Data\WorkData\SimulationResults\IEEE European\Single_scenario_fixed_PV\IEEEEuropean_60.mat",
    timeseries_names="N126.Vrel")
plt.figure(1, figsize=(12,8))
set_timeseries_labels(voltage_node126, "voltage N126")
plt.plot(voltage_node126.time/3600, voltage_node126.values, label=voltage_node126.label)
plt.legend()
plt.show(block=True)

# Example 2: read in multiple variables defined in a list
voltage_two_nodes = read_timeseries_Modelica(
    r"\\tsclient\N\Research\German Public\ACS0049_SINERGIEN_bsc\Data\WorkData\SimulationResults\IEEE European\Single_scenario_fixed_PV\IEEEEuropean_60.mat",
    timeseries_names=["N127.Vrel", "N128.Vrel"])
plt.figure(2, figsize=(12,8))
plt.plot(voltage_two_nodes[0].time/3600, voltage_two_nodes[0].values, label=voltage_two_nodes[0].label)
plt.plot(voltage_two_nodes[1].time/3600, voltage_two_nodes[1].values, label=voltage_two_nodes[1].label)
plt.legend()
plt.show(block=True)

# Example 3: read in all voltages using regular expressions
voltages_all_nodes = read_timeseries_Modelica(
    r"\\tsclient\N\Research\German Public\ACS0049_SINERGIEN_bsc\Data\WorkData\SimulationResults\IEEE European\Single_scenario_fixed_PV\IEEEEuropean_60.mat",
    timeseries_names='^[^.]*.Vrel$', is_regex=True)
plt.figure(3, figsize=(12, 8))
for i in range(len(voltages_all_nodes)):
    plt.plot(voltages_all_nodes[i].time / 3600, voltages_all_nodes[i].values, label=voltages_all_nodes[i].label)
plt.legend()
plt.show(block=True)

# Example 4: read in all variables
variables_all = read_timeseries_Modelica(
    r"\\tsclient\N\Research\German Public\ACS0049_SINERGIEN_bsc\Data\WorkData\SimulationResults\IEEE European\Single_scenario_fixed_PV\IEEEEuropean_60.mat")
dict_variables_all = {}
for ts in variables_all:
    dict_variables_all[ts.name] = ts
plt.figure(4, figsize=(12, 8))
plt.plot(dict_variables_all["L12.Irel"].time/3600, dict_variables_all["L12.Irel"].values, label=dict_variables_all["L12.Irel"].label)
plt.legend()
plt.show(block=True)