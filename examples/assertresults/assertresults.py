import re
import os
import sys

from dataprocessing.validationtools import *
from dataprocessing.readtools import *
print("Test Start")
# We need to extract all the result files from git now
for files in os.listdir(
        os.path.abspath("reference-results/Neplan/BasicGrids")):
        #  Assert the result, model result path read from cmd line
        assert_modelia_neplan_results(os.path.splitext(files)[0],
                                      os.path.abspath("reference-results/Modelica/BasicGrids/" +
                                                      os.path.splitext(files)[0] + ".mat"),
                                      os.path.abspath("reference-results/Neplan/BasicGrids/" +
                                                      os.path.splitext(files)[0] + ".rlf"))

print("Test End")
