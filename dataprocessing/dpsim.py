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
        ts_phasor = [ts_abs, ts_phase]
        voltage_phasor_list[ts.name] = ts_phasor

    return voltage_phasor_list