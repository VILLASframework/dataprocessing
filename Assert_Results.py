import re
import os
import sys

from dataprocessing.Validationtools import *
from dataprocessing.readtools import *
print("Test Start")
# We need to extract all the result files from git now
for files in os.listdir(
        os.path.abspath("reference-results/Neplan/BasicGrids")):
        assert_modelia_neplan_results(os.path.splitext(files)[0]) #  Assert the result, model result path read from cmd line
print("Test End")
