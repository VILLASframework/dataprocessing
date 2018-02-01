from dataprocessing.readtools import *
from dataprocessing.plottools import *
import matplotlib.pyplot as plt
from plottingtools.config import *
import numpy as np

# Comparison of P, Q and delta for 3rd order Synchronous Generator
syngen_modelica_1us = read_timeseries_Modelica(
    r"\\tsclient\N\Research\German Public\ACS0049_SINERGIEN_bsc\Data\WorkData\SimulationResults\SynchronousGenerator\DP\Modelica\SinglePhase\SMIB_3rdOrderModel_PmStep_ThetaVolt0_Euler_1us.mat",
    timeseries_names=["synchronousGenerator_Park.P", "synchronousGenerator_Park.Q", "synchronousGenerator_Park.delta", "synchronousGenerator_Park.i.re", "synchronousGenerator_Park.i.im"])
syngen_distaix = read_timeseries_dpsim_real(
    r"\\tsclient\N\Research\German Public\ACS0050_Swarmgrid_tis\Data\WorkData\AP5\simulation-results\distaix_syngen_power_step\10ms\agent_3.csv",
    timeseries_names=["P [W]", "Q [var]", "delta [rad]", "i.re [A]", "i.im [A]"])

num_vars = 5
subplot_title_list = ["P [W]\n", "Q [var]\n", "delta [rad]\n", "i.re [A]", "i.im [A]"]
plt.figure(1, figsize=(12, 8))
for i in range(num_vars):
    plt.subplot(num_vars, 1, i + 1)
    set_timeseries_labels(syngen_modelica_1us, ["Modelica 1us", "Modelica 1us", "Modelica 1us", "Modelica 1us", "Modelica 1us"])
    plt.plot(syngen_modelica_1us[i].time, syngen_modelica_1us[i].values, label=syngen_modelica_1us[i].label)
    set_timeseries_labels(syngen_distaix, ["DistAIX 10ms", "DistAIX 10ms", "DistAIX 10ms", "DistAIX 10ms", "DistAIX 10ms"])
    plt.plot(syngen_distaix[i].time, syngen_distaix[i].values, label=syngen_distaix[i].label, linestyle=':')
    plt.legend()
    plt.xlim([0, 30])
    plt.ylabel(subplot_title_list[i])
plt.show(block=True)
