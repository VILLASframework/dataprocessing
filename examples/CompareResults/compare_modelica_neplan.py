<<<<<<< HEAD
import sys
sys.path.append(r'/home/cafi/Desktop/data-processing/examples/CompareResults')

from compare_modelica_neplan import compare_modelica_neplan

# 1. Compare Result directly returns to dic type
error = compare_modelica_neplan(NET_NAME)  # NET_NAME is the path of the result file


# 2. Compare Result output to files

f_error = open(FILE_PATH, "w")  # FILE_PATH is the path of the output file
error = compare_modelica_neplan(NET_NAME)
for name in error.keys():
    f_error.write('Error of %s is %f \n ' % (name, error[name]))

# 3. Using assertion function to assert the model
assert_modelia_neplan_results(NET_NAME)



=======
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import os
import sys
sys.path.append(r'D:\HIWI\Git\data-processing\dataprocessing')
from dataprocessing.readtools import *
def compare_modelica_neplan(Net_Name):
    # Read in original nepaln result file
    file_Neplan = os.path.abspath("C:/Users/admin/Desktop/" + Net_Name + "/" + Net_Name + ".rlf")
    # Read in original Modelica result file
    file_Modelica = os.path.abspath("C:/Users/admin/Desktop/" + Net_Name + "/" + Net_Name + ".mat")
    result_neplan = read_timeseries_NEPLAN_loadflow(file_Neplan)
    result_modelica = read_timeseries_Modelica(file_Modelica)
    '''
    # neplan result output
    f_neplan = open(os.path.abspath("C:/Users/admin/Desktop/" + Net_Name + "/" + Net_Name + "_neplan.txt"), "w")
    # modelica result output
    f_modelica = open(os.path.abspath("C:/Users/admin/Desktop/" + Net_Name + "/" + Net_Name + "_modelica.txt"), "w")
    # error result output
    f_error = open(os.path.abspath("C:/Users/admin/Desktop/" + Net_Name + "/" + Net_Name +
                                   "_error_modelica_neplan.txt"), "w")'''
    list_del = []
    for i in range(len(result_neplan)):
        result_neplan[i].name = result_neplan[i].name.replace(' ', '')
        result_neplan[i].name = result_neplan[i].name.upper()
        if 'ANGLE' in result_neplan[i].name:
            pass
        else:
            result_neplan[i].values = result_neplan[i].values * 1000  # unification of the unit,which is kV/kA in neplan
        '''f_neplan.write(
            '%s is %s \n' % (result_neplan[i].name, result_neplan[i].values[0]))  # result as list of TimeSeries'''

    for i in range(len(result_modelica)):
        result_modelica[i].name = result_modelica[i].name.upper()
        if 'ANGLE' in result_modelica[i].name:
            result_modelica[i].values = result_modelica[i].values / cmath.pi * 180  # unification of the unit
        #f_modelica.write('%s is %s \n' % (result_modelica[i].name, result_modelica[i].values[1]))
    timeseries_names = []  # list for names
    timeseries_error = []  # list for error
    len_limit = len(result_modelica)
    for i in range(len(result_neplan)):
        flag_NOT_found = False
        for j in range(len_limit):
            if result_neplan[i].name == result_modelica[j].name:  # Find the same variable
                timeseries_names.append(result_neplan[i].name)
                timeseries_error.append(TimeSeries.rmse(result_modelica[j], result_neplan[i]))
                flag_NOT_found = True
        if not flag_NOT_found:
            timeseries_error.append(TimeSeries(result_neplan[i].name, 0, -1))
            # No such variable in Modelica model, set the error to -1
        '''
        f_error.write('Error of %s is %f \n Base value'
                      ' of %s is %s \n\n' % (timeseries_error[i].name, timeseries_error[i].values,
                                             timeseries_error[i].name, result_neplan[i].values[0]))'''
    return dict(zip(timeseries_names, timeseries_error))


>>>>>>> c8fad311a60b86ecb9356c051bb5e547faa07926
