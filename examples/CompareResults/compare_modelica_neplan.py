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



