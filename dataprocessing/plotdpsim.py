from .readtools import *
from .plottools import *
from .calc import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 8})

def plot_dpsim_abs_diff(filename1, label1, node1, filename2, label2, node2):
    ts_dpsim1 = read_timeseries_DPsim(filename1)
    ts_dpsim2 = read_timeseries_DPsim(filename2)

    ts_dpsim1_length = len(ts_dpsim1)
    im_offset1 = int(ts_dpsim1_length / 2)
    if im_offset1 <= node1 or node1 < 0:
        print('Node 1 not available')
        exit()

    ts_dpsim2_length = len(ts_dpsim2)
    im_offset2 = int(ts_dpsim2_length / 2)
    if im_offset2 <= node1 or node1 < 0:
        print('Node 2 not available')
        exit()

    # this assumes same timestep for both simulations
    ts_abs1 = complex_abs('node ' + str(node1) + 'abs', ts_dpsim1[node1], ts_dpsim1[node1 + im_offset1])
    ts_abs1 = scale_ts(ts_abs1.name, ts_abs1, 0.001)
    ts_abs1.label = label1
    ts_abs2 = complex_abs('node ' + str(node2) + 'abs', ts_dpsim2[node1], ts_dpsim2[node1 + im_offset2])
    ts_abs2 = scale_ts(ts_abs2.name, ts_abs2, 0.001)
    ts_abs2.label = label2
    ts_diff = diff('diff', ts_abs1, ts_abs2)
    ts_diff.label = 'difference'

    figure_id = 1
    #plt.figure(figure_id)
    plt.figure(figure_id, figsize=(12 / 2.54, 6 / 2.54), facecolor='w', edgecolor='k')
    #plot_single_ts(figure_id, ts_abs1)
    #plot_single_ts(figure_id, ts_abs2)
    plot_single_ts(figure_id, ts_diff)
    plt.xlabel('Time [s]')
    plt.ylabel('Voltage [kV]')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_dpsim_abs(filename1, label1, node1, filename2, label2, node2):
        ts_dpsim1 = read_timeseries_DPsim(filename1)
        ts_dpsim2 = read_timeseries_DPsim(filename2)

        ts_dpsim1_length = len(ts_dpsim1)
        im_offset1 = int(ts_dpsim1_length / 2)
        if im_offset1 <= node1 or node1 < 0:
            print('Node 1 not available')
            exit()

        ts_dpsim2_length = len(ts_dpsim2)
        im_offset2 = int(ts_dpsim2_length / 2)
        if im_offset2 <= node1 or node1 < 0:
            print('Node 2 not available')
            exit()

        # this assumes same timestep for both simulations
        ts_abs1 = complex_abs('node ' + str(node1) + 'abs', ts_dpsim1[node1], ts_dpsim1[node1 + im_offset1])
        ts_abs1 = scale_ts(ts_abs1.name, ts_abs1, 0.001)
        ts_abs1.label = label1
        ts_abs2 = complex_abs('node ' + str(node2) + 'abs', ts_dpsim2[node1], ts_dpsim2[node1 + im_offset2])
        ts_abs2 = scale_ts(ts_abs2.name, ts_abs2, 0.001)
        ts_abs2.label = label2

        figure_id = 1
        # plt.figure(figure_id)
        plt.figure(figure_id, figsize=(12 / 2.54, 6 / 2.54), facecolor='w', edgecolor='k')
        plot_single_ts(figure_id, ts_abs1)
        plot_single_ts(figure_id, ts_abs2)
        plt.xlabel('Time [s]')
        plt.ylabel('Voltage [kV]')
        plt.grid(True)
        plt.tight_layout()
        plt.show()


def plot_dpsim_emt_abs(filenameDP, nodeDP, filenameEMT, nodeEMT):
    ts_dpsimDP = read_timeseries_DPsim(filenameDP)
    ts_dpsimEMT = read_timeseries_DPsim(filenameEMT)

    ts_dpsimDP_length = len(ts_dpsimDP)
    im_offsetDP = int(ts_dpsimDP_length / 2)
    if im_offsetDP <= nodeDP or nodeDP < 0:
        print('Node DP not available')
        exit()

    ts_dpsimEMT_length = len(ts_dpsimEMT)
    if ts_dpsimEMT_length <= nodeEMT or nodeEMT < 0:
        print('Node EMT not available')
        exit()

    ts_absDP = complex_abs('node ' + str(nodeDP) + 'abs', ts_dpsimDP[nodeDP], ts_dpsimDP[nodeDP + im_offsetDP])
    ts_absDP = scale_ts(ts_absDP.name, ts_absDP, 0.001)
    ts_absDP.label = 'DP abs'

    ts_shiftDP = dyn_phasor_shift_to_emt('node ' + str(nodeDP) + 'shift', ts_dpsimDP[nodeDP], ts_dpsimDP[nodeDP + im_offsetDP], 50)
    ts_shiftDP = scale_ts(ts_shiftDP.name, ts_shiftDP, 0.001)
    ts_shiftDP.label = 'DP shift'

    ts_EMT = TimeSeries('node ' + str(nodeEMT), ts_dpsimEMT[nodeEMT].time, ts_dpsimEMT[nodeEMT].values)
    ts_EMT = scale_ts(ts_EMT.name, ts_EMT, 0.001)
    ts_EMT.label = 'EMT'

    figure_id = 1
    # plt.figure(figure_id)
    plt.figure(figure_id, figsize=(12 / 2.54, 6 / 2.54), facecolor='w', edgecolor='k')
    plot_timeseries(figure_id, ts_EMT)
    plot_timeseries(figure_id, ts_absDP)
    plot_timeseries(figure_id, ts_shiftDP)
    plt.xlabel('Time [s]')
    plt.ylabel('Voltage [kV]')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_dpsim_abs_single(filename, node):
    ts_dpsim = read_timeseries_DPsim(filename)

    ts_dpsim_length = len(ts_dpsim)
    print('DPsim results file length:')
    print(ts_dpsim_length)
    for result in ts_dpsim:
        print(result.name)

    im_offset = int(ts_dpsim_length / 2)
    if im_offset <= node or node < 0:
        print('Node 1 not available')
        exit()

    abs1 = complex_abs('node ' + str(node) + 'abs', ts_dpsim[node], ts_dpsim[node + im_offset])
    abs1.label = 'absolute'

    figure_id = 1
    plt.figure(figure_id)
    plot_single_ts(figure_id, abs1)
    plt.xlabel('Time [s]')
    plt.ylabel('Voltage [V]')
    plt.grid(True)
    plt.show()

def main():
    plot_dpsim_single()

if __name__ == "__main__":
    main()