import re
import os
import sys
sys.path.append(r'/home/cafi/Desktop/data-processing/dataprocessing')
from Validationtools import *
from readtools import *
print("Test Start")
assert_modelia_neplan_results(sys.argv[1]) #  Assert the result, model result path read from cmd line
print("Test End")