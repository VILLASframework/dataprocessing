from .readtools import *
from .plottools import *
from .calc import *
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
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


def plotNodeVoltageInterpDpRef(filenameRef, filenameDP, node):
    node = node - 1
    dfRef = pd.read_csv(filenameRef, header=None)
    dfDP = pd.read_csv(filenameDP, header=None)

    if (dfRef.shape[1] - 1) < node or node < 0:
        print('Node not available')
        exit()

    if (dfDP.shape[1] - 1) / 2 < node or node < 0:
        print('Node not available')
        exit()

    # Ref
    timeRef = np.array(dfRef.ix[:, 0])
    voltageRef = np.array(dfRef.ix[:, node + 1])

    # DP interpolated
    timeDP = np.array(dfDP.ix[:, 0])
    voltageReDP = np.array(dfDP.ix[:, node + 1])
    voltageImDP = np.array(dfDP.ix[:, int((dfDP.shape[1] - 1) / 2 + node + 1)])

    interpTime = np.arange(dfDP.ix[0, 0], dfDP.ix[dfDP.shape[0] - 1, 0], 0.00005)
    fVoltageRe = interp1d(timeDP, voltageReDP)
    fVoltageIm = interp1d(timeDP, voltageImDP)
    interpVoltageRe = fVoltageRe(interpTime)
    interpVoltageIm = fVoltageIm(interpTime)

    voltageShiftDPInterp = interpVoltageRe * np.cos(2 * np.pi * 50 * interpTime) - interpVoltageIm * np.sin(
        2 * np.pi * 50 * interpTime)
    voltageAbsDP = np.sqrt(voltageReDP ** 2 + voltageImDP ** 2)

    fig, ax1 = plt.subplots()
    ax1.plot(timeRef, voltageRef, 'm:', label='Ref')
    ax1.plot(interpTime, voltageShiftDPInterp, 'b--', label='DP interp')
    ax1.plot(timeDP, voltageAbsDP, 'r-', label='DP abs')

    # Now add the legend with some customizations.
    legend = ax1.legend(loc='lower right', shadow=True)

    # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('mag [V]')
    ax1.grid(True)
    plt.show()


def plotNodeVoltageDpEmtRef(filenameRef, filenameDP, filenameEMT, node):
    node = node - 1
    dfRef = pd.read_csv(filenameRef, header=None)
    dfEMT = pd.read_csv(filenameEMT, header=None)
    dfDP = pd.read_csv(filenameDP, header=None)

    if (dfRef.shape[1] - 1) < node or node < 0:
        print('Node not available')
        exit()

    if (dfEMT.shape[1] - 1) < node or node < 0:
        print('Node not available')
        exit()

    if (dfDP.shape[1] - 1) / 2 < node or node < 0:
        print('Node not available')
        exit()

    # Ref
    timeRef = np.array(dfRef.ix[:, 0])
    voltageRef = np.array(dfRef.ix[:, node + 1])

    # EMT
    timeEMT = np.array(dfEMT.ix[:, 0])
    voltageEMT = np.array(dfEMT.ix[:, node + 1])

    # DP
    timeDP = np.array(dfDP.ix[:, 0])
    voltageReDP = np.array(dfDP.ix[:, node + 1])
    voltageImDP = np.array(dfDP.ix[:, int((dfDP.shape[1] - 1) / 2 + node + 1)])
    voltageAbsDP = np.sqrt(voltageReDP ** 2 + voltageImDP ** 2)
    voltageShiftDP = voltageReDP * np.cos(2 * np.pi * 50 * timeDP) - voltageImDP * np.sin(2 * np.pi * 50 * timeDP)

    fig, ax1 = plt.subplots()
    ax1.plot(timeRef, voltageRef, 'm:', label='Ref')
    ax1.plot(timeEMT, voltageEMT, 'g--', label='EMT')
    ax1.plot(timeDP, voltageShiftDP, 'b--', label='DP shift')
    ax1.plot(timeDP, voltageAbsDP, 'r-', label='DP abs')

    # Now add the legend with some customizations.
    legend = ax1.legend(loc='lower right', shadow=True)

    # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('mag [V]')
    ax1.grid(True)
    plt.show()


def plotNodeVoltageDpEmt(filenameDP, filenameEMT, node):
    node = node - 1
    dfEMT = pd.read_csv(filenameEMT, header=None)
    dfDP = pd.read_csv(filenameDP, header=None)

    if (dfEMT.shape[1] - 1) < node or node < 0:
        print('Node not available')
        exit()

    if (dfDP.shape[1] - 1) / 2 < node or node < 0:
        print('Node not available')
        exit()

    # EMT
    timeEMT = np.array(dfEMT.ix[:, 0])
    voltageEMT = np.array(dfEMT.ix[:, node + 1])

    # DP
    timeDP = np.array(dfDP.ix[:, 0])
    voltageReDP = np.array(dfDP.ix[:, node + 1])
    voltageImDP = np.array(dfDP.ix[:, int((dfDP.shape[1] - 1) / 2 + node + 1)])
    voltageAbsDP = np.sqrt(voltageReDP ** 2 + voltageImDP ** 2)
    voltageShiftDP = voltageReDP * np.cos(2 * np.pi * 50 * timeDP) - voltageImDP * np.sin(2 * np.pi * 50 * timeDP)

    fig, ax1 = plt.subplots()
    ax1.plot(timeEMT, voltageEMT, 'g--', label='EMT')
    ax1.plot(timeDP, voltageShiftDP, 'b--', label='DP shift')
    ax1.plot(timeDP, voltageAbsDP, 'r-', label='DP abs')

    # Now add the legend with some customizations.
    legend = ax1.legend(loc='lower right', shadow=True)

    # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('mag [V]')
    ax1.grid(True)
    plt.show()


def plotEmtNodeResults(filename, node):
    node = node - 1
    df = pd.read_csv(filename, header=None)
    print(df.shape)

    if (df.shape[1] - 1) < node or node < 0:
        print('Node not available')
        exit()

    time = np.array(df.ix[:, 0])
    voltage = np.array(df.ix[:, node + 1])

    fig, ax1 = plt.subplots()
    ax1.plot(time, voltage, 'b-')
    # plt.yticks(np.arange(-10, 10, 1.0))
    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('mag [V] or [A]')
    ax1.grid(True)
    plt.show()


def plotNodeResults(filename, node):
    node = node - 1
    df = pd.read_csv(filename, header=None)
    print(df.shape)

    if (df.shape[1] - 1) / 2 < node or node < 0:
        print('Node not available')
        exit()

    time = np.array(df.ix[:, 0])
    voltageRe = np.array(df.ix[:, node + 1])
    voltageIm = np.array(df.ix[:, int((df.shape[1] - 1) / 2 + node + 1)])

    voltage = np.sqrt(voltageRe ** 2 + voltageIm ** 2)
    voltageEmt = voltageRe * np.cos(2 * np.pi * 50 * time) - voltageIm * np.sin(2 * np.pi * 50 * time)
    fig, ax1 = plt.subplots()
    ax1.plot(time, voltageEmt, 'b-', time, voltage, 'r-')
    # plt.yticks(np.arange(-10, 10, 1.0))
    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('mag [V] or [A]')
    ax1.grid(True)
    plt.show()


def plotInterpolatedNodeResults(filename, node):
    node = node - 1
    df = pd.read_csv(filename, header=None)
    print(df.shape)

    if (df.shape[1] - 1) / 2 < node or node < 0:
        print('Node not available')
        exit()

    time = np.array(df.ix[:, 0])
    voltageRe = np.array(df.ix[:, node + 1])
    voltageIm = np.array(df.ix[:, int((df.shape[1] - 1) / 2 + node + 1)])

    interpTime = np.arange(df.ix[0, 0], df.ix[df.shape[0] - 1, 0], 0.00005)
    fVoltageRe = interp1d(time, voltageRe)
    fVoltageIm = interp1d(time, voltageIm)

    interpVoltageRe = fVoltageRe(interpTime)
    interpVoltageIm = fVoltageIm(interpTime)

    voltageMeas = np.sqrt(voltageRe ** 2 + voltageIm ** 2)
    voltage = np.sqrt(interpVoltageRe ** 2 + interpVoltageIm ** 2)
    voltageEmt = interpVoltageRe * np.cos(2 * np.pi * 50 * interpTime) - interpVoltageIm * np.sin(
        2 * np.pi * 50 * interpTime)
    fig, ax1 = plt.subplots()
    ax1.plot(interpTime, voltageEmt, 'b-')
    ax1.plot(time, voltageMeas, 'r-')
    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('mag [V] or [A]')
    ax1.grid(True)
    plt.show()


def plotResultsInterfacedInductor(filename, node):
    node = node - 1
    df = pd.read_csv(filename, header=None)
    print(df.shape)

    if (df.shape[1] - 1) / 2 < node or node < 0:
        print('Voltage not available')
        exit()

    time = np.array(df.ix[:, 0])
    voltageRe = np.array(df.ix[:, node + 1])
    voltageIm = np.array(df.ix[:, int((df.shape[1] - 1) / 2 + node + 1)])

    voltage = np.sqrt(voltageRe ** 2 + voltageIm ** 2)
    voltageEmt = voltageRe * np.cos(2 * np.pi * 50 * time) - voltageIm * np.sin(2 * np.pi * 50 * time)
    fig, ax1 = plt.subplots()
    ax1.plot(time, voltageEmt, 'b-', time, voltage, 'r-')
    plt.yticks(np.arange(-10, 10, 1.0))
    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('voltage [V]')
    ax1.grid(True)
    plt.show()


def plotResultsSynGenUnitTest(filename, node1, node2, node3):
    node1 = node1 - 1
    node2 = node2 - 1
    node3 = node3 - 1
    df = pd.read_csv(filename, header=None)
    print(df.shape)

    if (df.shape[1] - 1) / 2 < node1 or node1 < 0 or \
                            (df.shape[1] - 1) / 2 < node2 or node2 < 0 or \
                            (df.shape[1] - 1) / 2 < node3 or node3 < 0:
        print('Voltage not available')
        exit()

    time = np.array(df.ix[:, 0])
    mag1 = np.array(df.ix[:, node1 + 1])
    mag2 = np.array(df.ix[:, node2 + 1])
    mag3 = np.array(df.ix[:, node3 + 1])

    fig, ax1 = plt.subplots()
    ax1.plot(time, mag1, 'b-', time, mag2, 'r-', time, mag3, 'g-')
    # ax1.plot(time, voltageEmt, 'b-', time, voltage, 'r-')
    # plt.yticks(np.arange(-10, 10, 1.0))
    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('Magnitude')
    ax1.grid(True)
    plt.show()


def plotResultsSynGenUnitTestVar(filename, varNum):
    df = pd.read_csv(filename, header=None)
    print(df.shape)

    if (df.shape[1]) < varNum or varNum < 0:
        print('Variable not available')
        exit()

    time = np.array(df.ix[:, 0])
    mag = np.array(df.ix[:, varNum])

    fig, ax1 = plt.subplots()
    ax1.plot(time, mag, 'b-')
    # plt.yticks(np.arange(-10, 10, 1.0))
    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('Magnitude')
    ax1.grid(True)
    plt.show()

