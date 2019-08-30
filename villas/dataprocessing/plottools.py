import matplotlib.pyplot as plt
import numpy as np
from .timeseries import *
import scipy.signal as signal


def plot_timeseries(figure_id, timeseries, marker='None', plt_linestyle='-', plt_linewidth=2, plt_color=None, plt_legend_loc='lower right', plt_legend=True, inlineLabel = False):
    """
    This function plots either a single timeseries or several timeseries in the figure defined by figure_id.
    Several timeseries (handed over in a list) are plotted in several subplots.
    In order to plot several timeseries in one plot, the function is to be called several times (hold is activated).
    """
    plt.figure(figure_id)
    if not isinstance(timeseries, list):
        if plt_color:
            plt.plot(timeseries.time, timeseries.values, marker=marker, linestyle=plt_linestyle, label=timeseries.label, linewidth=plt_linewidth, color=plt_color)
        else:
            plt.plot(timeseries.time, timeseries.values, marker=marker, linestyle=plt_linestyle, label=timeseries.label, linewidth=plt_linewidth)
        plt.gca().autoscale(axis='x', tight=True)
        if(plt_legend):
            plt.legend(loc=plt_legend_loc)
    else:
        for ts in timeseries:
            plt.subplot(len(timeseries), 1, timeseries.index(ts) + 1)
            if plt_color:
                plt.plot(ts.time, ts.values, marker=marker, linestyle=plt_linestyle, label=ts.label, linewidth=plt_linewidth, color=plt_color)
            else:
                plt.plot(ts.time, ts.values, marker=marker, linestyle=plt_linestyle, label=ts.label, linewidth=plt_linewidth)
            plt.gca().autoscale(axis='x', tight=True)
            if(plt_legend):
                plt.legend()
    if(inlineLabel):
        plt.text(timeseries.time[-1], timeseries.values[-1], timeseries.label)


def set_timeseries_labels(timeseries, timeseries_labels):
    """
    Sets label attribute of timeseries, later used in plotting functions.
    Suitable for single timeseries as well as for several timeseries (handed over in a list).
    """
    if not isinstance(timeseries, list):
        timeseries.label = timeseries_labels
    else:
        for ts in timeseries:
            ts.label = timeseries_labels[timeseries.index(ts)]