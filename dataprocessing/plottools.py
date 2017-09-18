import matplotlib.pyplot as plt
import numpy as np
from .timeseries import *


def plot_timeseries(figure_id, timeseries, plt_linestyle='-'):
    plt.figure(figure_id)

    if not isinstance(timeseries, list):
        plt.plot(timeseries.time, timeseries.values, linestyle=plt_linestyle, label=timeseries.label)
        plt.gca().autoscale(axis='x', tight=True)
        plt.legend()
    else:
        for ts in timeseries:
            plt.subplot(len(timeseries), 1, timeseries.index(ts) + 1)
            plt.plot(ts.time, ts.values, linestyle=plt_linestyle, label=ts.label)
            plt.gca().autoscale(axis='x', tight=True)
            plt.legend()

def set_time_series_labels(timeseries_list, time_series_labels):
    for ts in timeseries_list:
        ts.label = time_series_labels[timeseries_list.index(ts)]
