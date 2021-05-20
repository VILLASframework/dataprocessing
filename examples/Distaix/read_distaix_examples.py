from dataprocessing.readtools import *
from dataprocessing.plottools import *
import matplotlib.pyplot as plt

# Example 1: read in single variable included in the Modelica results file
agent3_i_re = read_timeseries_dpsim_real(
    r"agent_3.csv",
    timeseries_names=["i.re [A]"])
plt.figure(1, figsize=(12, 8))
set_timeseries_labels(agent3_i_re[0], "Agent 1 Ireal")
plt.plot(agent3_i_re[0].time, agent3_i_re[0].values, label=agent3_i_re[0].label)
plt.legend()
plt.show(block=True)
