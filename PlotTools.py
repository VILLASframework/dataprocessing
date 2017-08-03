import matplotlib.pyplot as plt
import numpy as np


def plot_in_subplots(figure_id, time_series, plt_linestyle='-'):
    plt.figure(figure_id)
    for ts in time_series:
        plt.subplot(len(time_series), 1, time_series.index(ts) + 1)
        plt.plot(ts.time, ts.values, linestyle=plt_linestyle, label=ts.label)
        plt.gca().autoscale(axis='x', tight=True)
        plt.legend()


def set_time_series_labels(time_series, time_series_labels):
    for ts in time_series:
        ts.label = time_series_labels[time_series.index(ts)]