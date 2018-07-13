from dataprocessing.readtools import *
from dataprocessing.timeseries import *

def get_node_voltage_phasors(dpsim_timeseries_list):
    """Calculate voltage phasors of all nodes
    :param dpsim_timeseries_list: timeseries list retrieved from dpsim results
    :return:
    """
    voltage_phasor_list = {}
    for ts in dpsim_timeseries_list:
        ts_abs = ts.abs(ts.name + '_abs')
        ts_phase = ts.phase(ts.name + '_phase')
        ts_phasor = {}
        ts_phasor['abs'] = ts_abs
        ts_phasor['phase'] = ts_phase
        voltage_phasor_list[ts.name] = ts_phasor

    return voltage_phasor_list

def get_node_emt_voltages(timeseries_list, freq):
    """Calculate voltage phasors of all nodes
    :param timeseries_list: timeseries list retrieved from dpsim results
    :return:
    """
    voltages_list = {}
    for ts in timeseries_list:
        ts_emt = ts.dynphasor_shift_to_emt(ts.name, freq)
        voltages_list[ts.name] = ts_emt

    return voltages_list
