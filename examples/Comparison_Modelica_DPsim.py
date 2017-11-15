from dataprocessing.readtools import *
from dataprocessing.plottools import *
import matplotlib.pyplot as plt
from plottingtools.config import *

current_EMT = read_timeseries_Modelica(    r"C:\Workspace\ReferenceExamples\Modelica\Synchronous Generator\UnitTest_Eremia_3rdOrderModel_Euler_1ms.mat", ["synchronousGenerator_Park.i[1]"])

figure_id = 1
plt.figure(figure_id, figsize=(12,8))
set_timeseries_labels(current_EMT, ["EMT"])
plot_timeseries(figure_id, current_EMT, plt_color=blue)
plt.xlabel('Zeit [s]')
plt.ylabel('Strom [A]')
plt.show(block=True)

multi_current_EMT = read_timeseries_Modelica(r"C:\Workspace\ReferenceExamples\Modelica\Synchronous Generator\UnitTest_Eremia_3rdOrderModel_Euler_1ms.mat",[["synchronousGenerator_Park.i[1]"],["synchronousGenerator_Park.i[2]"]])

figure_id = 2
plt.figure(figure_id, figsize=(12,8))
set_timeseries_labels(multi_current_EMT, ["Phase a","Phase b","Phase c"])
plot_timeseries(figure_id, multi_current_EMT)
plt.xlabel('Zeit [s]')
plt.ylabel('Strom [A]')
plt.show(block=True)




